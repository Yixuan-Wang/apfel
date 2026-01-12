"""
The abstraction for an iterator, alternative to Python's vanilla built-in iterator ABC [`collections.abc.Iterator`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Iterator){ .ref .py }.

# Implementation

Iterators have a large number of methods. Missing methods will be added gradually over time.

??? info "[`Iterator`](https://doc.rust-lang.org/std/iter/trait.Iterator.html){ .ref .rs }"

    | Reference [`Iterator`](https://doc.rust-lang.org/std/iter/trait.Iterator.html){ .ref .rs } | Counterpart |
    | --- | --- |
    | `advance_by`         | [:material-check-circle:][apfel.core.iter.Iterator.advance_by] |
    | `all`                | [:material-check-circle:][apfel.core.iter.Iterator.all] |
    | `any`                | [:material-check-circle:][apfel.core.iter.Iterator.any] |
    | `array_chunks`       | :material-close-circle: |
    | `by_ref`             | :material-minus-circle: |
    | `chain`              | :material-close-circle: |
    | `cloned`             | :material-close-circle: |
    | `cmp`                | :material-close-circle: |
    | `cmp_by`             | :material-close-circle: |
    | `collect`            | :material-close-circle: |
    | `collect_into`       | :material-close-circle: |
    | `copied`             | :material-close-circle: |
    | `count`              | [:material-check-circle:][apfel.core.iter.Iterator.count] |
    | `cycle`              | :material-close-circle: |
    | `enumerate`          | :material-close-circle: |
    | `eq`                 | [:material-check-circle:][apfel.core.iter.Iterator.eq] |
    | `eq_by`              | :material-close-circle: |
    | `filter`             | [:material-check-circle:][apfel.core.iter.Iterator.filter] |
    | `filter_map`         | :material-close-circle: |
    | `find`               | [:material-check-circle:][apfel.core.iter.Iterator.find] |
    | `find_map`           | :material-close-circle: |
    | `flat_map`           | :material-close-circle: |
    | `flatten`            | :material-close-circle: |
    | `fold`               | [:material-check-circle:][apfel.core.iter.Iterator.fold] |
    | `for_each`           | [:material-check-circle:][apfel.core.iter.Iterator.for_each] |
    | `fuse`               | :material-close-circle: |
    | `ge`                 | :material-close-circle: |
    | `gt`                 | :material-close-circle: |
    | `inspect`            | :material-close-circle: |
    | `intersperse`        | :material-close-circle: |
    | `intersperse_with`   | :material-close-circle: |
    | `is_partitioned`     | :material-close-circle: |
    | `is_sorted`          | :material-close-circle: |
    | `is_sorted_by`       | :material-close-circle: |
    | `is_sorted_by_key`   | :material-close-circle: |
    | `last`               | :material-close-circle: |
    | `le`                 | :material-close-circle: |
    | `lt`                 | :material-close-circle: |
    | `map`                | [:material-check-circle:][apfel.core.iter.Iterator.map] |
    | `map_while`          | :material-close-circle: |
    | `map_windows`        | :material-close-circle: |
    | `max`                | :material-close-circle: |
    | `max_by`             | :material-close-circle: |
    | `max_by_key`         | :material-close-circle: |
    | `min`                | :material-close-circle: |
    | `min_by`             | :material-close-circle: |
    | `min_by_key`         | :material-close-circle: |
    | `ne`                 | :material-close-circle: |
    | `next`               | [:material-check-circle:][apfel.core.iter.Iterator.next] |
    | `next_chunk`         | :material-close-circle: |
    | `nth`                | :material-close-circle: |
    | `partial_cmp`        | :material-close-circle: |
    | `partial_cmp_by`     | :material-close-circle: |
    | `partition`          | :material-close-circle: |
    | `partition_in_place` | :material-close-circle: |
    | `peekable`           | :material-close-circle: |
    | `position`           | :material-close-circle: |
    | `product`            | :material-close-circle: |
    | `reduce`             | [:material-check-circle:][apfel.core.iter.Iterator.reduce] |
    | `rev`                | :material-close-circle: |
    | `rposition`          | :material-close-circle: |
    | `scan`               | :material-close-circle: |
    | `size_hint`          | :material-close-circle: |
    | `skip`               | :material-close-circle: |
    | `skip_while`         | :material-close-circle: |
    | `step_by`            | :material-close-circle: |
    | `sum`                | :material-close-circle: |
    | `take`               | :material-close-circle: |
    | `take_while`         | :material-close-circle: |
    | `try_collect`        | :material-close-circle: |
    | `try_find`           | :material-close-circle: |
    | `try_fold`           | :material-close-circle: |
    | `try_for_each`       | :material-close-circle: |
    | `try_reduce`         | :material-close-circle: |
    | `unzip`              | :material-close-circle: |
    | `zip`                | :material-close-circle: |
"""

from abc import abstractmethod
import builtins
import collections.abc as _collections_abc
import functools as _functools
from typing import Generic, TypeVar

import apfel.container.maybe as _maybe
import apfel.container.result as _result
import apfel.core.dispatch as _dispatch

I = TypeVar("I")

class Iterator(_dispatch.ABCDispatch, Generic[I]):
    """
    ```python
    class Iterator[I](ABC):
        __next__
    ```

    The interface for an iterator.
    See module level documentation for more information.
    """

    @abstractmethod
    def __next__(self):
        """
        Return the next item of the iterator.
        If the iterator is exhausted, raise `StopIteration`.
        
        Any implementor of [`collections.abc.Iterator`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Iterator){ .ref .py } should be directly compatible with this interface.

        ```python
        iterator = itrt([1, 2, 3])
        assert next(iterator) == 1
        assert next(iterator) == 2
        assert next(iterator) == 3
        
        try:
            next(iterator)
        except StopIteration:
            # Iterator is exhausted
            pass
        ```
        """
        ...

    def next(self) -> _maybe.Maybe:
        """
        Return the next item of the iterator, wrapped in a [`Maybe`](apfel.container.maybe.Maybe).

        ```python
        iterator = itrt([1, 2, 3])
        assert iterator.next().unwrap() == 1
        assert iterator.next().unwrap() == 2
        assert iterator.next().unwrap() == 3
        assert iterator.next().is_nothing()
        ```
        """
        try:
            return _maybe.Maybe.make_just(next(self))
        except StopIteration:
            return _maybe.Maybe.make_nothing()

    def __iter__(self):
        return self

    def advance_by(self, n: int, /):
        """
        Advance the iterator by `n` steps.
        If the iterator is exhausted before advancing `n` steps,
        return an `Err` containing the number of remaining steps.
        Otherwise, return `Ok(())`.

        ```python
        iterator = itrt([1, 2, 3, 4, 5])
        assert iterator.advance_by(2).is_ok()
        assert iterator.next().unwrap() == 3
        assert iterator.advance_by(6).unwrap_err() == 4
        ```
        """
        for i in range(n):
            try:
                next(self)
            except StopIteration:
                return _result.Result.make_err(n - i)

        return _result.Result.make_ok(None)
    
    def all(self, pred, /):
        """
        Returns `True` if all elements of the iterator satisfy the predicate `f`.
        Otherwise, returns `False`.

        The iteration short-circuits if an element is found that does not satisfy the predicate.
        An empty iterator returns `True`.

        ```python
        iterator = itrt([2, 4, 6])
        assert iterator.all(lambda x: x % 2 == 0)
        assert iterator.next().is_nothing()
        
        iterator = itrt([2, 3, 6])
        assert not iterator.all(lambda x: x % 2 == 0)
        assert iterator.next().unwrap() == 6
        ```
        """
        return builtins.all(map(pred, self))
    
    def any(self, pred, /):
        """
        Returns `True` if any element of the iterator satisfies the predicate `f`.
        Otherwise, returns `False`.

        The iteration short-circuits if an element is found that satisfies the predicate.
        An empty iterator returns `False`.

        ```python
        iterator = itrt([1, 3, 5])
        assert not iterator.any(lambda x: x % 2 == 0)
        assert iterator.next().is_nothing()
        
        iterator = itrt([1, 2, 3])
        assert iterator.any(lambda x: x % 2 == 0)
        assert iterator.next().unwrap() == 3
        ```
        """
        return builtins.any(map(pred, self))
    
    def count(self):
        """
        Counts the number of elements in the iterator, until it is exhausted.

        ```python
        iterator = itrt([1, 2, 3, 4, 5])
        assert iterator.count() == 5
        ```
        """
        cnt = 0
        for _ in self:
            cnt += 1
        return cnt

    def eq(self, other, /):
        """
        Checks if two iterators are equal by comparing their elements pairwise.
        
        ```python
        iterator1 = itrt([1, 2, 3])
        iterator2 = itrt([1, 2, 3])
        assert iterator1.eq(iterator2)

        iterator1 = itrt([1, 2, 3])
        iterator3 = itrt([1, 2, 4])
        assert not iterator1.eq(iterator3)

        iterator1 = itrt([1, 2, 3])
        iterator4 = itrt([1, 2])
        assert not iterator1.eq(iterator4)
        ```
        """
        try:
            if not all(a == b for a, b in zip(self, other, strict=True)):
                return False
        except ValueError:
            return False
        
        return True

    def __eq__(self, other):
        if not isinstance(other, _collections_abc.Iterator):
            return NotImplemented
        return self.eq(other)
    
    def filter(self, pred, /):
        """
        Creates a new iterator that yields only the elements of the original iterator
        that satisfy the predicate `pred`.

        ```python
        iterator = itrt([1, 2, 3, 4, 5])
        filtered_iterator = iterator.filter(lambda x: x % 2 == 0)
        assert filtered_iterator.next().unwrap() == 2
        assert filtered_iterator.next().unwrap() == 4
        assert filtered_iterator.next().is_nothing()
        assert iterator.next().is_nothing()  # original iterator is also exhausted
        ```
        """
        return IteratorAdaptor(builtins.filter(pred, self))

    def find(self, pred, /):
        """
        Returns the first element in the iterator that satisfies the predicate `f`,
        wrapped in a [`Maybe`](apfel.container.maybe.Maybe).
        If no such element is found, returns `Nothing`.

        ```python
        iterator = itrt([1, 2, 3, 4, 5])
        assert iterator.find(lambda x: x % 2 == 0).unwrap() == 2
        assert iterator.find(lambda x: x <= 3).unwrap() == 3  # 1, 2 have been consumed
        assert iterator.find(lambda x: x > 10).is_nothing()  # no such element exists
        assert iterator.next().is_nothing()  # iterator is exhausted
        ```
        """
        for item in self:
            if pred(item):
                return _maybe.Maybe.make_just(item)
        return _maybe.Maybe.make_nothing()
    
    def fold(self, init, func):
        """
        Fold (reduce) the elements of the iterator using the accumulation function `func`,
        starting with the initial value `init`.

        See also [`reduce`][apfel.core.iter.Iterator.reduce] if the first element of the iterator should be used as the initial accumulator value.

        Tip:
            The default implementation of this method uses [`functools.reduce`](https://docs.python.org/3/library/functools.html#functools.reduce){ .ref .py }
            under the hood, but allows keyword arguments for both `init` and `func`.

        ```python
        iterator = itrt([1, 2, 3, 4, 5])
        result = iterator.fold(0, lambda acc, x: acc + x)
        assert result == 15  # 0 + 1 + 2 + 3 + 4 + 5

        iterator = itrt([])
        result = iterator.fold(10, lambda acc, x: acc + x)
        assert result == 10  # initial value only
        ```
        """
        return _functools.reduce(func, self, init)
    
    def for_each(self, func, /):
        """
        Applies the function `func` to each element of the iterator.
        Compare to [`map`](apfel.core.iter.Iterator.map), the result of each function application is discarded,
          and the iterator is consumed eagerly.

        ```python
        iterator = itrt([1, 2, 3])
        iterator.for_each(lambda x: print(x, end=" "))
        # Output: 1 2 3
        ```
        """
        for item in self:
            func(item)
    
    def map(self, func, /):
        """
        Creates a new iterator that applies the function `func` to each element of the original iterator.

        ```python
        iterator = itrt([1, 2, 3])
        mapped_iterator = iterator.map(lambda x: x * 2)
        assert mapped_iterator.next().unwrap() == 2
        assert mapped_iterator.next().unwrap() == 4
        assert mapped_iterator.next().unwrap() == 6
        assert mapped_iterator.next().is_nothing()
        assert iterator.next().is_nothing()  # original iterator is also exhausted
        ```
        """
        return IteratorAdaptor(builtins.map(func, self))
    
    def reduce(self, func, /):
        """
        Reduce the elements of the iterator using the accumulation function `func` and returns a [`Maybe`](apfel.container.maybe.Maybe).
        The first element of the iterator is used as the initial accumulator value.
        If the iterator is empty, returns `Nothing`.

        See also [`fold`](apfel.core.iter.Iterator.fold) if an explicit initial value is needed.

        ```python
        iterator = itrt([1, 2, 3, 4, 5])
        result = iterator.reduce(lambda acc, x: acc + x)
        assert result.unwrap() == 15  # 1 + 2 + 3 + 4 + 5

        iterator = itrt([])
        result = iterator.reduce(lambda acc, x: acc + x)
        assert result.is_nothing()  # no elements to reduce
        ```
        """
        try:
            return _maybe.Maybe.make_just(_functools.reduce(func, self))
        except TypeError:
            return _maybe.Maybe.make_nothing()

class IteratorAdaptor(Iterator):
    __slots__ = ("_iterator",)

    def __init__(self, iterator):
        self._iterator = iterator

    def __next__(self):
        return next(self._iterator)

    def __repr__(self):
        return f"<IteratorAdaptor {repr(self._iterator)}>"

    def __getattr__(self, name):
        return getattr(self._iterator, name)


def itrt(iterable, /):
    """
    Create an `Iterator` from a standard Python `Iterator` or `Iterable`.

    Args:
        iterable: A Python standard `collections.abc.Iterator` or `collections.abc.Iterable`.

    Returns:
        An iterator that guarantees the apfel `Iterator` interface.

    Raises:
        TypeError: If the input is neither an `Iterator` nor an `Iterable`.
    """
    if isinstance(iterable, Iterator):
        return iterable
    elif isinstance(iterable, _collections_abc.Iterator):
        return IteratorAdaptor(iterable)
    elif isinstance(iterable, _collections_abc.Iterable):
        iterator = iter(iterable)
        return IteratorAdaptor(iterator)
    else:
        raise TypeError(f"Cannot convert type {type(iterable)} to Iterator")


__all__ = ["Iterator", "itrt"]
