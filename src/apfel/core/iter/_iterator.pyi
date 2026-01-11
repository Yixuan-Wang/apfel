from abc import abstractmethod
from collections.abc import Callable, Iterator as VanillaIterator
from typing import overload
from apfel.container.maybe import Maybe
from apfel.container.result import Result
import apfel.core.dispatch as _dispatch


class Iterator[I](_dispatch.ABCDispatch):
    @abstractmethod
    def __next__(self) -> I: ...
    def __iter__(self) -> Iterator[I]: ...

    @overload
    @staticmethod
    def next[Item](self: VanillaIterator[Item]) -> Maybe[Item]: ... # pyright: ignore[reportInconsistentOverload, reportSelfClsParameterName]
    @overload
    def next(self) -> Maybe[I]: ...

    @overload
    @staticmethod
    def advance_by[Item](self: VanillaIterator[Item], n: int) -> Result[None, int]: ... # pyright: ignore[reportInconsistentOverload, reportSelfClsParameterName]
    @overload
    def advance_by(self, n: int) -> Result[None, int]: ...

    @overload
    @staticmethod
    def all[Item](self: VanillaIterator[Item], f: Callable[[Item], bool]) -> bool: ... # pyright: ignore[reportInconsistentOverload, reportSelfClsParameterName]
    @overload
    def all(self, f: Callable[[I], bool]) -> bool: ...
    
    @overload
    @staticmethod
    def any[Item](self: VanillaIterator[Item], f: Callable[[Item], bool]) -> bool: ... # pyright: ignore[reportInconsistentOverload, reportSelfClsParameterName]
    @overload
    def any(self, f: Callable[[I], bool]) -> bool: ...

    @overload
    @staticmethod
    def count[Item](self: VanillaIterator[Item]) -> int: ... # pyright: ignore[reportInconsistentOverload, reportSelfClsParameterName]
    @overload
    def count(self) -> int: ...
    
    @overload
    @staticmethod
    def eq[Item](self: VanillaIterator[Item], other: VanillaIterator[Item]) -> bool: ... # pyright: ignore[reportInconsistentOverload, reportSelfClsParameterName]
    @overload
    def eq(self, other: Iterator[I]) -> bool: ...
    @overload
    def eq(self, other: VanillaIterator[I]) -> bool: ...
    @overload
    def __eq__(self, other: Iterator[I]) -> bool: ...
    @overload
    def __eq__(self, other: VanillaIterator[I]) -> bool: ...

    @overload
    @staticmethod
    def find[Item](self: VanillaIterator[Item], f: Callable[[Item], bool]) -> Maybe[Item]: ... # pyright: ignore[reportInconsistentOverload, reportSelfClsParameterName]
    @overload
    def find(self, f: Callable[[I], bool]) -> Maybe[I]: ...
