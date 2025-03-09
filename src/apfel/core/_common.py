def identity(x):
    """
    Returns the sole argument passed to it doing nothing.
    
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

    Args:
        *exprs (*tuple[*Ts, R]): Any number of expressions. 
    
    Returns:
        out (R): The last expression passed into the function.
    """
    return exprs[-1] if exprs else None

def todo(message = None):
    """
    Marks an unimplemented location that **might** be implemented in the future.
    See [`todo!`](https://doc.rust-lang.org/std/macro.todo.html){ .ref .rs } for usage.

    Args:
        message (str | None): The extra message to be displayed.

    Raises:
        NotImplementedError: Always.
    """
    raise NotImplementedError("Todo" + f": {message}" if message else "")


def unimplemented(message = None):
    """
    Marks an unimplemented location that **might not** be implemented in the future.
    See [`unimplemented!`](https://doc.rust-lang.org/std/macro.unimplemented.html){ .ref .rs } for usage.

    Args:
        message (str | None): The extra message to be displayed.

    Raises:
        NotImplementedError: Always.
    """
    raise NotImplementedError("Not implemented" + f": {message}" if message else "")


__all__ = ["unimplemented", "todo", "identity"]
