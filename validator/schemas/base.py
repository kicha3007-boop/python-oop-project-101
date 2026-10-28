"""Общая часть всех схем: правила по имени, обязательность, запуск."""

from collections.abc import Callable
from typing import Any, Self

Check = Callable[[Any], bool]


class BaseSchema:
    """Хранит правила по имени: повторный вызов правила заменяет прежнее."""

    def __init__(self, custom_validators: dict[str, Callable[..., bool]]):
        # Реестр пользовательских правил своего типа. Читается при вызове
        # test(), поэтому правило, добавленное после создания схемы, доступно.
        self._custom_validators = custom_validators
        self._rules: dict[str, Check] = {}
        self._is_required = False

    def required(self) -> Self:
        self._is_required = True
        return self

    def test(self, name: str, *args: Any) -> Self:
        """Подключает правило, добавленное через Validator.add_validator."""
        if name not in self._custom_validators:
            raise ValueError(f'Unknown validator "{name}"')
        validate = self._custom_validators[name]
        return self._add_rule(name, lambda value: validate(value, *args))

    def is_valid(self, value: Any) -> bool:
        if self._is_empty(value):
            return not self._is_required
        return all(check(value) for check in self._rules.values())

    def _add_rule(self, name: str, check: Check) -> Self:
        self._rules[name] = check
        return self

    def _is_empty(self, value: Any) -> bool:
        """Пустое значение проходит без правил, если схема не обязательная."""
        return value is None
