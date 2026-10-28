"""Фабрика схем и реестр пользовательских правил."""

from collections.abc import Callable

from validator.schemas import (
    BaseSchema,
    DictSchema,
    ListSchema,
    NumberSchema,
    StringSchema,
)

# Классы схем по типу: новый тип — новая строка здесь и свой класс,
# базовый класс не меняется.
SCHEMA_CLASSES: dict[str, type[BaseSchema]] = {
    "string": StringSchema,
    "number": NumberSchema,
    "list": ListSchema,
    "dict": DictSchema,
}


class Validator:
    """Выдаёт новую схему на каждый вызов и хранит правила «тип и имя»."""

    def __init__(self):
        self._custom_validators: dict[str, dict[str, Callable[..., bool]]] = {
            schema_type: {} for schema_type in SCHEMA_CLASSES
        }

    def string(self) -> StringSchema:
        return self._create("string")

    def number(self) -> NumberSchema:
        return self._create("number")

    def list(self) -> ListSchema:
        return self._create("list")

    def dict(self) -> DictSchema:
        return self._create("dict")

    def add_validator(
        self, schema_type: str, name: str, fn: Callable[..., bool]
    ) -> None:
        if schema_type not in self._custom_validators:
            raise ValueError(f'Unknown schema type "{schema_type}"')
        self._custom_validators[schema_type][name] = fn

    def _create(self, schema_type: str):
        schema_class = SCHEMA_CLASSES[schema_type]
        return schema_class(self._custom_validators[schema_type])
