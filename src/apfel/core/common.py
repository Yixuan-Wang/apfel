"""
Common yet miscellaneous utilities functions.
"""

from apfel.experimental.introspect import call_expr


def identity(x):
    """
    Returns the sole argument passed to it doing nothing.

    This function is exposed in the [:material-earth: package namespace](../prelude.md#package-namespace)
      and the [:material-airballoon: builtins namespace](../prelude.md#builtins-namespace).

    Args:
        x (T): Any object.

    Returns:
        out (T): The same object passed to it.
    """
    return x


def imperative(*exprs):
    """
    Returns the last expression passed into the function.
    If no expression are passed, returns `None`, per Python's convention.

    This function is exposed in the [:material-earth: package namespace](../prelude.md#package-namespace)
      and the [:material-airballoon: builtins namespace](../prelude.md#builtins-namespace).

    Args:
        *exprs (*tuple[*Ts, R]): Any number of expressions.

    Returns:
        out (R): The last expression passed into the function.
    """
    return exprs[-1] if exprs else None


def not_none(x):
    """
    Type narrowing: assert the value isn't None.

    This function is exposed in the [:material-earth: package namespace](../prelude.md#package-namespace).

    Args:
        x (T): Any value that type-checked to be `None`,
        but guarantees to be non-`None`.

    Returns:
        out (T): The same value passed to it.

    Raises:
        ValueError: if the input is actually `None`.

    """
    if x is None:
        args = call_expr()
        if args:
            import ast

            arg = ast.unparse(args[0])
            raise ValueError(f"`{arg}` should not have been `None`")
        else:
            raise ValueError("The value should not have been `None`")

    return x


def todo(message=None):
    """
    Marks an unimplemented location that **might** be implemented in the future.
    See [`todo!`](https://doc.rust-lang.org/std/macro.todo.html){ .ref .rs } for usage.

    This function is exposed in the [:material-earth: package namespace](../prelude.md#package-namespace)
      and the [:material-airballoon: builtins namespace](../prelude.md#builtins-namespace).

    Args:
        message (str | None): The extra message to be displayed.

    Raises:
        NotImplementedError: Always.
    """
    raise NotImplementedError("Todo" + f": {message}" if message else "")


def unimplemented(message=None):
    """
    Marks an unimplemented location that **might not** be implemented in the future.
    See [`unimplemented!`](https://doc.rust-lang.org/std/macro.unimplemented.html){ .ref .rs } for usage.

    This function is exposed in the [:material-earth: package namespace](../prelude.md#package-namespace)
        and the [:material-airballoon: builtins namespace](../prelude.md#builtins-namespace).

    Args:
        message (str | None): The extra message to be displayed.

    Raises:
        NotImplementedError: Always.
    """
    raise NotImplementedError("Not implemented" + f": {message}" if message else "")


__all__ = ["unimplemented", "todo", "identity", "imperative", "not_none"]
