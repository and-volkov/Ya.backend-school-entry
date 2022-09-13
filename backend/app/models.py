from __future__ import annotations
from datetime import datetime as dt
from typing import Literal
from typing_extensions import Annotated

from pydantic import BaseModel, Field, PositiveInt, validator

from backend.db.schema import ItemType

DATE_FORMAT = '%Y-%m-%dT%H:%M:%SZ'


class BaseNode(BaseModel):
    id: str
    date: dt | None
    parentId: str | None
    type: ItemType

    class Config:
        orm_mode = True


class FileNode(BaseNode):
    type: Literal['FILE']
    url: str = Field(max_length=255)
    size: PositiveInt


class FolderNode(BaseNode):
    type: Literal['FOLDER']
    size: None = None
    url: None = None


Items = Annotated[FileNode | FolderNode, Field(discriminator='type')]


class ImportNode(BaseModel):
    items: list[Items] = Field(unique_items=True)
    updateDate: str

    @validator('updateDate', pre=True)
    def validate_date(cls, v):
        try:
            dt.strptime(v, DATE_FORMAT)
        except Exception:
            raise ValueError('Invalid date format, use ISO 8601')
        return v

    class Config:
        orm_mode = True


class ResponseNode(BaseNode):
    url: str | None
    size: int
    children: list[ResponseNode] | None

    @validator('date')
    def validate_date(cls, v):
        return v.strftime(DATE_FORMAT)

    @validator('children')
    def validate_children(cls, v):
        if not v:
            return None
        return v

    class Config:
        orm_mode = True


class ResponseUpdates(BaseModel):
    items: list[ResponseNode | None]
