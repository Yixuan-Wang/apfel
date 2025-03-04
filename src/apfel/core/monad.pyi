from __future__ import annotations
from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Self

class Functor[T](ABC):
    @abstractmethod
    def map[F: Callable[[T], R], R](self, f: F) -> Self[R]: ...
    def __xor__[F: Callable[[T], R], R](self, f: F) -> Self[R]: ...

class Applicative[T](Functor, ABC):
    @abstractmethod
    @classmethod
    def pure(cls, x: T) -> Self[T]: ...
    @classmethod
    def __matmul__(cls, x: T) -> Self[T]: ...
    @abstractmethod
    def apply[F: Callable[[T], R], R](self, f: Self[F]) -> Self[R]: ...

class Monad[T](Applicative, ABC):
    @abstractmethod
    def bind[F: Callable[[T], Self[R]], R](self, f: F) -> Self[R]: ...
