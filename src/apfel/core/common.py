"""
Common yet miscellaneous utilities functions.
"""

from functools import reduce as _reduce
from apfel.experimental.introspect import call_expr as _call_expr


def apply(value, func, /):
    """
    Applies a single-argument function to a value.
    For chained calls, see [`pipe`][apfel.core.common.pipe].

    See also [:python <code><del>apply</del></code>](https://docs.python.org/2.7/library/functions.html#apply) from Python 2.7.

    This function is different from [`Value.apply`][apfel.container.value.Value.apply],
      which is an implementation of [`Applicative`][apfel.core.monad.Applicative]
      who requires the function to be wrapped in `Value`.
    In contrast, this function accepts arbitrary callables.

    This function is exposed in the [package namespace](../prelude.md#package-namespace)
      and the [builtins namespace](../prelude.md#builtins-namespace).

    Args:
        value (T): The value to be passed to the function.
        func (Callable[[T], R]): The function to apply.

    Returns:
        R: The result of applying the function to the value.
    """
    return func(value)


def identity(value, /):
    """
    Returns the sole argument passed to it doing nothing.

    This function is exposed in the [package namespace](../prelude.md#package-namespace)
      and the [builtins namespace](../prelude.md#builtins-namespace).

    Args:
        value (T): Any object.

    Returns:
        T: The same object passed to it.
    """
    return value


def imperative(*exprs):
    """
    Returns the last expression passed into the function.
    If no expression are passed, returns `None`, per Python's convention.

    This function is exposed in the [package namespace](../prelude.md#package-namespace)
      and the [builtins namespace](../prelude.md#builtins-namespace).

    Args:
        *exprs (*tuple[*Ts, R]): Any number of expressions.

    Returns:
        R: The last expression passed into the function.
    """
    return exprs[-1] if exprs else None


def not_none(value, /):
    """
    Type narrowing: assert the value isn't None.

    This function is exposed in the [package namespace](../prelude.md#package-namespace).

    Args:
        x (T): Any value that type-checked to be `None`,
            but guarantees to be non-`None`.

    Returns:
        T: The same value passed to it.

    Raises:
        ValueError: if the input is actually `None`.

    """
    if value is None:
        args = _call_expr()
        if args:
            import ast

            arg = ast.unparse(args[0])
            raise ValueError(f"`{arg}` should not have been `None`")
        else:
            raise ValueError("The value should not have been `None`")

    return value


def pipe(
    value,
    /,
    *funcs,
):
    """
    Pipes a value through a sequence of functions.
    For single function application, see [`apply`][apfel.core.common.apply].

    See also [`Value.update`][apfel.container.value.Value.update],
      [`FunctionObject.__rand__`][apfel.core.function_object.FunctionObject.__rand__].
    See also [:haskell `&`](https://hackage.haskell.org/package/base/docs/Data-Function.html#v:-38-), [:julia `|>`](https://docs.julialang.org/en/v1/manual/functions/#Function-composition-and-piping) or roughly [:rlang `%>%`](https://magrittr.tidyverse.org/reference/pipe.html).

    This function is exposed in the [package namespace](../prelude.md#package-namespace)
        and the [builtins namespace](../prelude.md#builtins-namespace).

    Args:
        value (T): The initial value to be piped.
        *funcs (Callable[[Any], Any]): A sequence of functions to apply to the value.

    Returns:
        Any: The final result after applying all functions.
    """
    return _reduce(apply, funcs, value)


def todo(message=None, /):
    """
    Marks an unimplemented location that **might** be implemented in the future.
    See [:rust `todo!`](https://doc.rust-lang.org/std/macro.todo.html) for usage.

    This function is exposed in the [package namespace](../prelude.md#package-namespace)
      and the [builtins namespace](../prelude.md#builtins-namespace).

    Args:
        message (str | None): The extra message to be displayed.

    Raises:
        NotImplementedError: Always.
    """
    raise NotImplementedError("Todo" + f": {message}" if message else "")


def unimplemented(message=None, /):
    """
    Marks an unimplemented location that **might not** be implemented in the future.
    See [:rust `unimplemented!`](https://doc.rust-lang.org/std/macro.unimplemented.html) for usage.

    This function is exposed in the [package namespace](../prelude.md#package-namespace)
        and the [builtins namespace](../prelude.md#builtins-namespace).

    Args:
        message (str | None): The extra message to be displayed.

    Raises:
        NotImplementedError: Always.
    """
    raise NotImplementedError("Not implemented" + f": {message}" if message else "")


__all__ = [
    "apply",
    "identity",
    "imperative",
    "not_none",
    "pipe",
    "todo",
    "unimplemented",
]
