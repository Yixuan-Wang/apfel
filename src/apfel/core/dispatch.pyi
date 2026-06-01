from __future__ import annotations
from abc import ABCMeta
from collections.abc import Callable, Mapping, Sequence
from typing import Any, ClassVar, Protocol, Self

class ABCDispatchMeta(ABCMeta): ...

class ABCDispatchProxy[T, I]:
    #? Here type is used instead of TypeForm
    #?   since it must be a concrete type, not an annotation.
    interface: type[I]
    implementor: type[T]
    def __init__(self, interface: type[I], implementor: type[T], /) -> None: ...
    def __getattr__(self, name: str) -> Any: ...

class IABCDispatch(Protocol):
    __dispatch_methods__: ClassVar[set[str]]

class ABCDispatch(IABCDispatch, metaclass=ABCDispatchMeta):
    __dispatch_methods__: ClassVar[set[str]]
    @classmethod
    def dispatch[T](cls, implementor: type[T], /) -> Self: ...

class IDispatchRegistry[**P, **K, R](Protocol):
    def decide_impl(self, *args: P.args, **kwargs: P.kwargs) -> Callable[P, R]: ...
    def make_dispatch_func(self, func: Callable[P, R]) -> Callable[P, R]: ...
    def add_impl(
        self, func: Callable[P, R], *args: K.args, **kwargs: K.kwargs
    ) -> None: ...
    def get_impl(self, *args: K.args, **kwargs: K.kwargs) -> Callable[P, R]: ...

class DispatchRegistry[**P, **K, R](IDispatchRegistry[P, K, R]):
    function: Callable[P, R]
    registry: dict[type, Callable[P, R]]
    enclosing_class: type | None
    decorate_assignments: Sequence[str]

    def __init__(
        self,
        func: Callable[P, R] | None = None,
        *,
        enclosing_class: type | None = None,
        decorate_assignments: Sequence[str] | None = None,
    ) -> None: ...

class DispatchRegistryForClassMethod[**P, **K, R](DispatchRegistry[P, K, R]): ...
class DispatchRegistryForStaticMethod[**P, **K, R](
    DispatchRegistryForClassMethod[P, K, R]
): ...

# dummy class
class DispatchFunction[**P, R]:
    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> R: ...
    def impl_for(self, cls: type) -> Callable[[Callable[P, R]], Callable[P, R]]: ...
    @property
    def __dispatch__(self) -> DispatchRegistry[P, [type], R]: ...

def dispatched[**P, R](func: Callable[P, R], /) -> DispatchFunction[P, R]: ...
def dispatch[**P, R](func: Callable[P, R], /) -> DispatchFunction[P, R]: ...
def impl[T](interface: IABCDispatch, /) -> Callable[[type[T]], type[T]]: ...
def add_impl(
    interface: IABCDispatch,
    implementation: Mapping[str, Callable],
    *impl_for_args,
    **impl_for_kwargs,
) -> None: ...
