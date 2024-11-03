"""
This module provides [**`FunctionObject`**](./#functionobject),
a wrapper to extend functions with methods and operator overloads,
and can be called and passed around just like normal <span class="ref py">Python</span> functions,
or further combined and mutated as the functions in <span class="ref hs">Haskell</span>.
Conceptually, [**function objects**](https://en.wikipedia.org/Function_objects) are
objects that implement the function call operator.

## Usage

`FunctionObject`s are particularly useful in interactive environments.
Instead of wrapping a large expression in another level of parentheses,
you can use [`|`](./#operator-applicationor) or [`@`](./#operator-applicationat) operators to apply the function on the following expression.
If an expression guarantees to not overload the [`&`](./#operator-applicationand) operator, you can also use `&` to apply the function on the left-hand side,
which is handy in REPLs.

```python
f | although(we(are_not(using(lisp() or are_we()))))
do_not(want_to(see(these(parentheses())))) & f
```

Sometimes writing `f(...)` as `f@(...)` or `f|(...)` is kind of redundant,
but these usages can be purged easily with simple search and replace.
These operators are carefully chosen, as they are relatively rare in Python code.
This is especially useful when you wrap some debugging or logging code around a function call.
For example, with the following usage with [`icecream`](https://pypi.org/project/icecream/){ .ref .py },
you can replace `ic @ ` with empty string to remove all debugging code,
without worrying of breaking the `get_pic()` call:

```python
from icecream import ic as _ic

ic = func(_ic)
result = ic @ (
    get_pic(iris)
        .filter(...)
        .sort_values(...)
        .apply(...)
        .head(10)
)
```

[`|`](./#operator-applicationor) and [`@`](./#operator-applicationat) have different operator precedence,
the `|` has almost the lowest precedence of all Python operators, while the `@` has almost the highest precedence.
This allows you combine expressions more flexibly without worrying about parentheses.

[`**`](./#operator-composition) and [`%`](./#operator-bind) operators are also provided for function composition and partial function creation.

!!! tip
    **Do not use `FunctionObject`s in library or main code base.**
    **Only use them in scripts, notebooks or REPLs.**
    Function objects come with runtime costs.
    Albeit negligible most of the time, the cost could accumulate on critical paths.

    `FunctionObject`s also have less static typing support.
    Do not use them in type-checked code.

!!! warning
    Wrapping callables with `FunctionObject` will lose fields and methods of the original callable.
    Be cautious especially when wrapping other callable objects.

!!! warning
    For performance considerations, the majority of `apfel` APIs are not wrapped in `FunctionObject`s.
"""

from functools import partial as _functools_partial

class FunctionObject:
    #? This class cannot have docstring, as class level docstring will
    #? conflict with object specific __doc__ used to wrap the original
    #? function's docstring.

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
        return str(self.__wrapped__)

    def __repr__(self):
        return repr(self.__wrapped__)

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

        `f | x` is equivalent to `f(x)`. This operator behaves the same as [`@`](./#operator-applicationat), but with a different precedence.

        !!! example
            ```python
            @func
            def f(x):
                return x * 2

            f | 1 + 2
            # 6
            ```
        """
        return self.__call__(rhs)

    def __rand__(self, lhs):
        """\
        ```python
        def &[
            T, R,
            Self: Callable[[T], R],
        ](
            self,
            lhs: T,
        ) -> R
        ```
        Reverse function application operator `&` for `FunctionObject`s.
        **This operator overloading targets the right-hand side**.

        `x & f` is equivalent to `f(x)`, if `&` operator (left, `__and__`) is not overloaded by `x`'s type.

        !!! warning
            `np.array` and array-like types are common overloaders of `&`, therefore this operator cannot be used with them.


        !!! example
            ```python
            @func
            def f(x):
                return x + 1

            1 + 2 & f
            # 6
            ```
        """
        return self.__call__(lhs)
    
    def __matmul__(self, rhs):
        """\
        ```python
        def @[F: Callable](self, rhs: F) -> ...
        ```

        Function application operator `@` for `FunctionObject`s.

        `f @ x` is equivalent to `f(x)`. This operator behaves the same as [`|`](./#operator-applicationor), but with a different precedence.

        !!! example
            ```python
            @func
            def f(x):
                return x * 2

            f @ 1 + 2
            # 4
            ```
        """
        return self.__call__(rhs)
            
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
        def f(*args, **kwargs):
            return self(rhs(*args, **kwargs))

        return FunctionObject(f)
    
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



def _partial(f, *args, **kwargs):
    """
    Internal helper for creating partial function objects.
    """
    return FunctionObject(_functools_partial(f, *args, **kwargs))

def func(f, *fs):
    """\
    ```python
    def func[F: Callable](f: F) -> F
    def func[*Fs](*fs: *Fs) -> tuple[*Fs]
    ```

    Turn callables into `FunctionObject` yet keeps their original type hints.

    !!! example
        ```python
        @func
        def f(a: int) -> int:
            return f + 1

        f | 1
        # 2

        print, display, str = func(print, display, str)
        ```

    !!! note
        As a callable, `FunctionObject` has less static typing support.
        `@func` erases type hints of `FunctionObject` while keeping the runtime type.
        If you want to retain the type hints, directly use `FunctionObject`'s
        constructor, or use `reveal_func` on an object with runtime type `FunctionObject`.
    """
    return tuple(map(FunctionObject, [f, *fs])) if fs else FunctionObject(f)

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
