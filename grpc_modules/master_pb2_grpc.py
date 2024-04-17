# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import master_pb2 as master__pb2


class MasterServicerStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.startMapper = channel.unary_unary(
                '/master.MasterServicer/startMapper',
                request_serializer=master__pb2.invokeMapper.SerializeToString,
                response_deserializer=master__pb2.response.FromString,
                )
        self.startReducer = channel.unary_unary(
                '/master.MasterServicer/startReducer',
                request_serializer=master__pb2.invokeReducer.SerializeToString,
                response_deserializer=master__pb2.response.FromString,
                )
        self.workCompleteMap = channel.unary_unary(
                '/master.MasterServicer/workCompleteMap',
                request_serializer=master__pb2.ifComplete.SerializeToString,
                response_deserializer=master__pb2.status.FromString,
                )
        self.workCompleteReduce = channel.unary_unary(
                '/master.MasterServicer/workCompleteReduce',
                request_serializer=master__pb2.ifComplete.SerializeToString,
                response_deserializer=master__pb2.status.FromString,
                )


class MasterServicerServicer(object):
    """Missing associated documentation comment in .proto file."""

    def startMapper(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def startReducer(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def workCompleteMap(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def workCompleteReduce(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_MasterServicerServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'startMapper': grpc.unary_unary_rpc_method_handler(
                    servicer.startMapper,
                    request_deserializer=master__pb2.invokeMapper.FromString,
                    response_serializer=master__pb2.response.SerializeToString,
            ),
            'startReducer': grpc.unary_unary_rpc_method_handler(
                    servicer.startReducer,
                    request_deserializer=master__pb2.invokeReducer.FromString,
                    response_serializer=master__pb2.response.SerializeToString,
            ),
            'workCompleteMap': grpc.unary_unary_rpc_method_handler(
                    servicer.workCompleteMap,
                    request_deserializer=master__pb2.ifComplete.FromString,
                    response_serializer=master__pb2.status.SerializeToString,
            ),
            'workCompleteReduce': grpc.unary_unary_rpc_method_handler(
                    servicer.workCompleteReduce,
                    request_deserializer=master__pb2.ifComplete.FromString,
                    response_serializer=master__pb2.status.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'master.MasterServicer', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class MasterServicer(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def startMapper(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/master.MasterServicer/startMapper',
            master__pb2.invokeMapper.SerializeToString,
            master__pb2.response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def startReducer(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/master.MasterServicer/startReducer',
            master__pb2.invokeReducer.SerializeToString,
            master__pb2.response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def workCompleteMap(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/master.MasterServicer/workCompleteMap',
            master__pb2.ifComplete.SerializeToString,
            master__pb2.status.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def workCompleteReduce(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/master.MasterServicer/workCompleteReduce',
            master__pb2.ifComplete.SerializeToString,
            master__pb2.status.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
