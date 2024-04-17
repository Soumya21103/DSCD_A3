from concurrent import futures
import time
import grpc
import grpc_modules.master_pb2 as pb2
import grpc_modules.master_pb2_grpc as pb2_grpc

class MasterServicer(pb2_grpc.MasterServicer):
    def __init__(self) -> None:
        super().__init__()

    def startMapper(self, request: pb2.invokeMapper, context):
        pass

    def startReducer(self, request: pb2.invokeReducer, context):
        pass

    def workComplete(self, request: pb2.ifComplete, context):
        pass

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_MasterServicer_to_server(MasterServicer(), server)
    server.add_insecure_port('localhost:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()