"""\
Tip: Meme
    <del>A monad is a **monoid** in the category of **endofunctors**.</del>

The [`monad`](/core/monad) module provides monadic interfaces that enable
structured ways to compose and manipulate computations on a single effectful construction.

The module defines three abstract classes: [`Functor`][apfel.core.monad.Functor],
[`Applicative`][apfel.core.monad.Applicative], and [`Monad`][apfel.core.monad.Monad].

# Guide

Here's a high-level comparison of the three.
Assume `Value` is a `Monad`.
**A `Monad` is always a `Functor` and an `Applicative`.**

```python

value = Value(42)

assert value.map  (      lambda x: x + 1 ) == Value(43)
assert value.apply(Value(lambda x: x + 1)) == Value(43)
assert value.bind (lambda x: Value(x + 1)) == Value(43)

```

If you are familiar with Rust,
[`Option`](https://doc.rust-lang.org/std/option/enum.Option.html){.ref .rs} is a `Monad`,
[`Option.map`](https://doc.rust-lang.org/std/option/enum.Option.html#method.map){.ref .rs} is its `Functor.map`,
[`Option.and_then`](https://doc.rust-lang.org/std/option/enum.Option.html#method.and_then){.ref .rs} is its `Monad.bind`.

"""

from abc import abstractmethod

from apfel.core.dispatch import ABCDispatch


class Functor(ABCDispatch):
    """\
    ```python
    class Functor[T](ABC):
        map
        * = ...
    ```

    A [functor](https://en.wikipedia.org/wiki/Functor) is a type that can apply
    a function to its inner value(s) without changing its structure.

    To implement a `Functor`, you need to implement at least the `map` method.

    See [Functor](https://wiki.haskell.org/Functor){.ref .hs} for more information.

    !!! info
        A `Functor` implementation must adhere to the
        [Functor Laws](https://wiki.haskell.org/Functor#Functor_Laws):

        1. **Identity**: `f.map(lambda x: x) == f`
        2. **Composition**: `f.map(lambda x: h(g(x))) == f.map(g).map(h)`

    """

    @abstractmethod
    def map(self, f):
        """\
        ```python
        def map[F, R](self, f: F) -> Self[R]
            where F: Callable[[T], R]
        ```

        Apply a function to the inner value(s) of the functor, returning a new 
        instance of the functor.
        This corresponds to the [`fmap`](https://hackage.haskell.org/package/base/docs/Prelude.html#v:fmap){.ref .hs} in Haskell.
        
        Built-in [`map`](https://docs.python.org/3/library/functions.html#map){.ref .py} function
        returns an iterator, not a new instance of the functor.

        Example:
            ```python
            add = lambda x: x + 1
            Functor.map([1, 2, 3], add) # [2, 3, 4]
            map([1, 2, 3], add)         # <map object at ...>
            ```

        Args:
            f (Callable[[T], R]): The function to apply.

        Returns:
            A new instance of the functor with transformed inner value(s).
        """
        ...

    def __xor__(self, f):
        """\
        ```python
        def ^[F: Callable[[T], R], R](self, f: F)-> Self[R]
        ```

        Map operator `^`, purely syntactic sugar for [`map`][apfel.core.monad.Functor.map].
        """

        return self.map(f)


class Applicative(Functor, ABCDispatch):
    """\
    ```python
    class Applicative[T](Functor):
        pure
        apply
        @ = ...
    ```

    An [applicative functor](https://en.wikipedia.org/wiki/Applicative_functor) is a functor
    extended with the ability to apply an effectful function to its inner value(s).

    To implement an `Applicative`, you need to implement at least the `pure` and `apply` methods.

    See [Applicative](https://wiki.haskell.org/Applicative){ .ref .hs } for more information.
    """

    @classmethod
    @abstractmethod
    def pure(cls, x):
        """\
        ```python
        def pure(cls, x: T) -> Self[T]
        ```

        Wrap a value into the applicative structure.

        Args:
            x: The value to wrap.

        Returns:
            A new instance of the applicative with the value wrapped.
        """
        ...

    @classmethod
    def __matmul__(cls, x):
        """\
        ```python
        def @(self, x: T) -> Self[T]
        ```

        Applicative operator `@`, purely syntactic sugar for [`pure`][apfel.core.monad.Applicative.pure].
        """

        return Applicative.pure[cls](x)  # type: ignore

    @abstractmethod
    def apply(self, f):
        """\
        ```python
        def apply[F, R](self, f: F) -> Self[R]
            where F: Self[Callable[[T], R]]
        ```

        Applies a function wrapped inside the applicative structure to the inner value(s) of this applicative.

        Args:
            f: The applicative that contains the function to apply.

        Returns:
            A new instance of the applicative with the transformed inner value(s).
        """
        ...

    def map(self, f):
        # ? This is the default implementation of `Functor.map` for `Applicative`.
        # ? ```haskell
        # ? map f x = pure f <*> x
        # ? ```

        # return self.apply(self.pure(f))
        return Applicative.apply[self](self, Applicative.pure[self](f))  # type: ignore


class Monad(Applicative, ABCDispatch):
    """\
    ```python
    class Monad[T](Applicative):
        bind
        (Applicative.pure)
    ```

    A [monad](https://en.wikipedia.org/wiki/Monad_(functional_programming)) is an applicative
    functor extended with the ability to reuse results of previous computations and chain
    effectful computations together.

    To implement a `Monad`, you need to implement at least the `bind` method, and
    the [`pure`][apfel.core.monad.Applicative.pure] method from `Applicative`.

    See [Monad](https://wiki.haskell.org/Monad){ .ref .hs } for more information.

    Notes:
        `return` is a reserved keyword in Python, and Haskell [`return`](https://hackage.haskell.org/package/base/docs/Prelude.html#v:return){.ref .hs} is a historical mistake that is now
        pointing to [`pure`](https://hackage.haskell.org/package/base/docs/Prelude.html#v:pure){.ref .hs}.
    """

    @abstractmethod
    def bind(self, f):
        """\
        ```python
        def bind[F, R](self, f: F) -> Self[R]
            where F: Callable[[T], Self[R]]
        ```

        Chain a new monadic computation to the current one.

        The argument `f` maps a pure value of the monad's inner type to the monadic value.
        `bind` chains this computation to the one it represents.
        If its computation fails, the following computations will not be executed.

        The function `f` is called a [Kleisli arrow](https://en.wikipedia.org/wiki/Kleisli_category).
        This `bind` operation has other names in different programming languages.
        For example, in [`Option`](https://doc.rust-lang.org/std/option/enum.Option.html){.ref .rs} monad, it is called [`and_then`](https://doc.rust-lang.org/std/option/enum.Option.html#method.and_then){.ref .rs}.

        Args:
            f: The function that returns a new monadic computation.

        Returns:
            A new instance of the monad with the result of the chained computation.
        """
        ...

    def apply(self, f):
        # ? This is the default implementation of `Applicative.apply` for `Monad`.
        # ? ```haskell
        # ? apply f x = f >>= \g -> x >>= \y -> return (g y)
        # ? ```

        return Monad.bind( # type: ignore
            f, lambda g: Monad.bind(self, lambda y: Applicative.pure[self](g(y))) # type: ignore
        )

    def map(self, f):
        # ? This is the default implementation of `Functor.map` for `Monad`.
        # ? ```haskell
        # ? map f x = x >>= \a -> return (f a)
        # ? ```

        return Monad.bind(self, lambda a: Applicative.pure[self](f(a)))  # type: ignore

__all__ = ["Functor", "Applicative", "Monad"]
