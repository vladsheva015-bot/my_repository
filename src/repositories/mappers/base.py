from typing import TypeVar, Generic

from pydantic import BaseModel

from src.database import Base


DBModelType = TypeVar("DBModelType", bound=Base)
SchemaType = TypeVar("SchemaType", bound=BaseModel)


class DataMapper(Generic[DBModelType, SchemaType]):
    db_model: type[DBModelType] | None= None
    schema: type[SchemaType] | None = None

    @classmethod
    def map_to_domain_entity(cls, data)-> SchemaType:
        assert cls.schema is not None, f"В классе {cls.__name__} не задано поле schema"
        return cls.schema.model_validate(data, from_attributes=True)

    @classmethod
    def map_to_persistence_entity(cls, data)-> DBModelType:
        assert cls.db_model is not None, f"В классе {cls.__name__} не задано поле db_model"
        return cls.db_model(**data.model_dump())