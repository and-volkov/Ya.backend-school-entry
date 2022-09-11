from enum import Enum, unique

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column, DateTime, Integer, ForeignKey,
    MetaData, String, PrimaryKeyConstraint, UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import ENUM as PgEnum

Base = declarative_base()

convention = {
    'all_column_names': lambda constraint, table: '_'.join([
        column.name for column in constraint.columns.values()
    ]),
    'ix': 'ix__%(table_name)s__%(all_column_names)s',
    'uq': 'uq__%(table_name)s__%(all_column_names)s',
    'ck': 'ck__%(table_name)s__%(constraint_name)s',
    'fk': 'fk__%(table_name)s__%(all_column_names)s__%(referred_table_name)s',
    'pk': 'pk__%(table_name)s'
}

Base.metadata = MetaData(naming_convention=convention)


@unique
class ItemType(str, Enum):
    file = 'FILE'
    folder = 'FOLDER'


class Node(Base):
    __tablename__ = 'nodes'

    id = Column(String, primary_key=True, index=True, unique=True)
    url = Column(String, nullable=True)
    date = Column(DateTime, nullable=False)
    type = Column(PgEnum(ItemType, name='type'), nullable=False)
    size = Column(Integer, nullable=True)


class Relation(Base):
    __tablename__ = 'relations'
    __table_args__ = (
        PrimaryKeyConstraint('parent_id', 'children_id'),
    )

    parent_id = Column(
        String, ForeignKey('nodes.id', ondelete='SET NULL'), nullable=True
    )
    children_id = Column(String, ForeignKey('nodes.id', ondelete='CASCADE'))
    UniqueConstraint(parent_id, children_id)
