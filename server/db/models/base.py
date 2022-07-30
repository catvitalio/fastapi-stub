from typing import Any

from sqlalchemy import Table
from sqlalchemy.orm import as_declarative, declared_attr

from db.meta import meta


@as_declarative(metadata=meta)
class Base:
    __table__: Table
    __table_args__: tuple[Any, ...]

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
