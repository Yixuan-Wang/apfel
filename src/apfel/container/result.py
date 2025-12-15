"""
A container that holds either a success or a failure.

See [`Result`](https://doc.rust-lang.org/std/result/enum.Result.html){ .ref .rs }
  and [`Either`](https://hackage.haskell.org/package/base/docs/Data-Either.html){ .ref .hs }.

A `Result` has two possible states, `Ok` or `Err`.
`Ok` means a successful value is present,
  and `Err` means a failure value is present.

This module also provides a [`caught`][apfel.container.result.caught] decorator, which wraps a partial function to a total function returning a `Result`.

## Rationale

Python [`raise`](https://docs.python.org/3/reference/simple_stmts.html#the-raise-statement){ .ref .py }
  is easily missed, since the gradual typing system does not support checked exceptions.
An alternative is to return [nullable error flags](https://go.dev/blog/error-handling-and-go){ .ref .go },
  which is cumbersome to work with.

## Implementation

`Result`'s APIs are based on the Rust [`Result`](https://doc.rust-lang.org/std/result/enum.Result.html){ .ref .rs },
and the comparison table is provided below.

| Reference [`Result`](https://doc.rust-lang.org/std/result/enum.Result.html){ .ref .rs } | Counterpart |
| --- | --- |
| `and` | [:material-arrow-right-circle: `and_`][apfel.container.result.Result.and_] |
| `and_then` | [:material-check-circle:][apfel.container.result.Result.and_then] |
| `as_deref` | :material-minus-circle: |
| `as_deref_mut` | :material-minus-circle: |
| `as_mut` | :material-minus-circle: |
| `as_ref` | :material-minus-circle: |
| `cloned` | :material-close-circle: |
| `copied` | :material-minus-circle: |
| `err` | [:material-check-circle:][apfel.container.result.Result.err] |
| `expect` | [:material-check-circle:][apfel.container.result.Result.expect] |
| `expect_err` | [:material-check-circle:][apfel.container.result.Result.expect_err] |
| `flatten` | [:material-check-circle:][apfel.container.result.Result.flatten] |
| `inspect` | [:material-dots-horizontal-circle: `tap`][apfel.container.result.Result.tap] |
| `inspect_err` | [:material-dots-horizontal-circle: `tap_err`][apfel.container.result.Result.tap_err] |
| `into_err` | :material-close-circle: |
| `into_ok` | :material-close-circle: |
| `is_err` | [:material-check-circle:][apfel.container.result.Result.is_err] |
| `is_err_and` | [:material-check-circle:][apfel.container.result.Result.is_err_and] |
| `is_ok` | [:material-check-circle:][apfel.container.result.Result.is_ok] |
| `is_ok_and` | [:material-check-circle:][apfel.container.result.Result.is_ok_and] |
| `iter` | :material-close-circle: |
| `iter_mut` | :material-minus-circle: |
| `map` | [:material-check-circle:][apfel.container.result.Result.map] |
| `map_err` | [:material-check-circle:][apfel.container.result.Result.map_err] |
| `map_or` | [:material-check-circle:][apfel.container.result.Result.map_or] |
| `map_or_default` | :material-minus-circle: |
| `map_or_else` | [:material-check-circle:][apfel.container.result.Result.map_or_else] |
| `ok` | [:material-check-circle:][apfel.container.result.Result.ok] |
| `or` | [:material-arrow-right-circle: `or_`][apfel.container.result.Result.or_] |
| `or_else` | [:material-check-circle:][apfel.container.result.Result.or_else] |
| `transpose` | [:material-dots-horizontal-circle:][apfel.container.result.Result.transpose] |
| `unwrap` | [:material-check-circle:][apfel.container.result.Result.unwrap] |
| `unwrap_err` | [:material-check-circle:][apfel.container.result.Result.unwrap_err] |
| `unwrap_err_unchecked` | [:material-check-circle:][apfel.container.result.Result.unwrap_err_unchecked] |
| `unwrap_or` | [:material-check-circle:][apfel.container.result.Result.unwrap_or] |
| `unwrap_or_default` | :material-minus-circle: |
| `unwrap_or_else` | [:material-check-circle:][apfel.container.result.Result.unwrap_or_else] |
| `unwrap_unchecked` | [:material-check-circle:][apfel.container.result.Result.unwrap_unchecked] |
"""

import functools
import types
from typing import TYPE_CHECKING

import apfel.container.maybe as _maybe
from apfel.core.monad import Monad
from apfel.experimental.adt import variant
import apfel.experimental.expr as _expr
import apfel.experimental.introspect as _introspect

if TYPE_CHECKING:
    from collections.abc import Callable
    from typing import Any


class Result(Monad):
    """A container that holds either a success or a failure.
    See [module-level documentation](result.md#result) for more details.
    """

    __slots__ = ("_val", "_is_ok")

    def __init__(self, val, /, *, is_ok=True):
        self._val = val
        self._is_ok = is_ok

    def __class_getitem__(cls, item):
        return cls

    @classmethod
    def make_ok(cls, val, /):
        """
        Construct an `Ok` value.
        """
        return cls(val)

    @classmethod
    def make_err(cls, val, /):
        """
        Construct an `Err` value.
        """
        return cls(val, is_ok=False)

    def and_(self, other, /):
        """
        If the value is `Ok`, return a shallow copy of the other `Result`. Otherwise, return a new `Err` of type `Result[T, E]`.
        """
        return (
            Result(other._val, is_ok=other._is_ok)
            if self._is_ok
            else Result(self._val, is_ok=False)
        )

    __and__ = and_

    def and_then(self, f, /):
        """
        If the value is `Ok`, apply a function that maps the inner value to a `Result[U, E]` value. Otherwise, return `Err` of type `Result[U, E]`.
        """
        return f(self._val) if self._is_ok else Result(self._val, is_ok=False)

    def apply(
        self,
        f,  # pyright: ignore[reportRedeclaration]
    ):
        """
        Implementation of [Applicative.apply][apfel.core.monad.Applicative.apply].
        Applies the callable wrapped within a `Result` to the inner value, if both are `Ok`.
        """
        if self._is_ok:
            f: "Result[Callable[[Any], Any], Any]" = f  # type: ignore[type-var]
            if f._is_ok:
                return Result(f._val(self._val))
            else:
                return Result(f._val, is_ok=False)
        else:
            return Result(self._val, is_ok=False)

    def bind(self, f):
        """
        Implementation of [`Monad.bind`][apfel.core.monad.Monad.bind].
        Alias of [`and_then`][apfel.container.result.Result.and_then].
        """
        return f(self._val) if self._is_ok else Result(self._val, is_ok=False)

    def __bool__(self):
        return self._is_ok

    def done(self):
        if self._is_ok:
            return self._val, None
        else:
            return None, self._val

    def __eq__(self, other, /):
        if not isinstance(other, Result):
            return NotImplemented
        return self._is_ok == other._is_ok and self._val == other._val

    def err(self):
        """
        Convert a `Result[T, E]` to a `Maybe[E]`.
        """
        return (
            _maybe.Maybe.make_just(self._val)
            if not self._is_ok
            else _maybe.Maybe.make_nothing()
        )

    def expect(self, message):
        """
        Unwrap the inner `Ok` value, if any. Otherwise, raise a `ValueError` with a custom message.
        """
        if not self._is_ok:
            raise ValueError(message)
        return self._val

    def expect_err(self, message):
        """
        Unwrap the inner `Err` value, if any. Otherwise, raise a `ValueError` with a custom message.
        """
        if self._is_ok:
            raise ValueError(message)
        return self._val

    def flatten(self):
        """
        Flatten a nested `Result` (`Result[Result[T, E], E]`) value for one level (`Result[T, E]`).
        """
        if self._is_ok and isinstance(self._val, Result):
            return self._val
        return self

    def __hash__(self):
        return hash((id(Result), self._is_ok, self._val))

    def is_err(self):
        """
        Check if the value is an `Err`.
        """
        return not self._is_ok

    def is_err_and(self, p, /):
        """
        Check if the value is an `Err` and satisfies the predicate.
        """
        return not self._is_ok and p(self._val)

    def is_ok(self):
        """
        Check if the value is an `Ok`.
        """
        return self._is_ok

    def is_ok_and(self, p, /):
        """
        Check if the value is an `Ok` and satisfies the predicate.
        """
        return self._is_ok and p(self._val)

    def map(self, f, /):
        """
        Map a `Result[T, E]` to `Result[U, E]` by applying a function to a contained `Ok` value, leaving an `Err` value untouched.
        """
        return Result(f(self._val)) if self._is_ok else Result(self._val, is_ok=False)

    def map_err(self, f, /):
        """
        Map a `Result[T, E]` to `Result[T, F]` by applying a function to a contained `Err` value, leaving an `Ok` value untouched.
        """
        return Result(self._val) if self._is_ok else Result(f(self._val), is_ok=False)

    def map_or(self, default, f, /):
        """
        Apply a function to a contained `Ok` value, or return a provided default value.
        """
        return f(self._val) if self._is_ok else default

    def map_or_else(self, d, f, /):
        """
        Map a `Result[T, E]` to `U` by applying a function to a contained `Ok` value, or a fallback function to a contained `Err` value.
        """
        return f(self._val) if self._is_ok else d(self._val)

    def ok(self):
        """
        Convert a `Result[T, E]` to a `Maybe[T]`.
        """
        return (
            _maybe.Maybe.make_just(self._val)
            if self._is_ok
            else _maybe.Maybe.make_nothing()
        )

    def or_(self, other, /):
        """
        If the value is `Err`, return a shallow copy of the other `Result`. Otherwise, return a new `Ok` of type `Result[T, F]`.
        """
        return (
            Result(self._val) if self._is_ok else Result(other._val, is_ok=other._is_ok)
        )

    __or__ = or_

    def or_else(self, f, /):
        """
        Return a shallow copy of the `Result` if it contains an `Ok` value, otherwise call a function to get a result.
        """
        return Result(self._val) if self._is_ok else f(self._val)

    @classmethod
    def pure(cls, x):
        """
        Implementation of [`Applicative.pure`][apfel.core.monad.Applicative.pure], which is equivalent to [`Result.make_ok`][apfel.container.result.Result.make_ok].
        """
        return cls(x)

    def __repr__(self):
        return (
            f"<Result Ok {self._val!r}>"
            if self._is_ok
            else f"<Result Err {self._val!r}>"
        )

    def __str__(self):
        return f"Ok({self._val})" if self._is_ok else f"Err({self._val})"

    def tap(self, f, /):
        """
        Call a function with the contained `Ok` value if it exists.

        Unlike [`Result::inspect`](https://doc.rust-lang.org/std/result/enum.Result.html#method.inspect){ .ref .rs },
        this method does not require the function to return `None`.

        ```python
        some_ok = ok(5)
        some_err = err("error")
        some_ok.tap(print)  # prints: 5
        some_err.tap(print)  # prints nothing
        ```
        """
        if self._is_ok:
            f(self._val)
        return self

    def tap_err(self, f, /):
        """
        Call a function with the contained `Err` value if it exists.
        """
        if not self._is_ok:
            f(self._val)
        return self

    @_expr.cover_up
    def throw(self):
        """
        Raise the contained exception if it is an `Err`. Otherwise, return the inner `Ok` value.
        """
        if self._is_ok:
            return self._val
        else:
            raise self._val

    def transpose(self):
        """
        Transpose a `Result` of a `Maybe` into a `Maybe` of a `Result`.
        `Result[Maybe[T], E]` -> `Maybe[Result[T, E]]`
        """
        if self._is_ok:
            val = self._val
            if isinstance(val, _maybe.Maybe):
                return (
                    _maybe.just(Result(val.unwrap_unchecked()))
                    if val._has_value
                    else _maybe.nothing()
                )
            else:
                # Not a Maybe, so just wrap it.
                return _maybe.just(Result(val))
        else:
            return _maybe.just(Result(self._val, is_ok=False))

    def unwrap(self):
        """
        Unwrap the inner `Ok` value, if any. Otherwise, raise a `ValueError`.
        """
        if not self._is_ok:
            raise ValueError(
                f"called `Result.unwrap()` on an `Err` value: {self._val!r}"
            )
        return self._val

    def unwrap_or(self, default, /):
        """
        Unwrap the inner `Ok` value, or return a default value if contains an `Err`.
        """
        return self._val if self._is_ok else default

    def unwrap_or_else(self, f, /):
        """
        Unwrap the inner `Ok` value, or return a value computed by a function if contains an `Err`.
        """
        return self._val if self._is_ok else f(self._val)

    def unwrap_err(self):
        """
        Unwrap the inner `Err` value, if any. Otherwise, raise a `ValueError`.
        """
        if self._is_ok:
            raise ValueError(
                f"called `Result.unwrap_err()` on an `Ok` value: {self._val!r}"
            )
        return self._val

    def unwrap_unchecked(self):
        """
        Return the inner value without checking if it is an `Ok` or `Err`.
        """
        return self._val

    def unwrap_err_unchecked(self):
        """
        Return the inner `Err` value without checking if it is an `Err`.
        """
        return self._val


@variant(Result)
class ok:
    """
    Construct an `Ok` value.

    ```python
    some_ok = ok(42)

    match some_ok:
        case ok(value):
            print(f"Got an Ok with value: {value}")
        case err(error):
            print(f"Got an Err with error: {error}")

    # Output: Got an Ok with value: 42
    ```
    """

    __slots__ = ()
    __match_args__ = ("_val",)

    def __class_getitem__(cls, item):
        return cls

    def __new__(cls, val, /):
        return Result(val)

    @classmethod
    def __instancecheck__(cls, instance):
        return instance._is_ok


@variant(Result)
class err:
    """
    Construct an `Err` value.

    ```python
    some_err = err("Something went wrong")
    match some_err:
        case ok(value):
            print(f"Got an Ok with value: {value}")
        case err(error):
            print(f"Got an Err with error: {error}")

    # Output: Got an Err with error: Something went wrong
    ```
    """

    __slots__ = ()
    __match_args__ = ("_val",)

    def __class_getitem__(cls, item):
        return cls

    def __new__(cls, val, /):
        return Result(val, is_ok=False)

    @classmethod
    def __instancecheck__(cls, instance):
        return not instance._is_ok


class caught:
    """
    A decorator that wraps a partial function to a total function returning a `Result`.

    Usage:
        ```python
        @caught[ZeroDivisionError]
        def divide(a: float, b: float) -> float:
            return a / b

        divide(4, 2)  # Ok(2.0)
        divide(4, 0)  # Err(ZeroDivisionError)
        ```
    """

    def __class_getitem__(cls, item):
        return cls

    @classmethod
    def __wrap_func(cls, func, exception: "Any" = Exception):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return Result.make_ok(func(*args, **kwargs))
            except exception as e:
                return Result.make_err(e)

        return wrapper

    def __new__(cls, first=None, /, *exceptions):
        if _introspect.call_expr() is None:
            return cls.__wrap_func(first)
        else:
            if first is None:
                first = Exception

            if isinstance(first, types.UnionType):
                first = first.__args__

            if exceptions:
                first = tuple([first, *exceptions])

            def decorator(func):
                return cls.__wrap_func(func, first)

            return decorator


__all__ = ["Result", "ok", "err", "caught"]
