from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class HeartBeatRequest(_message.Message):
    __slots__ = ("reducer_id",)
    REDUCER_ID_FIELD_NUMBER: _ClassVar[int]
    reducer_id: int
    def __init__(self, reducer_id: _Optional[int] = ...) -> None: ...

class HeartBeatResponse(_message.Message):
    __slots__ = ("reducer_id", "status")
    REDUCER_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    reducer_id: int
    status: bool
    def __init__(self, reducer_id: _Optional[int] = ..., status: bool = ...) -> None: ...

class OutputFileRequest(_message.Message):
    __slots__ = ("reducer_id", "out_file_name")
    REDUCER_ID_FIELD_NUMBER: _ClassVar[int]
    OUT_FILE_NAME_FIELD_NUMBER: _ClassVar[int]
    reducer_id: int
    out_file_name: str
    def __init__(self, reducer_id: _Optional[int] = ..., out_file_name: _Optional[str] = ...) -> None: ...

class OutputFileResponse(_message.Message):
    __slots__ = ("reducer_id", "out_file_name", "out_file_line")
    REDUCER_ID_FIELD_NUMBER: _ClassVar[int]
    OUT_FILE_NAME_FIELD_NUMBER: _ClassVar[int]
    OUT_FILE_LINE_FIELD_NUMBER: _ClassVar[int]
    reducer_id: int
    out_file_name: str
    out_file_line: str
    def __init__(self, reducer_id: _Optional[int] = ..., out_file_name: _Optional[str] = ..., out_file_line: _Optional[str] = ...) -> None: ...

class centroidKeys(_message.Message):
    __slots__ = ("centroid_id", "x", "y")
    CENTROID_ID_FIELD_NUMBER: _ClassVar[int]
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    centroid_id: int
    x: float
    y: float
    def __init__(self, centroid_id: _Optional[int] = ..., x: _Optional[float] = ..., y: _Optional[float] = ...) -> None: ...

class invocationRequest(_message.Message):
    __slots__ = ("reducer_id", "mapper_socket", "centroids")
    REDUCER_ID_FIELD_NUMBER: _ClassVar[int]
    MAPPER_SOCKET_FIELD_NUMBER: _ClassVar[int]
    CENTROIDS_FIELD_NUMBER: _ClassVar[int]
    reducer_id: int
    mapper_socket: _containers.RepeatedScalarFieldContainer[str]
    centroids: _containers.RepeatedCompositeFieldContainer[centroidKeys]
    def __init__(self, reducer_id: _Optional[int] = ..., mapper_socket: _Optional[_Iterable[str]] = ..., centroids: _Optional[_Iterable[_Union[centroidKeys, _Mapping]]] = ...) -> None: ...

class invocationResponse(_message.Message):
    __slots__ = ("reducer_id", "status")
    REDUCER_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    reducer_id: int
    status: bool
    def __init__(self, reducer_id: _Optional[int] = ..., status: bool = ...) -> None: ...
