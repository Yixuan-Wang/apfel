from __future__ import annotations

from typing import Literal, NoReturn, Any, overload, Self
from collections.abc import Callable

from apfel.core.monad import Monad

class Maybe[T](Monad[T]):
    __slots__: tuple[str, str]
    _val: T
    _has_value: bool

    @overload
    def __init__(self, val: T, /) -> None: ...
    @overload
    def __init__(self, /, *, has_value: Literal[False]) -> None: ...

    def __class_getitem__[U](cls, val: type[U], /) -> Maybe[U]: ...

    @classmethod
    def just(cls, val: T, /) -> Self: ...

    @classmethod
    def nothing(cls) -> Self: ...
    
    @classmethod
    def some(cls, val: T | None, /) -> Self: ...

    @classmethod
    def duplicate(cls, m: Maybe[T], /) -> Maybe[T]: ...

    def and_[U](self, other: Maybe[U], /) -> Maybe[U]: ...
    def __and__[U](self, other: Maybe[U], /) -> Maybe[U]: ...
    def and_then[U](self, f: Callable[[T], Maybe[U]], /) -> Maybe[U]: ... 
    def apply[U](self, f: Maybe[Callable[[T], U]]) -> Maybe[U]: ...  # type: ignore
    def bind[U](self, f: Callable[[T], Maybe[U]], /) -> Maybe[U]: ...  # type: ignore
    def __bool__(self) -> bool: ...
    def __eq__(self, other: Any, /) -> bool: ...
    def expect(self, message: str) -> T: ...
    def filter(self, p: Callable[[T], bool], /) -> Maybe[T]: ...
    @overload
    def flatten(self: Maybe[T]) -> Maybe[T]: ...
    @overload
    def flatten(self: Maybe[Maybe[T]]) -> Maybe[T]: ...
    def get_or_insert(self, default: T, /) -> T: ...
    def get_or_insert_with(self, f: Callable[[], T], /) -> T: ...
    def __hash__(self) -> int: ...
    def insert(self, val: T, /) -> T: ...
    def is_just(self) -> bool: ...
    def is_just_and(self, p: Callable[[T], bool], /) -> bool: ...
    def is_nothing(self) -> bool: ...
    def __len__(self) -> int: ...
    def map[U](self, f: Callable[[T], U]) -> Maybe[U]: ...
    def map_or[U](self, default: U, f: Callable[[T], U], /) -> U: ...
    def map_or_else[U](self, d: Callable[[], U], f: Callable[[T], U], /) -> U: ...
    def or_(self, other: Maybe[T], /) -> Maybe[T]: ...
    def __or__(self, other: Maybe[T], /) -> Maybe[T]: ...
    def or_else(self, f: Callable[[], Maybe[T]], /) -> Maybe[T]: ...
    @classmethod
    def pure(cls, x) -> Maybe: ...  # type: ignore
    def replace(self, other: T, /) -> Maybe[T]: ...
    def __repr__(self) -> str: ...
    def __str__(self) -> str: ...
    def take(self) -> Maybe[T]: ...
    def take_if[U](self, p: Callable[[T], bool], /) -> Maybe[T]: ...
    def tap(self, f: Callable[[T], Any], /) -> Maybe[T]: ...
    def unwrap(self) -> T: ...
    def unwrap_or(self, default: T, /) -> T: ...
    def unwrap_or_else(self, f: Callable[[], T], /) -> T: ...
    def unwrap_unchecked(self) -> T | Any: ...
    def xor(self, other: Maybe[T], /) -> Maybe[T]: ...
    @overload
    def zip(self, *others: *tuple[()]) -> Maybe[tuple[T,]]: ...
    @overload
    def zip[T1](self, *others: *tuple[Maybe[T1],]) -> Maybe[tuple[T, T1]]: ...
    @overload
    def zip[T1, T2](self, *others: *tuple[Maybe[T1], Maybe[T2]]) -> Maybe[tuple[T, T1, T2]]: ...
    @overload
    def zip[T1, T2, T3](self, *others: *tuple[Maybe[T1], Maybe[T2], Maybe[T3]]) -> Maybe[tuple[T, T1, T2, T3]]: ...
    @overload
    def zip[T1, T2, T3, T4](self, *others: *tuple[Maybe[T1], Maybe[T2], Maybe[T3], Maybe[T4]]) -> Maybe[tuple[T, T1, T2, T3, T4]]: ...

class just[T]:
    def __class_getitem__[U](cls, val: type[U], /) -> Maybe[U]: ...
    def __new__(cls, val: T, /) -> Maybe[T]: ...
    __match_args__ = ('_val',)

class nothing[T]():
    def __class_getitem__[U](cls, val: type[U], /) -> Maybe[U]: ...
    def __new__(cls) -> Maybe[T]: ...
    __match_args__ = ()

class some[T]():
    def __class_getitem__[U](cls, val: type[U], /) -> Maybe[U]: ...
    def __new__(cls, val: T, /) -> Maybe[T]: ...
