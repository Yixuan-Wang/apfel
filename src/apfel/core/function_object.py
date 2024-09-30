"""
[**Function Objects**](https://en.wikipedia.org/Function_objects) are functions enhanced with methods and operator overloads.
`FunctionObject`s can be called and passed around just like normal :simple-python: Python functions,
or further combined and mutated as the functions in :simple-haskell: Haskell.

!!! warning
    Function objects come with runtime costs.
    Albeit negligble most of the time, the cost could accumulate on critical paths.
"""

import inspect as _inspect
from functools import partial as _functools_partial

class FunctionObject:
    __slots__ = (
        "__call__",
        "__wrapped__", "__doc__", "__name__", "__qualname__"
    )

    def __init__(self, f):
        self.__doc__ = f.__doc__
        self.__name__ = getattr(f, "__name__", "<λ>")
        self.__qualname__ = getattr(f, "__qualname__", "<λ>")
        self.__call__ = f
        self.__wrapped__ = f

    def __str__(self):
        return self.__name__

    def __repr__(self):
        return str(_inspect.signature(self.__call__))
    
    def __matmul__(self, rhs):
        """\
        'Curry/call' operator `@` for `FunctionObject`s.

        Its exact behavior depends on the function's positional-only and positional-or-keyword parameters.

        1. If no such parameters, the right operand will be ignored and the function fired with no argument;
        2. If there's exactly one parameter, the function will be called on the right operand;
        3. Otherwise there's more than one parameter, the function will be Curried first before being called on the right operand.
        """
        param_count_positional = 0
        param_count_var_positional = False
        for p in _inspect.signature(self.__call__).parameters.values():
            if p.kind <= 1:
                param_count_positional += 1
            if p.kind == 2:
                param_count_var_positional = True
            
        match param_count_positional:
            case 0:
                return self.__call__() if not param_count_var_positional else _partial(self.__call__, rhs)
            case 1:
                return self.__call__(rhs)
            case _:
                return _partial(self.__call__, rhs)
            
    def __pow__(self, rhs):
        """\
        Functional composition operator `**` for `FunctionObject`s.

        `f ** g` is mathematically similar to $f \\circ g$.
        """
        # FIXME: Lambda function is not sufficient enough
        f = lambda *args, **kwargs: self.__call__(rhs.__call__(*args, **kwargs))
        return FunctionObject(f)

    def __or__(self, rhs):
        """\
        Function application operator `|` for `FunctionObject`s.

        `f | x` is equivalent to `f(x)`.
        """
        return self.__call__(rhs)

    def __rand__(self, lhs):
        """\
        Reverse function application operator `&` for `FunctionObject`s.

        `x & f` is equivalent to `f(x)`, if `&` operator (left, `__and__`) is not overloaded by `x`'s type.

        !!! warning
            `np.array` and array-like types are common overloaders of `&`, therefore this operator cannot be used with them.
        """
        return self.__call__(lhs)
    
    def __mod__(self, rhs):
        """\
        Bind operator `%` for `FunctionObject`s to create partial functions.

        `x % (a, b, c)` binds positional arguments.
        `x % {"a": 1, "b": 2}` binds keyword arguments.

        !!! note
            Use `bind` method for all usage `functools.partial` supported.
        """
        if isinstance(rhs, tuple):
            return _partial(self.__call__, *rhs)
        elif isinstance(rhs, dict):
            return _partial(self.__call__, **rhs)
        else:
            raise TypeError(
                f"Cannot bind {rhs!r} of type {type(rhs)} to {self.__class__.__name__}"
            )

    def bind(self, *args, **kwargs):
        """\
        Bind extra arguments to a `FunctionObject`.
        The returned function will be wrapped in another `FuncObject`.
        """
        return FunctionObject(_functools_partial(self.__call__, *args, **kwargs))
    
    def reveal(self):
        """\
        Cast a `FunctionObject` to its original callable.
        """
        return self
    
    def unwrap(self):
        """\
        Cast a `FunctionObject` to its original callable.
        """
        return self.__call__


def _partial(f, *args, **kwargs):
    return FunctionObject(_functools_partial(f, *args, **kwargs))

func = FunctionObject(FunctionObject)
"""\
Turns a callable into `FunctionObject` yet keeps its original type hints.

!!! example
    ```python
    @func
    def f(a: int) -> int:
        return f + 1

    f | 1 # 2
    ```

!!! note
    As a callable, `FunctionObject` has less static typing support.
    `@func` erases type hints of `FunctionObject` while keeping the runtime type.
    If you want to retain the type hints, directly use `FunctionObject`'s
    constructor, or use `reveal_func` on an object with runtime type `FunctionObject`.
"""

@func
def reveal_func(f):
    """\
    Cast a `FunctionObject` hidden as built-in function back to a `FunctionObject`.
    """
    if not isinstance(f, FunctionObject):
        raise TypeError(f"F must be called with a FunctionObject, not {type(f)}")
    return f
