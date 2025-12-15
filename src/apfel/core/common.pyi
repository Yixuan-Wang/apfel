from collections.abc import Callable
from typing import Any, NoReturn, overload

def apply[T, R](value: T, func: Callable[[T], R], /) -> R: ...
def identity[T](x: T) -> T: ...
@overload
def imperative() -> None: ...
@overload
def imperative[*Ts, R](*exprs: *tuple[*Ts, R]) -> R: ...
def not_none[T](x: T | None) -> T: ...
@overload
def pipe[T](value: T, /) -> T: ...
@overload
def pipe[T, T1](value: T, /, __func1: Callable[[T], T1]) -> T1: ...
@overload
def pipe[T, T1, T2](
    value: T, /, __func1: Callable[[T], T1], __func2: Callable[[T1], T2]
) -> T2: ...
@overload
def pipe[T, T1, T2, T3](
    value: T,
    /,
    __func1: Callable[[T], T1],
    __func2: Callable[[T1], T2],
    __func3: Callable[[T2], T3],
) -> T3: ...
@overload
def pipe[T, T1, T2, T3, T4](
    value: T,
    /,
    __func1: Callable[[T], T1],
    __func2: Callable[[T1], T2],
    __func3: Callable[[T2], T3],
    __func4: Callable[[T3], T4],
) -> T4: ...
@overload
def pipe[T](value: T, /, *funcs: Callable[[T], T]) -> T: ...
@overload
def pipe[T, T1, T2, T3, T4, R](
    value: T, /,
    __func1: Callable[[T], T1],
    __func2: Callable[[T1], T2],
    __func3: Callable[[T2], T3],
    __func4: Callable[[T3], T4],
    *funcs: *tuple[*tuple[Callable[[Any], Any], ...], Callable[[Any], R]] 
) -> R: ...
@overload
def pipe(value: Any, /, *funcs: Callable[[Any], Any]) -> Any: ...
def todo(message: str | None = None) -> NoReturn: ...
def unimplemented(message: str | None = None) -> NoReturn: ...
