from pydantic import BaseModel, Field
from typing import List,Optional
from redis.commands.search.field import TextField, TagField, NumericField



class OutletIndexSchema:
    name = "outlets_index"
    prefix = "outlets:"
    schema = (
        TextField("name"),
        TagField("email"),
        TagField("twitter")
    )
class ReporterIndexSchema:
    name = "reporters_index"
    prefix = "reporters:"
    schema = (
    TextField("name"),
    TagField("email"),
    TagField("twitter"),
    NumericField("outlet_id")
)


class DuplicateIn(BaseModel):
    table: str = Field(..., pattern="^(tbl_reporters|tbl_outlets)$", description="The table to check for duplicates")
    field: str = Field(..., pattern="^(name|email|twitter)$", description="The field to check for duplicates")
    value: str = Field(..., description="The value to check for duplicates")

class Duplicate(BaseModel):
    class Config:
        extra = 'allow'  # Allows extra fields not explicitly defined


class RDuplicateOut(Duplicate):
    reporter_id: str
    name: str
    outlet_id : Optional[int] = None

class RCheckDuplicatesResponse(BaseModel):
    duplicates: List[RDuplicateOut]


class ODuplicateOut(Duplicate):
    id: str
    name: str

class OCheckDuplicatesResponse(BaseModel):
    duplicates: List[ODuplicateOut]
