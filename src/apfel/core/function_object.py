"""
[**Function Objects**](https://en.wikipedia.org/Function_objects) are
objects that implement the function call operator.
This module provides [`FunctionObject`](./#functionobject).
These are functions enhanced with methods and operator overloads,
and can be called and passed around just like normal :simple-python: Python functions,
or further combined and mutated as the functions in :simple-haskell: Haskell.

!!! warning
    Function objects come with runtime costs.
    Albeit negligble most of the time, the cost could accumulate on critical paths.
"""

import inspect as _inspect
from functools import partial as _functools_partial

class FunctionObject:
    """\
    ```python
    class FunctionObject
    ```

    A wrapper for callable that provides additional methods and operator overloads.
    """

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
        ```python
        def @[F: Callable](self, rhs: F) -> ...
        ```

        'curry/call' operator `@` for `FunctionObject`s.
        This operator mimics :simple-haskell: Haskell's calling behavior.

        Its exact behavior depends on the wrapped function's positional-only and positional-or-keyword parameters.

        1. If no such parameters, the right operand will be ignored and the function **fired** with no argument;
        2. If there's exactly one parameter, the function will be **called on** the right operand;
        3. Otherwise there's more than one parameter, the function will be **curried** first before being **called on** the right operand. This will return a new `FunctionObject`.
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
        ```python
        def **[F: Callable](self, rhs: F) -> FunctionObject
        ```
        
        Functional composition operator `**` for `FunctionObject`s.

        `f ** g` is mathematically similar to $f \\circ g$.
        
        !!! example
            ```python
            @func
            def f(x):
                return x + 1

            @func
            def g(x):
                return x * 2

            h = f ** g
            h(1)
            # 3
            ```
        """
        # FIXME: Lambda function is not sufficient enough
        f = lambda *args, **kwargs: self.__call__(rhs.__call__(*args, **kwargs))
        return FunctionObject(f)

    def __or__(self, rhs):
        """\
        ```python
        def |[
            T, R,
            Self: Callable[[T], R],
        ](
            self,
            rhs: T,
        ) -> R
        ```

        Function application operator `|` for `FunctionObject`s.

        `f | x` is equivalent to `f(x)`.

        !!! example
            ```python
            @func
            def f(x):
                return x + 1

            f | 1
            # 2
            ```
        """
        return self.__call__(rhs)

    def __rand__(self, lhs):
        """\
        ```python
        def _&[
            T, R,
            Self: Callable[[T], R],
        ](
            self,
            lhs: T,
        ) -> R
        ```
        Reverse function application operator `&` for `FunctionObject`s.

        `x & f` is equivalent to `f(x)`, if `&` operator (left, `__and__`) is not overloaded by `x`'s type.

        !!! warning
            `np.array` and array-like types are common overloaders of `&`, therefore this operator cannot be used with them.


        !!! example
            ```python
            @func
            def f(x):
                return x + 1

            1 & f
            # 2
            ```
        """
        return self.__call__(lhs)
    
    def __mod__(self, rhs):
        """\
        ```python
        def %(self, rhs: tuple | dict) -> FunctionObject raise TypeError
        ```

        Bind operator `%` for `FunctionObject`s to create partial functions.

        `x % (a, b, c)` binds positional arguments.
        `x % { "a": 1, "b": 2 }` binds keyword arguments.

        !!! note
            Use [`bind` method](./#bind) for all usage `functools.partial` supported.

        !!! example
            ```python
            @func
            def f(a, b, c):
                return a + b + c

            g = f % (1, 2)
            g(3)
            # 6
            ```
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
        ```python
        def bind(self, *args, **kwargs) -> FunctionObject
        ```

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
```python
def func[F: Callable](f: F) -> F
```

Turns a callable into `FunctionObject` yet keeps its original type hints.

!!! example
    ```python
    @func
    def f(a: int) -> int:
        return f + 1

    f | 1
    # 2
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
    ```python
    def reveal_func(func: Any) -> FunctionObject raise TypeError
    ```

    Cast a `FunctionObject` to `FunctionObject` type.

    !!! failure "Exception"
        This function performs runtime check and raises `TypeError` if the input is not a `FunctionObject`.
    """
    if not isinstance(f, FunctionObject):
        raise TypeError(f"`reveal_func` must be called on a FunctionObject, not {type(f)}")
    return f
