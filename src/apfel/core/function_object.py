"""
This module provides [**`FunctionObject`**](./#functionobject),
a wrapper to extend functions with methods and operator overloads,
and can be called just like normal <span class="ref py">Python</span> functions.
Yet they support numerous additional operators for function calling.

Conceptually, [**function objects**](https://en.wikipedia.org/Function_objects) are
objects that implement the function call operator.

## Usage

!!! tip
    Use `FunctionObject` in interactive environments.

`FunctionObject`s are particularly useful in interactive environments.
Instead of wrapping a large expression in another level of parentheses,
you can use application operators provided by `FunctionObject` to apply the function on the following expression.

```python
f | although(we(are_not(using(lisp() or are_we()))))
do_not(want_to(see(these(parentheses())))) & f
```

Writing `f(...)` as `f@(...)` seems redundant,
but these `@` usages can be purged easily with simple search and replace.
`FunctionObject`'s operators are carefully chosen, as they:

1. are relatively rare in Python
2. have different precedence and associativity

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

[`|`](./#operator-or) and [`@`](./#operator-at) have different operator precedence,
the `|` has almost the lowest precedence of all Python operators, while the `@` has almost the highest precedence.
This allows you combine expressions more flexibly without worrying about parentheses.

[`&`](./#operator-and) operator can be used to apply the function to its left-hand side,
if the left-hand side does not overload the `&` operator.
This is similar to [`&`](https://hackage.haskell.org/package/base/docs/Data-Function.html#v:-38-){ .ref .hs }, [`|>`](https://docs.julialang.org/en/v1/manual/functions/#Function-composition-and-piping){ .ref .jl } or roughly [`%>%`](https://magrittr.tidyverse.org/reference/pipe.html){ .ref .rl }.

[`**`](./#operator-pow) operator has the highest precedence of all, and it has a unique
associtivity from right to left.
It can be used in wrapping multiple calls together without parentheses, like `f(g(x))` can be written as `f ** g ** x`.
It roughly simulates [`$`](https://hackage.haskell.org/package/base/docs/Prelude.html#v:-36-){ .ref .hs }.

[`%`](./#operator-mod) operator is used for calling multi-argument functions.

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

from collections.abc import Sequence as _Sequence, Mapping as _Mapping

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
        def |[T, R](self, rhs: T) -> R
        ```

        Function application operator `|` for `FunctionObject`s.

        `f | x` is equivalent to `f(x)`. This operator behaves the same as [`@`](./#operator-at), but with a different precedence.

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
        def &[T, R](self, lhs: T) -> R
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
        def @[T, R](self, rhs: T) -> R
        ```

        Function application operator `@` for `FunctionObject`s.

        `f @ x` is equivalent to `f(x)`. This operator behaves the same as [`|`](./#operator-or), but with a different precedence.

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
        def **[T, R](self, rhs: T) -> R
        ```
        
        Function application operator `**` for `FunctionObject`s.

        `f ** g ** x` is equivalent to `f(g(x))`.
        This operator has the highest precedence of all overloadable operators,
        and it binds from right to left.
        It intends to simulate [`$`](https://hackage.haskell.org/package/base/docs/Prelude.html#v:-36-){ .ref .hs } operator, except the precedence.
        
        !!! example
            ```python
            @func
            def f(x):
                return x + 1

            @func
            def g(x):
                return x * 2

            f ** g ** 1
            # 3
            ```
        """
        return self.__call__(rhs)
    
    def __mod__(self, rhs):
        """\
        ```python
        def %[R](self, rhs) -> R
        ```

        Function application operator `%` for `FunctionObject`s of multi-argument functions.

        - If the right hand side is a [Sequence](https://docs.python.org/3/library/collections.abc.html#collections.abc.Sequence){ .ref .py }, spreads the sequence as positional arguments. For example, `x % (a, b, c)` is equivalent to `x(a, b, c)`.
        - If the right hand side is a [Mapping](https://docs.python.org/3/library/collections.abc.html#collections.abc.Mapping){ .ref .py }, spreads the mapping as keyword arguments. For example, `x % { "a": 1, "b": 2, "c": 3 }` is equivalent to `x(a=1, b=2, c=3)`.
        - Specifically, you can use `...` as the map key to pass keyword arguments with keyword arguments at the same time, `x % { ...: (1, 2), "c": 3 }` is equivalent to `x(1, 2, c=3)`.
        - Otherwise, it calls on the right-hand side. This catches the case where you forget the trailing comma in the right-hand side tuple.

        !!! example
            ```python
            @func
            def f(a, b, c):
                return a + b + c

            f % (1, 2, 3)                  # 6
            f % { "a": 1, "b": 2, "c": 3 } # 6
            f % { ...: (1, 2), "c": 3 }    # 6
            ```

        !!! warning
            This operator does not support the case where `...` (the `Ellipsis`, not `"..."`) is used as a keyword argument.
            However, this case is relatively rare, as `...` cannot be declared as argument name.
        """
        if isinstance(rhs, _Sequence):
            return self.__call__(*rhs)
        elif isinstance(rhs, _Mapping):
            if ... in rhs:
                return self.__call__(*rhs[...], **{k: v for k, v in rhs.items() if k is not ...})
            return self.__call__(**rhs)
        else:
            return self.__call__(rhs)


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
