from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class coordinate(_message.Message):
    __slots__ = ("x", "y")
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    x: int
    y: int
    def __init__(self, x: _Optional[int] = ..., y: _Optional[int] = ...) -> None: ...

class invokeMapper(_message.Message):
    __slots__ = ("startIndex", "endIndex", "centroids")
    STARTINDEX_FIELD_NUMBER: _ClassVar[int]
    ENDINDEX_FIELD_NUMBER: _ClassVar[int]
    CENTROIDS_FIELD_NUMBER: _ClassVar[int]
    startIndex: int
    endIndex: int
    centroids: _containers.RepeatedCompositeFieldContainer[coordinate]
    def __init__(self, startIndex: _Optional[int] = ..., endIndex: _Optional[int] = ..., centroids: _Optional[_Iterable[_Union[coordinate, _Mapping]]] = ...) -> None: ...

class invokeReducer(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class response(_message.Message):
    __slots__ = ("willWork", "id")
    WILLWORK_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    willWork: bool
    id: int
    def __init__(self, willWork: bool = ..., id: _Optional[int] = ...) -> None: ...

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
