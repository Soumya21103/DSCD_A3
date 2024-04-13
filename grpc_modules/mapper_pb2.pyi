from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MapperRequest(_message.Message):
    __slots__ = ("partition_index",)
    PARTITION_INDEX_FIELD_NUMBER: _ClassVar[int]
    partition_index: int
    def __init__(self, partition_index: _Optional[int] = ...) -> None: ...

class Point(_message.Message):
    __slots__ = ("x", "y")
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    x: float
    y: float
    def __init__(self, x: _Optional[float] = ..., y: _Optional[float] = ...) -> None: ...

class MapperItem(_message.Message):
    __slots__ = ("index", "point", "count")
    INDEX_FIELD_NUMBER: _ClassVar[int]
    POINT_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    index: int
    point: Point
    count: int
    def __init__(self, index: _Optional[int] = ..., point: _Optional[_Union[Point, _Mapping]] = ..., count: _Optional[int] = ...) -> None: ...

class MapperResponse(_message.Message):
    __slots__ = ("items",)
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    items: _containers.RepeatedCompositeFieldContainer[MapperItem]
    def __init__(self, items: _Optional[_Iterable[_Union[MapperItem, _Mapping]]] = ...) -> None: ...
