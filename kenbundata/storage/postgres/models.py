import math
import uuid
from datetime import datetime

from sqlalchemy import (
    UUID,
    Column,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    LargeBinary,
    String,
)
from sqlalchemy.engine.default import DefaultExecutionContext
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import DeclarativeBase, relationship

from ...fields import CursorValue, Id, Timestamp


class Base(DeclarativeBase):
    ...


chunk_size = 1024 * 1024 * 4


def format_cursor_value(context: DefaultExecutionContext) -> str:
    params = context.current_parameters
    if params is None:
        raise ValueError("No parameters")
    return str(
        CursorValue.from_timestamp_and_id(Timestamp(params['updated_at']), Id(params.get('id', params.get('url_id'))))
    )


class Url(Base):
    __tablename__ = "url"

    id = Column(UUID, primary_key=True)
    url = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    cursor_value = Column(
        String,
        default=format_cursor_value,
        onupdate=format_cursor_value,
        index=True,
        unique=True,
        nullable=False,
    )


class Blob(Base):
    __tablename__ = 'blob'

    id = Column(UUID, primary_key=True)
    mime_type = Column(String)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    chunks = relationship(
        "Chunk", cascade="all, delete", order_by="Chunk.index", backref='parent', lazy=True, uselist=True
    )

    @hybrid_property
    def data(self) -> bytes:
        return b''.join((d.body_chunk for d in self.chunks))

    @data.setter
    def _(self, value: bytes) -> None:
        self.chunks = [
            Chunk(parent=self, index=i, body_chunk=value[(i * chunk_size) : min(len(value), (i + 1) * chunk_size)])
            for i in range(math.ceil(len(value) / chunk_size))
        ]


class Chunk(Base):
    __tablename__ = 'chunk'

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    blob_id = Column(UUID, ForeignKey('blob.id', ondelete='CASCADE'))
    index = Column(Integer)
    body_chunk = Column(LargeBinary)

    __table_args__ = (Index('uk_chunk_blob_id_index', 'blob_id', 'index', unique=True),)
