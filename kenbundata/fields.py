import uuid
from abc import ABCMeta, abstractmethod
from base64 import (
    b64encode,
    standard_b64decode,
    standard_b64encode,
    urlsafe_b64decode,
    urlsafe_b64encode,
)
from collections.abc import Callable, Generator
from datetime import datetime as _datetime
from datetime import timezone as _timezone
from enum import Enum
from io import BytesIO
from typing import Any, Generic, Optional, TypeVar, Union
from uuid import UUID

from PIL import Image

T = TypeVar("T")


class Serializable(Generic[T], metaclass=ABCMeta):
    @abstractmethod
    def serialize(self) -> T:
        raise NotImplementedError


class Id(UUID, Serializable[str]):
    r"""Id is a UUID4 type that can be used as a primary key.
    >>> from unittest.mock import patch
    >>> with patch("uuid.uuid4", return_value=UUID('cf57432e-809e-4353-adbd-9d5c0d733868')):
    ...     x = Id.generate()
    ...
    >>> x
    Id('z1dDLoCeQ1OtvZ1cDXM4aA')
    >>> x.bytes
    b'\xcfWC.\x80\x9eCS\xad\xbd\x9d\\\rs8h'
    >>> x.hex
    'cf57432e809e4353adbd9d5c0d733868'
    >>> x.int
    275603287559914445491632874575877060712
    >>> x == Id('cf57432e809e4353adbd9d5c0d733868')
    True
    >>> x == Id('z1dDLoCeQ1OtvZ1cDXM4aA')
    True
    >>> x == Id(275603287559914445491632874575877060712)
    True
    """

    def __init__(self, value: Union[str, UUID, bytes, int]) -> None:
        if isinstance(value, UUID):
            super(Id, self).__init__(value.hex)
            return
        if isinstance(value, int):
            super(Id, self).__init__(value.to_bytes(16, "big").hex())
            return
        if isinstance(value, bytes):
            super(Id, self).__init__(value.hex())
            return
        if len(value) == 22:
            super(Id, self).__init__(urlsafe_b64decode(value + "==").hex())
            return
        super(Id, self).__init__(value)

    @classmethod
    def generate(cls) -> "Id":
        return cls(uuid.uuid4().hex)

    @property
    def b64encoded(self) -> str:
        return urlsafe_b64encode(self.bytes).rstrip(b"=").decode("utf-8")

    def __str__(self) -> str:
        return self.b64encoded

    def serialize(self) -> str:
        return self.b64encoded

    @classmethod
    def __get_validators__(cls) -> Generator[Callable[[Any], "Id"], None, None]:
        yield cls.validate

    @classmethod
    def validate(cls, v: Any) -> "Id":
        if isinstance(v, cls):
            return v
        if isinstance(v, (UUID, bytes, str, int)):
            return cls(v)
        raise ValueError(f"Cannot convert {v} to {cls}")


class Timestamp(int):
    """
    Timestamp class
    >>> a = Timestamp(1674397764479000)
    >>> a
    Timestamp(1674397764479000)
    >>> a.milliseconds
    1674397764479
    >>> a.microseconds
    1674397764479000
    >>> a.datetime
    datetime.datetime(2023, 1, 22, 14, 29, 24, 479000, tzinfo=datetime.timezone.utc)
    >>> dt = a.datetime
    >>> Timestamp.from_datetime(dt)
    Timestamp(1674397764479000)
    >>> ts = dt.timestamp()
    >>> Timestamp.from_float(ts)
    Timestamp(1674397764479000)
    """

    @property
    def milliseconds(self) -> int:
        """
        >>> a = Timestamp(1674365364479000)
        >>> a.milliseconds
        1674365364479
        """
        return int(self // 1000)

    @property
    def microseconds(self) -> int:
        """
        >>> a = Timestamp(1674365364479000)
        >>> a.microseconds
        1674365364479000
        """
        return int(self)

    @property
    def datetime(self) -> _datetime:
        """
        >>> a = Timestamp(1674397764479000)
        >>> a.datetime
        datetime.datetime(2023, 1, 22, 14, 29, 24, 479000, tzinfo=datetime.timezone.utc)
        """
        return _datetime.fromtimestamp(self / 1000000, tz=_timezone.utc)

    @classmethod
    def from_datetime(cls, dt: _datetime) -> "Timestamp":
        """
        >>> Timestamp.from_datetime(_datetime(2023, 1, 22, 14, 29, 24, 479000, tzinfo=_timezone.utc))
        Timestamp(1674397764479000)
        """
        return cls.from_float(dt.timestamp())

    @classmethod
    def from_float(cls, f: float) -> "Timestamp":
        """
        >>> Timestamp.from_datetime(_datetime(2023, 1, 22, 14, 29, 24, 479000, tzinfo=_timezone.utc))
        Timestamp(1674397764479000)
        """
        return cls(int(f * 1000000))

    @classmethod
    def now(cls) -> "Timestamp":
        """
        >>> import freezegun
        >>> from datetime import timedelta, timezone
        >>> with freezegun.freeze_time(_datetime(2023, 1, 22, 14, 29, 23, 123321, tzinfo=_timezone.utc)):
        ...     Timestamp.now()
        Timestamp(1674397763123321)
        """
        return cls.from_datetime(_datetime.utcnow())

    def __repr__(self) -> str:
        return f"Timestamp({super(Timestamp, self).__repr__()})"


class MimeType(str, Enum):
    """
    >>> MimeType("application/json")
    <MimeType.application_json: 'application/json'>
    >>> MimeType("application/json").value
    'application/json'
    >>> MimeType("application/json").name
    'application_json'
    >>> MimeType("application/json").mime_type
    'application/json'
    >>> MimeType("application/json").extension
    'json'
    >>> MimeType("text/plain").extension
    'txt'
    >>> MimeType("application/octet-stream").extension
    'bin'
    >>> MimeType("nonsuch/mimetype")
    Traceback (most recent call last):
        ...
    ValueError: 'nonsuch/mimetype' is not a valid MimeType
    """

    application_json = "application/json"
    application_octet_stream = "application/octet-stream"
    application_pdf = "application/pdf"
    application_xml = "application/xml"
    application_zip = "application/zip"
    image_gif = "image/gif"
    image_jpeg = "image/jpeg"
    image_png = "image/png"
    image_svg_xml = "image/svg+xml"
    image_tiff = "image/tiff"
    text_html = "text/html"
    text_plain = "text/plain"
    text_xml = "text/xml"

    @property
    def mime_type(self) -> str:
        return self.value

    @property
    def extension(self) -> str:
        return {"text/plain": "txt", "application/octet-stream": "bin"}.get(self.value, self.value.split("/")[-1])


class Bytes(bytes, Serializable[str]):
    r"""
    >>> Bytes(b"hello")
    Bytes(b'hello')
    >>> Bytes("aGVsbG8=")
    Bytes(b'hello')
    >>> Bytes(123)
    Bytes(b'{')
    >>> Bytes(b"hello").hex()
    '68656c6c6f'
    >>> Bytes(b"hello").b64encoded
    'aGVsbG8='
    >>> Bytes(b"hello").urlsafe_b64encoded
    'aGVsbG8='
    """

    def __new__(cls, value: Union[bytes, str, int]) -> "Bytes":
        if isinstance(value, bytes):
            return super(Bytes, cls).__new__(cls, value)
        if isinstance(value, str):
            return super(Bytes, cls).__new__(cls, standard_b64decode(value))
        if isinstance(value, int):
            return super(Bytes, cls).__new__(cls, value.to_bytes((value.bit_length() + 7) // 8, "big"))
        raise ValueError(f"Cannot create Bytes from {value}")

    @property
    def b64encoded(self) -> str:
        return b64encode(self).decode("utf-8")

    @property
    def urlsafe_b64encoded(self) -> str:
        return urlsafe_b64encode(self).decode("utf-8")

    @property
    def standard_b64encoded(self) -> str:
        return standard_b64encode(self).decode("utf-8")

    def __repr__(self) -> str:
        return f"Bytes({super(Bytes, self).__repr__()})"

    @classmethod
    def __get_validators__(cls) -> Generator[Callable[[Any], "Bytes"], None, None]:
        yield cls.validate

    @classmethod
    def validate(cls, v: Any) -> "Bytes":
        if isinstance(v, cls):
            return v
        return cls(v)

    def serialize(self) -> str:
        return self.standard_b64encoded


class EncodedImage(str):
    """
    >>> from PIL import Image
    >>> image = Image.new("RGB", (1, 1))
    >>> EncodedImage.from_image(image)
    EncodedImage('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAADElEQVR4nGNgYGAAAAAEAAH2FzhVAAAAAElFTkSuQmCC')
    >>> EncodedImage.from_image(image).image.size
    (1, 1)
    >>> EncodedImage.from_image(image).image.mode
    'RGB'
    >>> EncodedImage.from_image(image).image.format
    'PNG'
    >>> EncodedImage.from_image(image).image.getpixel((0, 0))
    (0, 0, 0)
    >>> encoded_image = EncodedImage(
    ...     'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAADElEQVR4nGNgYGAAAAAEAAH2FzhVAAAAAElFTkSuQmCC')
    >>> encoded_image.image.size
    (1, 1)
    >>> encoded_image.image.mode
    'RGB'
    >>> encoded_image.image.format
    'PNG'
    >>> encoded_image.image.getpixel((0, 0))
    (0, 0, 0)
    """

    def __init__(self, value: str) -> None:
        super(EncodedImage, self).__init__()
        self._image: Optional[Image.Image] = None

    @classmethod
    def from_image(cls, image: Image.Image) -> "EncodedImage":
        buf = BytesIO()
        image.save(buf, format="png")
        return EncodedImage(standard_b64encode(buf.getvalue()).decode("utf-8"))

    @property
    def image(self) -> Image.Image:
        if self._image is None:
            self._image = Image.open(BytesIO(standard_b64decode(self)), formats=("png",))
            self._image.load()
        return self._image

    @classmethod
    def __get_validators__(cls) -> Generator[Callable[[Any], "EncodedImage"], None, None]:
        yield cls._validate_image_can_be_loaded

    @classmethod
    def _validate_image_can_be_loaded(cls, v: Any) -> "EncodedImage":
        if isinstance(v, Image.Image):
            v = cls.from_image(v)
        if not isinstance(v, str):
            raise TypeError(f"PIL.Image.Image or str required. not {type(v)}")
        v = EncodedImage(v)
        v.image
        return v

    def __repr__(self) -> str:
        return f"EncodedImage({super(EncodedImage, self).__repr__()})"
