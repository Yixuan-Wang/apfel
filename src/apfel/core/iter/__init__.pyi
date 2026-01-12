from abc import abstractmethod
from collections.abc import Callable, Iterable, Iterator as VanillaIterator
from typing import TYPE_CHECKING, Any, Self, overload

from apfel.container.maybe import Maybe
from apfel.container.result import Result
import apfel.core.dispatch as _dispatch

if TYPE_CHECKING:
    from builtins import SupportsIter, SupportsNext

class Iterator[I](_dispatch.ABCDispatch):
    @abstractmethod
    def __next__(self) -> I: ...
    def __iter__(self) -> Iterator[I]: ...
    #
    @overload
    @staticmethod
    def next[Item](self: VanillaIterator[Item]) -> Maybe[Item]: ... # pyright: ignore[reportInconsistentOverload, reportSelfClsParameterName]
    @overload
    def next(self) -> Maybe[I]: ...
    #
    @overload
    @staticmethod
    def advance_by[Item](self: VanillaIterator[Item], n: int, /) -> Result[None, int]: ... # pyright: ignore[reportInconsistentOverload, reportSelfClsParameterName]
    @overload
    def advance_by(self, n: int, /) -> Result[None, int]: ...
    #
    @overload
    @staticmethod
    def all[Item](self: VanillaIterator[Item], pred: Callable[[Item], bool], /) -> bool: ... # pyright: ignore[reportInconsistentOverload, reportSelfClsParameterName]
    @overload
    def all(self, pred: Callable[[I], bool], /) -> bool: ...
    #
    @overload
    @staticmethod
    def any[Item](self: VanillaIterator[Item], pred: Callable[[Item], bool], /) -> bool: ... # pyright: ignore[reportInconsistentOverload, reportSelfClsParameterName]
    @overload
    def any(self, pred: Callable[[I], bool], /) -> bool: ...
    #
    @overload
    @staticmethod
    def count[Item](self: VanillaIterator[Item]) -> int: ... # pyright: ignore[reportInconsistentOverload, reportSelfClsParameterName]
    @overload
    def count(self) -> int: ...
    #
    @overload
    @staticmethod
    def eq[Item](self: VanillaIterator[Item], other: VanillaIterator[Item], /) -> bool: ... # pyright: ignore[reportInconsistentOverload, reportSelfClsParameterName]
    @overload
    def eq(self, other: Iterator[I], /) -> bool: ...
    @overload
    def eq(self, other: VanillaIterator[I], /) -> bool: ...
    @overload
    def __eq__(self, other: Iterator[I]) -> bool: ...
    @overload
    def __eq__(self, other: VanillaIterator[I]) -> bool: ...
    #
    @overload
    @staticmethod
    def find[Item](self: VanillaIterator[Item], pred: Callable[[Item], bool], /) -> Maybe[Item]: ... # pyright: ignore[reportInconsistentOverload, reportSelfClsParameterName]
    @overload
    def find(self, pred: Callable[[I], bool], /) -> Maybe[I]: ...
    #
    @overload
    @staticmethod
    def fold[Item, T](self: VanillaIterator[Item], init: T, func: Callable[[T, Item], T]) -> T: ... # pyright: ignore[reportInconsistentOverload, reportSelfClsParameterName]
    @overload
    def fold[T](self, init: T, func: Callable[[T, I], T]) -> T: ...
    #
    @overload
    @staticmethod
    def for_each[Item](self: VanillaIterator[Item], func: Callable[[Item], Any]) -> None: ... # pyright: ignore[reportInconsistentOverload, reportSelfClsParameterName]
    @overload
    def for_each(self, func: Callable[[I], Any]) -> None: ...
    #
    #
    @overload
    @staticmethod
    def reduce[Item](self: VanillaIterator[Item], func: Callable[[Item, Item], Item]) -> Maybe[Item]: ... # pyright: ignore[reportInconsistentOverload, reportSelfClsParameterName]
    @overload
    def reduce(self, func: Callable[[I, I], I]) -> Maybe[I]: ...

class IteratorAdaptor[I](Iterator[I], VanillaIterator[I]):
    def __init__(self, iterator: VanillaIterator[I]): ...
    def __next__(self) -> I: ...
    def __iter__(self) -> Self: ...

@overload
def itrt[I](iterable: Iterator[I], /) -> Iterator[I]: ...
@overload
def itrt[I](iterable: SupportsIter[SupportsNext[I]], /) -> IteratorAdaptor[I]: ...
@overload
def itrt[I](iterable: Iterable[I], /) -> IteratorAdaptor[I]: ...

__all__ = ["Iterator", "itrt"]
