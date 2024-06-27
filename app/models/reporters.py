from app import connections
from typing import Optional
from redis_om import HashModel
from pydantic import validator

class BaseModel(HashModel):

    def __init__(self, **data):
        # Convert None values to empty strings
        data = {key: '' if value is None else value for key, value in data.items()}
        super().__init__(**data)

    class Meta:
        database = connections.redis_client

class Reporter(BaseModel):

    name: Optional[str] = None
    email: Optional[str] = None
    twitter: Optional[str] = None
    outlet_id: Optional[int] = None
    active: Optional[int] = None

    @validator('active', pre=True)
    def convert_bool_to_int(cls, value):
        if isinstance(value, bool):
            return 1 if value else 0
        return value
    
    class Meta:
        table_name = 'reporters'

    class Config:
        extra = 'ignore'
    