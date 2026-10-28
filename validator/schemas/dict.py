from typing import Self

from validator.schemas.base import BaseSchema


class DictSchema(BaseSchema):
    def shape(self, fields: dict[str, BaseSchema]) -> Self:
        """Каждый ключ проверяется своей схемой, как отдельное значение."""
        return self._add_rule(
            "shape",
            lambda value: all(
                schema.is_valid(value.get(key))
                for key, schema in fields.items()
            ),
        )
