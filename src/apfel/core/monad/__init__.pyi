from __future__ import annotations
from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Self, override

class Functor[T](ABC):
    @abstractmethod
    def map[R](self, f: Callable[[T], R]) -> Functor[R]: ...

    def __xor__[R](self, f: Callable[[T], R]) -> Functor[R]: ...

class Applicative[T](Functor, ABC):
    @abstractmethod
    @classmethod
    def pure(cls, x: T) -> Self: ...
    @classmethod
    def __matmul__(cls, x: T) -> Self: ...
    @abstractmethod
    def apply[R](self, f: Applicative[Callable[[T], R]]) -> Applicative[R]: ...

    @override
    def map[R](self, f: Callable[[T], R]) -> Applicative[R]: ...

class Monad[T](Applicative, ABC):
    @abstractmethod
    def bind[R](self, f: Callable[[T], Monad[R]]) -> Monad[R]: ...

    @override
    def map[R](self, f: Callable[[T], R]) -> Monad[R]: ...
    
    @override
    @classmethod
    def pure(cls, x: T) -> Self: ...

    @override
    def apply[R](self, f: Applicative[Callable[[T], R]]) -> Monad[R]: ...
