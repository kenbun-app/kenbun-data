import binascii
import re
import uuid
from abc import ABCMeta, abstractmethod
from base64 import (
    b64encode,
    standard_b64decode,
    standard_b64encode,
    urlsafe_b64decode,
    urlsafe_b64encode,
)
from collections.abc import Callable, Generator, Mapping
from datetime import datetime as _datetime
from datetime import timezone as _timezone
from enum import Enum
from io import BytesIO
from typing import Any, Generic, Optional, TypeVar, Union
from uuid import UUID

from dateutil.parser import parse as parse_datetime
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
    >>> x.uuid
    'cf57432e-809e-4353-adbd-9d5c0d733868'
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

    @property
    def uuid(self) -> str:
        return super(Id, self).__str__()

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
    >>> ts = dt.timestamp()
    >>> Timestamp(dt)
    Timestamp(1674397764479000)
    >>> Timestamp(ts)
    Timestamp(1674397764479000)
    >>> Timestamp("2023-01-22T14:29:24.422Z")
    Timestamp(1674397764422000)
    >>> Timestamp("2023/02/12 12:21:12")
    Timestamp(1676172072000000)
    >>> Timestamp("invalid")
    Traceback (most recent call last):
      ...
    dateutil.parser._parser.ParserError: Unknown string format: invalid

    """

    def __new__(cls, value: Union[int, float, _datetime, str]) -> "Timestamp":
        if isinstance(value, _datetime):
            return super(Timestamp, cls).__new__(cls, int(value.timestamp() * 1000000))
        if isinstance(value, str):
            return super(Timestamp, cls).__new__(cls, int(parse_datetime(value).timestamp() * 1000000))
        if isinstance(value, float):
            return super(Timestamp, cls).__new__(cls, int(value * 1000000))
        return super(Timestamp, cls).__new__(cls, value)

    @classmethod
    def __get_validators__(cls) -> Generator[Callable[[Any], "Timestamp"], None, None]:
        yield cls.validate

    @classmethod
    def validate(cls, v: Any) -> "Timestamp":
        if isinstance(v, cls):
            return v
        if isinstance(v, (int, float, _datetime, str)):
            return cls(v)
        raise ValueError(f"Cannot convert {v} to {cls}")

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
    def now(cls) -> "Timestamp":
        """
        >>> import freezegun
        >>> from datetime import timedelta, timezone
        >>> with freezegun.freeze_time(_datetime(2023, 1, 22, 14, 29, 23, 123321, tzinfo=_timezone.utc)):
        ...     Timestamp.now()
        Timestamp(1674397763123321)
        """
        return cls(_datetime.utcnow())

    def __repr__(self) -> str:
        return f"Timestamp({super(Timestamp, self).__repr__()})"


class MimeType(str):
    _regex = re.compile(
        r"^(?P<type>[a-z]+)/(?P<subtype>[a-z0-9\-\+\.]+)(?P<params>(;\s?[a-zA-Z0-9\-\+\.]+=[a-zA-Z0-9\-\+\.]+)*)$"
    )
    """
    >>> MimeType("application/json")
    MimeType('application/json')
    >>> str(MimeType("application/json"))
    'application/json'
    >>> mt = MimeType("text/plain;charset=utf-8")
    >>> mt.type
    'text'
    >>> mt.subtype
    'plain'
    >>> mt.parameters
    {'charset': 'utf-8'}
    >>> mt
    MimeType('text/plain;charset=utf-8')
    >>> MimeType("wrongformat")
    Traceback (most recent call last):
        ...
    ValueError: 'wrongformat' is not a valid MimeType
    """

    def __init__(self, value: str) -> None:
        super(MimeType, self).__init__()
        if len(value) == 0:
            self._type = ""
            self._subtype = ""
            self._parameters = {}
        else:
            m = self._regex.match(value)
            if m is None:
                raise ValueError(f"'{value}' is not a valid MimeType")
            self._type = m.group("type")
            self._subtype = m.group("subtype")
            self._parameters = dict([p.split("=") for p in m.group("params").split(";")[1:]])

    @property
    def type(self) -> str:
        return self._type

    @property
    def subtype(self) -> str:
        return self._subtype

    @property
    def parameters(self) -> Mapping[str, str]:
        return self._parameters

    def __repr__(self) -> str:
        return f"MimeType('{self}')"

    @classmethod
    def __get_validators__(cls) -> Generator[Callable[[Any], "MimeType"], None, None]:
        yield cls.validate

    @classmethod
    def validate(cls, v: Any) -> "MimeType":
        if isinstance(v, cls):
            return v
        if isinstance(v, str):
            m = cls._regex.match(v)
            if m is None:
                raise ValueError(f"'{v}' is not a valid MimeType")
            return cls(v)
        raise ValueError(f"Cannot convert {v} to {cls}")


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


class CursorValue(str):
    """
    >>> CursorValue("1674397764479|z1dDLoCeQ1OtvZ1cDXM4aA")
    CursorValue('1674397764479|z1dDLoCeQ1OtvZ1cDXM4aA')
    >>> CursorValue("12345679098|z1dDLoCeQ1OtvZ1cDXM4aA")
    Traceback (most recent call last):
     ...
    ValueError: Invalid cursor value: 12345679098|z1dDLoCeQ1OtvZ1cDXM4aA
    """

    cursor_regex = re.compile(r"^\d{13}\|[a-zA-Z0-9_-]{22}$")

    def __init__(self, value: str) -> None:
        super(CursorValue, self).__init__()
        if not self.cursor_regex.match(value):
            raise ValueError(f"Invalid cursor value: {value}")

    @classmethod
    def __get_validators__(cls) -> Generator[Callable[[Any], "CursorValue"], None, None]:
        yield cls.validate

    @classmethod
    def validate(cls, v: Any) -> "CursorValue":
        if isinstance(v, cls):
            return v
        if not isinstance(v, str):
            raise TypeError(f"str required. not {type(v)}")
        return cls(v)

    def __repr__(self) -> str:
        return f"CursorValue({super(CursorValue, self).__repr__()})"

    @classmethod
    def from_timestamp_and_id(cls, ts: Timestamp, id: Id) -> "CursorValue":
        return cls(f"{ts}|{id}")


class Cursor(str):
    """
    >>> Cursor("PHwxNjc0Mzk3NzY0NDc5fHoxZERMb0NlUTFPdHZaMWNEWE00YUE=")
    Cursor('PHwxNjc0Mzk3NzY0NDc5fHoxZERMb0NlUTFPdHZaMWNEWE00YUE=')
    >>> Cursor("invalid")
    Traceback (most recent call last):
     ...
    ValueError: Invalid cursor value: invalid
    >>> Cursor.from_value("1674397764479|z1dDLoCeQ1OtvZ1cDXM4aA", Cursor.Direction.NEXT)
    Cursor('PnwxNjc0Mzk3NzY0NDc5fHoxZERMb0NlUTFPdHZaMWNEWE00YUE=')
    >>> Cursor.from_value("1674397764479|z1dDLoCeQ1OtvZ1cDXM4aA", Cursor.Direction.PREV)
    Cursor('PHwxNjc0Mzk3NzY0NDc5fHoxZERMb0NlUTFPdHZaMWNEWE00YUE=')
    >>> Cursor.from_value("invalid", Cursor.Direction.NEXT)
    Traceback (most recent call last):
        ...
    ValueError: Invalid cursor value: PnxpbnZhbGlk
    >>> Cursor("PHwxNjc0Mzk3NzY0NDc5fHoxZERMb0NlUTFPdHZaMWNEWE00YUE=").decode()
    '<|1674397764479|z1dDLoCeQ1OtvZ1cDXM4aA'
    >>> Cursor("PnwxNjc0Mzk3NzY0NDc5fHoxZERMb0NlUTFPdHZaMWNEWE00YUE=").direction
    <Direction.NEXT: '>'>
    >>> Cursor("PHwxNjc0Mzk3NzY0NDc5fHoxZERMb0NlUTFPdHZaMWNEWE00YUE=").direction
    <Direction.PREV: '<'>
    >>> Cursor("PHwxNjc0Mzk3NzY0NDc5fHoxZERMb0NlUTFPdHZaMWNEWE00YUE=").is_next()
    False
    >>> Cursor("PnwxNjc0Mzk3NzY0NDc5fHoxZERMb0NlUTFPdHZaMWNEWE00YUE=").is_next()
    True
    >>> Cursor("PHwxNjc0Mzk3NzY0NDc5fHoxZERMb0NlUTFPdHZaMWNEWE00YUE=").is_prev()
    True
    >>> Cursor("PnwxNjc0Mzk3NzY0NDc5fHoxZERMb0NlUTFPdHZaMWNEWE00YUE=").is_prev()
    False
    >>> Cursor("PHwxNjc0Mzk3NzY0NDc5fHoxZERMb0NlUTFPdHZaMWNEWE00YUE=").value
    CursorValue('1674397764479|z1dDLoCeQ1OtvZ1cDXM4aA')
    """

    class Direction(str, Enum):
        NEXT = ">"
        PREV = "<"

    cursor_regex = re.compile(r"^[<>]\|\d{13}\|[a-zA-Z0-9_-]{22}$")

    def __init__(self, value: str) -> None:
        super(Cursor, self).__init__()
        try:
            raw = urlsafe_b64decode(value).decode("utf-8")
        except binascii.Error:
            raise ValueError(f"Invalid cursor value: {value}")
        if not self.cursor_regex.match(raw):
            raise ValueError(f"Invalid cursor value: {value}")

    def __repr__(self) -> str:
        return f"Cursor({super(Cursor, self).__repr__()})"

    @classmethod
    def from_value(cls, value: CursorValue, direction: Direction) -> "Cursor":
        return cls(urlsafe_b64encode(f"{direction.value}|{value}".encode("utf-8")).decode("utf-8"))

    @classmethod
    def __get_validators__(cls) -> Generator[Callable[[Any], "Cursor"], None, None]:
        yield cls.validate

    @classmethod
    def validate(cls, v: Any) -> "Cursor":
        if isinstance(v, cls):
            return v
        if not isinstance(v, str):
            raise TypeError(f"str required. not {type(v)}")
        return cls(v)

    def decode(self) -> str:
        return urlsafe_b64decode(self).decode("utf-8")

    @property
    def direction(self) -> Direction:
        return self.Direction(self.decode()[0])

    def is_next(self) -> bool:
        return self.direction == self.Direction.NEXT

    def is_prev(self) -> bool:
        return self.direction == self.Direction.PREV

    @property
    def value(self) -> CursorValue:
        return CursorValue(self.decode()[2:])
