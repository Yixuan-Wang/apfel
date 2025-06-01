import builtins
import apfel
import pytest
from typing import reveal_type

def test_not_none():
    assert apfel.not_none(42) == 42
    with pytest.raises(ValueError):
        apfel.not_none(None)

    def fake_func() -> int | None:
        return 1
    
    a = fake_func()
    reveal_type(a)
    reveal_type(apfel.not_none(a))

def test_identity():
    assert apfel.identity(1) == 1  # noqa: F821

def test_imperative():
    assert apfel.imperative(1, 2, 3) == 3 # noqa: F821
    assert apfel.imperative() is None  # noqa: F821

    lst = []
    assert apfel.imperative(lst) is lst  # noqa: F821

def test_todo():
    with pytest.raises(NotImplementedError):
        apfel.todo() # noqa: F821

def test_unimplemented():
    with pytest.raises(NotImplementedError):
        apfel.unimplemented() # noqa: F821

def test_apfel_namespace():
    assert apfel.not_none is getattr(builtins, "not_none")
    assert apfel.identity is getattr(builtins, "identity")
    assert apfel.imperative is getattr(builtins, "imperative")
    assert apfel.todo is getattr(builtins, "todo")
    assert apfel.unimplemented is getattr(builtins, "unimplemented")

