from __future__ import annotations
from typing_extensions import Never
import functools


def cover_up(func, /):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            e.__traceback__ = None
            raise

    return wrapper


def throw(exc: BaseException, /) -> Never:
    """
    Raise an exception.

    Similar to the [`raise`](docs.python.org/3/reference/simple_stmts.html#the-raise-statement) statement, but can be used in expressions.
    This function will pop the top stack frame, simulating the statement.
    """
    try:
        raise exc
    except BaseException as e:
        if (
            hasattr(e, "__traceback__")
            and e.__traceback__ is not None
            and hasattr(e.__traceback__, "tb_next")
        ):
            e.__traceback__ = e.__traceback__.tb_next  # pyright: ignore[reportOptionalMemberAccess]
        raise
