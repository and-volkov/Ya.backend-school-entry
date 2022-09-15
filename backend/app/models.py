from __future__ import annotations
from datetime import datetime as dt
from typing import Literal
from typing_extensions import Annotated

from pydantic import BaseModel, Extra, Field, PositiveInt, validator

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
    """FileNode Validation model."""
    type: Literal['FILE']
    url: str = Field(max_length=255)
    size: PositiveInt

    class Config:
        extra = Extra.forbid


class FolderNode(BaseNode):
    """FolderNode Validation model."""
    type: Literal['FOLDER']
    size: None = None
    url: None = None

    class Config:
        extra = Extra.forbid


# List of possible Node Schemas.
Items = Annotated[FileNode | FolderNode, Field(discriminator='type')]


class ImportNode(BaseModel):
    """Import Validation."""
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
    """Preprocess response model."""
    url: str | None
    size: int
    children: list[ResponseNode] | None

    @validator('date')
    def validate_date(cls, v):
        """Convert datetime to api format."""
        return v.strftime(DATE_FORMAT)

    @validator('children')
    def validate_children(cls, v):
        """Set children for file = null."""
        if not v:
            return None
        return v

    class Config:
        orm_mode = True


class ResponseUpdates(BaseModel):
    items: list[ResponseNode | None]
