from __future__ import annotations

from collections.abc import Callable
from typing import Literal, TypeVar, Union

from typing_extensions import ParamSpec

_T = TypeVar("_T")
_P = ParamSpec("_P")
_R = TypeVar("_R")


class NeverRun:
    """
    A sentinel singleton class used to distinguish omitted keyword arguments
    from those passed in with the value None (which may have different behavior).
    """

    def __bool__(self) -> Literal[False]:
        return False

    def __repr__(self) -> str:
        return "NOT_GIVEN"


NeverRunOr = Union[_T, NeverRun]
NEVER_RUN = NeverRun()


def once(func: Callable[_P, _R]) -> Callable[_P, _R]:
    once_cache: NeverRunOr[_R] = NEVER_RUN

    def wrapper(*args: _P.args, **kwargs: _P.kwargs) -> _R:
        nonlocal once_cache
        if isinstance(once_cache, NeverRun):
            once_cache = func(*args, **kwargs)

        return once_cache

    return wrapper


__all__ = ["once", "NEVER_RUN", "NeverRun"]
