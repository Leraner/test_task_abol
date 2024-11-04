from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Metadata(_message.Message):
    __slots__ = ("name", "size", "content_type")
    NAME_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    CONTENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    name: str
    size: int
    content_type: str
    def __init__(self, name: _Optional[str] = ..., size: _Optional[int] = ..., content_type: _Optional[str] = ...) -> None: ...

class UploadImageRequest(_message.Message):
    __slots__ = ("meta", "image")
    META_FIELD_NUMBER: _ClassVar[int]
    IMAGE_FIELD_NUMBER: _ClassVar[int]
    meta: Metadata
    image: bytes
    def __init__(self, meta: _Optional[_Union[Metadata, _Mapping]] = ..., image: _Optional[bytes] = ...) -> None: ...

class UploadImageResponse(_message.Message):
    __slots__ = ("images",)
    IMAGES_FIELD_NUMBER: _ClassVar[int]
    images: _containers.RepeatedCompositeFieldContainer[Image]
    def __init__(self, images: _Optional[_Iterable[_Union[Image, _Mapping]]] = ...) -> None: ...

class GetImagesRequest(_message.Message):
    __slots__ = ("page", "size")
    PAGE_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    page: int
    size: int
    def __init__(self, page: _Optional[int] = ..., size: _Optional[int] = ...) -> None: ...

class Image(_message.Message):
    __slots__ = ("id", "name", "file_path", "upload_date", "resolution", "size")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    FILE_PATH_FIELD_NUMBER: _ClassVar[int]
    UPLOAD_DATE_FIELD_NUMBER: _ClassVar[int]
    RESOLUTION_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    file_path: str
    upload_date: str
    resolution: str
    size: int
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., file_path: _Optional[str] = ..., upload_date: _Optional[str] = ..., resolution: _Optional[str] = ..., size: _Optional[int] = ...) -> None: ...

class GetImagesResponse(_message.Message):
    __slots__ = ("has_next_page", "has_previous_page", "total_count", "total_pages", "page", "items")
    HAS_NEXT_PAGE_FIELD_NUMBER: _ClassVar[int]
    HAS_PREVIOUS_PAGE_FIELD_NUMBER: _ClassVar[int]
    TOTAL_COUNT_FIELD_NUMBER: _ClassVar[int]
    TOTAL_PAGES_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    has_next_page: bool
    has_previous_page: bool
    total_count: int
    total_pages: int
    page: int
    items: _containers.RepeatedCompositeFieldContainer[Image]
    def __init__(self, has_next_page: bool = ..., has_previous_page: bool = ..., total_count: _Optional[int] = ..., total_pages: _Optional[int] = ..., page: _Optional[int] = ..., items: _Optional[_Iterable[_Union[Image, _Mapping]]] = ...) -> None: ...

class GetImageRequest(_message.Message):
    __slots__ = ("image_id",)
    IMAGE_ID_FIELD_NUMBER: _ClassVar[int]
    image_id: str
    def __init__(self, image_id: _Optional[str] = ...) -> None: ...

class GetImageResponse(_message.Message):
    __slots__ = ("image",)
    IMAGE_FIELD_NUMBER: _ClassVar[int]
    image: Image
    def __init__(self, image: _Optional[_Union[Image, _Mapping]] = ...) -> None: ...

class DeleteImagesRequest(_message.Message):
    __slots__ = ("all_", "images_ids")
    ALL__FIELD_NUMBER: _ClassVar[int]
    IMAGES_IDS_FIELD_NUMBER: _ClassVar[int]
    all_: bool
    images_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, all_: bool = ..., images_ids: _Optional[_Iterable[str]] = ...) -> None: ...

class DeleteImagesResponse(_message.Message):
    __slots__ = ("images",)
    IMAGES_FIELD_NUMBER: _ClassVar[int]
    images: _containers.RepeatedCompositeFieldContainer[Image]
    def __init__(self, images: _Optional[_Iterable[_Union[Image, _Mapping]]] = ...) -> None: ...

class UpdateImagesRequest(_message.Message):
    __slots__ = ("image_id", "update_schema")
    IMAGE_ID_FIELD_NUMBER: _ClassVar[int]
    UPDATE_SCHEMA_FIELD_NUMBER: _ClassVar[int]
    image_id: str
    update_schema: str
    def __init__(self, image_id: _Optional[str] = ..., update_schema: _Optional[str] = ...) -> None: ...

class UpdateImagesResponse(_message.Message):
    __slots__ = ("images",)
    IMAGES_FIELD_NUMBER: _ClassVar[int]
    images: _containers.RepeatedCompositeFieldContainer[Image]
    def __init__(self, images: _Optional[_Iterable[_Union[Image, _Mapping]]] = ...) -> None: ...
