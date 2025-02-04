from __future__ import annotations
from abc import ABCMeta 
from collections.abc import Callable
from typing import Any, Protocol, overload

class ABCDispatchMeta(ABCMeta): ...

class IABCDispatch(Protocol):
    @property
    def __dispatch_methods__(self) -> set[str]: ...

class ABCDispatch(metaclass=ABCDispatchMeta): ...

class IDispatchRegistry[**P, R, F: Callable[P, R]](Protocol):
    def dispatch(self, *args: P.args, **kwargs: P.kwargs) -> Callable[..., R]: ...
    def decorate(self, func: F) -> F: ...
    def register(self, func: F, *args: Any, **kwargs: Any) -> None: ...

class DispatchRegistry[**P, R](IDispatchRegistry[P, R, Callable[P, R]]):
    func: Callable[P, R]
    registry: dict[type, Callable[P, R]]
    enclosing_class: type | None
    decorate_assignments: list[str]

    def __init__(self, func: Callable[P, R], *, enclosing_class: type | None = None, decorate_assignments: list[str] | None = None) -> None: ...
    def dispatch(self, *args: P.args, **kwargs: P.kwargs) -> Callable[..., R]: ...
    def decorate(self, func: Callable[P, R]) -> Callable[P, R]: ...
    def register(self, func: Callable[P, R], cls: type) -> None: ...

class DispatchRegistryForClassMethod[**P, R](DispatchRegistry[P, R]):
    def dispatch(self, *args: P.args, **kwargs: P.kwargs) -> Callable[..., R]: ...
    def decorate(self, func: Callable[P, R]) -> Callable[P, R]: ...

class DispatchRegistryForStaticMethod[**P, R](DispatchRegistryForClassMethod[P, R]):
    def decorate(self, func: Callable[P, R]) -> Callable[P, R]: ...

def dispatch[**P, R](func: Callable[P, R]) -> DispatchFunction[P, R]: ...

class DispatchFunction[**P, R]:
    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> R: ...
    def impl_for(self, cls: type) -> Callable[[Callable[P, R]], Callable[P, R]]: ...
    @property
    def __dispatch__(self) -> DispatchRegistry[P, R]: ...

def impl[T](definition: type) -> Callable[[type[T]], type[T]]: ...
