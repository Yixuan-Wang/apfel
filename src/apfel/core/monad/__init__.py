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

from ._definition import Functor, Applicative, Monad
from . import _implementation

for name, impl in vars(_implementation).items():
    if name.startswith("do_impl_for_"):
        impl()

__all__ = ["Functor", "Applicative", "Monad"]
