import builtins
import apfel.core.common as common
import pytest
from typing import reveal_type

def test_not_none():
    assert common.not_none(42) == 42
    with pytest.raises(ValueError):
        common.not_none(None)

    def fake_func() -> int | None:
        return 1
    
    a = fake_func()
    reveal_type(a)
    reveal_type(common.not_none(a))

def test_identity():
    assert common.identity(1) == 1  # noqa: F821

def test_imperative():
    assert common.imperative(1, 2, 3) == 3 # noqa: F821
    assert common.imperative() is None  # noqa: F821

    lst = []
    assert common.imperative(lst) is lst  # noqa: F821

def test_todo():
    with pytest.raises(NotImplementedError):
        common.todo() # noqa: F821

def test_unimplemented():
    with pytest.raises(NotImplementedError):
        common.unimplemented() # noqa: F821
