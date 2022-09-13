from enum import Enum, unique

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    ForeignKey,
    MetaData,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ENUM as PgEnum

Base = declarative_base()

convention = {
    'all_column_names': lambda constraint, table: '_'.join(
        [column.name for column in constraint.columns.values()]
    ),
    'ix': 'ix__%(table_name)s__%(all_column_names)s',
    'uq': 'uq__%(table_name)s__%(all_column_names)s',
    'ck': 'ck__%(table_name)s__%(constraint_name)s',
    'fk': 'fk__%(table_name)s__%(all_column_names)s__%(referred_table_name)s',
    'pk': 'pk__%(table_name)s',
}

Base.metadata = MetaData(naming_convention=convention)


@unique
class ItemType(Enum):
    file = 'FILE'
    folder = 'FOLDER'


class Node(Base):
    __tablename__ = 'nodes'

    id = Column(String, primary_key=True, index=True)
    url = Column(String, nullable=True)
    date = Column(DateTime(timezone=True), nullable=False)
    parentId = Column(
        ForeignKey('nodes.id', ondelete='CASCADE'), nullable=True
    )
    type = Column(PgEnum(ItemType, name='type'), nullable=False)
    size = Column(Integer, default=0, nullable=False)
    children = relationship(
        'Node', lazy='joined', join_depth=2, cascade='all, delete'
    )
    UniqueConstraint('id', 'parentId')
