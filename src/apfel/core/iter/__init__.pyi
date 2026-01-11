from collections.abc import Iterable, Iterator as _Iterator
from typing import TYPE_CHECKING, Self, overload

if TYPE_CHECKING:
    from builtins import SupportsIter, SupportsNext

from ._iterator import Iterator

class IteratorAdaptor[I](Iterator[I], _Iterator[I]):
    def __init__(self, iterator: _Iterator[I]): ...
    def __next__(self) -> I: ...
    def __iter__(self) -> Self: ...

@overload
def itrt[I](iterable: Iterator[I], /) -> Iterator[I]: ...
@overload
def itrt[I](iterable: SupportsIter[SupportsNext[I]], /) -> IteratorAdaptor[I]: ...
@overload
def itrt[I](iterable: Iterable[I], /) -> IteratorAdaptor[I]: ...

__all__ = ["Iterator", "itrt"]
