from __future__ import annotations

import abc
from collections.abc import Callable
from attrs import define, field
from typing import TypeVar
from typing_extensions import ParamSpec

_P = ParamSpec("_P")
_R = TypeVar("_R")


class HookLike(abc.ABC):
    @abc.abstractmethod
    def register(self, func: Callable[[], None]) -> Callable[[], None]:
        ...
    
    @abc.abstractmethod
    def fire(self) -> None:
        ...

@define
class Hook(HookLike):
    name: str = field()
    list_lazy: list[Callable[[], None]] = field(factory=list, init=False)
    list_eager: list[Callable[[], None]] = field(factory=list, init=False)

    def register_lazy(self, func: Callable[[], None]) -> Callable[[], None]:
        self.list_lazy.append(func)
        return func

    def register_eager(self, func: Callable[[], None]) -> Callable[[], None]:
        self.list_eager.append(func)
        return func
    
    register = register_lazy

    def __call__(self, wrapped: Callable[_P, _R]) -> Callable[_P, _R]:
        self.fire_eager()

        def wrapper(*args: _P.args, **kwargs: _P.kwargs) -> _R:
            self.fire_lazy()
            return wrapped(*args, **kwargs)

        return wrapper

    def fire_eager(self) -> None:
        for func in self.list_eager:
            func()

    def fire_lazy(self) -> None:
        for func in self.list_lazy:
            func()

    fire = fire_lazy

__all__ = ["HookLike", "Hook"]
