from __future__ import annotations

from apfel.core.monad import Functor, Applicative, Monad
from apfel.core.dispatch import impl

class Maybe[T](Monad):
    value: T
    is_nothing: bool

    def __init__(self, value: T | None = None):
        if value is None:
            self.is_nothing = True
        else:
            self.value = value
            self.is_nothing = False

    @classmethod
    def pure(cls, x):
        return cls(x)
    
    def bind(self, f):
        if self.is_nothing:
            return self
        return f(self.value)
    
    def __eq__(self, other):
        return isinstance(other, Maybe) and self.is_nothing == other.is_nothing and self.value == other.value


def test_monad_maybe():
    assert Maybe.__abstractmethods__ == set()

    maybe = Maybe(42)  # type: ignore
    
    assert maybe.map(lambda x: x + 1) == Maybe(43) # type: ignore
    assert maybe.apply(Maybe(lambda x: x + 1)) == Maybe(43) # type: ignore
    assert maybe.bind(lambda x: Maybe(x + 1)) == Maybe(43) # type: ignore
