from abc import abstractmethod
from collections.abc import Callable, Iterable, Iterator as VanillaIterator
from typing import TYPE_CHECKING, Any, Self, overload, Concatenate

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
    def chain[Item](self: VanillaIterator[Item], *others: VanillaIterator[Item]) -> Iterator[Item]: ... # pyright: ignore[reportInconsistentOverload, reportSelfClsParameterName]
    @overload
    def chain(self, *others: Iterator[I]) -> Iterator[I]: ...
    #
    @overload
    @staticmethod
    def count[Item](self: VanillaIterator[Item]) -> int: ... # pyright: ignore[reportInconsistentOverload, reportSelfClsParameterName]
    @overload
    def count(self) -> int: ...
    #
    @overload
    @staticmethod
    def enumerate[Item](self: VanillaIterator[Item], init: int = 0) -> Iterator[tuple[int, Item]]: ... # pyright: ignore[reportInconsistentOverload, reportSelfClsParameterName]
    @overload
    def enumerate(self, init: int = 0) -> Iterator[tuple[int, I]]: ...
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
    def filter[Item](self: VanillaIterator[Item], pred: Callable[[Item], bool], /) -> Iterator[Item]: ... # pyright: ignore[reportInconsistentOverload, reportSelfClsParameterName]
    @overload
    def filter(self, pred: Callable[[I], bool], /) -> Iterator[I]: ...
    #
    @overload
    @staticmethod
    def find[Item](self: VanillaIterator[Item], pred: Callable[[Item], bool], /) -> Maybe[Item]: ... # pyright: ignore[reportInconsistentOverload, reportSelfClsParameterName]
    @overload
    def find(self, pred: Callable[[I], bool], /) -> Maybe[I]: ...
    #
    @overload
    @staticmethod
    def flatten[Item]( # pyright: ignore[reportInconsistentOverload]
        self: Iterator[VanillaIterator[Item]], # pyright: ignore[reportSelfClsParameterName]
    ) -> Iterator[Item]: ... 
    @overload
    def flatten[Item](self: Iterator[VanillaIterator[Item]]) -> Iterator[Item]: ...
    @overload
    def flatten[Item](self: Iterator[Iterable[Item]]) -> Iterator[Item]: ...
    @overload
    def flatten[Item](self: Iterator[Iterator[Item]]) -> Iterator[Item]: ...
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
    @overload
    @staticmethod
    def last[Item](self: VanillaIterator[Item]) -> Maybe[Item]: ... # pyright: ignore[reportInconsistentOverload, reportSelfClsParameterName]
    @overload
    def last(self) -> Maybe[I]: ...
    #
    @overload
    @staticmethod
    def map[Item, U](self: VanillaIterator[Item], func: Callable[[Item], U]) -> Iterator[U]: ... # pyright: ignore[reportInconsistentOverload, reportSelfClsParameterName]
    @overload
    def map[U](self, func: Callable[[I], U]) -> Iterator[U]: ...
    #
    @overload
    @staticmethod
    def nth[Item](self: VanillaIterator[Item], n: int, /) -> Maybe[Item]: ... # pyright: ignore[reportInconsistentOverload, reportSelfClsParameterName]
    @overload
    def nth(self, n: int, /) -> Maybe[I]: ...
    #
    @overload
    @staticmethod
    def pipe[Item, **P, T](  # pyright: ignore[reportInconsistentOverload]
        self: VanillaIterator[Item],  # pyright: ignore[reportSelfClsParameterName]
        func: Callable[Concatenate[Iterable[Item], P], T],
        /,
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> T: ...
    @overload
    def pipe[**P, T](  # pyright: ignore[reportInconsistentOverload]
        self,
        func: Callable[Concatenate[Iterable[I], P], T],
        /,
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> T: ...
    #
    @overload
    @staticmethod
    def position[Item](self: VanillaIterator[Item], pred: Callable[[Item], bool], /) -> Maybe[int]: ... # pyright: ignore[reportInconsistentOverload, reportSelfClsParameterName]
    @overload
    def position(self, pred: Callable[[I], bool], /) -> Maybe[int]: ...
    #
    @overload
    @staticmethod
    def reduce[Item](self: VanillaIterator[Item], func: Callable[[Item, Item], Item]) -> Maybe[Item]: ... # pyright: ignore[reportInconsistentOverload, reportSelfClsParameterName]
    @overload
    def reduce(self, func: Callable[[I, I], I]) -> Maybe[I]: ...
    #
    @overload
    @staticmethod
    def skip[Item](self: VanillaIterator[Item], n: int, /) -> Iterator[Item]: ... # pyright: ignore[reportInconsistentOverload, reportSelfClsParameterName]
    @overload
    def skip(self, n: int, /) -> Iterator[I]: ...
    #
    @overload
    @staticmethod
    def skip_while[Item](self: VanillaIterator[Item], pred: Callable[[Item], bool], /) -> Iterator[Item]: ... # pyright: ignore[reportInconsistentOverload, reportSelfClsParameterName]
    @overload
    def skip_while(self, pred: Callable[[I], bool], /) -> Iterator[I]: ...
    #
    @overload
    @staticmethod
    def step_by[Item](self: VanillaIterator[Item], step: int, /) -> Iterator[Item]: ... # pyright: ignore[reportInconsistentOverload, reportSelfClsParameterName]
    @overload
    def step_by(self, step: int, /) -> Iterator[I]: ...
    #
    @overload
    @staticmethod
    def take[Item](self: VanillaIterator[Item], n: int, /) -> Iterator[Item]: ... # pyright: ignore[reportInconsistentOverload, reportSelfClsParameterName]
    @overload
    def take(self, n: int, /) -> Iterator[I]: ...
    #
    @overload
    @staticmethod
    def take_while[Item](self: VanillaIterator[Item], pred: Callable[[Item], bool], /) -> Iterator[Item]: ... # pyright: ignore[reportInconsistentOverload, reportSelfClsParameterName]
    @overload
    def take_while(self, pred: Callable[[I], bool], /) -> Iterator[I]: ...

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
