# Валидатор данных (Python)

[![hexlet-check](https://github.com/kicha3007-boop/python-oop-project-101/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/kicha3007-boop/python-oop-project-101/actions)
[![CI](https://github.com/kicha3007-boop/python-oop-project-101/actions/workflows/ci.yml/badge.svg)](https://github.com/kicha3007-boop/python-oop-project-101/actions/workflows/ci.yml)

Библиотека для проверки данных с fluent-интерфейсом по мотивам [yup](https://github.com/jquense/yup):
строки, числа, списки, словари со вложенными схемами и собственные правила.

## Установка

Нужен [uv](https://docs.astral.sh/uv/) (Python 3.12+ он поставит сам).

```bash
git clone https://github.com/kicha3007-boop/python-oop-project-101.git
cd python-oop-project-101
make install         # зависимости
make test            # тесты (pytest)
make test-coverage   # тесты с покрытием
make lint            # ruff
```

## Использование

```python
from validator import Validator

v = Validator()

# строки: required — непустая строка, min_len, contains
name = v.string().required().min_len(3)
name.is_valid('hexlet')  # True
name.is_valid('')        # False

# числа: required — любое число, включая 0; positive; range — границы включительно
age = v.number().required().positive().range(1, 120)
age.is_valid(30)  # True
age.is_valid(-1)  # False

# списки: required — значение-список; sizeof — точная длина
v.list().required().sizeof(2).is_valid(['a', 'b'])  # True

# словари: каждый ключ проверяется своей схемой
user = v.dict().shape({
    'name': v.string().required(),
    'age': v.number().positive(),
})
user.is_valid({'name': 'kolya', 'age': 100})  # True
user.is_valid({'name': '', 'age': None})      # False

# собственные правила: add_validator(тип, имя, fn), вызов через test(имя, *аргументы)
v.add_validator('string', 'startWith', lambda value, start: value.startswith(start))
v.string().test('startWith', 'H').is_valid('Hexlet')  # True
```

Каждый вызов `v.string()` и т. п. возвращает новую независимую схему. Без `required()` пустое значение
(`None`, у строки ещё `''`) проходит проверку. Повторный вызов правила заменяет прежнее.

## Устройство

- `validator/validator.py` — фабрика схем и реестр пользовательских правил по паре «тип и имя»;
- `validator/schemas/base.py` — общий базовый класс: правила хранятся по имени, `required`, `test`, `is_valid`;
- `validator/schemas/*.py` — схемы типов, каждая добавляет только свои правила.

Новый тип — новый класс схемы и строка в `SCHEMA_CLASSES`; базовый класс не меняется.
