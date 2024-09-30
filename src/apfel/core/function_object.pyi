from __future__ import annotations
from collections.abc import Callable
from typing import Any, Concatenate, Never, overload

from apfel.core.reveal import Reveal
class FunctionObject:
    @overload
    def __new__[R](cls, f: Callable[[], R]) -> FunctionObjectA0[R]: ...
    @overload
    def __new__[P1, R](cls, f: Callable[[P1], R]) -> FunctionObjectA1[P1, R]: ...
    @overload
    def __new__[P1, P2, R](cls, f: Callable[[P1, P2], R]) -> FunctionObjectA2[P1, P2, R]: ...
    @overload
    def __new__[P1, P2, P3, R](cls, f: Callable[[P1, P2, P3], R]) -> FunctionObjectA3[P1, P2, P3, R]: ...
    @overload
    def __new__[P1, P2, P3, P4, R](cls, f: Callable[[P1, P2, P3, P4], R]) -> FunctionObjectA4[P1, P2, P3, P4, R]: ...
    @overload
    def __new__[P1, P2, P3, P4, R, **Ps](cls, f: Callable[Concatenate[P1, P2, P3, P4, Ps], R]) -> FunctionObjectA4P[P1, P2, P3, P4, R, Ps]: ...
    @overload
    def __new__[P1, P2, P3, R, **Ps](cls, f: Callable[Concatenate[P1, P2, P3, Ps], R]) -> FunctionObjectA3P[P1, P2, P3, R, Ps]: ...
    @overload
    def __new__[P1, P2, R, **Ps](cls, f: Callable[Concatenate[P1, P2, Ps], R]) -> FunctionObjectA2P[P1, P2, R, Ps]: ...
    @overload
    def __new__[P1, R, **Ps](cls, f: Callable[Concatenate[P1, Ps], R]) -> FunctionObjectA1P[P1, R, Ps]: ...
    @overload
    def __new__[R, **Ps](cls, f: Callable[Concatenate[Ps], R]) -> FunctionObjectA0P[R, Ps]: ...

class FunctionObjectA0[R](
    FunctionObject,
    Reveal[Callable[[], R]],
):
    type Function = Callable[[], R]
    def __init__(self, f: Function) -> None: ...
    __call__: Function
    def __or__(self, rhs: Never, ) -> R: ...
    def __rand__(self, lhs: Never, ) -> R: ...
    def __matmul__(self, rhs: Any, ) -> R: ...
    def __pow__(self, rhs: Never, ) -> Callable[[Never], R]: ...
    def __mod__(self, *args: tuple[()], ) -> FunctionObjectA0[R]: ...
    def bind(self, *args: tuple[()], ) -> FunctionObjectA0[R]: ...

class FunctionObjectA1[P1, R](
    FunctionObject,
    Reveal[Callable[[P1], R]],
):
    type Function = Callable[[P1], R]
    def __init__(self, f: Function) -> None: ...
    __call__: Function
    def __or__(self, rhs: P1, ) -> R: ...
    def __rand__(self, lhs: P1, ) -> R: ...
    def __matmul__(self, rhs: P1, ) -> R: ...
    @overload
    def __pow__[RP](self, rhs: Callable[[RP], P1], ) -> FunctionObjectA1[RP, R]: ...
    @overload
    def __pow__[RP, **RPs](self, rhs: Callable[Concatenate[RP, RPs], P1], ) -> FunctionObjectA1P[RP, R, RPs]: ...
    @overload
    def __pow__[**RPs](self, rhs: Callable[RPs, P1], ) -> FunctionObjectA0P[R, RPs]: ...
    @overload
    def __mod__(self, *args: tuple[()], ) -> FunctionObjectA1[P1, R]: ...
    @overload
    def __mod__(self, *args: tuple[P1], ) -> FunctionObjectA0[R]: ...
    @overload
    def bind(self, *args: tuple[()], ) -> FunctionObjectA1[P1, R]: ...
    @overload
    def bind(self, *args: tuple[P1], ) -> FunctionObjectA0[R]: ...

class FunctionObjectA2[P1, P2, R](
    FunctionObject,
    Reveal[Callable[[P1, P2], R]],
):
    type Function = Callable[[P1, P2], R]
    def __init__(self, f: Function) -> None: ...
    __call__: Function
    def __or__(self, rhs: Never, ) -> R: ...
    def __rand__(self, lhs: Never, ) -> R: ...
    def __matmul__(self, rhs: P1, ) -> FunctionObjectA1[P2, R]: ...
    def __pow__(self, rhs: Never, ) -> Callable[[Never], R]: ...
    @overload
    def __mod__(self, *args: tuple[()], ) -> FunctionObjectA2[P1, P2, R]: ...
    @overload
    def __mod__(self, *args: tuple[P1], ) -> FunctionObjectA1[P2, R]: ...
    @overload
    def __mod__(self, *args: tuple[P1, P2], ) -> FunctionObjectA0[R]: ...
    @overload
    def bind(self, *args: tuple[()], ) -> FunctionObjectA2[P1, P2, R]: ...
    @overload
    def bind(self, *args: tuple[P1], ) -> FunctionObjectA1[P2, R]: ...
    @overload
    def bind(self, *args: tuple[P1, P2], ) -> FunctionObjectA0[R]: ...

class FunctionObjectA3[P1, P2, P3, R](
    FunctionObject,
    Reveal[Callable[[P1, P2, P3], R]],
):
    type Function = Callable[[P1, P2, P3], R]
    def __init__(self, f: Function) -> None: ...
    __call__: Function
    def __or__(self, rhs: Never, ) -> R: ...
    def __rand__(self, lhs: Never, ) -> R: ...
    def __matmul__(self, rhs: P1, ) -> FunctionObjectA2[P2, P3, R]: ...
    def __pow__(self, rhs: Never, ) -> Callable[[Never], R]: ...
    @overload
    def __mod__(self, *args: tuple[()], ) -> FunctionObjectA3[P1, P2, P3, R]: ...
    @overload
    def __mod__(self, *args: tuple[P1], ) -> FunctionObjectA2[P2, P3, R]: ...
    @overload
    def __mod__(self, *args: tuple[P1, P2], ) -> FunctionObjectA1[P3, R]: ...
    @overload
    def __mod__(self, *args: tuple[P1, P2, P3], ) -> FunctionObjectA0[R]: ...
    @overload
    def bind(self, *args: tuple[()], ) -> FunctionObjectA3[P1, P2, P3, R]: ...
    @overload
    def bind(self, *args: tuple[P1], ) -> FunctionObjectA2[P2, P3, R]: ...
    @overload
    def bind(self, *args: tuple[P1, P2], ) -> FunctionObjectA1[P3, R]: ...
    @overload
    def bind(self, *args: tuple[P1, P2, P3], ) -> FunctionObjectA0[R]: ...

class FunctionObjectA4[P1, P2, P3, P4, R](
    FunctionObject,
    Reveal[Callable[[P1, P2, P3, P4], R]],
):
    type Function = Callable[[P1, P2, P3, P4], R]
    def __init__(self, f: Function) -> None: ...
    __call__: Function
    def __or__(self, rhs: Never, ) -> R: ...
    def __rand__(self, lhs: Never, ) -> R: ...
    def __matmul__(self, rhs: P1, ) -> FunctionObjectA3[P2, P3, P4, R]: ...
    def __pow__(self, rhs: Never, ) -> Callable[[Never], R]: ...
    @overload
    def __mod__(self, *args: tuple[()], ) -> FunctionObjectA4[P1, P2, P3, P4, R]: ...
    @overload
    def __mod__(self, *args: tuple[P1], ) -> FunctionObjectA3[P2, P3, P4, R]: ...
    @overload
    def __mod__(self, *args: tuple[P1, P2], ) -> FunctionObjectA2[P3, P4, R]: ...
    @overload
    def __mod__(self, *args: tuple[P1, P2, P3], ) -> FunctionObjectA1[P4, R]: ...
    @overload
    def __mod__(self, *args: tuple[P1, P2, P3, P4], ) -> FunctionObjectA0[R]: ...
    @overload
    def bind(self, *args: tuple[()], ) -> FunctionObjectA4[P1, P2, P3, P4, R]: ...
    @overload
    def bind(self, *args: tuple[P1], ) -> FunctionObjectA3[P2, P3, P4, R]: ...
    @overload
    def bind(self, *args: tuple[P1, P2], ) -> FunctionObjectA2[P3, P4, R]: ...
    @overload
    def bind(self, *args: tuple[P1, P2, P3], ) -> FunctionObjectA1[P4, R]: ...
    @overload
    def bind(self, *args: tuple[P1, P2, P3, P4], ) -> FunctionObjectA0[R]: ...

class FunctionObjectA4P[P1, P2, P3, P4, R, **Ps](
    FunctionObject,
    Reveal[Callable[Concatenate[P1, P2, P3, P4, Ps], R]],
):
    type Function = Callable[Concatenate[P1, P2, P3, P4, Ps], R]
    def __init__(self, f: Function) -> None: ...
    __call__: Function
    def __or__(self, rhs: Never) -> R: ...
    def __rand__(self, lhs: Never) -> R: ...
    def __matmul__(self, rhs: P1, ) -> FunctionObjectA3P[P2, P3, P4, R, Ps]: ...
    def __pow__(self, rhs: Never, ) -> Callable[[Never], R]: ...
    @overload
    def __mod__(self, rhs: tuple[()]) -> FunctionObjectA4P[P1, P2, P3, P4, R, Ps]: ...
    @overload
    def __mod__(self, rhs: tuple[P1]) -> FunctionObjectA3P[P2, P3, P4, R, Ps]: ...
    @overload
    def __mod__(self, rhs: tuple[P1, P2]) -> FunctionObjectA2P[P3, P4, R, Ps]: ...
    @overload
    def __mod__(self, rhs: tuple[P1, P2, P3]) -> FunctionObjectA1P[P4, R, Ps]: ...
    @overload
    def __mod__(self, rhs: tuple[P1, P2, P3, P4]) -> FunctionObjectA0P[R, Ps]: ...
    @overload
    def __mod__(self, rhs: dict[str, Any]) -> FunctionObjectA4P[P1, P2, P3, P4, R, Ps]: ...
    @overload
    def bind(self, *args: Ps.args, **kwargs: Ps.kwargs) -> FunctionObjectA4P[P1, P2, P3, P4, R, Ps]: ...
    @overload
    def bind(self, arg1: P1, *args: Ps.args, **kwargs: Ps.kwargs) -> FunctionObjectA3P[P2, P3, P4, R, Ps]: ...
    @overload
    def bind(self, arg1: P1, arg2: P2, *args: Ps.args, **kwargs: Ps.kwargs) -> FunctionObjectA2P[P3, P4, R, Ps]: ...
    @overload
    def bind(self, arg1: P1, arg2: P2, arg3: P3, *args: Ps.args, **kwargs: Ps.kwargs) -> FunctionObjectA1P[P4, R, Ps]: ...
    @overload
    def bind(self, arg1: P1, arg2: P2, arg3: P3, arg4: P4, *args: Ps.args, **kwargs: Ps.kwargs) -> FunctionObjectA0P[R, Ps]: ...

class FunctionObjectA3P[P1, P2, P3, R, **Ps](
    FunctionObject,
    Reveal[Callable[Concatenate[P1, P2, P3, Ps], R]],
):
    type Function = Callable[Concatenate[P1, P2, P3, Ps], R]
    def __init__(self, f: Function) -> None: ...
    __call__: Function
    def __or__(self, rhs: Never) -> R: ...
    def __rand__(self, lhs: Never) -> R: ...
    def __matmul__(self, rhs: P1, ) -> FunctionObjectA2P[P2, P3, R, Ps]: ...
    def __pow__(self, rhs: Never, ) -> Callable[[Never], R]: ...
    @overload
    def __mod__(self, rhs: tuple[()]) -> FunctionObjectA3P[P1, P2, P3, R, Ps]: ...
    @overload
    def __mod__(self, rhs: tuple[P1]) -> FunctionObjectA2P[P2, P3, R, Ps]: ...
    @overload
    def __mod__(self, rhs: tuple[P1, P2]) -> FunctionObjectA1P[P3, R, Ps]: ...
    @overload
    def __mod__(self, rhs: tuple[P1, P2, P3]) -> FunctionObjectA0P[R, Ps]: ...
    @overload
    def __mod__(self, rhs: dict[str, Any]) -> FunctionObjectA3P[P1, P2, P3, R, Ps]: ...
    @overload
    def bind(self, *args: Ps.args, **kwargs: Ps.kwargs) -> FunctionObjectA3P[P1, P2, P3, R, Ps]: ...
    @overload
    def bind(self, arg1: P1, *args: Ps.args, **kwargs: Ps.kwargs) -> FunctionObjectA2P[P2, P3, R, Ps]: ...
    @overload
    def bind(self, arg1: P1, arg2: P2, *args: Ps.args, **kwargs: Ps.kwargs) -> FunctionObjectA1P[P3, R, Ps]: ...
    @overload
    def bind(self, arg1: P1, arg2: P2, arg3: P3, *args: Ps.args, **kwargs: Ps.kwargs) -> FunctionObjectA0P[R, Ps]: ...

class FunctionObjectA2P[P1, P2, R, **Ps](
    FunctionObject,
    Reveal[Callable[Concatenate[P1, P2, Ps], R]],
):
    type Function = Callable[Concatenate[P1, P2, Ps], R]
    def __init__(self, f: Function) -> None: ...
    __call__: Function
    def __or__(self, rhs: Never) -> R: ...
    def __rand__(self, lhs: Never) -> R: ...
    def __matmul__(self, rhs: P1, ) -> FunctionObjectA1P[P2, R, Ps]: ...
    def __pow__(self, rhs: Never, ) -> Callable[[Never], R]: ...
    @overload
    def __mod__(self, rhs: tuple[()]) -> FunctionObjectA2P[P1, P2, R, Ps]: ...
    @overload
    def __mod__(self, rhs: tuple[P1]) -> FunctionObjectA1P[P2, R, Ps]: ...
    @overload
    def __mod__(self, rhs: tuple[P1, P2]) -> FunctionObjectA0P[R, Ps]: ...
    @overload
    def __mod__(self, rhs: dict[str, Any]) -> FunctionObjectA2P[P1, P2, R, Ps]: ...
    @overload
    def bind(self, *args: Ps.args, **kwargs: Ps.kwargs) -> FunctionObjectA2P[P1, P2, R, Ps]: ...
    @overload
    def bind(self, arg1: P1, *args: Ps.args, **kwargs: Ps.kwargs) -> FunctionObjectA1P[P2, R, Ps]: ...
    @overload
    def bind(self, arg1: P1, arg2: P2, *args: Ps.args, **kwargs: Ps.kwargs) -> FunctionObjectA0P[R, Ps]: ...

class FunctionObjectA1P[P1, R, **Ps](
    FunctionObject,
    Reveal[Callable[Concatenate[P1, Ps], R]],
):
    type Function = Callable[Concatenate[P1, Ps], R]
    def __init__(self, f: Function) -> None: ...
    __call__: Function
    def __or__(self, rhs: Never) -> R: ...
    def __rand__(self, lhs: Never) -> R: ...
    def __matmul__(self, rhs: P1, ) -> R: ...
    @overload
    def __pow__[RP](self, rhs: Callable[[RP], P1], ) -> FunctionObjectA1[RP, R]: ...
    @overload
    def __pow__[RP, **RPs](self, rhs: Callable[Concatenate[RP, RPs], P1], ) -> FunctionObjectA1P[RP, R, RPs]: ...
    @overload
    def __pow__[**RPs](self, rhs: Callable[RPs, P1], ) -> FunctionObjectA0P[R, RPs]: ...
    @overload
    def __mod__(self, rhs: tuple[()]) -> FunctionObjectA1P[P1, R, Ps]: ...
    @overload
    def __mod__(self, rhs: tuple[P1]) -> FunctionObjectA0P[R, Ps]: ...
    @overload
    def __mod__(self, rhs: dict[str, Any]) -> FunctionObjectA1P[P1, R, Ps]: ...
    @overload
    def bind(self, *args: Ps.args, **kwargs: Ps.kwargs) -> FunctionObjectA1P[P1, R, Ps]: ...
    @overload
    def bind(self, arg1: P1, *args: Ps.args, **kwargs: Ps.kwargs) -> FunctionObjectA0P[R, Ps]: ...

class FunctionObjectA0P[R, **Ps](
    FunctionObject,
    Reveal[Callable[Concatenate[Ps], R]],
):
    type Function = Callable[Concatenate[Ps], R]
    def __init__(self, f: Function) -> None: ...
    __call__: Function
    def __or__(self, rhs: Never) -> R: ...
    def __rand__(self, lhs: Never) -> R: ...
    def __matmul__(self, rhs: Any, ) -> R: ...
    def __pow__(self, rhs: Never, ) -> Callable[[Never], R]: ...
    @overload
    def __mod__(self, rhs: tuple[()]) -> FunctionObjectA0P[R, Ps]: ...
    @overload
    def __mod__(self, rhs: dict[str, Any]) -> FunctionObjectA0P[R, Ps]: ...
    def bind(self, *args: Ps.args, **kwargs: Ps.kwargs) -> FunctionObjectA0P[R, Ps]: ...

def func[F: Callable](f: F) -> F: ...

@overload
def reveal_func[R](f: Callable[[], R],) -> FunctionObjectA0[R]: ...
@overload
def reveal_func[P1, R](f: Callable[[P1], R],) -> FunctionObjectA1[P1, R]: ...
@overload
def reveal_func[P1, P2, R](f: Callable[[P1, P2], R],) -> FunctionObjectA2[P1, P2, R]: ...
@overload
def reveal_func[P1, P2, P3, R](f: Callable[[P1, P2, P3], R],) -> FunctionObjectA3[P1, P2, P3, R]: ...
@overload
def reveal_func[P1, P2, P3, P4, R](f: Callable[[P1, P2, P3, P4], R],) -> FunctionObjectA4[P1, P2, P3, P4, R]: ...
@overload
def reveal_func[P1, P2, P3, P4, R, **Ps](f: Callable[Concatenate[P1, P2, P3, P4, Ps], R],) -> FunctionObjectA4P[P1, P2, P3, P4, R, Ps]: ...
@overload
def reveal_func[P1, P2, P3, R, **Ps](f: Callable[Concatenate[P1, P2, P3, Ps], R],) -> FunctionObjectA3P[P1, P2, P3, R, Ps]: ...
@overload
def reveal_func[P1, P2, R, **Ps](f: Callable[Concatenate[P1, P2, Ps], R],) -> FunctionObjectA2P[P1, P2, R, Ps]: ...
@overload
def reveal_func[P1, R, **Ps](f: Callable[Concatenate[P1, Ps], R],) -> FunctionObjectA1P[P1, R, Ps]: ...
@overload
def reveal_func[R, **Ps](f: Callable[Concatenate[Ps], R],) -> FunctionObjectA0P[R, Ps]: ...
