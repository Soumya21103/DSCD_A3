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




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0creduce.proto\x12\x07Reducer\"&\n\x10HeartBeatRequest\x12\x12\n\nreducer_id\x18\x01 \x01(\x05\"7\n\x11HeartBeatResponse\x12\x12\n\nreducer_id\x18\x01 \x01(\x05\x12\x0e\n\x06status\x18\x02 \x01(\x08\"\x1a\n\x04OFRR\x12\x12\n\nreducer_id\x18\x01 \x01(\x03\"<\n\x03OFR\x12\x12\n\nreducer_id\x18\x01 \x01(\x05\x12\x10\n\x08out_file\x18\x02 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x03 \x01(\t\"9\n\x0c\x63\x65ntroidKeys\x12\x13\n\x0b\x63\x65ntroid_id\x18\x01 \x01(\x05\x12\t\n\x01x\x18\x02 \x01(\x01\x12\t\n\x01y\x18\x03 \x01(\x01\"h\n\x11invocationRequest\x12\x12\n\nreducer_id\x18\x01 \x01(\x05\x12\x15\n\rmapper_socket\x18\x02 \x03(\t\x12(\n\tcentroids\x18\x03 \x03(\x0b\x32\x15.Reducer.centroidKeys\"8\n\x12invocationResponse\x12\x12\n\nreducer_id\x18\x01 \x01(\x05\x12\x0e\n\x06status\x18\x02 \x01(\x08\x32\xbb\x01\n\x07Reducer\x12H\n\rinvokeReducer\x12\x1a.Reducer.invocationRequest\x1a\x1b.Reducer.invocationResponse\x12\x42\n\tHeartBeat\x12\x19.Reducer.HeartBeatRequest\x1a\x1a.Reducer.HeartBeatResponse\x12\"\n\x03gOF\x12\r.Reducer.OFRR\x1a\x0c.Reducer.OFRb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'reduce_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_HEARTBEATREQUEST']._serialized_start=25
  _globals['_HEARTBEATREQUEST']._serialized_end=63
  _globals['_HEARTBEATRESPONSE']._serialized_start=65
  _globals['_HEARTBEATRESPONSE']._serialized_end=120
  _globals['_OFRR']._serialized_start=122
  _globals['_OFRR']._serialized_end=148
  _globals['_OFR']._serialized_start=150
  _globals['_OFR']._serialized_end=210
  _globals['_CENTROIDKEYS']._serialized_start=212
  _globals['_CENTROIDKEYS']._serialized_end=269
  _globals['_INVOCATIONREQUEST']._serialized_start=271
  _globals['_INVOCATIONREQUEST']._serialized_end=375
  _globals['_INVOCATIONRESPONSE']._serialized_start=377
  _globals['_INVOCATIONRESPONSE']._serialized_end=433
  _globals['_REDUCER']._serialized_start=436
  _globals['_REDUCER']._serialized_end=623
# @@protoc_insertion_point(module_scope)
