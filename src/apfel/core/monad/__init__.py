from ._definition import Functor, Applicative, Monad
from . import _implementation

for name, impl in vars(_implementation).items():
    if name.startswith("do_impl_for_"):
        impl()

__all__ = ["Functor", "Applicative", "Monad"]
