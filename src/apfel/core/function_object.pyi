from __future__ import annotations
from collections.abc import Callable
from typing import Any, Concatenate, Mapping, Never, Sequence, overload

class FunctionObject:
    @overload
    def __new__[R](cls, f: Callable[[], R]) -> FunctionObjectA0[R]: ...
    @overload
    def __new__[T, R](cls, f: Callable[[T], R]) -> FunctionObjectA1[T, R]: ...
    @overload
    def __new__[T, **P, R](cls, f: Callable[Concatenate[T, P], R]) -> FunctionObjectA1P[T, P, R]: ...
    @overload
    def __new__[**P, R](cls, f: Callable[P, R]) -> FunctionObjectA0P[P, R]: ...

class FunctionObjectA0[R](FunctionObject):
    def __call__(self) -> R: ...
    @overload
    def __mod__(self, rhs: tuple[()]) -> R: ...
    @overload
    def __mod__(self, rhs: Sequence) -> R: ...
    @overload
    def __mod__(self, rhs: Mapping) -> R: ...

class FunctionObjectA1[T, R](FunctionObject):
    def __call__(self, rhs: T) -> R: ...
    def __or__(self, rhs: T) -> R: ...
    def __rand__(self, lhs: T) -> R: ...
    def __matmul__(self, rhs: T) -> R: ...
    def __pow__(self, rhs: T) -> R: ...
    @overload
    def __mod__(self, rhs: tuple[T]) -> R: ...
    @overload
    def __mod__(self, rhs: Sequence) -> R: ...
    @overload
    def __mod__(self, rhs: Mapping) -> R: ...

class FunctionObjectA1P[T, **P, R](FunctionObject):
    def __call__(self, rhs: T, *args: P.args, **kwargs: P.kwargs) -> R: ...
    @overload
    def __mod__(self, rhs: tuple[T, ...]) -> R: ...
    @overload
    def __mod__(self, rhs: Sequence) -> R: ...
    @overload
    def __mod__(self, rhs: Mapping) -> R: ...

class FunctionObjectA0P[**P, R](FunctionObject):
    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> R: ...
    @overload
    def __mod__(self, rhs: Sequence) -> R: ...
    @overload
    def __mod__(self, rhs: Mapping) -> R: ...


@overload
def func[F: Callable](f: F) -> F: ...
def func[*Fs](*fs: *Fs) -> tuple[*Fs]: ...

@overload
def reveal_func[R](f: Callable[[], R]) -> FunctionObjectA0[R]: ...
@overload
def reveal_func[T, R](f: Callable[[T], R]) -> FunctionObjectA1[T, R]: ...
@overload
def reveal_func[T, **P, R](f: Callable[Concatenate[T, P], R]) -> FunctionObjectA1P[T, P, R]: ...
@overload
def reveal_func[**P, R](f: Callable[P, R]) -> FunctionObjectA0P[P, R]: ...
def reveal_func(f: Callable) -> FunctionObject: ...
