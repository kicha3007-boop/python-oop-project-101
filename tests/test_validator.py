import pytest

from validator import Validator


@pytest.fixture
def v():
    return Validator()


class TestString:
    @pytest.mark.parametrize("value", ["", None, "hexlet"])
    def test_optional_accepts_any(self, v, value):
        assert v.string().is_valid(value)

    @pytest.mark.parametrize(
        ("value", "expected"),
        [("hexlet", True), ("", False), (None, False)],
    )
    def test_required(self, v, value, expected):
        assert v.string().required().is_valid(value) is expected

    def test_schemas_are_independent(self, v):
        schema = v.string()
        other = v.string()
        schema.required()
        assert other.is_valid("")
        assert not schema.is_valid("")

    @pytest.mark.parametrize(
        ("substring", "expected"), [("what", True), ("whatthe", False)]
    )
    def test_contains(self, v, substring, expected):
        schema = v.string().contains(substring)
        assert schema.is_valid("what does the fox say") is expected

    def test_min_len_includes_border(self, v):
        assert v.string().min_len(6).is_valid("hexlet")
        assert not v.string().min_len(7).is_valid("hexlet")

    def test_repeated_rule_replaces_previous(self, v):
        assert v.string().min_len(10).min_len(4).is_valid("hexlet")
        assert not v.string().min_len(4).min_len(10).is_valid("hexlet")


class TestNumber:
    @pytest.mark.parametrize("value", [None, 0, -3])
    def test_optional_accepts_any(self, v, value):
        assert v.number().is_valid(value)

    def test_required_accepts_zero(self, v):
        schema = v.number().required()
        assert schema.is_valid(0)
        assert not schema.is_valid(None)

    @pytest.mark.parametrize(
        ("value", "expected"), [(10, True), (0, False), (-10, False)]
    )
    def test_positive(self, v, value, expected):
        assert v.number().positive().is_valid(value) is expected

    @pytest.mark.parametrize(
        ("value", "expected"),
        [(-5, True), (5, True), (0, True), (-6, False), (6, False)],
    )
    def test_range_includes_borders(self, v, value, expected):
        assert v.number().range(-5, 5).is_valid(value) is expected

    def test_rules_combine(self, v):
        schema = v.number().required().positive().range(-5, 5)
        assert not schema.is_valid(-5)
        assert schema.is_valid(5)


class TestList:
    @pytest.mark.parametrize("value", [None, [], ["hexlet"]])
    def test_optional_accepts_any(self, v, value):
        assert v.list().is_valid(value)

    @pytest.mark.parametrize(
        ("value", "expected"),
        [([], True), (["hexlet"], True), (None, False), ("hexlet", False)],
    )
    def test_required(self, v, value, expected):
        assert v.list().required().is_valid(value) is expected

    @pytest.mark.parametrize(
        ("value", "expected"),
        [(["hexlet", "code-basics"], True), (["hexlet"], False), ([], False)],
    )
    def test_sizeof(self, v, value, expected):
        assert v.list().sizeof(2).is_valid(value) is expected


class TestDict:
    @pytest.fixture
    def user(self, v):
        return v.dict().shape(
            {"name": v.string().required(), "age": v.number().positive()}
        )

    @pytest.mark.parametrize("value", [None, {}])
    def test_optional_accepts_any(self, v, value):
        assert v.dict().is_valid(value)

    @pytest.mark.parametrize(
        ("value", "expected"),
        [
            ({"name": "kolya", "age": 100}, True),
            ({"name": "maya", "age": None}, True),
            ({"name": "maya"}, True),
            ({"name": "", "age": None}, False),
            ({"name": "ada", "age": -5}, False),
            ({"age": 10}, False),
        ],
    )
    def test_shape(self, user, value, expected):
        assert user.is_valid(value) is expected

    def test_nested_dicts(self, v):
        schema = v.dict().shape(
            {
                "user": v.dict()
                .required()
                .shape({"name": v.string().required()})
            }
        )
        assert schema.is_valid({"user": {"name": "kolya"}})
        assert not schema.is_valid({"user": {"name": ""}})
        assert not schema.is_valid({})


class TestAddValidator:
    def test_string_rule(self, v):
        v.add_validator(
            "string", "startWith", lambda value, start: value.startswith(start)
        )
        schema = v.string().test("startWith", "H")
        assert not schema.is_valid("exlet")
        assert schema.is_valid("Hexlet")

    def test_number_rule(self, v):
        v.add_validator("number", "min", lambda value, low: value >= low)
        schema = v.number().test("min", 5)
        assert not schema.is_valid(4)
        assert schema.is_valid(6)

    def test_rule_added_after_schema_creation(self, v):
        schema = v.string()
        v.add_validator("string", "is_upper", lambda value: value.isupper())
        assert schema.test("is_upper").is_valid("HEXLET")
        assert not schema.is_valid("hexlet")

    def test_rule_is_bound_to_type(self, v):
        v.add_validator(
            "string", "startWith", lambda value, start: value.startswith(start)
        )
        with pytest.raises(ValueError, match="Unknown validator"):
            v.number().test("startWith", 1)

    def test_unknown_type(self, v):
        with pytest.raises(ValueError, match="Unknown schema type"):
            v.add_validator("date", "past", lambda value: True)
