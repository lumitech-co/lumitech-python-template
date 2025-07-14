from datetime import UTC, datetime

from pydantic import AliasGenerator, BaseModel, ConfigDict, computed_field
from pydantic.alias_generators import to_camel, to_snake


class BaseCreateSchema(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    @computed_field  # type: ignore[prop-decorator]
    @property
    def created_at(self) -> datetime:
        return datetime.now(UTC)

    @computed_field  # type: ignore[prop-decorator]
    @property
    def updated_at(self) -> datetime:
        return datetime.now(UTC)


class BaseReadSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        alias_generator=AliasGenerator(validation_alias=to_snake, serialization_alias=to_camel),
    )

    id: int
    created_at: datetime
    updated_at: datetime  # type: ignore[pydantic-alias]


class BaseUpdateSchema(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    @computed_field  # type: ignore[prop-decorator]
    @property
    def updated_at(self) -> datetime:
        return datetime.now(UTC)
