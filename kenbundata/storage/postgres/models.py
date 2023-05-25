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
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    ...


chunk_size = 1024 * 1024 * 4


class Url(Base):
    __tablename__ = "url"

    id = Column(UUID, primary_key=True)
    url = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)


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