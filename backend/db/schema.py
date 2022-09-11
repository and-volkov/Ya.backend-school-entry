from enum import Enum, unique

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    ForeignKey,
    MetaData,
    String,
    Table,
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

relations_table = Table(
    'relations_table',
    Base.metadata,
    Column('parent_id', String, ForeignKey('nodes.id'), primary_key=True),
    Column('child_id', String, ForeignKey('nodes.id'), primary_key=True)
)


@unique
class ItemType(Enum):
    file = 'FILE'
    folder = 'FOLDER'


class Node(Base):
    __tablename__ = 'nodes'

    id = Column(String, primary_key=True, index=True, unique=True)
    url = Column(String, nullable=True)
    date = Column(DateTime, nullable=False)
    parentId = Column(
        ForeignKey('nodes.id', ondelete='SET NULL'), nullable=True
    )
    type = Column(PgEnum(ItemType, name='type'), nullable=False)
    size = Column(Integer, nullable=True)
    children = relationship(
        'Node',
        secondary=relations_table,
        primaryjoin=id == relations_table.c.parent_id,
        secondaryjoin=id == relations_table.c.child_id,
        backref='parent'
    )
    UniqueConstraint('id', 'parentId')
