# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: proto/battlecity.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x16proto/battlecity.proto\x12\nbattlecity\";\n\nAckRequest\x12\x0c\n\x04\x66lag\x18\x01 \x01(\x05\x12\x11\n\ttimestamp\x18\x02 \x01(\x05\x12\x0c\n\x04node\x18\x03 \x01(\t\"9\n\x08\x41\x63kReply\x12\x0c\n\x04\x66lag\x18\x01 \x01(\x05\x12\x11\n\ttimestamp\x18\x02 \x01(\x05\x12\x0c\n\x04node\x18\x03 \x01(\t\"\x83\x01\n\tOpRequest\x12\x0c\n\x04left\x18\x01 \x01(\x08\x12\r\n\x05right\x18\x02 \x01(\x08\x12\n\n\x02up\x18\x03 \x01(\x08\x12\x0c\n\x04\x64own\x18\x04 \x01(\x08\x12\r\n\x05space\x18\x05 \x01(\x08\x12\x0f\n\x07KEYDOWN\x18\x06 \x01(\x08\x12\x11\n\ttimestamp\x18\x07 \x01(\x05\x12\x0c\n\x04node\x18\x08 \x01(\t\"\xb4\x01\n\x08MapReply\x12\x11\n\twall_rect\x18\x01 \x03(\t\x12\x12\n\nsteel_rect\x18\x02 \x03(\t\x12\x12\n\nwater_rect\x18\x03 \x03(\t\x12\x13\n\x0b\x62ullet_rect\x18\x04 \x03(\t\x12\x0f\n\x07tank_id\x18\x05 \x03(\t\x12\x13\n\x0btank_facing\x18\x06 \x03(\t\x12\x11\n\ttank_rect\x18\x07 \x03(\t\x12\x11\n\ttimestamp\x18\x08 \x01(\x05\x12\x0c\n\x04node\x18\t \x01(\t\"A\n\x0bTankRequest\x12\x11\n\ttank_rect\x18\x01 \x01(\t\x12\x11\n\ttimestamp\x18\x02 \x01(\x05\x12\x0c\n\x04node\x18\x03 \x01(\t2\xfb\x01\n\x11\x62\x61ttlecityService\x12\x37\n\x05\x41\x63kOp\x12\x16.battlecity.AckRequest\x1a\x14.battlecity.AckReply\"\x00\x12\x36\n\x05GetOp\x12\x15.battlecity.OpRequest\x1a\x14.battlecity.AckReply\"\x00\x12\x38\n\x06GetMap\x12\x16.battlecity.AckRequest\x1a\x14.battlecity.MapReply\"\x00\x12;\n\x08SendTank\x12\x17.battlecity.TankRequest\x1a\x14.battlecity.AckReply\"\x00\x62\x06proto3')



_ACKREQUEST = DESCRIPTOR.message_types_by_name['AckRequest']
_ACKREPLY = DESCRIPTOR.message_types_by_name['AckReply']
_OPREQUEST = DESCRIPTOR.message_types_by_name['OpRequest']
_MAPREPLY = DESCRIPTOR.message_types_by_name['MapReply']
_TANKREQUEST = DESCRIPTOR.message_types_by_name['TankRequest']
AckRequest = _reflection.GeneratedProtocolMessageType('AckRequest', (_message.Message,), {
  'DESCRIPTOR' : _ACKREQUEST,
  '__module__' : 'proto.battlecity_pb2'
  # @@protoc_insertion_point(class_scope:battlecity.AckRequest)
  })
_sym_db.RegisterMessage(AckRequest)

AckReply = _reflection.GeneratedProtocolMessageType('AckReply', (_message.Message,), {
  'DESCRIPTOR' : _ACKREPLY,
  '__module__' : 'proto.battlecity_pb2'
  # @@protoc_insertion_point(class_scope:battlecity.AckReply)
  })
_sym_db.RegisterMessage(AckReply)

OpRequest = _reflection.GeneratedProtocolMessageType('OpRequest', (_message.Message,), {
  'DESCRIPTOR' : _OPREQUEST,
  '__module__' : 'proto.battlecity_pb2'
  # @@protoc_insertion_point(class_scope:battlecity.OpRequest)
  })
_sym_db.RegisterMessage(OpRequest)

MapReply = _reflection.GeneratedProtocolMessageType('MapReply', (_message.Message,), {
  'DESCRIPTOR' : _MAPREPLY,
  '__module__' : 'proto.battlecity_pb2'
  # @@protoc_insertion_point(class_scope:battlecity.MapReply)
  })
_sym_db.RegisterMessage(MapReply)

TankRequest = _reflection.GeneratedProtocolMessageType('TankRequest', (_message.Message,), {
  'DESCRIPTOR' : _TANKREQUEST,
  '__module__' : 'proto.battlecity_pb2'
  # @@protoc_insertion_point(class_scope:battlecity.TankRequest)
  })
_sym_db.RegisterMessage(TankRequest)

_BATTLECITYSERVICE = DESCRIPTOR.services_by_name['battlecityService']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _ACKREQUEST._serialized_start=38
  _ACKREQUEST._serialized_end=97
  _ACKREPLY._serialized_start=99
  _ACKREPLY._serialized_end=156
  _OPREQUEST._serialized_start=159
  _OPREQUEST._serialized_end=290
  _MAPREPLY._serialized_start=293
  _MAPREPLY._serialized_end=473
  _TANKREQUEST._serialized_start=475
  _TANKREQUEST._serialized_end=540
  _BATTLECITYSERVICE._serialized_start=543
  _BATTLECITYSERVICE._serialized_end=794
# @@protoc_insertion_point(module_scope)
