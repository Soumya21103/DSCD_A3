# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mapper.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0cmapper.proto\"(\n\rMapperRequest\x12\x17\n\x0fpartition_index\x18\x01 \x01(\x05\")\n\x05Point\x12\n\n\x02id\x18\x03 \x01(\x05\x12\t\n\x01x\x18\x01 \x01(\x01\x12\t\n\x01y\x18\x02 \x01(\x01\"A\n\nMapperItem\x12\r\n\x05index\x18\x01 \x01(\x05\x12\x15\n\x05point\x18\x02 \x01(\x0b\x32\x06.Point\x12\r\n\x05\x63ount\x18\x03 \x01(\x05\",\n\x0eMapperResponse\x12\x1a\n\x05items\x18\x01 \x03(\x0b\x32\x0b.MapperItem\"]\n\x12StartMapperRequest\x12\x0f\n\x07indices\x18\x01 \x03(\x05\x12\x18\n\x08\x63\x65ntroid\x18\x02 \x03(\x0b\x32\x06.Point\x12\x11\n\tmapper_id\x18\x03 \x01(\x05\x12\t\n\x01R\x18\x04 \x01(\x05\"&\n\x13StartMapperResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\"%\n\x10HeartBeatRequest\x12\x11\n\tmapper_id\x18\x01 \x01(\x05\"6\n\x11HeartBeatResponse\x12\x11\n\tmapper_id\x18\x01 \x01(\x05\x12\x0e\n\x06status\x18\x02 \x01(\x08\x32\xab\x01\n\x06Mapper\x12\x31\n\x0cGetPartition\x12\x0e.MapperRequest\x1a\x0f.MapperResponse\"\x00\x12:\n\x0bStartMapper\x12\x13.StartMapperRequest\x1a\x14.StartMapperResponse\"\x00\x12\x32\n\tHeartBeat\x12\x11.HeartBeatRequest\x1a\x12.HeartBeatResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'mapper_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_MAPPERREQUEST']._serialized_start=16
  _globals['_MAPPERREQUEST']._serialized_end=56
  _globals['_POINT']._serialized_start=58
  _globals['_POINT']._serialized_end=99
  _globals['_MAPPERITEM']._serialized_start=101
  _globals['_MAPPERITEM']._serialized_end=166
  _globals['_MAPPERRESPONSE']._serialized_start=168
  _globals['_MAPPERRESPONSE']._serialized_end=212
  _globals['_STARTMAPPERREQUEST']._serialized_start=214
  _globals['_STARTMAPPERREQUEST']._serialized_end=307
  _globals['_STARTMAPPERRESPONSE']._serialized_start=309
  _globals['_STARTMAPPERRESPONSE']._serialized_end=347
  _globals['_HEARTBEATREQUEST']._serialized_start=349
  _globals['_HEARTBEATREQUEST']._serialized_end=386
  _globals['_HEARTBEATRESPONSE']._serialized_start=388
  _globals['_HEARTBEATRESPONSE']._serialized_end=442
  _globals['_MAPPER']._serialized_start=445
  _globals['_MAPPER']._serialized_end=616
# @@protoc_insertion_point(module_scope)
