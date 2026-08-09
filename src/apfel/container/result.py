"""
A container that holds either a success or a failure.

See [:rust `Result`](https://doc.rust-lang.org/std/result/enum.Result.html)
  and [:haskell `Either`](https://hackage.haskell.org/package/base/docs/Data-Either.html).

A `Result` has two possible states, `Ok` or `Err`.
`Ok` means a successful value is present,
  and `Err` means a failure value is present.

This module also provides a [`caught`][apfel.container.result.caught] decorator, which wraps a partial function to a total function returning a `Result`.

The [`Result`][apfel.container.result.Result] class, and the [`ok`][apfel.container.result.ok], [`err`][apfel.container.result.err], and [`caught`][apfel.container.result.caught] functions
  are exposed in the [package namespace](../prelude#package-namespace).

## Rationale

Python [:python `raise`](https://docs.python.org/3/reference/simple_stmts.html#the-raise-statement)
  is easily missed, since the gradual typing system does not support checked exceptions.
An alternative is to return [:golang nullable error flags](https://go.dev/blog/error-handling-and-go),
  which is cumbersome to work with.

## Implementation

`Result`'s APIs are based on the Rust [:rust `Result`](https://doc.rust-lang.org/std/result/enum.Result.html),
and the comparison table is provided below.

| Reference [:rust `Result`](https://doc.rust-lang.org/std/result/enum.Result.html) | Counterpart |
| --- | --- |
| `and` | [`and_`][apfel.container.result.Result.and_] |
| `and_then` | [`and_then`][apfel.container.result.Result.and_then] |
| `as_deref` | / |
| `as_deref_mut` | / |
| `as_mut` | / |
| `as_ref` | / |
| `cloned` | - |
| `copied` | / |
| `err` | [`err`][apfel.container.result.Result.err] |
| `expect` | [`expect`][apfel.container.result.Result.expect] |
| `expect_err` | [`expect_err`][apfel.container.result.Result.expect_err] |
| `flatten` | [`flatten`][apfel.container.result.Result.flatten] |
| `inspect` | [~`tap`][apfel.container.result.Result.tap] |
| `inspect_err` | [~`tap_err`][apfel.container.result.Result.tap_err] |
| `into_err` | - |
| `into_ok` | - |
| `is_err` | [`is_err`][apfel.container.result.Result.is_err] |
| `is_err_and` | [`is_err_and`][apfel.container.result.Result.is_err_and] |
| `is_ok` | [`is_ok`][apfel.container.result.Result.is_ok] |
| `is_ok_and` | [`is_ok_and`][apfel.container.result.Result.is_ok_and] |
| `iter` | - |
| `iter_mut` | / |
| `map` | [`map`][apfel.container.result.Result.map] |
| `map_err` | [`map_err`][apfel.container.result.Result.map_err] |
| `map_or` | [`map_or`][apfel.container.result.Result.map_or] |
| `map_or_default` | / |
| `map_or_else` | [`map_or_else`][apfel.container.result.Result.map_or_else] |
| `ok` | [`ok`][apfel.container.result.Result.ok] |
| `or` | [`or_`][apfel.container.result.Result.or_] |
| `or_else` | [`or_else`][apfel.container.result.Result.or_else] |
| `transpose` | [~`transpose`][apfel.container.result.Result.transpose] |
| `unwrap` | [`unwrap`][apfel.container.result.Result.unwrap] |
| `unwrap_err` | [`unwrap_err`][apfel.container.result.Result.unwrap_err] |
| `unwrap_err_unchecked` | [`unwrap_err_unchecked`][apfel.container.result.Result.unwrap_err_unchecked] |
| `unwrap_or` | [`unwrap_or`][apfel.container.result.Result.unwrap_or] |
| `unwrap_or_default` | / |
| `unwrap_or_else` | [`unwrap_or_else`][apfel.container.result.Result.unwrap_or_else] |
| `unwrap_unchecked` | [`unwrap_unchecked`][apfel.container.result.Result.unwrap_unchecked] |
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
    from typing import Any


class Result(Monad):
    """A container that holds either a success or a failure.
    See [module-level documentation](result#result) for more details.

    This class is exposed in the [package namespace](../prelude#package-namespace).
    """

    __slots__ = ("_val", "_is_ok")

    def __init__(self, value, /, *, is_ok=True):
        self._val = value
        self._is_ok = is_ok

    def __class_getitem__(cls, item):
        return cls

    @classmethod
    def make_ok(cls, value, /):
        """
        Construct an `Ok` value.
        """
        return cls(value)

    @classmethod
    def make_err(cls, value, /):
        """
        Construct an `Err` value.
        """
        return cls(value, is_ok=False)

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

    def and_then(self, func, /):
        """
        If the value is `Ok`, apply a function that maps the inner value to a `Result[U, E]` value. Otherwise, return `Err` of type `Result[U, E]`.
        """
        return func(self._val) if self._is_ok else Result(self._val, is_ok=False)

    def apply(
        self,
        func,
        /,
    ):
        """
        Implementation of [Applicative.apply][apfel.core.monad.Applicative.apply].
        Applies the callable wrapped within a `Result` to the inner value, if both are `Ok`.
        """
        if self._is_ok:
            if func._is_ok:  # pyright: ignore[reportAttributeAccessIssue]
                return Result(func._val(self._val))  # pyright: ignore[reportAttributeAccessIssue]
            else:
                return Result(func._val, is_ok=False)  # pyright: ignore[reportAttributeAccessIssue]
        else:
            return Result(self._val, is_ok=False)

    def bind(self, func, /):
        """
        Implementation of [`Monad.bind`][apfel.core.monad.Monad.bind].
        Alias of [`and_then`][apfel.container.result.Result.and_then].
        """
        return func(self._val) if self._is_ok else Result(self._val, is_ok=False)

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

    def is_err_and(self, pred, /):
        """
        Check if the value is an `Err` and satisfies the predicate.
        """
        return not self._is_ok and pred(self._val)

    def is_ok(self):
        """
        Check if the value is an `Ok`.
        """
        return self._is_ok

    def is_ok_and(self, pred, /):
        """
        Check if the value is an `Ok` and satisfies the predicate.
        """
        return self._is_ok and pred(self._val)

    def map(self, func, /):
        """
        Map a `Result[T, E]` to `Result[U, E]` by applying a function to a contained `Ok` value, leaving an `Err` value untouched.
        """
        return (
            Result(func(self._val)) if self._is_ok else Result(self._val, is_ok=False)
        )

    def map_err(self, func, /):
        """
        Map a `Result[T, E]` to `Result[T, F]` by applying a function to a contained `Err` value, leaving an `Ok` value untouched.
        """
        return Result(self._val) if self._is_ok else Result(func(self._val), is_ok=False)

    def map_or(self, default, func):
        """
        Apply a function to a contained `Ok` value, or return a provided default value.
        """
        return func(self._val) if self._is_ok else default

    def map_or_else(self, default, func):
        """
        Map a `Result[T, E]` to `U` by applying a function to a contained `Ok` value, or a fallback function to a contained `Err` value.
        """
        return func(self._val) if self._is_ok else default(self._val)

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

    def or_else(self, func, /):
        """
        Return a shallow copy of the `Result` if it contains an `Ok` value, otherwise call a function to get a result.
        """
        return Result(self._val) if self._is_ok else func(self._val)

    @classmethod
    def pure(cls, value, /):
        """
        Implementation of [`Applicative.pure`][apfel.core.monad.Applicative.pure], which is equivalent to [`Result.make_ok`][apfel.container.result.Result.make_ok].
        """
        return cls(value)

    def __repr__(self):
        return (
            f"<Result Ok {self._val!r}>"
            if self._is_ok
            else f"<Result Err {self._val!r}>"
        )

    def __str__(self):
        return f"Ok({self._val})" if self._is_ok else f"Err({self._val})"

    def tap(self, func, /):
        """
        Call a function with the contained `Ok` value if it exists.

        Unlike [:rust `Result::inspect`](https://doc.rust-lang.org/std/result/enum.Result.html#method.inspect),
        this method does not require the function to return `None`.

        ```python
        some_ok = ok(5)
        some_err = err("error")
        some_ok.tap(print)  # prints: 5
        some_err.tap(print)  # prints nothing
        ```
        """
        if self._is_ok:
            func(self._val)
        return self

    def tap_err(self, func, /):
        """
        Call a function with the contained `Err` value if it exists.
        """
        if not self._is_ok:
            func(self._val)
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
            value = self._val
            if isinstance(value, _maybe.Maybe):
                return (
                    _maybe.just(Result(value.unwrap_unchecked()))
                    if value._has_value
                    else _maybe.nothing()
                )
            else:
                # Not a Maybe, so just wrap it.
                return _maybe.just(Result(value))
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

    def unwrap_or_else(self, func, /):
        """
        Unwrap the inner `Ok` value, or return a value computed by a function if contains an `Err`.
        """
        return self._val if self._is_ok else func(self._val)

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

    This function is exposed in the [package namespace](../prelude#package-namespace).

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

    def __new__(cls, value, /):
        return Result(value)

    @classmethod
    def __instancecheck__(cls, instance):
        return instance._is_ok


@variant(Result)
class err:
    """
    Construct an `Err` value.

    This function is exposed in the [package namespace](../prelude#package-namespace).

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

    def __new__(cls, value, /):
        return Result(value, is_ok=False)

    @classmethod
    def __instancecheck__(cls, instance):
        return not instance._is_ok


class caught:
    """
    A decorator that wraps a partial function to a total function returning a `Result`.

    It supports multiple usages:

    - Use as a decorator without arguments (`@caught`) to catch all exceptions.
    - Use as a decorator with specific exception types (either type union `@caught(ExceptionA | ExceptionB)` or args `@caught(ExceptionA, ExceptionB)`) to catch only those exceptions.
    - Use as a higher-order function by passing the target function (`caught(func)`) to catch all exceptions.
    - Use as a higher-order function with specific exception types as args (`caught(func, ExceptionA, ExceptionB)`) to catch only those exceptions.
    - Use generic syntax to provide type hints (`@caught[ExceptionA]`, `@caught[ExceptionA]()`, `caught[ExceptionA]()`), *without affecting runtime behavior*.

    This function is exposed in the [package namespace](../prelude#package-namespace).

    Usage:
        ```python
        @caught(ZeroDivisionError)
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
            elif not isinstance(first, type) or not issubclass(first, BaseException):
                exception = Exception if not exceptions else exceptions
                return cls.__wrap_func(first, exception)

            if exceptions:
                first = tuple([first, *exceptions])

            def decorator(func):
                return cls.__wrap_func(func, first)

            return decorator


__all__ = ["Result", "ok", "err", "caught"]
