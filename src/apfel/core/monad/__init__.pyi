from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Self, override
from apfel.core.dispatch import ABCDispatch

class Functor[T](ABC, ABCDispatch):
    @abstractmethod
    def map[R](self, func: Callable[[T], R], /) -> Functor[R]: ...
    def __xor__[R](self, func: Callable[[T], R], /) -> Functor[R]: ...

class Applicative[T](Functor, ABC, ABCDispatch):
    @abstractmethod
    @classmethod
    def pure(cls, value: T, /) -> Self: ...
    @classmethod
    def __matmul__(cls, value: T, /) -> Self: ...
    @abstractmethod
    def apply[R](self, func: Applicative[Callable[[T], R]], /) -> Applicative[R]: ...
    @override
    def map[R](self, func: Callable[[T], R], /) -> Applicative[R]: ...

class Monad[T](Applicative, ABC, ABCDispatch):
    @abstractmethod
    def bind[R](self, func: Callable[[T], Monad[R]], /) -> Monad[R]: ...
    @override
    def map[R](self, func: Callable[[T], R], /) -> Monad[R]: ...
    @override
    @classmethod
    def pure(cls, value: T, /) -> Self: ...
    @override
    def apply[R](self, func: Applicative[Callable[[T], R]], /) -> Monad[R]: ...

fmap = Functor.map

__all__ = ["Functor", "Applicative", "Monad", "fmap"]
