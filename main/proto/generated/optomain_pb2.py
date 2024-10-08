# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: optomain.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import tasks_pb2 as tasks__pb2
import optorun_pb2 as optorun__pb2
import optopy_pb2 as optopy__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='optomain.proto',
  package='optorunpb',
  syntax='proto3',
  serialized_options=b'Z\023optorunpb;optorunpb',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x0eoptomain.proto\x12\toptorunpb\x1a\x0btasks.proto\x1a\roptorun.proto\x1a\x0coptopy.proto2\xe7\x04\n\x0eOptoRunService\x12\x42\n\x07OptoRun\x12\x19.optorunpb.OptoRunRequest\x1a\x1a.optorunpb.OptoRunResponse\"\x00\x12O\n\x10OptoRunStreaming\x12\x19.optorunpb.OptoRunRequest\x1a\x1a.optorunpb.OptoRunResponse\"\x00(\x01\x30\x01\x12W\n\x18OptoRunStreamingParallel\x12\x19.optorunpb.OptoRunRequest\x1a\x1a.optorunpb.OptoRunResponse\"\x00(\x01\x30\x01\x12\x41\n\x11OptoStreamingTask\x12\x0f.optorunpb.Task\x1a\x15.optorunpb.TaskResult\"\x00(\x01\x30\x01\x12\x34\n\x08OptoTask\x12\x0f.optorunpb.Task\x1a\x15.optorunpb.TaskResult\"\x00\x12\x46\n\rOptimizeUnary\x12\x18.optorunpb.OptopyRequest\x1a\x19.optorunpb.OptopyResponse\"\x00\x12N\n\x11OptimizeStreaming\x12\x18.optorunpb.OptopyRequest\x1a\x19.optorunpb.OptopyResponse\"\x00(\x01\x30\x01\x12V\n\x19OptimizeStreamingParallel\x12\x18.optorunpb.OptopyRequest\x1a\x19.optorunpb.OptopyResponse\"\x00(\x01\x30\x01\x42\x15Z\x13optorunpb;optorunpbb\x06proto3'
  ,
  dependencies=[tasks__pb2.DESCRIPTOR,optorun__pb2.DESCRIPTOR,optopy__pb2.DESCRIPTOR,])



_sym_db.RegisterFileDescriptor(DESCRIPTOR)


DESCRIPTOR._options = None

_OPTORUNSERVICE = _descriptor.ServiceDescriptor(
  name='OptoRunService',
  full_name='optorunpb.OptoRunService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=72,
  serialized_end=687,
  methods=[
  _descriptor.MethodDescriptor(
    name='OptoRun',
    full_name='optorunpb.OptoRunService.OptoRun',
    index=0,
    containing_service=None,
    input_type=optorun__pb2._OPTORUNREQUEST,
    output_type=optorun__pb2._OPTORUNRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='OptoRunStreaming',
    full_name='optorunpb.OptoRunService.OptoRunStreaming',
    index=1,
    containing_service=None,
    input_type=optorun__pb2._OPTORUNREQUEST,
    output_type=optorun__pb2._OPTORUNRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='OptoRunStreamingParallel',
    full_name='optorunpb.OptoRunService.OptoRunStreamingParallel',
    index=2,
    containing_service=None,
    input_type=optorun__pb2._OPTORUNREQUEST,
    output_type=optorun__pb2._OPTORUNRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='OptoStreamingTask',
    full_name='optorunpb.OptoRunService.OptoStreamingTask',
    index=3,
    containing_service=None,
    input_type=tasks__pb2._TASK,
    output_type=tasks__pb2._TASKRESULT,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='OptoTask',
    full_name='optorunpb.OptoRunService.OptoTask',
    index=4,
    containing_service=None,
    input_type=tasks__pb2._TASK,
    output_type=tasks__pb2._TASKRESULT,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='OptimizeUnary',
    full_name='optorunpb.OptoRunService.OptimizeUnary',
    index=5,
    containing_service=None,
    input_type=optopy__pb2._OPTOPYREQUEST,
    output_type=optopy__pb2._OPTOPYRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='OptimizeStreaming',
    full_name='optorunpb.OptoRunService.OptimizeStreaming',
    index=6,
    containing_service=None,
    input_type=optopy__pb2._OPTOPYREQUEST,
    output_type=optopy__pb2._OPTOPYRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='OptimizeStreamingParallel',
    full_name='optorunpb.OptoRunService.OptimizeStreamingParallel',
    index=7,
    containing_service=None,
    input_type=optopy__pb2._OPTOPYREQUEST,
    output_type=optopy__pb2._OPTOPYRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_OPTORUNSERVICE)

DESCRIPTOR.services_by_name['OptoRunService'] = _OPTORUNSERVICE

# @@protoc_insertion_point(module_scope)
