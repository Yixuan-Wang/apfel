"""\
Tip: Meme
    <del>A monad is a **monoid** in the category of **endofunctors**.</del>

Monadic interfaces that enable
structured ways to compose and manipulate computations on a single effectful construction.

The module defines three abstract classes: [`Functor`][apfel.core.monad.Functor],
[`Applicative`][apfel.core.monad.Applicative], and [`Monad`][apfel.core.monad.Monad].

# Rationale

Monadic abstractions like [`Functor`](https://hackage.haskell.org/package/base/docs/Data-Functor.html){.ref .hs}, [`Applicative`](https://hackage.haskell.org/package/base/docs/Control-Applicative.html){.ref .hs}, and [`Monad`](https://hackage.haskell.org/package/base/docs/Control-Monad.html){.ref .hs} are popularized by Haskell.
Although Python has weak support for functional programming, we include these abstractions to provide a uniform interface for such calculations.

Under the hood, these abstractions use dynamic single dispatch provided in [`apfel.core.dispatch`](/core/dispatch), which
allows us to define monadic helper functions for standard built-in types.
This module provides default implementations for `list`, `tuple`, `set`, and `function` as `Functor`, `Applicative`, and `Monad`, `dict` as `Functor`.

Note that we losen the constraints of such abstractions, as writing pure functional code is not a goal of this library.

# Usage

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

## Case: `list`

```python
assert Functor.map([1, 2, 3], lambda x: x + 1) == [2, 3, 4]
assert Applicative.apply([1, 2, 3], [lambda x: x + 1, lambda x: x + 2]) == [2, 3, 4, 3, 4, 5]
assert Monad.bind([1, 2, 3], lambda x: [x, x + 1]) == [1, 2, 2, 3, 3, 4]
```

## Case: `function`

`Functor.map` of a function is exactly a composition of functions.

```python
assert Functor.map(lambda x: x * 2, lambda x: x + 1)(2) == 5
```
"""

from ._definition import Functor, Applicative, Monad
from . import _implementation

"""
Use the default implementations for the built-in types, namely `list`, `tuple`, `set`, `dict` and `function`.
Besides `dict` which is only a `Functor`, all other types are `Functor`, `Applicative`, and `Monad`.

This function should be called before using the monadic abstractions.

See the [module level usage guide][apfel.core.monad--usage] for more information.
"""
for name, impl in vars(_implementation).items():
    if name.startswith("do_impl_for_"):
        impl()

fmap = Functor.map
"""
An alias for [`Functor.map`][apfel.core.monad.Functor.map].
"""

__all__ = ["Functor", "Applicative", "Monad", "fmap"]
