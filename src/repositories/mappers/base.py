from typing import TypeVar, Generic

from pydantic import BaseModel

from src.database import Base

DBModelType = TypeVar("DBModelType", bound=Base)
SchemaType = TypeVar("SchemaType", bound=BaseModel)

class DataMapper(Generic[DBModelType, SchemaType]):
    db_model: type[DBModelType] | None = None
    schema: type[SchemaType] | None = None

    @classmethod
    def map_to_domain_entity(cls, data):
        return cls.schema.model_validate(data, from_attributes=True) # type: ignore

    @classmethod
    def map_to_persistence_entity(cls, data):
        return cls.db_model(**data.model_dump()) # type: ignore