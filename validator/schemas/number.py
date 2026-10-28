from typing import Self

from validator.schemas.base import BaseSchema


class NumberSchema(BaseSchema):
    def positive(self) -> Self:
        return self._add_rule("positive", lambda value: value > 0)

    def range(self, start: int, end: int) -> Self:
        """Число в диапазоне, границы включительно."""
        return self._add_rule("range", lambda value: start <= value <= end)
