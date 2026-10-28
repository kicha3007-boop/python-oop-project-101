from typing import Any, Self

from validator.schemas.base import BaseSchema


class StringSchema(BaseSchema):
    def min_len(self, length: int) -> Self:
        return self._add_rule("min_len", lambda value: len(value) >= length)

    def contains(self, substring: str) -> Self:
        return self._add_rule("contains", lambda value: substring in value)

    def _is_empty(self, value: Any) -> bool:
        """Для строки пустая строка — тоже пустое значение."""
        return super()._is_empty(value) or value == ""
