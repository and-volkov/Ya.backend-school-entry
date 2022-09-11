from __future__ import annotations
from datetime import datetime as dt
from typing import Literal, Optional
from typing_extensions import Annotated

from pydantic import BaseModel, Field, PositiveInt, validator, root_validator

from backend.db.schema import ItemType


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
        format_string = '%Y-%m-%dT%H:%M:%SZ'
        try:
            dt.strptime(v, format_string)
        except Exception:
            raise ValueError('Invalid date format, use ISO 8601')
        return v

    class Config:
        fields = {'parentId': {'exclude': True}}
        orm_mode = True


class RetrieveFileNode(BaseNode):
    children: None


class RetrieveFolderNode(BaseNode):
    children: list[RetrieveFolderNode | RetrieveFileNode] = []


RetrieveFolderNode.update_forward_refs()


class NodeRelation(BaseModel):
    parent_id: str
    children_id: str
