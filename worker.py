import mapper_pb2  as mapper_pb2
import mapper_pb2_grpc
import reduce_pb2 as rd2
import reduce_pb2_grpc as rd2g
import master_pb2 as ms2
import master_pb2_grpc as ms2g
from concurrent import futures
import grpc
import asyncio
import json
import threading
import math, os
import sys
STATE = {
    "idle"   : 0,
    "reducer": 1,
    "mapper" : 2
}
MASTER_SOCKET = "localhost:9090"
class ReduceServicer(rd2g.ReducerServicer):
    '''Reciever for all rpc'''
    def __init__(self,parent) -> None:
        super().__init__()
        self.parent: Worker = parent
        
    def invokeReducer(self, request: rd2.invocationRequest, context):
        print(request)
        if self.parent.set_as_reducer(request.centroids,request.mapper_socket,request.reducer_id):
            return rd2.invocationResponse(reducer_id=self.parent.ID,status=True)
        return rd2.invocationResponse(reducer_id=-1,status=False)
    
    def getOutputFile(self, request: rd2.OutputFileRequest, context):
        print("out_request",request)
        if self.parent.state == STATE["reducer"] and self.parent.ID == request.reducer_id:
            file_name,desc = self.parent.reducer_api.open_output_descriptor()
            ret = rd2.OutputFileResponse(reducer_id=self.parent.ID,out_file_name=file_name,out_file_line=desc)
            print(ret)
            self.parent.reducer_api.set_output_collected()
            return ret
    
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
            self.centroids[i.centroid_id] =   {"x":i.x, "y": i.y}
        for i in mapper:
            self.mapper.append(i)

    def execute(self):
        self.partition = asyncio.run(self.get_reduce_partitions(),debug=True)
        if self.partition == None:
            self.send_failiure()
            self.parent.state = STATE["idle"]
            self.parent.ID = -1
        else:
            for i in self.partition.keys():
                self.final[i] = self.reduce(self.partition[i])
                self.output_ready = self.create_output(self.final)
            if self.send_success():
                self.wait_for_collection()
            self.parent.state = STATE["idle"]
            self.parent.ID = -1
        self.parent.state = STATE["idle"]
        self.parent.ID = -1
        return
        # del self.parent.reducer_api

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
                stub = mapper_pb2_grpc.MapperStub(channel)
                raw_ret: mapper_pb2.MapperResponse = stub.GetPartition(mapper_pb2.MapperRequest(partition_index=self.parent.ID))
    
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
        final_value = [0,0]
        count = 0
        for i in int_list:
            final_value[0] += i[0][0]
            final_value[1] += i[0][1]
            count += i[1]

        final_value[0] /= count
        final_value[1] /= count
        return tuple(final_value)
    
    def create_output(self, final:dict):
        try:
            with open(f"R{self.parent.ID}.json","w") as f:
                json.dump(final,f,indent=4)
        except:
            return False
        return True
    
    def open_output_descriptor(self):
        f = open(f"R{self.parent.ID}.json","r")
        r = f.read()
        f.close()
        return f"R{self.parent.ID}.json", r
    def send_success(self):
        # TODO: write after master grpc are made
        with grpc.insecure_channel(MASTER_SOCKET) as channel:
            stub = ms2g.MasterServicerStub(channel)
            ret: ms2.status = stub.workCompleteReducer(ms2.ifComplete(status=True,id=int(self.parent.ID)))
        return ret.status

    def send_failiure(self):
        # TODO: write after master grpc are made
        with grpc.insecure_channel(MASTER_SOCKET) as channel:
            stub = ms2g.MasterServicerStub(channel)
            ret: ms2.status = stub.workCompleteReducer(ms2.ifComplete(status=False,id=int(self.parent.ID)))
        return ret.status
    
    def set_output_collected(self):
        self.event_output.set()

    def wait_for_collection(self):
        if self.event_output.wait():
            self.event_output.clear()
        return

class MapperServer(mapper_pb2_grpc.MapperServicer):
    def __init__(self, parent):
        super().__init__()
        self.parent: Worker = parent

    def StartMapper(self, request: mapper_pb2.StartMapperRequest, context):
        print("reciever request: ",request)

        # ASSUMED every mapper already knows location of input file
        # self.input_file = request.input_file
        centroids = [(point.x, point.y) for point in request.centroid]

        if self.parent.set_as_mapper(centroids, list(request.indices), request.mapper_id, request.R):
            return mapper_pb2.StartMapperResponse(success = True)

        return mapper_pb2.StartMapperResponse(success=False)

    def GetPartition(self, request, context):
        partition_index = request.partition_index
        pd = self.parent.mapper_api.partitioned_data

        if partition_index in pd:
            partition_items = pd[partition_index]
            response = mapper_pb2.MapperResponse()
            for item in partition_items:
                partition_item = response.items.add()
                partition_item.index = item[0]
                partition_item.point.x = item[1][0][0]
                partition_item.point.y = item[1][0][1]
                partition_item.count = item[1][1]
            return response
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Partition not found")
            return mapper_pb2.MapperResponse()

    def HeartBeat(self, request: mapper_pb2.HeartBeatRequest, context):
        if self.parent.state == STATE["mapper"] and request.mapper_id == self.parent.ID:
            return mapper_pb2.HeartBeatResponse(mapper_id=self.parent.ID,status=True)
        return mapper_pb2.HeartBeatResponse(mapper_id=-1,status=False)

class Mapper:
    def __init__(self,parent, id, input_indices,  centroids,R) -> None:
        self.parent: Worker = parent
        self.centroids = centroids
        self.points = self.points_from_file("Data/Input/points.txt", input_indices)
        self.partitioned_data = {}
        self.R =R
        
    
    def points_from_file(self, input_file, indices):
        with open(input_file, 'r') as file:
            lines = file.readlines()
        points = [tuple(map(float, line.strip().split(','))) for i, line in enumerate(lines) if i in indices] 
        return points
    
    def map(self, centroids, points, R):
        intermediate_output = []
        for p in points:
            distance = []
            for c in range(len(centroids)):
                x1 = p[0]
                y1 = p[1]
                x2 = centroids[c][0]
                y2 = centroids[c][1]
                distance.append((c, math.pow(x1-x2, 2) + math.pow(y1-y2, 2)))
            closest_centroid = min(distance, key=lambda x: x[1])
            intermediate_output.append((closest_centroid[0], (p, 1)))

        self.partition(intermediate_output, R)

    def partition(self, inter, R):
        id = self.parent.ID
        node_dir = f"M{id}"
        script_dir = os.path.dirname(os.path.abspath(__file__))
        node_dir = os.path.join(script_dir, f"M{id}")
        os.makedirs(node_dir, exist_ok=True)

        K = set()
        for j in inter:
            K.add(j[0])
            partition = j[0] % R
            partition_file = os.path.join(node_dir, f"partition_{partition+1}.txt")

            if partition not in self.partitioned_data.keys():
                with open(partition_file, "w") as file:
                    file.write(f"{j}\n")
                self.partitioned_data[partition] = [j]
            else:
                with open(partition_file, "a") as file:
                    file.write(f"{j}\n")
                self.partitioned_data[partition].append(j)

        # If R>K, create empty files for the extra partitions
        if R>len(K):
            k = len(K)+1
            while k <= R:
                partition_file = os.path.join(node_dir, f"partition_{k}.txt")
                with open(partition_file, "w") as file:
                    file.write(f"")
                self.partitioned_data[k-1] = []
                k+=1

    def execute(self):
        
        self.map(self.centroids, self.points, self.R)
        self.send_success()
        self.parent.state = STATE["idle"]
        self.parent.ID = -1
        # del self.parent.mapper_api

    def send_success(self):
        with grpc.insecure_channel(MASTER_SOCKET) as channel:
            stub = ms2g.MasterServicerStub(channel)
            ret: ms2.status = stub.workCompleteMapper(ms2.ifComplete(status=True,id=int(self.parent.ID)))
        return ret.status

    def send_failiure(self):
        with grpc.insecure_channel(MASTER_SOCKET) as channel:
            stub = ms2g.MasterServicerStub(channel)
            ret: ms2.status = stub.workCompleteMapper(ms2.ifComplete(status=False,id=int(self.parent.ID)))
        return ret.status


class Worker:
    def __init__(self) -> None:
        self.state = STATE["idle"]
        self.ID = -1
        self.reducer_api: Reducer = None
        self.mapper_api: Mapper  = None
        self.invoke_event = threading.Event()
        
        pass
    
    def start_server(self,mapper_socket,reducer_socket):
        self.server_r = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        self.server_c = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        rd2g.add_ReducerServicer_to_server(ReduceServicer(self),self.server_r)
        mapper_pb2_grpc.add_MapperServicer_to_server(MapperServer(self),self.server_c)
        self.server_r.add_insecure_port(reducer_socket)
        self.server_c.add_insecure_port(mapper_socket)

        self.server_r.start()
        self.server_c.start()
        try:
            while(True):
                if self.state == STATE["reducer"]:
                    self.reducer_api.execute()  
                elif self.state == STATE["mapper"]:
                    self.mapper_api.execute()
                else:
                    print(self.state)
                    self.wait_for_invocation()
        
        except KeyboardInterrupt:
            self.stop_server()

    def stop_server(self):
        self.server_r.stop(0)
        self.server_c.stop(0)
        pass

    def set_as_reducer(self,centroids : list[rd2.centroidKeys], mapper: list[str],r_id: int) -> bool:
        if self.state == STATE["idle"]:
            self.state = STATE["reducer"]
            self.reducer_api = Reducer(self,centroids,mapper)
            self.ID = r_id
            self.work_invocation()
            return True
        return False
    
    def set_as_mapper(self, centroids, input_indices, id, R):
        if self.state == STATE["idle"]:
            self.state = STATE["mapper"]
            self.mapper_api = Mapper(self, id, input_indices, centroids, R)
            self.ID = id
            self.work_invocation()
            return True
        return False
    
    
    def wait_for_invocation(self):
        if self.invoke_event.wait():
            self.invoke_event.clear()
        print("done waiting", self.state)
        return
        
    def work_invocation(self):
        ''' when any work is start call this after setting'''
        self.invoke_event.set()

if __name__ == "__main__":
    l = len(sys.argv)
    try:
        if l == 2:
            f = open("worker.json")
            jd = json.load(f)
            reducer_socket = jd[sys.argv[1]]["reducer"]
            mapper_socket = jd[sys.argv[1]]["mapper"]
            wserver = Worker()
            wserver.start_server(mapper_socket,reducer_socket)
            wserver.stop_server()
        else:
            print("Invalid arguments")
    except KeyboardInterrupt:
        wserver.stop_server()
    