from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ifComplete(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class status(_message.Message):
    __slots__ = ("ifDone", "id")
    IFDONE_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    ifDone: bool
    id: int
    def __init__(self, ifDone: bool = ..., id: _Optional[int] = ...) -> None: ...
