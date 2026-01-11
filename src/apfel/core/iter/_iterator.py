from abc import abstractmethod
import collections.abc as _collections_abc
import builtins

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

    def advance_by(self, n: int):
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
    
    def all(self, f):
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
        return builtins.all(map(f, self))
    
    def any(self, f):
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
        return builtins.any(map(f, self))
    
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

    def eq(self, other):
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

    def find(self, f):
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
            if f(item):
                return _maybe.Maybe.make_just(item)
        return _maybe.Maybe.make_nothing()
