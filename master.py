from concurrent import futures
import time
import grpc
import grpc_modules.master_pb2 as master_pb2
import grpc_modules.master_pb2_grpc as master_pb2_grpc
import grpc_modules.mapper_pb2 as mapper_pb2
import grpc_modules.mapper_pb2_grpc as mapper_pb2_grpc
import grpc_modules.reduce_pb2 as reduce_pb2
import grpc_modules.reduce_pb2_grpc as reduce_pb2_grpc

NODELIST = ["localhost:50051", "localhost:50052", "localhost:50053"]

class MasterServicer(master_pb2_grpc.MasterServicer):
    def __init__(self) -> None:
        super().__init__()

    def workComplete(self, request: master_pb2.ifComplete, context):
        pass


class Master:
    def __init__(self) -> None:
        self.numNodes = 3
        self.k = 3
        self.flag = 0
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        master_pb2_grpc.add_MasterServicerServicer_to_server(
            MasterServicer(), self.server
        )
        self.port = self.server.add_insecure_port("[::]:50051")
        print("Master Server is running on port:", self.port)
        self.mapFinished = False
        self.reducedData = []

    def startServer(self):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        master_pb2_grpc.add_MasterServicerServicer_to_server(MasterServicer(), server)
        server.start()
        server.wait_for_termination()

    def dividePoints(self, numNodes):
        numPoints = 0
        with open("Data/Input/points.txt", "r") as fp:
            for line in fp:
                numPoints += 1

        numPartition = numPoints / numNodes
        fs = []
        for i in range(numNodes - 1):
            start = i * numPartition
            end = (i + 1) * numPartition
            fs.append((start, end))
        fs.append((end, numPoints))
        return fs

    def invokeMapper(self, start, end):
        channel = grpc.insecure_channel("localhost:50051")
        mapperStub = mapper_pb2_grpc.add_MapperServicer_to_server(
            MasterServicer, grpc.server([grpc.local_stack()])
        )
        stub = mapper_pb2_grpc.MapperStub(channel)
        request = mapper_pb2.MapperRequest(start=start, end=end)
        response = stub.GetPartition(request)
        print(response)

    def invokeReducer(self):
        channel = grpc.insecure_channel("localhost:50051")
        reducerStub = reduce_pb2_grpc.add_ReducerServicer_to_server(
            MasterServicer, grpc.server([grpc.local_stack()])
        )
        stub = reduce_pb2_grpc.ReducerStub(channel)
        request = reduce_pb2.invocationRequest(data=self.reducedData)
        result = stub.invokeReducer(request)
        self.finalResult = result
        print(result)

    def checkIfMapFinished(self):
        channel = grpc.insecure_channel("localhost:50051")
        masterStub = master_pb2_grpc.add_MasterServicerServicer_to_server(
            MasterServicer, grpc.server([grpc.local_stack()])
        )
        stub = master_pb2_grpc.MasterServicerStub(channel)
        request = master_pb2.ifComplete()
        response = stub.workComplete(request)
        if response.status == "True":
            self.mapFinished = True

    def checkIfReduceFinished(self):
        channel = grpc.insecure_channel("localhost:50051")
        masterStub = master_pb2_grpc.add_MasterServicerServicer_to_server(
            MasterServicer, grpc.server([grpc.local_stack()])
        )
        stub = master_pb2_grpc.MasterServicerStub(channel)
        request = master_pb2.ifComplete()
        response = stub.workComplete(request)
        if response.status == "True":
            self.reduceFinished = True

    def checkReducerHeartBeat(self, node):
        channel = grpc.insecure_channel(node)
        stub = reduce_pb2_grpc.add_ReducerServicer_to_server()
        request = reduce_pb2.HeartBeatRequest()
        try:
            response = reduce_pb2.HeartBeatResponse()
            print(response)
        except Exception as e:
            print(e)
        

    def masterbate(self):
        if self.flag == 1:
            print("Converged")
            return
        
        fs = self.dividePoints(self.numNodes)

        
