from concurrent import futures
import threading
import asyncio
import time
import math
import grpc
import json
import master_pb2 as master_pb2
import master_pb2_grpc as master_pb2_grpc
import mapper_pb2 as mapper_pb2
import mapper_pb2_grpc as mapper_pb2_grpc
import reduce_pb2 as reduce_pb2
import reduce_pb2_grpc as reduce_pb2_grpc
import sys

# NODELIST = ["localhost:50051", "localhost:50052", "localhost:50053"]
MASTER_SOCKET = "localhost:9090"
class MasterServicer(master_pb2_grpc.MasterServicerServicer):
    def __init__(self,parrent) -> None:
        self._p: Master = parrent
        super().__init__()
    def workCompleteMapper(self, request : master_pb2.ifComplete, context):
        print("recieved mapper",request)
        if request.status == False:
            self._p.assign_mapper_with_task(self._p.task[request.id])
        else:
            socket = None
            for i in self._p.mapper_list.keys():
                if request.id == self._p.mapper_list[i]["id"]:
                    socket = self._p.mapper_list[i]["socket"]
                    self._p.mapper_list[i]["status"] = STATUS["completed"]
            self._p.completed_mappers.append(socket)
            if(len(self._p.completed_mappers) == self._p.m_max):
                self._p.completion_event.set()
        return master_pb2.status(status=True)
    
    def workCompleteReducer(self, request : master_pb2.ifComplete, context):
        print("recieved reducer",request)
        if request.status == False:
            self._p.assign_reducer_with_task(self._p.task[request.id],self._p.completed_mapper)
        else:
            id = None
            for i in self._p.reducer_list.keys():
                if request.id ==  self._p.reducer_list[i]["id"]:
                    id = i
                    self._p.reducer_list[i]["status"] = STATUS["completed"]
            self._p.completed_reducers.append(id)
            if(len(self._p.completed_reducers) == self._p.r_max):
                self._p.completion_event.set()
        return master_pb2.status(status=True)

STATUS = {
    "idle": 0,
    "working": 1,
    "completed": 2
}

class Master:
    def __init__(self,n_map,n_reduce,n_iiter,k_centroids,input_file) -> None:
        # WE asume that the n_map + n_reduce <= n_workers
        self.w_lock = threading.Lock() # to access passive list
        self.c_lock = threading.Lock() # to access centrioid
        self.completion_event = threading.Event()
        self.r_itter = 0
        self.r_max = int(n_reduce)
        self.m_itter = 0
        self.m_max = int(n_map)
        self.n_centroids = int(k_centroids)
        self.n_itter = int(n_iiter)

        w_list = self.get_list_of_workers()
        self.reducer_list, self.mapper_list = self.partition_workers(w_list)
        self.passive_mapper_list  = list(self.mapper_list.keys())
        self.passive_reducer_list = list(self.reducer_list.keys())
        self.input_file_meta = self.get_input_file_meta(input_file) # number of lines
        self.assign_initial_centroid_list()
    
    def get_list_of_workers(self) -> list[str]:
        ret = []
        with open("worker.json","r") as f:
            jd: dict = json.load(f)
        for i in jd.keys():
            ret.append(jd[i])
        return ret
    
    def partition_workers(self,w_list: list[str]) -> tuple[dict,dict]:
        ''' returns (reducer_list, mapper_list)'''
        r = {}
        m = {}
        flag = False
        if self.m_max > len(w_list)/2 or self.r_max > len(w_list)/2:
            for i in range(self.m_max):
                m[i] = {
                    "socket": w_list[i]["mapper"],
                    "status": STATUS["idle"],
                    "id": i
                    }
            for i in range(self.m_max,self.m_max+self.r_max):
                r[i] = w_list[i]
        else:
            for i in range(len(w_list)):
                if i % 2  == 0:
                    m[i//2] = {
                    "socket": w_list[i]["mapper"],
                    "status": STATUS["idle"],
                    "id": i//2
                    }
                else:
                    r[i//2] = {
                    "socket": w_list[i]["reducer"],
                    "status": STATUS["idle"],
                    "id": i//2
                    }
        return r, m 
    
    def get_input_file_meta(self,input_file: str) -> dict:
        l = 0
        c_dict = {}
        read = ""
        with open(input_file,"r") as f:
            for i in range(self.n_centroids):
                read = f.readline()
                x = read.strip().split(",")
                l += 1
                c_dict[i] = {"x": float(x[0]),"y":float(x[1])}
            while read != "":
                read = f.readline()
                l+=1
        return {
            "len": l,
            "centroid": c_dict
        }
    
    def assign_initial_centroid_list(self):
        with open("centroids.json","w") as f:
            json.dump(self.input_file_meta["centroid"],f,indent=4)

    
    def start_server(self):
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        master_pb2_grpc.add_MasterServicerServicer_to_server(
            MasterServicer(self), self.server
        )
        self.server.add_insecure_port(MASTER_SOCKET)
        self.server.start()
        threading.Thread(target=self.hearbeat_checker).start()
        asyncio.run(self.execution(),debug=True)

    def stop_sever(self):
        self.server.stop()

    def hearbeat_checker(self): 
        asyncio.run(self.h_check(),debug=True)

    async def h_check(self):
        tasks = []
        init = time.time()
        for i in self.mapper_list.keys():
            if self.mapper_list[i]["status"] == STATUS["working"]:
                tasks.append(asyncio.create_task(self.send_heartbeat(self.mapper_list[i]["id"],self.mapper_list[i]["socket"],"mapper")))
        for i in self.reducer_list.keys():
            if self.reducer_list[i]["status"] == STATUS["working"]:
                tasks.append(asyncio.create_task(self.send_heartbeat(self.reducer_list[i]["id"],self.reducer_list[i]["socket"],"reducer")))
        ret = asyncio.gather(*tasks)
        for s,i,t in ret:
            if s == False:
                if t == "reducer":
                    threading.Thread(target=self.rerun_reducer,args=(i,)).start()
                else:
                    threading.Thread(target=self.rerun_reducer,args=(i,)).start()
        

    def rerun_reducer(self,id):
        self.assign_reducer_with_task(id,mapper_socket=self.completed_mapper)

    def rerun_mapper(self,id):
        self.assign_mapper_with_task(self.task[id])
    
    async def send_heartbeat(self,id:int,socket:str, type: str) -> tuple[bool,int,str]:
        try:
            if type == "reducer":
                with grpc.insecure_channel(socket,options=[('grpc.connect_timeout_ms', 2000),]) as channel:
                    stub = reduce_pb2_grpc.ReducerStub()
                    ret: reduce_pb2.HeartBeatResponse = stub.HeartBeat(reduce_pb2.HeartBeatRequest(reducer_id=id))
                if ret.status:
                    print(f"sent heartbeat to {(id)} r")
                    return True,id,"reducer"
                else:
                    print(f"failed heartbeat to {(id)} r")
                    return False,id,"reducer"
            else:
                with grpc.insecure_channel(socket,options=[('grpc.connect_timeout_ms', 2000),]) as channel:
                    stub = mapper_pb2_grpc.MapperStub()
                    ret: mapper_pb2.HeartBeatResponse = stub.HeartBeat(mapper_pb2.HeartBeatRequest(mapper_id=id))
                if ret.status:
                    print(f"sent heartbeat to {(id)}m")
                    return True,id,"mapper"
                else:
                    print(f"failed heartbeat to {(id)}m")
                    return False,id,"mapeer"
        except:
            return False, id , type

    async def execution(self):
        for i in range(self.n_itter):
            print(i)
            self.completed_mapper = self.map_phase()
            print("map phase done",i)
            completed_reducers = self.reduce_phase(self.completed_mapper)
            print("reduce phase done",i)
            if self.collect_from_reducers(completed_reducers):
                print("collect phase done",i)
                continue
            else:
                print("something went horibly wrong")
                break

    def map_phase(self) -> list:
        self.task: list[tuple] = self.partition_mapper_task(self.input_file_meta,self.m_max)
        self.completed_mappers = [] # will be updated by completion rpc  LIST OF SOCKETS
        for j in self.task:
            self.assign_mapper_with_task(j)
            # wait for map completion
        if self.completion_event.wait():
            self.completion_event.clear()
        else:
            print("check what ive done wrong mapper")
        return self.completed_mappers
    
    def partition_mapper_task(self,input_file_meta: dict,max_map: int) -> list[tuple]:
        task = []
        f_len = input_file_meta["len"]
        n_map = max_map
        division = math.ceil(f_len / n_map)
        for i in range(n_map - 1):
            task.append((i,i*division, (i+1)*division))
        task.append(((n_map-1),(n_map-1)*division, f_len))
        return task
    
    def assign_mapper_with_task(self,task: tuple) -> bool:
        mappers = list(self.mapper_list.keys())
        while(True):
            self.m_itter += 1
            self.m_itter %= self.m_max
            try:
                with grpc.insecure_channel(self.mapper_list[mappers[self.m_itter]]["socket"]) as channel:
                    stub = mapper_pb2_grpc.MapperStub(channel)
                    ret: mapper_pb2.StartMapperResponse = stub.StartMapper(mapper_pb2.StartMapperRequest(
                        indices=range(task[1],task[2]),
                        centroid=self.get_centroid_for_mapper(),
                        mapper_id=task[0],
                        R=self.r_max
                    ))
                if ret.success:
                    self.mapper_list[mappers[self.m_itter]]["status"] = STATUS["working"]
                    break

            # except grpc.RpcError as e:
            except KeyboardInterrupt as e:
                if isinstance(e, grpc.Call):
                    if e.code() == grpc.StatusCode.DEADLINE_EXCEEDED:
                        print(f"Timeout occurred: ", e.details())
                    else:
                        print(f"UNable to connect to remote host",e.details())

    def get_centroid_for_mapper(self) -> list[mapper_pb2.Point]:
        ret = []
        with self.c_lock:
            f = open("centroids.json","r")
            jd :dict = json.load(f)
        for i in jd.keys():
            ret.append(mapper_pb2.Point(
                id=int(i), x = float(jd[i]["x"]), y = float(jd[i]["y"])
            ))
        return ret
    
    def reduce_phase(self, completed_mapper: list)  -> list:
        self.completed_reducers = [] # will be updated by completion rpc LIST OF IDS
        for j in range(self.r_max):
            self.assign_reducer_with_task(j, completed_mapper)
            
        if self.completion_event.wait():
            self.completion_event.clear()
        else:
            print("check what ive done wrong reducer")
        return self.completed_reducers
    
    def assign_reducer_with_task(self,id:int, mapper_socket:list[str]):
        reducer = list(self.reducer_list.keys())
        while(True):
            self.r_itter += 1
            self.r_itter %= self.r_max
            try:
                with grpc.insecure_channel(self.reducer_list[reducer[self.r_itter]]["socket"]) as channel:
                    stub = reduce_pb2_grpc.ReducerStub(channel)
                    ret: reduce_pb2.invocationResponse = stub.invokeReducer(reduce_pb2.invocationRequest(
                        reducer_id=id,
                        mapper_socket=mapper_socket,
                        centroids= self.get_centroid_reducer()
                    ))
                if ret.status:
                    self.reducer_list[reducer[self.m_itter]]["status"] = STATUS["working"]
                    break

            # except grpc.RpcError as e:
            except KeyboardInterrupt as e:
                if isinstance(e, grpc.Call):
                    if e.code() == grpc.StatusCode.DEADLINE_EXCEEDED:
                        print(f"Timeout occurred: ", e.details())
                    else:
                        print(f"UNable to connect to remote host",e.details())

    def get_centroid_reducer(self) -> list[reduce_pb2.centroidKeys]:
        ret = []
        with self.c_lock:
            f = open("centroids.json","r")
            jd :dict = json.load(f)
        for i in jd.keys():
            ret.append(reduce_pb2.centroidKeys(
                centroid_id=int(i), x = float(jd[i]["x"]), y = float(jd[i]["y"])
            ))
        return ret
    def collect_from_reducers(self,completed_reducer: list) -> bool:
        # This data collection is serial in nature
        full_data = {}
        sanity_check = True
        print(completed_reducer)
        for i in completed_reducer:
            data: dict = self.get_data_from_reducer(self.reducer_list[i])
            for j in data.keys():
                if j in full_data:
                    print("multiple centroid for of same key")
                    sanity_check = False
                else:
                    full_data[j] = data[j]
        if sanity_check and self.save_centroid_list(full_data):
            return False
        else:
            return True
    
    def get_data_from_reducer(self,red: dict) -> dict:
        fin = {}
        while True:
            try:
                with grpc.insecure_channel(red["socket"]) as channel:
                    stub = reduce_pb2_grpc.ReducerStub(channel)
                    id = red["id"]
                    ret:reduce_pb2.OutputFileResponse = stub.getOutputFile(reduce_pb2.OutputFileRequest(
                        reducer_id=int(id)
                        ))
                file_s =ret.out_file_line
                # for i in ret:
                #     file_s += i.out_file_line
                jd = json.loads(file_s) # hopefully this works or i'm going to cry
                for i in jd:
                    fin[i] = jd[i]
                return fin
            # except grpc.RpcError as e:
            except KeyboardInterrupt as e:
                if isinstance(e, grpc.Call):
                    if e.code() == grpc.StatusCode.DEADLINE_EXCEEDED:
                        print(f"Timeout occurred: ", e.details())
                    else:
                        print(f"UNable to connect to remote host",e.details())

    def save_centroid_list(self, data: dict) -> bool:
        with self.c_lock:
            with open("centroids.json","r") as f:
                jd: dict = json.load(f)
            try:
                for i in jd.keys():
                    data[int(i)]
            except KeyError:
                print("key",i,"does not exist")
                return False
            with open("centroids.json","w") as f:
                json.dump(data,f)
            return True
        

if __name__ == "__main__":
    l = len(sys.argv)
    try:
        if l == 6:
            wserver = Master(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5],)
            wserver.start_server()
            wserver.stop_sever()
        else:
            print("Invalid argument needs n_map n_reduce n_itter k_cent inputfile")
    except KeyboardInterrupt:
        wserver.stop_sever()
    