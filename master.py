from concurrent import futures
import time
import grpc
import grpc_modules.master_pb2 as master_pb2
import grpc_modules.master_pb2_grpc as master_pb2_grpc
import grpc_modules.mapper_pb2 as mapper_pb2
import grpc_modules.mapper_pb2_grpc as mapper_pb2_grpc
import grpc_modules.reduce_pb2 as reduce_pb2
import grpc_modules.reduce_pb2_grpc as reduce_pb2_grpc


class MasterServicer(master_pb2_grpc.MasterServicer):
    def __init__(self) -> None:
        super().__init__()

    def workComplete(self, request: master_pb2.ifComplete, context):
        pass


class Master:
    def __init__(self) -> None:
        self.numNodes = 3
        self.k = 3
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        master_pb2_grpc.add_MasterServicerServicer_to_server(MasterServicer(), self.server)
        self.port = self.server.add_insecure_port('[::]:50051')
        print("Master Server is running on port:", self.port)
        self.mapFinished = False
        self.reducedData = []

    def startServer(self):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        master_pb2_grpc.add_MasterServicerServicer_to_server(MasterServicer(), server)
        server.start()
        server.wait_for_termination()

    def dividePoints(self,numNodes):
        numPoints = 0
        with open("Data/Input/points.txt", "r") as fp:
            for line in fp:
                numPoints += 1

        numPartition = numPoints/numNodes
        fs = []
        for i in range(numNodes-1):
            start = i*numPartition
            end = (i+1)*numPartition
            fs.append((start,end))
        fs.append((end,numPoints))
        return fs
    
    def invokeMapper(self, start, end):
        channel = grpc.insecure_channel('localhost:50051')
        mapperStub = mapper_pb2_grpc(channel)
        request = mapper_pb2.MapperRequest(
            start = start,
            end = end
        )
        response = mapperStub.MapperResponse(request)
        print(response)

    def invokeReducer(self):
        channel = grpc.insecure_channel('localhost:50051')
        reducerStub = reduce_pb2_grpc.add_ReducerServicer_to_server(MasterServicer, grpc.server([grpc.local_stack()]))
        request = reduce_pb2.StartReduceRequest(
            data = self.reducedData
        )
        response = reducerStub.StartReduce(request)
        print(response.success)