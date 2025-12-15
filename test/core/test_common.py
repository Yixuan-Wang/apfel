import builtins
import sys
import apfel.core.common as common
import pytest

from typing_extensions import reveal_type

def test_apply():
    assert common.apply(2, lambda x: x + 3) == 5
    assert common.apply("Hello, ", lambda x: x + "world!") == "Hello, world!"


def test_identity():
    assert common.identity(1) == 1  # noqa: F821


def test_imperative():
    assert common.imperative(1, 2, 3) == 3  # noqa: F821
    assert common.imperative() is None  # noqa: F821

    lst = []
    assert common.imperative(lst) is lst  # noqa: F821


def test_not_none():
    assert common.not_none(42) == 42
    with pytest.raises(ValueError):
        common.not_none(None)

    def fake_func() -> int | None:
        return 1

    a = fake_func()
    reveal_type(a)
    reveal_type(common.not_none(a))


def test_pipe():
    from collections.abc import Callable
    def add(x: int) -> Callable[[int], int]:
        return lambda y: y + x
    
    assert common.pipe(1) == 1
    assert common.pipe(1, add(2)) == 3
    assert common.pipe(1, add(2), add(3)) == 6
    assert common.pipe(1, add(2), add(3), add(4)) == 10
    assert common.pipe(1, add(2), add(3), add(4), add(5)) == 15
    assert common.pipe(1, add(2), add(3), add(4), add(5), str) == "15"


def test_todo():
    with pytest.raises(NotImplementedError):
        common.todo()  # noqa: F821


def test_unimplemented():
    with pytest.raises(NotImplementedError):
        common.unimplemented()  # noqa: F821
