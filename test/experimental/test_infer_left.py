import ast

import pytest

from apfel.experimental.infer_left import infer_left


def _capture():
    """Thin wrapper so infer_left sees the assignment one frame up."""
    return infer_left()


class TestInferLeft:
    def test_simple_assign(self):
        x = _capture()
        assert x is not None
        assert x["__class__"] is ast.Name
        assert x["id"] == "x"

    def test_annotated_assign(self):
        x: int = _capture()
        assert x is not None
        assert x["__class__"] is ast.Name
        assert x["id"] == "x"
        assert x["annotation"] is not None

    def test_augmented_assign(self):
        class _Sink:
            def __iadd__(self, other):
                return other

        x = _Sink()
        x += _capture()
        assert x is not None
        assert x["__class__"] is ast.Name
        assert x["id"] == "x"
        assert x["op"] is not None

    def test_tuple_unpack(self):
        a, b = _capture()
        assert isinstance(a, dict) and isinstance(b, dict)
        assert a["__class__"] is ast.Name and a["id"] == "a"
        assert b["__class__"] is ast.Name and b["id"] == "b"

    def test_walrus(self):
        if result := _capture():
            assert result["__class__"] is ast.Name
            assert result["id"] == "result"

    def test_no_assignment_returns_none(self):
        assert _capture() is None

    def test_attribute_target(self):
        class Namespace:
            pass

        ns = Namespace()
        ns.value = _capture()
        assert ns.value is not None
        assert ns.value["__class__"] is ast.Attribute
        assert ns.value["attr"] == "value"
