import pytest

from apfel.expr.affirm import affirm, is_type


def test_affirm():
    with pytest.raises(AssertionError):
        affirm(False)

    assert affirm(1) == 1
    assert affirm(5, True) == 5


def test_affirm_with_predicate():
    with pytest.raises(AssertionError):
        affirm(1, lambda x: x > 2)

    assert affirm(3, lambda x: x > 2) == 3
    assert affirm(4, lambda x: x > 2) == 4


def test_affirm_ty() -> None:
    assert affirm(5, is_type[int]) == 5
    with pytest.raises(AssertionError):
        affirm("5", is_type[int])

    # type[T] checks if the value is an instance of T.
    assert affirm(True, type[int]) is True
    # is_type[T] checks if the value is exactly of type T.
    with pytest.raises(AssertionError):
        affirm(True, is_type[int])
