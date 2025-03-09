"""
A container that optionally holds a value.

See [`Option`](https://doc.rust-lang.org/std/option/enum.Option.html){ .ref .rs } and [`Maybe`](https://hackage.haskell.org/package/base/docs/Prelude.html#t:Maybe){ .ref .hs }.

A `Maybe` has two possible states, `Just` or `Nothing`. `Just` means a value is present, and `Nothing` means the value is absent.
The reason that we don't use `Some`-`None` or `Nil` nomencalture is to avoid [confusion with the built-in `None`][apfel.container.maybe--rationale].

This module also provides a [`some`][apfel.container.maybe.some] constructor, which converts an `Optional[T]` value to a `Maybe[T]` value.


# Rationale

Python has a built-in [`None`](https://docs.python.org/3/reference/datamodel.html#none){ .ref .py } object that represents the absence of a value,
and a corresponding type hint [`Optional[T]`](https://docs.python.org/3/library/html#Optional){ .ref .py }.
However, an `Optional[T]` is semantically different from a `Maybe[T]` object.
An `Optional[T]` is a *union* of `T` and `None`, not a single object.
To use a union, you must explicitly check its type before every use.

```python
# Usage 1
if optional is None:
    ...
else:
    do_something(optional)

# Usage 2
do_something(optional) if optional is not None else ...

# Usage 3
optional is not None and do_something(optional)
```


On the other hand, a `Maybe[T]` object represents the absence of a value as a *state*.
Operations defined on `Maybe[T]` objects behave differently depending on the state of the object, but they are always available regardless of the state.

``` { .python .annotate }
j: Maybe[int] = just(42)
j.map(do_something) #(1)!

n: Maybe[int] = nothing()
n.map(do_something) #(2)!
```

1. `do_something` is called because `j` is `Just`.
2. `do_something` is not called because `n` is `Nothing`.


!!! warning
    Notice that `None` **is not equal** to `Nothing`.
    Use `Maybe.is_nothing()` to check if a `Maybe` object is `Nothing`.

    ```python
    nothing = Maybe[int].Nothing()

    assert nothing.is_nothing()
    assert nothing is not None
    assert nothing != None
    ```

# Implementation

`Maybe` implements the following interfaces:

| Interface | Methods |
| --- | --- |
| [`Functor`][apfel.core.monad.Functor] | [`map`][apfel.container.maybe.Maybe.map] |
| [`Applicative`][apfel.core.monad.Applicative] | [`pure`][apfel.container.maybe.Maybe.pure], [`apply`][apfel.container.maybe.Maybe.apply] |
| [`Monad`][apfel.core.monad.Monad] | [`bind`][apfel.container.maybe.Maybe.bind]([`and_then`][apfel.container.maybe.Maybe.and_then]) |


The `Maybe` class is a generic class that holds a value of type `T` inside `_val` field.
A boolean flag `_has_value` is used to indicate whether the value is present or absent.
If `_has_value` is `False`, reading from `_val` is an undefined behavior.

`Maybe` and its methods **do not** support inherit-based subclassing.

`Maybe`'s APIs are based on the Rust [`Option`](https://doc.rust-lang.org/std/option/enum.Option.html){ .ref .rs },
and the comparison table is provided below.

| Reference [`Option`](https://doc.rust-lang.org/std/option/enum.Option.html){ .ref .rs } | Counterpart |
| --- | --- |
| `and` | [:material-arrow-right-circle: `and_`][apfel.container.maybe.Maybe.and_] |
| `and_then` | [:material-check-circle:][apfel.container.maybe.Maybe.and_then] |
| `as_deref` | :material-minus-circle: |
| `as_deref_mut` | :material-minus-circle: |
| `as_mut` | :material-minus-circle: |
| `as_mut_slice` | :material-minus-circle: |
| `as_pin_mut` | :material-minus-circle: |
| `as_pin_ref` | :material-minus-circle: |
| `as_ref` | :material-minus-circle: |
| `as_slice` | :material-minus-circle: |
| `cloned` | :material-close-circle: |
| `copied` | :material-minus-circle: |
| `expect` | [:material-check-circle:][apfel.container.maybe.Maybe.expect] |
| `filter` | [:material-check-circle:][apfel.container.maybe.Maybe.filter] |
| `flatten` | [:material-dots-horizontal-circle:][apfel.container.maybe.Maybe.flatten] |
| `get_or_insert` | [:material-check-circle:][apfel.container.maybe.Maybe.get_or_insert] |
| `get_or_insert_default` | :material-minus-circle: |
| `get_or_insert_with` | [:material-check-circle:][apfel.container.maybe.Maybe.get_or_insert_with] |
| `insert` | [:material-check-circle:][apfel.container.maybe.Maybe.insert] |
| `inspect` | [:material-dots-horizontal-circle: `tap`][apfel.container.maybe.Maybe.tap] |
| `is_none` | [:material-arrow-right-circle: `is_nothing`][apfel.container.maybe.Maybe.is_nothing] |
| `is_some` | [:material-arrow-right-circle: `is_just`][apfel.container.maybe.Maybe.is_just] |
| `is_some_and` | [:material-arrow-right-circle: `is_just_and`][apfel.container.maybe.Maybe.is_just_and]|
| `iter` | :material-close-circle: |
| `iter_mut` | :material-minus-circle: |
| `map` | [:material-check-circle:][apfel.container.maybe.Maybe.map] |
| `map_or` | [:material-check-circle:][apfel.container.maybe.Maybe.map_or] |
| `map_or_else` | [:material-check-circle:][apfel.container.maybe.Maybe.map_or_else] |
| `ok_or` | :material-close-circle: |
| `ok_or_else` | :material-close-circle: |
| `or` | [:material-arrow-right-circle: `or_`][apfel.container.maybe.Maybe.__or__] |
| `or_else` | [:material-check-circle:][apfel.container.maybe.Maybe.or_else] |
| `replace` | [:material-check-circle:][apfel.container.maybe.Maybe.replace] |
| `take` | [:material-check-circle:][apfel.container.maybe.Maybe.take] |
| `take_if` | [:material-check-circle:][apfel.container.maybe.Maybe.take_if] |
| `transpose` | :material-close-circle: |
| `unwrap` | [:material-check-circle:][apfel.container.maybe.Maybe.unwrap] |
| `unwrap_or` | [:material-check-circle:][apfel.container.maybe.Maybe.unwrap_or] |
| `unwrap_or_default` | :material-minus-circle: |
| `unwrap_or_else` | [:material-check-circle:][apfel.container.maybe.Maybe.unwrap_or_else] |
| `unwrap_unchecked` | [:material-check-circle:][apfel.container.maybe.Maybe.unwrap_unchecked] |
| `unzip` | :material-minus-circle: |
| `xor` | [:material-check-circle:][apfel.container.maybe.Maybe.xor] |
| `zip` | [:material-dots-horizontal-circle:][apfel.container.maybe.Maybe.zip] |
| `zip_with` | :material-minus-circle: |
"""

from apfel.core.monad import Monad

from apfel.experimental.adt import variant


class Maybe(Monad):
    """
    A container that optionally holds a value.
    See [module-level documentation](maybe.md#maybe) for more information.
    """

    __slots__ = ("_val", "_has_value")

    def __init__(self, val=..., /, *, has_value=True):
        self._val = val
        self._has_value = has_value

    def __class_getitem__(cls, item):
        return cls

    @classmethod
    def just(cls, val, /):
        """
        Construct a `Just` value.

        !!! warning
            Prefer using [`just`][apfel.container.maybe.just] instead, unless in performance-critical code.
        """
        return cls(val)

    @classmethod
    def nothing(cls):
        """
        Construct a `Nothing` value.

        !!! warning
            Prefer using [`Nothing`][apfel.container.maybe.nothing] instead, unless in performance-critical code.
        """

        return cls(has_value=False)

    @classmethod
    def some(cls, val, /):
        """
        Convert an `Optional[T]` value to a `Maybe` value.

        !!! warning
            Prefer using [`some`][apfel.container.maybe.some] function instead, unless in performance-critical code.

        ```python
        some = Maybe.some(42)
        assert some.is_just()

        none = Maybe.some(None)
        assert none.is_nothing()
        ```
        """
        return cls(val) if val is not None else cls(has_value=False)
    
    @classmethod
    def duplicate(cls, m, /):
        """
        Create a shallow copy of a `Maybe` value.
        """
        return cls(m._val, has_value=m._has_value)

    def and_(self, other, /):
        """
        If the value is `Just`, return a shallow copy of the other `Maybe`. Otherwise, return a new `Nothing` of type `Maybe[U]`.

        ```python
        j1 = just[int](42)
        j2 = just[bool](True)

        assert j1.and_(j2).unwrap() == True
        assert (j1 & j2).unwrap() == True
        assert (j1 & nothing[bool]()).is_nothing()
        assert (nothing[int]() & j2).is_nothing()
        ```
        """
        return Maybe(other._val, has_value=other._has_value) if self._has_value else Maybe(has_value=False)

    __and__ = and_
    """
    Alias of [`and_`][apfel.container.maybe.Maybe.and_].
    """

    def and_then(self, f, /):
        """
        If the value is `Just`, apply a function that maps the inner value to a `Maybe[U]` value. Otherwise, return `Nothing` of type `Maybe[U]`.

        ```python
        j = just[int](114514)

        assert j.and_then(lambda x: some(x + 1805296)).unwrap() == 1919810
        ```
        """
        return f(self._val) if self._has_value else Maybe(has_value=False)  # type: ignore

    def apply(self, f):  # type: ignore
        """
        Implementation of [Applicative.apply][apfel.core.monad.Applicative.apply].
        Applies the callable wrapped within a `Maybe` to the inner value, if both are `Just`.
        """
        return (
            (
                Maybe(f._val(self._val))  # type: ignore
                if f._has_value  # type: ignore
                else Maybe(has_value=False)
            )
            if self._has_value
            else Maybe(has_value=False)
        )
    
    def bind(self, f):
        """
        Implementation of [`Monad.bind`][apfel.core.monad.Monad.bind].
        Alias of [`and_then`][apfel.container.maybe.Maybe.and_then].
        """
        return f(self._val) if self._has_value else Maybe(has_value=False)

    def __bool__(self):
        """
        Equivalent to [`is_just`][apfel.container.maybe.Maybe.is_just].
        """
        return self._has_value

    def __eq__(self, other, /):
        """
        If both values are `Just`, compare the inner values. Otherwise, return `True` if both are `Nothing`.

        !!! warning
            Notice that `None` is not equal to `Nothing`.
        """
        if not isinstance(other, Maybe):
            return NotImplemented

        return (
            self._has_value and other._has_value and self._val == other._val
        ) or not (self._has_value or other._has_value)

    def expect(self, message):
        """
        Unwrap the inner value, if any. Otherwise, raise a `ValueError` with a custom message.

        Raises:
            ValueError: If the value is a `Nothing`.
        """
        if not self._has_value:
            raise ValueError(message)
        return self._val

    def filter(self, p, /):
        """
        If the value is `Just` and satisfies the predicate, return the value. Otherwise, return `Nothing`.

        ```python
        j = just[int](42)
        assert j.filter(lambda x: x > 0).unwrap() == 42
        assert j.filter(lambda x: x < 0).is_nothing()
        ```
        """
        return Maybe(has_value=False) if not self._has_value or not p(self._val) else Maybe(self._val)
    
    def flatten(self):
        """
        Flatten a nested `Maybe` value for one level.
        Unlike [`Option::flatten`](https://doc.rust-lang.org/std/option/enum.Option.html#method.flatten){ .ref .rs }, this method does not require the inner value to be a `Maybe`.
        If it's not a nested `Maybe`, this is a no-op.

        ```python
        j = just[Maybe[int]](just(42))
        assert j.flatten() == just(42)

        j2 = just[Maybe[Maybe[int]]](just(just(42)))
        assert j2.flatten() == just(just(42))
        assert j2.flatten().flatten() == just(42)
        ```
        """
        return self._val if self._has_value and isinstance(self._val, Maybe) else self
    
    def get_or_insert(self, val, /):
        """
        Get the inner value, if any. Otherwise, insert the new value and return the value.

        ```python
        j = just[int](42)
        assert j.get_or_insert(114514) == 42

        n = nothing[int]()
        assert n.get_or_insert(114514) == 114514
        ```
        """
        if not self._has_value:
            self._val = val
            self._has_value = True
        return self._val

    def get_or_insert_with(self, d, /):
        """
        Get the inner value, if any. Otherwise, call a function to get a new value and return the value.

        ```python
        j = just[int](42)
        assert j.get_or_insert_with(lambda: 114514) == 42

        n = nothing[int]()
        assert n.get_or_insert_with(lambda: 114514) == 114514
        ```
        """
        if not self._has_value:
            self._val = d()
            self._has_value = True
        return self._val

    def __hash__(self):
        return hash((id(Maybe), self._has_value, self._val))
    
    def insert(self, val, /):
        """
        Insert a value and returns it.
        """
        self._val = val
        self._has_value = True
        return self._val

    def is_just(self):
        """
        Check if the value is a `Just`.
        """
        return self._has_value

    def is_just_and(self, p, /):
        """
        Check if the value is a `Just` and satisfies the predicate.
        """
        return self._has_value and p(self._val)

    def is_nothing(self):
        """
        Check if the value is a `Nothing`.

        !!! note
            A `Just(Nothing)` value of type `Maybe[Maybe[T]]` or a `Just(None)` value of type `Maybe[Optional[T]]` are not `Nothing`s.
        """
        return not self._has_value
    
    def __len__(self):
        """
        Return 1 if the value is `Just`, otherwise 0.
        """
        return 1 if self._has_value else 0

    def map(self, f):
        """
        Apply a function that maps the inner value to a new value, if any. Otherwise, return `Nothing`.

        See [`Option::map`](https://doc.rust-lang.org/std/option/enum.Option.html#method.map){ .ref .rs }.

        ```python
        j = just[int](42)
        assert j.map(lambda x: x + 1) == just(43)

        n = nothing[int]()
        assert n.map(lambda x: x + 1) == nothing()
        ```
        """
        return (
            Maybe(f(self._val)) if self._has_value else Maybe(has_value=False)  # type: ignore
        )

    def map_or(self, default, f, /):
        """
        Map the inner value using a function, or use the default value if absent.

        !!! tip
            If the default value is an expensive expression, use [`map_or_else`][apfel.container.maybe.Maybe.map_or_else] instead.

        ```python
        j = just[int](42)
        n = nothing[int]()

        assert j.map_or(0, lambda x: x + 1) == 43
        assert n.map_or(0, lambda x: x + 1) == 0
        ```z
        """
        return f(self._val) if self._has_value else default

    def map_or_else(self, d, f, /):
        """
        Map the inner value using a function, or use a lazy default value if absent.

        ```python
        j = just[int](42)
        n = nothing[int]()

        assert j.map_or_else(lambda: 0, lambda x: x + 1) == 43
        assert n.map_or_else(lambda: 0, lambda x: x + 1) == 0
        ```
        """
        return f(self._val) if self._has_value else d()

    def or_(self, other, /):
            """
            If the value is `Just`, return a shallow copy of itself. Otherwise, return the other `Maybe`'s shallow copy.

            Notice that the right-hand side should be a `Maybe` object with the same inner type,
            although this is not enforced at runtime.
            And also this method does not short-circuit.

            ```python
            j1 = just[int](42)
            j2 = just[int](114514)

            assert (j1 | j2).unwrap() == 42
            assert (nothing[int]() | j2).unwrap() == 114514
            assert (j1 | nothing[int]()).unwrap() == 42
            ```
            """
            return Maybe(self._val, has_value=self._has_value) if self._has_value else Maybe(other._val, has_value=other._has_value)

    __or__ = or_
    """
    Alias of [`or_`][apfel.container.maybe.Maybe.or_].
    """

    def or_else(self, f, /):
        """
        Return a shallow copy of the `Maybe` if it contains a value, otherwise call a function to get a result.
        """

        return Maybe(self._val) if self._has_value else f()

    @classmethod
    def pure(cls, x):
        """
        Implementation of [Applicative.pure][apfel.core.monad.Applicative.pure], which is equivalent to [Maybe.just][apfel.container.maybe.Maybe.just].
        """
        return cls(x)

    def replace(self, val, /):
        """
        Replace the inner value with a new value, returning the old value.
        After replacement, `self` will always have a value.
        
        ```python
        j = just[int](42)
        old = j.replace(114514)
        assert j == just(114514)
        assert old == just(42)

        n = nothing[int]()
        old = n.replace(1919810)
        assert n == just(1919810)
        assert old == nothing()
        ```
        """
        if self._has_value:
            swapped = Maybe(self._val)
            self._val = val
            return swapped
        else:
            self._val = val
            self._has_value = True
            return Maybe(has_value=False)

    def __repr__(self):
        return f"<Maybe Just {self._val!r}>" if self._has_value else "<Maybe Nothing>"

    def __str__(self):
        return f"Just({self._val})" if self._has_value else "Nothing"

    def take(self):
        """
        Take the inner value out and leave no value in place.

        ```python
        j = just[int](42)
        out = j.take()
        assert j.is_nothing()
        assert out == just(42)
        ```
        """

        if self._has_value:
            self._has_value = False
            out = Maybe(self._val)
            self._val = ...
            return out
        else:
            return Maybe(has_value=False)
        
    def take_if(self, p, /):
        """
        Take the inner value out if it satisfies the predicate, and leave no value in place.
        Otherwise, take out nothing.

        ```python
        j = just[int](42)
        out = j.take_if(lambda x: x > 0)
        assert j.is_nothing()
        assert out == just(42)

        j = just[int](42)
        out = j.take_if(lambda x: x < 0)
        assert j.is_just()
        assert out == nothing()
        ```
        """

        if self._has_value and p(self._val):
            self._has_value = False
            out = Maybe(self._val)
            self._val = ...
            return out
        else:
            return Maybe(has_value=False)

    def tap(self, f, /):
        """
        Call a function with the inner value, if any, and return the `Maybe` itself.
        Unlike [`Option::inspect`](https://doc.rust-lang.org/std/option/enum.Option.html#method.inspect){ .ref .rs }, this method does not require the function to return `None`.

        ```python
        j = just[int](42)
        j.tap(print)  # prints 42
        ```
        """
        if self._has_value:
            f(self._val)
        return self

    def unwrap(self):
        """
        Unwrap the inner value, if any. Otherwise, raise a `ValueError`.

        ``` { .python .annotate }
        j = just[int](42)
        n = nothing[int]()

        assert j.unwrap() == 42

        try: n.unwrap()
        except ValueError: pass
        else: assert False
        ```

        Raises:
            ValueError: If the value is a `Nothing`.
        """
        if not self._has_value:
            raise ValueError("called `Maybe.unwrap()` on a `Nothing` value")
        return self._val

    def unwrap_or(self, default, /):
        """
        Unwrap the inner value, or return a default value if absent.

        ```python
        j = just[int](42)
        n = nothing[int]()
        assert j.unwrap_or(0) == 42
        assert n.unwrap_or(0) == 0
        ```
        """
        return self._val if self._has_value else default

    def unwrap_or_else(self, f, /):
        """
        Unwrap the inner value, or return a value computed by a function if absent.
        """
        return self._val if self._has_value else f()

    def unwrap_unchecked(self):
        """
        Return the inner value without checking if it is a `Just` or `Nothing`.
        """
        return self._val
    
    def xor(self, other, /):
        """
        If only one side has a value, return that side. Otherwise, return a `Nothing`.

        ```python
        j1 = just[int](42)
        j2 = just[int](114514)
        assert j1.xor(j2).is_nothing()
        ```
        """
        return (
            Maybe(has_value=False)
            if self._has_value == other._has_value
            else (
                Maybe(self._val) if self._has_value else Maybe(other._val)
            )
        )
    
    def zip(self, *others):
        """
        Combine multiple `Maybe` values into a single `Maybe` value containing a tuple of them.
        If all values are `Just`, return a `Just` value with a tuple of inner values.
        Otherwise, return a `Nothing`.
        Calling this method with no arguments is equivalent to calling `map` with a tuple constructor.

        !!! warning "Typing"
            The type checker only supports zipping up to 5-tuple.

        ```python
        j1 = just[int](42)
        j2 = just[int](114514)
        assert j1.zip(j2).unwrap() == (42, 114514)

        n = nothing[int]()
        assert j1.zip(n).is_nothing()
        ```
        """
        if not (self._has_value and all(other._has_value for other in others)):
            return Maybe(has_value=False)
        return Maybe((self._val, *(other._val for other in others)))  # type: ignore

@variant(Maybe)
class just:
    """
    Constructs a `Just` value.

    ```python
    j: Maybe[int] = just(42)
    j = just[int](42)

    assert j.is_just()
    assert j.unwrap() == 42
    ```

    !!! warning
        Calling `just(None)` will return a `Just(None)` value, not a `Nothing` value.
        If you want to map `None` to `Nothing`, use [`some`][apfel.container.maybe.some] instead.
    """

    __slots__ = ()

    __match_args__ = ("_val",)

    def __class_getitem__(cls, item):
        return cls

    def __new__(cls, val, /):
        return Maybe(val)

    @classmethod
    def __instancecheck__(cls, instance):
        return instance._has_value


@variant(Maybe)
class nothing:
    """
    Constructs a `Nothing` value.
    Notice that this is not a literal.

    ```python
    n: Maybe[int] = nothing()
    n = nothing[int]()

    assert n.is_nothing()
    ```
    """

    __slots__ = ()

    def __class_getitem__(cls, item):
        return cls

    def __new__(cls):
        return Maybe(has_value=False)
    
    @classmethod
    def __instancecheck__(cls, instance):
        return not instance._has_value


class some:
    """
    Converts an `Optional[T]` to a `Maybe[T]` value.

    ```python
    something: Maybe[int] = some(42)
    assert something.is_just()
    assert something.unwrap() == 42

    something = some[int](None)
    assert something.is_nothing()
    ```
    """

    __slots__ = ()

    def __class_getitem__(cls, item):
        return cls

    def __new__(cls, val, /):
        return Maybe.some(val)


__all__ = ["Maybe", "just", "nothing", "some"]
