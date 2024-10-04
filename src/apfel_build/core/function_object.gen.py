from apfel_build.common import PYI

TUPLE_MAX = 4

pyi = PYI()

pyi.emit(
    "from __future__ import annotations",
    "from collections.abc import Callable",
    "from typing import Any, Concatenate, Never, overload",
    "",
)

pyi.emit("class FunctionObject:")
with pyi.indent():
    for N in range(TUPLE_MAX + 1):
        inner_func_type = f"Callable[[{', '.join(f'P{i+1}' for i in range(N))}], R]"

        pyi.emit(
            f"@overload",
            f"def __new__[{''.join(f'P{i+1}, ' for i in range(N))}R](cls, f: {inner_func_type}) -> FunctionObjectA{N}[{''.join(f'P{i+1}, ' for i in range(N))}R]: ..."
        )

    for N in range(TUPLE_MAX, -1, -1):
        inner_func_type = f"Callable[Concatenate[{''.join(f'P{i+1}, ' for i in range(N))}Ps], R]"

        pyi.emit(
            f"@overload",
            f"def __new__[{''.join(f'P{i+1}, ' for i in range(N))}R, **Ps](cls, f: {inner_func_type}) -> FunctionObjectA{N}P[{''.join(f'P{i+1}, ' for i in range(N))}R, Ps]: ..."
        )

for N in range(TUPLE_MAX + 1):
    inner_func_type = f"Callable[[{', '.join(f'P{i+1}' for i in range(N))}], R]"

    pyi.emit((
        f"class FunctionObjectA{N}"
        "["
        f"{''.join(f'P{i+1}, ' for i in range(N))}"
        "R]("
    ))

    with pyi.indent(is_item=False):
        pyi.emit(
            "FunctionObject,",
        )

    pyi.emit("):")
    
    with pyi.indent():
        # type
        pyi.emit(
            f"type Function = {inner_func_type}"
        )

        # __init__
        pyi.emit(
            (
                "def __init__(self, f: Function) -> None: ..."
            ),
        )

        # __call__
        pyi.emit("__call__: Function")

        # __or__
        pyi.emit(
            (
                "def __or__(self, "
                "rhs: "
                f"{'P1' if N == 1 else 'Never'}, "
                ") -> R: "
                "..."
            )
        )

        # __rand__:
        pyi.emit(
            (
                "def __rand__(self, "
                "lhs: "
                f"{'P1' if N == 1 else 'Never'}, "
                ") -> R: "
                "..."
            )
        )

        # __matmul__
        match N:
            case 0:
                pyi.emit(
                    "def __matmul__(self, rhs: Any, ) -> R: ..."
                )
            case 1:
                pyi.emit(
                    "def __matmul__(self, rhs: P1, ) -> R: ..."
                )
            case _:
                pyi.emit(
                    (
                        "def __matmul__(self, rhs: P1, ) -> "
                        f"{f'FunctionObjectA{N-1}' if N != 0 else 'FunctionObjectA0'}"
                        f"[{''.join(f'P{i+1}, ' for i in range(1, N))}R]"
                        ": ..."
                    )
                )
        
        # __pow__
        if N == 1:
            pyi.emit(
                "@overload",
                "def __pow__[RP](self, rhs: Callable[[RP], P1], ) -> FunctionObjectA1[RP, R]: ...",
                "@overload",
                "def __pow__[RP, **RPs](self, rhs: Callable[Concatenate[RP, RPs], P1], ) -> FunctionObjectA1P[RP, R, RPs]: ...",
                "@overload",
                "def __pow__[**RPs](self, rhs: Callable[RPs, P1], ) -> FunctionObjectA0P[R, RPs]: ...",
            )
        else:
            pyi.emit(
                "def __pow__(self, rhs: Never, ) -> Callable[[Never], R]: ..."
            )

        # __mod__ and __bind__
        for func in ("__mod__", "bind"):
            for i in range(N + 1):
                if N != 0:
                    pyi.emit("@overload")
                pyi.emit(
                    f"def {func}(self, *args: "
                    f"tuple[{', '.join(f'P{j+1}' for j in range(i)) or '()'}], "
                    ") -> "
                    f"FunctionObjectA{N-i}"
                    f"[{''.join(f'P{j+1}, ' for j in range(i, N))}R]"
                    ": ..."
                )

for N in range(TUPLE_MAX, -1, -1):
    inner_func_type = f"Callable[Concatenate[{''.join(f'P{i+1}, ' for i in range(N))}Ps], R]"

    pyi.emit((
        f"class FunctionObjectA{N}P"
        "["
        f"{''.join(f'P{i+1}, ' for i in range(N))}"
        "R, **Ps]("
    ))

    with pyi.indent(is_item=False):
        pyi.emit(
            "FunctionObject,",
        )

    pyi.emit("):")

    with pyi.indent():
        # associated type
        pyi.emit(
            f"type Function = {inner_func_type}"
        )


        # __init__
        pyi.emit("def __init__(self, f: Function) -> None: ...") 

        # __call__
        pyi.emit("__call__: Function")

        # __or__
        pyi.emit(
            "def __or__(self, rhs: Never) -> R: ..."
        )

        # __rand__:
        pyi.emit("def __rand__(self, lhs: Never) -> R: ...")

        # __matmul__
        match N:
            case 0:
                pyi.emit(
                    "def __matmul__(self, rhs: Any, ) -> R: ..."
                )
            case 1:
                pyi.emit(
                    "def __matmul__(self, rhs: P1, ) -> R: ..."
                )
            case _:
                pyi.emit(
                    (
                        "def __matmul__(self, rhs: P1, ) -> "
                        f"{f'FunctionObjectA{N-1}P' if N != 0 else 'FunctionObjectA0P'}"
                        f"[{''.join(f'P{i+1}, ' for i in range(1, N))}R, Ps]"
                        ": ..."
                    )
                )
        
        # __pow__
        if N == 1:
            pyi.emit(
                "@overload",
                "def __pow__[RP](self, rhs: Callable[[RP], P1], ) -> FunctionObjectA1[RP, R]: ...",
                "@overload",
                "def __pow__[RP, **RPs](self, rhs: Callable[Concatenate[RP, RPs], P1], ) -> FunctionObjectA1P[RP, R, RPs]: ...",
                "@overload",
                "def __pow__[**RPs](self, rhs: Callable[RPs, P1], ) -> FunctionObjectA0P[R, RPs]: ...",
            )
        else:
            pyi.emit(
                "def __pow__(self, rhs: Never, ) -> Callable[[Never], R]: ..."
            )

        # __mod__
        for i in range(N + 1):
            pyi.emit(
                "@overload",
                (
                    "def __mod__(self, "
                    f"rhs: tuple[{', '.join(f'P{j+1}' for j in range(i)) or '()'}]"
                    ") -> "
                    f"FunctionObjectA{N-i}P"
                    f"[{''.join(f'P{j+1}, ' for j in range(i, N))}"
                    "R, Ps]: ..."
                )
            )

        pyi.emit(
            "@overload",
            f"def __mod__(self, rhs: dict[str, Any]) -> FunctionObjectA{N}P[{''.join(f'P{j+1}, ' for j in range(N))}R, Ps]: ..."
        )

        # bind
        for i in range(N + 1):
            if N != 0:
                pyi.emit("@overload")

            pyi.emit(
                f"def bind(self, "
                f"{''.join(f'arg{j+1}: P{j+1}, ' for j in range(i))}"
                "*args: Ps.args, **kwargs: Ps.kwargs"
                ") -> "
                f"FunctionObjectA{N-i}P"
                f"[{''.join(f'P{j+1}, ' for j in range(i, N))}"
                "R, Ps]: ..."
            )


pyi.emit(
    "def func[F: Callable](f: F) -> F: ...",
    "",
)

for N in range(TUPLE_MAX + 1):
    pyi.emit(
        "@overload",
        (
            f"def reveal_func[{''.join(f'P{i+1}, ' for i in range(N))}R]("
            f"f: Callable[[{', '.join(f'P{i+1}' for i in range(N))}], R],"
            f") -> FunctionObjectA{N}[{''.join(f'P{i+1}, ' for i in range(N))}R]: ..."
        )
    )

for N in range(TUPLE_MAX, -1, -1):
    pyi.emit(
        "@overload",
        (
            f"def reveal_func[{''.join(f'P{i+1}, ' for i in range(N))}R, **Ps]("
            f"f: Callable[Concatenate[{''.join(f'P{i+1}, ' for i in range(N))}Ps], R],"
            f") -> FunctionObjectA{N}P[{''.join(f'P{i+1}, ' for i in range(N))}R, Ps]: ..."
        )
    )

__all__ = ["pyi"]
