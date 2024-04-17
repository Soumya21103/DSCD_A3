from grpc_modules import mapper_pb2 as mp2
from grpc_modules import mapper_pb2_grpc as mp2g
from grpc_modules import reduce_pb2 as rd2
from grpc_modules import reduce_pb2_grpc as rd2g
import grpc
import asyncio
import json
import threading
STATE = {
    "idle"   : 0,
    "reducer": 1,
    "mapper" : 2
}

class ReduceServicer(rd2g.ReducerServicer):
    '''Reciever for all rpc'''
    def __init__(self,parent) -> None:
        super().__init__()
        self.parent: Worker = parent
        
    def invokeReducer(self, request: rd2.invocationRequest, context):
        if self.parent.set_as_reducer(request.centroids,request.mapper_socket,request.reducer_id):
            return rd2.invocationResponse(reducer_id=self.parent.ID,status=True)
        return rd2.invocationResponse(reducer_id=-1,status=False)
    
    def getOutputFile(self, request: rd2.OutputFileRequest, context):
        if self.parent.state == STATE["reducer"] and self.parent.ID == request.reducer_id:
            file_name,desc = self.parent.reducer_api.open_output_descriptor()
            line = "<start>"
            while line != "":
                line = desc.readline()
                yield rd2.OutputFileResponse(reducer_id=self.parent.ID,out_file_name=file_name,out_file_line=line)
            self.parent.reducer_api.set_output_collected()
    
    def HeartBeat(self, request: rd2.HeartBeatRequest, context):
        if self.parent.state == STATE["reducer"] and request.reducer_id == self.parent.ID:
            return rd2.HeartBeatResponse(reducer_id=self.parent.ID,status=True)
        return rd2.HeartBeatResponse(reducer_id=-1,status=False)
    
class Reducer:
    def __init__(self,parent,centroids : list[rd2.centroidKeys], mapper: list[str]) -> None:
        self.parent: Worker = parent
        self.mapper: list[str] = []
        self.centroids = dict()
        self.final = dict()
        self.output_ready = False
        self.event_output = threading.Event()

        for i in centroids:
            self.centroids[i.centroid_id] =  i.value
        for i in mapper:
            self.mapper.append(i)

    def execute(self):
        self.partition = asyncio.run(self.get_reduce_partitions())
        if self.partition == None:
            self.send_failiure()
        else:
            for i in self.partition.keys():
                self.final[i] = self.reduce(self.partition[i])
                self.output_ready = self.create_output(self.final)
            if self.send_success():
                self.wait_for_collection()
        self.parent.state = STATE["idle"]
        self.parent.ID = -1
        del self.parent.reducer_api

    async def get_reduce_partitions(self) -> dict:
        TIMEOUT = 10 #sec
        self.fail = False
        tasks = [asyncio.create_task(self.get_partition_task(i,TIMEOUT)) for i in self.mapper]
        ret = await asyncio.gather(*tasks)
        sorted_inter = self.suffle_sort(ret)
        return sorted_inter

    async def get_partition_task(self,m_socket,timeout) -> list:
        partition = []
        try:
            with grpc.insecure_channel(m_socket,options=[('grpc.connect_timeout_ms', timeout*1000),]) as channel:
                stub = mp2g.MapperStub(channel)
                raw_ret: mp2.MapperResponse = stub.GetPartition(mp2.MapperRequest(partition_index=self.parent.ID))
        except grpc.RpcError as e:
            if isinstance(e, grpc.Call):
                if e.code() == grpc.StatusCode.DEADLINE_EXCEEDED:
                    print(f"Timeout occurred for Mapper: {m_socket}: ", e.details())
                else:
                    print(f"UNable to connect to remote host",e.details())
                self.fail = True
                return partition
        
        for i in raw_ret.items:
            partition.append({
                "index": i.index,
                "position": (i.point.x,i.point.y),
                "count": i.count
            })
        return partition

    def suffle_sort(self,recieved_partitions) -> dict:
        sorted_ret = dict()
        if(self.fail):
            return None
        for i in recieved_partitions:
            for j in i:
                if j["index"] not in sorted_ret.keys():
                    sorted_ret[j["index"]] = [(j["position"],j["count"])]
                else:
                    sorted_ret[j["index"]].append((j["position"],j["count"]))         
        return sorted_ret

    def reduce(self,int_list: list) -> tuple:
        final_value = (0,0)
        count = 0
        for i in int_list:
            final_value[0] += i[0][0]
            final_value[1] += i[0][1]
            count += i[1]

        final_value[0] /= count
        final_value[1] /= count
        return final_value
    
    def create_output(self, final:dict):
        try:
            with open(f"R{self.parent.ID}.json","w") as f:
                json.dump(final,f,indent=4)
        except:
            return False
        return True
    
    def open_output_descriptor(self):
        return f"R{self.parent.ID}.json", open(f"R{self.parent.ID}.json","r")
    
    def send_success(self):
        # TODO: write after master grpc are made
        pass

    def send_failiure(self):
        # TODO: write after master grpc are made
        pass
    
    def set_output_collected(self):
        self.event_output.set()

    def wait_for_collection(self):
        if self.event_output.wait():
            self.event_output.clear()
        return

class Mapper:
    pass

class Worker:
    def __init__(self) -> None:
        self.state = STATE["idle"]
        self.ID = -1
        self.reducer_api: Reducer = None
        self.mapper_api: Mapper  = None
        self.invoke_event = threading.Event()
        pass
    
    def start_server(self):
        try:
            while(True):
                if self.state == STATE["reducer"]:
                    self.reducer_api.execute()  
                elif self.state == STATE["mapper"]:
                    self.mapper_api.execute()
                else:
                    self.wait_for_invocation()
                
        except KeyboardInterrupt:
            self.stop_server()

    def stop_server(self):
        pass

    def set_as_reducer(self,centroids : list[rd2.centroidKeys], mapper: list[str],r_id: int) -> bool:
        if self.state == STATE["idle"]:
            self.reducer_api = Reducer(self,centroids,mapper)
            self.ID = r_id
            self.work_invocation()
            return True
        return False
    
    def wait_for_invocation(self):
        if self.invoke_event.wait():
            self.invoke_event.clear()
            return
        
    def work_invocation(self):
        ''' when any work is start call this after setting'''
        self.invoke_event.set()

    
