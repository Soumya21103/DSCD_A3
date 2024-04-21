# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: reduce.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0creduce.proto\x12\x07Reducer\"&\n\x10HeartBeatRequest\x12\x12\n\nreducer_id\x18\x01 \x01(\x05\"7\n\x11HeartBeatResponse\x12\x12\n\nreducer_id\x18\x01 \x01(\x05\x12\x0e\n\x06status\x18\x02 \x01(\x08\"\'\n\x11OutputFileRequest\x12\x12\n\nreducer_id\x18\x01 \x01(\x03\"V\n\x12OutputFileResponse\x12\x12\n\nreducer_id\x18\x01 \x01(\x05\x12\x15\n\rout_file_name\x18\x02 \x01(\t\x12\x15\n\rout_file_line\x18\x03 \x01(\t\"9\n\x0c\x63\x65ntroidKeys\x12\x13\n\x0b\x63\x65ntroid_id\x18\x01 \x01(\x05\x12\t\n\x01x\x18\x02 \x01(\x01\x12\t\n\x01y\x18\x03 \x01(\x01\"h\n\x11invocationRequest\x12\x12\n\nreducer_id\x18\x01 \x01(\x05\x12\x15\n\rmapper_socket\x18\x02 \x03(\t\x12(\n\tcentroids\x18\x03 \x03(\x0b\x32\x15.Reducer.centroidKeys\"8\n\x12invocationResponse\x12\x12\n\nreducer_id\x18\x01 \x01(\x05\x12\x0e\n\x06status\x18\x02 \x01(\x08\x32\xe1\x01\n\x07Reducer\x12H\n\rinvokeReducer\x12\x1a.Reducer.invocationRequest\x1a\x1b.Reducer.invocationResponse\x12\x42\n\tHeartBeat\x12\x19.Reducer.HeartBeatRequest\x1a\x1a.Reducer.HeartBeatResponse\x12H\n\rgetOutputFile\x12\x1a.Reducer.OutputFileRequest\x1a\x1b.Reducer.OutputFileResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'reduce_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_HEARTBEATREQUEST']._serialized_start=25
  _globals['_HEARTBEATREQUEST']._serialized_end=63
  _globals['_HEARTBEATRESPONSE']._serialized_start=65
  _globals['_HEARTBEATRESPONSE']._serialized_end=120
  _globals['_OUTPUTFILEREQUEST']._serialized_start=122
  _globals['_OUTPUTFILEREQUEST']._serialized_end=161
  _globals['_OUTPUTFILERESPONSE']._serialized_start=163
  _globals['_OUTPUTFILERESPONSE']._serialized_end=249
  _globals['_CENTROIDKEYS']._serialized_start=251
  _globals['_CENTROIDKEYS']._serialized_end=308
  _globals['_INVOCATIONREQUEST']._serialized_start=310
  _globals['_INVOCATIONREQUEST']._serialized_end=414
  _globals['_INVOCATIONRESPONSE']._serialized_start=416
  _globals['_INVOCATIONRESPONSE']._serialized_end=472
  _globals['_REDUCER']._serialized_start=475
  _globals['_REDUCER']._serialized_end=700
# @@protoc_insertion_point(module_scope)
