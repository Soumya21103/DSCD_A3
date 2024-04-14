from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class MapperRequest(_message.Message):
    __slots__ = ("inputData",)
    INPUTDATA_FIELD_NUMBER: _ClassVar[int]
    inputData: str
    def __init__(self, inputData: _Optional[str] = ...) -> None: ...

class MapperResponse(_message.Message):
    __slots__ = ("intermediateData", "status")
    INTERMEDIATEDATA_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    intermediateData: str
    status: bool
    def __init__(self, intermediateData: _Optional[str] = ..., status: bool = ...) -> None: ...

class ReducerRequest(_message.Message):
    __slots__ = ("intermediateData",)
    INTERMEDIATEDATA_FIELD_NUMBER: _ClassVar[int]
    intermediateData: str
    def __init__(self, intermediateData: _Optional[str] = ...) -> None: ...

class ReducerResponse(_message.Message):
    __slots__ = ("output", "status")
    OUTPUT_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    output: str
    status: bool
    def __init__(self, output: _Optional[str] = ..., status: bool = ...) -> None: ...
