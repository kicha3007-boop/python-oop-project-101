from collections.abc import Callable
from typing import Self

from validator.schemas.base import BaseSchema


class ListSchema(BaseSchema):
    def __init__(self, custom_validators: dict[str, Callable[..., bool]]):
        super().__init__(custom_validators)
        self._add_rule("is_list", lambda value: isinstance(value, list))

    def sizeof(self, size: int) -> Self:
        return self._add_rule("sizeof", lambda value: len(value) == size)
