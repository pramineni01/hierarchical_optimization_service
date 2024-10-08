# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: hierarchical_svc.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from google.protobuf import duration_pb2 as google_dot_protobuf_dot_duration__pb2
import resources_pb2 as resources__pb2
import collections_pb2 as collections__pb2
import economics_pb2 as economics__pb2
import optorun_pb2 as optorun__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='hierarchical_svc.proto',
  package='optorunpb',
  syntax='proto3',
  serialized_options=b'Z\023optorunpb;optorunpb',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x16hierarchical_svc.proto\x12\toptorunpb\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x1egoogle/protobuf/duration.proto\x1a\x0fresources.proto\x1a\x11\x63ollections.proto\x1a\x0f\x65\x63onomics.proto\x1a\roptorun.proto\"\x9c\x01\n\nRunHorizon\x12\x36\n\x12horizon_start_time\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x39\n\x16\x62\x61se_interval_duration\x18\x02 \x01(\x0b\x32\x19.google.protobuf.Duration\x12\x1b\n\x13number_of_intervals\x18\x03 \x01(\x03\"\xd2\x01\n\x16HierarchicalSvcRequest\x12,\n\x08settings\x18\x01 \x01(\x0b\x32\x1a.optorunpb.OptoRunSettings\x12+\n\tresources\x18\x02 \x03(\x0b\x32\x18.optorunpb.InputResource\x12/\n\x0b\x63ollections\x18\x05 \x03(\x0b\x32\x1a.optorunpb.InputCollection\x12,\n\teconomics\x18\x06 \x01(\x0b\x32\x19.optorunpb.InputEconomics\"\xb8\x01\n\x17HierarchicalSvcResponse\x12<\n\x06status\x18\x01 \x01(\x0e\x32,.optorunpb.HierarchicalSvcResponse.RunStatus\x12\r\n\x05token\x18\x02 \x01(\t\x12\x15\n\rerror_message\x18\x03 \x01(\t\x12\x14\n\x0cresults_path\x18\x04 \x01(\t\"#\n\tRunStatus\x12\x0b\n\x07RUNNING\x10\x00\x12\t\n\x05\x45RROR\x10\x01\x32m\n\x0fHierarchicalSvc\x12Z\n\x0fRunHierarchical\x12!.optorunpb.HierarchicalSvcRequest\x1a\".optorunpb.HierarchicalSvcResponse\"\x00\x42\x15Z\x13optorunpb;optorunpbb\x06proto3'
  ,
  dependencies=[google_dot_protobuf_dot_timestamp__pb2.DESCRIPTOR,google_dot_protobuf_dot_duration__pb2.DESCRIPTOR,resources__pb2.DESCRIPTOR,collections__pb2.DESCRIPTOR,economics__pb2.DESCRIPTOR,optorun__pb2.DESCRIPTOR,])



_HIERARCHICALSVCRESPONSE_RUNSTATUS = _descriptor.EnumDescriptor(
  name='RunStatus',
  full_name='optorunpb.HierarchicalSvcResponse.RunStatus',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='RUNNING', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='ERROR', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=692,
  serialized_end=727,
)
_sym_db.RegisterEnumDescriptor(_HIERARCHICALSVCRESPONSE_RUNSTATUS)


_RUNHORIZON = _descriptor.Descriptor(
  name='RunHorizon',
  full_name='optorunpb.RunHorizon',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='horizon_start_time', full_name='optorunpb.RunHorizon.horizon_start_time', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='base_interval_duration', full_name='optorunpb.RunHorizon.base_interval_duration', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='number_of_intervals', full_name='optorunpb.RunHorizon.number_of_intervals', index=2,
      number=3, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=171,
  serialized_end=327,
)


_HIERARCHICALSVCREQUEST = _descriptor.Descriptor(
  name='HierarchicalSvcRequest',
  full_name='optorunpb.HierarchicalSvcRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='settings', full_name='optorunpb.HierarchicalSvcRequest.settings', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='resources', full_name='optorunpb.HierarchicalSvcRequest.resources', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='collections', full_name='optorunpb.HierarchicalSvcRequest.collections', index=2,
      number=5, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='economics', full_name='optorunpb.HierarchicalSvcRequest.economics', index=3,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=330,
  serialized_end=540,
)


_HIERARCHICALSVCRESPONSE = _descriptor.Descriptor(
  name='HierarchicalSvcResponse',
  full_name='optorunpb.HierarchicalSvcResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='status', full_name='optorunpb.HierarchicalSvcResponse.status', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='token', full_name='optorunpb.HierarchicalSvcResponse.token', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='error_message', full_name='optorunpb.HierarchicalSvcResponse.error_message', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='results_path', full_name='optorunpb.HierarchicalSvcResponse.results_path', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _HIERARCHICALSVCRESPONSE_RUNSTATUS,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=543,
  serialized_end=727,
)

_RUNHORIZON.fields_by_name['horizon_start_time'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_RUNHORIZON.fields_by_name['base_interval_duration'].message_type = google_dot_protobuf_dot_duration__pb2._DURATION
_HIERARCHICALSVCREQUEST.fields_by_name['settings'].message_type = optorun__pb2._OPTORUNSETTINGS
_HIERARCHICALSVCREQUEST.fields_by_name['resources'].message_type = resources__pb2._INPUTRESOURCE
_HIERARCHICALSVCREQUEST.fields_by_name['collections'].message_type = collections__pb2._INPUTCOLLECTION
_HIERARCHICALSVCREQUEST.fields_by_name['economics'].message_type = economics__pb2._INPUTECONOMICS
_HIERARCHICALSVCRESPONSE.fields_by_name['status'].enum_type = _HIERARCHICALSVCRESPONSE_RUNSTATUS
_HIERARCHICALSVCRESPONSE_RUNSTATUS.containing_type = _HIERARCHICALSVCRESPONSE
DESCRIPTOR.message_types_by_name['RunHorizon'] = _RUNHORIZON
DESCRIPTOR.message_types_by_name['HierarchicalSvcRequest'] = _HIERARCHICALSVCREQUEST
DESCRIPTOR.message_types_by_name['HierarchicalSvcResponse'] = _HIERARCHICALSVCRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

RunHorizon = _reflection.GeneratedProtocolMessageType('RunHorizon', (_message.Message,), {
  'DESCRIPTOR' : _RUNHORIZON,
  '__module__' : 'hierarchical_svc_pb2'
  # @@protoc_insertion_point(class_scope:optorunpb.RunHorizon)
  })
_sym_db.RegisterMessage(RunHorizon)

HierarchicalSvcRequest = _reflection.GeneratedProtocolMessageType('HierarchicalSvcRequest', (_message.Message,), {
  'DESCRIPTOR' : _HIERARCHICALSVCREQUEST,
  '__module__' : 'hierarchical_svc_pb2'
  # @@protoc_insertion_point(class_scope:optorunpb.HierarchicalSvcRequest)
  })
_sym_db.RegisterMessage(HierarchicalSvcRequest)

HierarchicalSvcResponse = _reflection.GeneratedProtocolMessageType('HierarchicalSvcResponse', (_message.Message,), {
  'DESCRIPTOR' : _HIERARCHICALSVCRESPONSE,
  '__module__' : 'hierarchical_svc_pb2'
  # @@protoc_insertion_point(class_scope:optorunpb.HierarchicalSvcResponse)
  })
_sym_db.RegisterMessage(HierarchicalSvcResponse)


DESCRIPTOR._options = None

_HIERARCHICALSVC = _descriptor.ServiceDescriptor(
  name='HierarchicalSvc',
  full_name='optorunpb.HierarchicalSvc',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=729,
  serialized_end=838,
  methods=[
  _descriptor.MethodDescriptor(
    name='RunHierarchical',
    full_name='optorunpb.HierarchicalSvc.RunHierarchical',
    index=0,
    containing_service=None,
    input_type=_HIERARCHICALSVCREQUEST,
    output_type=_HIERARCHICALSVCRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_HIERARCHICALSVC)

DESCRIPTOR.services_by_name['HierarchicalSvc'] = _HIERARCHICALSVC

# @@protoc_insertion_point(module_scope)
