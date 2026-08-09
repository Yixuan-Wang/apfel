"""
The abstraction for an iterator, alternative to Python's vanilla built-in iterator ABC [:python `collections.abc.Iterator`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Iterator).
It provides a large number of methods that are commonly found in Rust [:rust `Iterator`](https://doc.rust-lang.org/std/iter/trait.Iterator.html) and Python [:python `itertools`](https://docs.python.org/3/library/itertools.html).

To create or use this abstraction of iterator:

- Use [`itrt`][apfel.core.iter.itrt] to wrap any iterable or Python vanilla iterator,
- Use `Iterator` methods directly on any Python vanilla iterator.

[`Iterator`][apfel.core.iter.Iterator] and [`itrt`][apfel.core.iter.itrt] are are exposed in the [package namespace](../prelude#package-namespace).

# Implementation

Iterators have a large number of methods. Missing methods will be added gradually over time.

Note:
    **[:rust `Iterator`](https://doc.rust-lang.org/std/iter/trait.Iterator.html)**


    | Reference [:rust `Iterator`](https://doc.rust-lang.org/std/iter/trait.Iterator.html) | Counterpart |
    | --- | --- |
    | `advance_by`         | [`advance_by`][apfel.core.iter.Iterator.advance_by] |
    | `all`                | [`all`][apfel.core.iter.Iterator.all] |
    | `any`                | [`any`][apfel.core.iter.Iterator.any] |
    | `array_chunks`       | - |
    | `by_ref`             | / |
    | `chain`              | [`chain`][apfel.core.iter.Iterator.chain] |
    | `cloned`             | - |
    | `cmp`                | - |
    | `cmp_by`             | - |
    | `collect`            | - |
    | `collect_into`       | - |
    | `copied`             | - |
    | `count`              | [`count`][apfel.core.iter.Iterator.count] |
    | `cycle`              | - |
    | `enumerate`          | [~`enumerate`][apfel.core.iter.Iterator.enumerate] |
    | `eq`                 | [`eq`][apfel.core.iter.Iterator.eq] |
    | `eq_by`              | - |
    | `filter`             | [`filter`][apfel.core.iter.Iterator.filter] |
    | `filter_map`         | [`filter_map`][apfel.core.iter.Iterator.filter_map] |
    | `find`               | [`find`][apfel.core.iter.Iterator.find] |
    | `find_map`           | [`find_map`][apfel.core.iter.Iterator.find_map] |
    | `flat_map`           | [`flat_map`][apfel.core.iter.Iterator.flat_map] |
    | `flatten`            | [`flatten`][apfel.core.iter.Iterator.flatten] |
    | `fold`               | [`fold`][apfel.core.iter.Iterator.fold] |
    | `for_each`           | [`for_each`][apfel.core.iter.Iterator.for_each] |
    | `fuse`               | - |
    | `ge`                 | - |
    | `gt`                 | - |
    | `inspect`            | [`tap`][apfel.core.iter.Iterator.tap] |
    | `intersperse`        | [`intersperse`][apfel.core.iter.Iterator.intersperse] |
    | `intersperse_with`   | [`intersperse_with`][apfel.core.iter.Iterator.intersperse_with] |
    | `is_partitioned`     | - |
    | `is_sorted`          | - |
    | `is_sorted_by`       | - |
    | `is_sorted_by_key`   | - |
    | `last`               | [`last`][apfel.core.iter.Iterator.last] |
    | `le`                 | - |
    | `lt`                 | - |
    | `map`                | [`map`][apfel.core.iter.Iterator.map] |
    | `map_while`          | [`map_while`][apfel.core.iter.Iterator.map_while] |
    | `map_windows`        | - |
    | `max`                | - |
    | `max_by`             | - |
    | `max_by_key`         | - |
    | `min`                | - |
    | `min_by`             | - |
    | `min_by_key`         | - |
    | `ne`                 | - |
    | `next`               | [`next`][apfel.core.iter.Iterator.next] |
    | `next_chunk`         | - |
    | `nth`                | [`nth`][apfel.core.iter.Iterator.nth] |
    | `partial_cmp`        | - |
    | `partial_cmp_by`     | - |
    | `partition`          | - |
    | `partition_in_place` | - |
    | `peekable`           | - |
    | `position`           | [`position`][apfel.core.iter.Iterator.position] |
    | `product`            | [`pipe(math.product)`][apfel.core.iter.Iterator.pipe] |
    | `reduce`             | [`reduce`][apfel.core.iter.Iterator.reduce] |
    | `rev`                | - |
    | `rposition`          | - |
    | `scan`               | [`scan`][apfel.core.iter.Iterator.scan] |
    | `size_hint`          | - |
    | `skip`               | [`skip`][apfel.core.iter.Iterator.skip] |
    | `skip_while`         | [`skip_while`][apfel.core.iter.Iterator.skip_while] |
    | `step_by`            | [`step_by`][apfel.core.iter.Iterator.step_by] |
    | `sum`                | [`pipe(sum)`][apfel.core.iter.Iterator.pipe]|
    | `take`               | [`take`][apfel.core.iter.Iterator.take] |
    | `take_while`         | [`take_while`][apfel.core.iter.Iterator.take_while] |
    | `try_collect`        | - |
    | `try_find`           | - |
    | `try_fold`           | - |
    | `try_for_each`       | - |
    | `try_reduce`         | - |
    | `unzip`              | - |
    | `zip`                | [`zip`][apfel.core.iter.Iterator.zip] |

Note:
    **[:python `itertools`](https://docs.python.org/3/library/itertools.html)**


    This table tracks named `Iterator` counterparts in [:python `itertools`](https://docs.python.org/3/library/itertools.html).
    Standalone `itertools` functions can still be used through [`pipe`][apfel.core.iter.Iterator.pipe] when their first argument is an iterable.

    | Reference [:python `itertools`](https://docs.python.org/3/library/itertools.html) | Counterpart |
    | --- | --- |
    | `accumulate`                       | [`accumulate`][apfel.core.iter.Iterator.accumulate] |
    | `batched`                          | - |
    | `chain`                            | [`chain`][apfel.core.iter.Iterator.chain] |
    | `chain.from_iterable`              | [`flatten`][apfel.core.iter.Iterator.flatten] |
    | `compress`                         | - |
    | `count`                            | - |
    | `cycle`                            | - |
    | `dropwhile`                        | [`skip_while`][apfel.core.iter.Iterator.skip_while] |
    | `filterfalse`                      | [~`filter`][apfel.core.iter.Iterator.filter] |
    | `groupby`                          | - |
    | `islice`                           | [~`take`][apfel.core.iter.Iterator.take] / [`skip`][apfel.core.iter.Iterator.skip] / [`step_by`][apfel.core.iter.Iterator.step_by] |
    | `pairwise`                         | - |
    | `repeat`                           | - |
    | `starmap`                          | [~`map`][apfel.core.iter.Iterator.map] |
    | `takewhile`                        | [`take_while`][apfel.core.iter.Iterator.take_while] |
    | `tee`                              | - |
    | `zip_longest`                      | - |
    | `product`                          | - |
    | `permutations`                     | - |
    | `combinations`                     | - |
    | `combinations_with_replacement`    | - |
"""

import builtins
import collections.abc as _collections_abc
import functools as _functools
import itertools as _itertools
from abc import abstractmethod
from typing import Generic, TypeVar

import apfel.container.maybe as _maybe
import apfel.container.result as _result
import apfel.core.dispatch as _dispatch

I = TypeVar("I")


def _func_iterator_last(acc: I, x: I) -> I:
    return x


_sentinal_iterator_last = object()


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

        Any implementor of [:python `collections.abc.Iterator`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Iterator) should be directly compatible with this interface.

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
        Return the next item of the iterator, wrapped in a [`Maybe`][apfel.container.maybe.Maybe].

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

    def accumulate(self, state, func):
        """
        Creates a new iterator that yields the accumulated state after applying `func`
        to each element, starting with `state`. Unlike [`fold`][apfel.core.iter.Iterator.fold],
        this yields each intermediate state rather than consuming the iterator.

        Compared to [:python `itertools.accumulate`](https://docs.python.org/3/library/itertools.html#itertools.accumulate),
        this method enforces an explicit initial state and binary function;
        it also *does not* yield the initial state before consuming any element.
        This is also consistent with the [:python `numpy.ufunc.accumulate`](https://numpy.org/doc/stable/reference/generated/numpy.ufunc.accumulate.html#numpy.ufunc.accumulate) behavior.
        Also check [`Iterator.scan`][apfel.core.iter.Iterator.scan] for a method that provides more generalized state control.

        ```python
        iterator = itrt([1, 2, 3, 4])
        result = iterator.accumulate(0, lambda acc, x: acc + x)
        assert result.next().unwrap() == 1
        assert result.next().unwrap() == 3
        assert result.next().unwrap() == 6
        assert result.next().unwrap() == 10
        assert result.next().is_nothing()
        ```
        """
        return IteratorAdaptor(
            _itertools.islice(_itertools.accumulate(self, func, initial=state), 1, None)
        )

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
        i = 0
        try:
            for i in range(n):
                next(self)
            return _result.Result.make_ok(None)
        except StopIteration:
            return _result.Result.make_err(n - i)

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

    def chain(self, *others):
        """
        Creates a new iterator that yields elements from this iterator until it is exhausted,
        then yields elements from the `other` iterator.

        ```python
        iterator1 = itrt([1, 2])
        iterator2 = itrt([3, 4])
        iterator3 = itrt([5, 6])
        chained_iterator = iterator1.chain(iterator2, iterator3)

        assert chained_iterator.next().unwrap() == 1
        assert chained_iterator.next().unwrap() == 2
        assert iterator1.next().is_nothing()  # original iterator1 is also exhausted
        assert chained_iterator.next().unwrap() == 3
        assert chained_iterator.next().unwrap() == 4
        assert iterator2.next().is_nothing()  # original iterator2 is also exhausted
        assert chained_iterator.next().unwrap() == 5
        assert chained_iterator.next().unwrap() == 6
        assert chained_iterator.next().is_nothing()
        ```
        """
        return IteratorAdaptor(_itertools.chain(self, *others))

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

    def enumerate(self, init: int = 0):
        """
        Creates a new iterator that yields tuples of (index, element) pairs,
        where index starts from 0 or the specified `init` value.

        Args:
            init (int): The starting index for enumeration. Default is 0.

        ```python
        iterator = itrt(['a', 'b', 'c'])
        enumerated_iterator = iterator.enumerate()
        assert enumerated_iterator.next().unwrap() == (0, 'a')
        assert enumerated_iterator.next().unwrap() == (1, 'b')
        assert enumerated_iterator.next().unwrap() == (2, 'c')
        assert enumerated_iterator.next().is_nothing()
        ```
        """
        return IteratorAdaptor(builtins.enumerate(self, init))

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

    def filter_map(self, pred, /):
        """
        Creates a new iterator that applies `pred` to each element and yields the unwrapped
        value for each result that is a [`Just`][apfel.container.maybe.Maybe], skipping `Nothing`.

        ```python
        from apfel.container.maybe import Maybe

        def try_parse(s):
            try:
                return Maybe.make_just(int(s))
            except ValueError:
                return Maybe.make_nothing()

        iterator = itrt(["1", "two", "3", "four"])
        filtered = iterator.filter_map(try_parse)
        assert filtered.next().unwrap() == 1
        assert filtered.next().unwrap() == 3
        assert filtered.next().is_nothing()
        ```
        """

        def _gen():
            for item in self:
                result = pred(item)
                if result.is_just():
                    yield result.unwrap()

        return IteratorAdaptor(_gen())

    def find(self, pred, /):
        """
        Returns the first element in the iterator that satisfies the predicate `f`,
        wrapped in a [`Maybe`][apfel.container.maybe.Maybe].
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

    def find_map(self, pred, /):
        """
        Applies the function `pred` to each element of the iterator and returns the first
        result that is a [`Just`][apfel.container.maybe.Maybe], unwrapped.
        If no element produces a `Just`, returns `Nothing`.

        ```python
        from apfel import Maybe

        iterator = itrt(["lol", "NaN", "2", "5"])
        def try_parse(s):
            try:
                return Maybe.make_just(int(s))
            except ValueError:
                return Maybe.make_nothing()

        assert iterator.find_map(try_parse).unwrap() == 2
        ```
        """
        for item in self:
            result = pred(item)
            if result.is_just():
                return result
        return _maybe.Maybe.make_nothing()

    def flat_map(self, func, /):
        """
        Creates a new iterator that applies `func` to each element and flattens the results.
        Equivalent to `.map(func).flatten()`.

        ```python
        iterator = itrt([1, 2, 3])
        result = iterator.flat_map(lambda x: itrt([x, x * 10]))
        assert result.next().unwrap() == 1
        assert result.next().unwrap() == 10
        assert result.next().unwrap() == 2
        assert result.next().unwrap() == 20
        assert result.next().unwrap() == 3
        assert result.next().unwrap() == 30
        assert result.next().is_nothing()
        ```
        """
        return IteratorAdaptor(_itertools.chain.from_iterable(builtins.map(func, self)))

    def flatten(self: "_collections_abc.Iterable[Iterator[I]]") -> "Iterator[I]":
        """
        Flattens an iterable of iterators into a single iterator by yielding all elements
        from each inner iterator in sequence.

        ```python
        iterator = itrt([itrt([1, 2]), itrt([3, 4]), itrt([5])])
        flattened_iterator = iterator.flatten()
        assert flattened_iterator.next().unwrap() == 1
        assert flattened_iterator.next().unwrap() == 2
        assert flattened_iterator.next().unwrap() == 3
        assert flattened_iterator.next().unwrap() == 4
        assert flattened_iterator.next().unwrap() == 5
        assert flattened_iterator.next().is_nothing()
        assert iterator.next().is_nothing()  # original iterator is also exhausted
        ```
        """
        return IteratorAdaptor(_itertools.chain.from_iterable(self))

    def fold(self, init, func):
        """
        Fold (reduce) the elements of the iterator using the accumulation function `func`,
        starting with the initial value `init`.

        See also [`reduce`][apfel.core.iter.Iterator.reduce] if the first element of the iterator should be used as the initial accumulator value.

        Tip:
            The default implementation of this method uses [:python `functools.reduce`](https://docs.python.org/3/library/functools.html#functools.reduce)
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
        Compare to [`map`][apfel.core.iter.Iterator.map], the result of each function application is discarded,
          and the iterator is consumed eagerly.

        ```python
        iterator = itrt([1, 2, 3])
        iterator.for_each(lambda x: print(x, end=" "))
        # Output: 1 2 3
        ```
        """
        for item in self:
            func(item)

    def hint(self, hint, /):
        """
        Hints the type of items in the iterator for better type inference.
        This method does not affect runtime behavior.

        ```python
        iterator = itrt([1, 2, 3]).hint(int)
        assert iterator.next().unwrap() == 1
        ```
        """
        return self

    def intersperse(self, separator, /):
        """
        Creates a new iterator that places `separator` between adjacent elements.

        ```python
        iterator = itrt([1, 2, 3])
        result = iterator.intersperse(0)
        assert result.next().unwrap() == 1
        assert result.next().unwrap() == 0
        assert result.next().unwrap() == 2
        assert result.next().unwrap() == 0
        assert result.next().unwrap() == 3
        assert result.next().is_nothing()

        assert itrt([]).intersperse(0).next().is_nothing()
        assert itrt([1]).intersperse(0).next().unwrap() == 1
        ```
        """

        def _gen():
            first = True
            for item in self:
                if not first:
                    yield separator
                first = False
                yield item

        return IteratorAdaptor(_gen())

    def intersperse_with(self, sep_fn, /):
        """
        Creates a new iterator that places the value returned by `sep_fn` between adjacent elements.
        `sep_fn` is called once for each separator inserted.

        ```python
        iterator = itrt([1, 2, 3])
        result = iterator.intersperse_with(lambda: 0)
        assert result.next().unwrap() == 1
        assert result.next().unwrap() == 0
        assert result.next().unwrap() == 2
        assert result.next().unwrap() == 0
        assert result.next().unwrap() == 3
        assert result.next().is_nothing()

        n = 0
        def counter():
            nonlocal n
            n += 1
            return n
        result = itrt(['a', 'b', 'c']).intersperse_with(counter)
        assert list(result) == ['a', 1, 'b', 2, 'c']
        ```
        """

        def _gen():
            first = True
            for item in self:
                if not first:
                    yield sep_fn()
                first = False
                yield item

        return IteratorAdaptor(_gen())

    def last(self):
        """
        Returns the last element of the iterator, wrapped in a [`Maybe`][apfel.container.maybe.Maybe].
        If the iterator is empty, returns `Nothing`.

        ```python
        iterator = itrt([1, 2, 3, 4, 5])
        assert iterator.last().unwrap() == 5
        assert iterator.next().is_nothing()  # iterator is exhausted

        iterator = itrt([])
        assert iterator.last().is_nothing()
        ```
        """
        global _sentinal_iterator_last, _func_iterator_last
        last = _functools.reduce(_func_iterator_last, self, _sentinal_iterator_last)
        return (
            _maybe.Maybe.make_just(last)
            if last is not _sentinal_iterator_last
            else _maybe.Maybe.make_nothing()
        )

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

    def map_while(self, pred, /):
        """
        Creates a new iterator that applies `pred` to each element and yields the unwrapped
        value while the result is a [`Just`][apfel.container.maybe.Maybe].
        Once `pred` returns `Nothing`, iteration stops immediately.

        ```python
        from apfel.container.maybe import just, nothing

        def checked_double(x):
            if x < 4:
                return just(x * 2)
            return nothing()

        iterator = itrt([1, 2, 3, 4, 5])
        result = iterator.map_while(checked_double)
        assert result.next().unwrap() == 2
        assert result.next().unwrap() == 4
        assert result.next().unwrap() == 6
        assert result.next().is_nothing()
        ```
        """

        def _gen():
            for item in self:
                result = pred(item)
                if result.is_nothing():
                    return
                yield result.unwrap()

        return IteratorAdaptor(_gen())

    def nth(self, n: int, /):
        """
        Returns the `n`-th element of the iterator (0-indexed), wrapped in a [`Maybe`][apfel.container.maybe.Maybe].
        If the iterator has fewer than `n + 1` elements, returns `Nothing`.

        Note:
            This method consumes the first `n + 1` elements of the iterator.

        ```python
        iterator = itrt([1, 2, 3, 4, 5])
        assert iterator.nth(2).unwrap() == 3  # gets index 2 (third element)
        assert iterator.next().unwrap() == 4  # continues from after nth element

        iterator = itrt([1, 2])
        assert iterator.nth(5).is_nothing()  # not enough elements
        ```
        """
        try:
            return _maybe.Maybe.make_just(next(_itertools.islice(self, n, None)))
        except StopIteration:
            return _maybe.Maybe.make_nothing()

    def pipe(self, func, *args, **kwargs):
        """
        Pipes the iterator into the function `func`, passing any additional positional and keyword arguments.
        This allows for chaining operations in a functional style.

        ```python
        iterator = itrt([1, 2, 3, 4, 5])
        result = iterator.pipe(sum, start=10)
        assert result == 25  # 10 + 1 + 2 + 3 + 4 + 5

        iterator = itrt([1, 2, 3])
        result = iterator.pipe(max)
        assert result == 3

        iterator = itrt([1, 2, 3, 4])
        result = iterator.map(str).pipe("-".join)
        assert result == "1-2-3-4"
        ```
        """
        return func(self, *args, **kwargs)

    def position(self, pred, /):
        """
        Returns the index of the first element in the iterator that satisfies the predicate `pred`,
        wrapped in a [`Maybe`][apfel.container.maybe.Maybe].
        If no such element is found, returns `Nothing`.

        ```python
        iterator = itrt([1, 2, 3, 4, 5])
        assert iterator.position(lambda x: x % 2 == 0).unwrap() == 1
        assert iterator.next().unwrap() == 3  # 1, 2 have been consumed

        iterator = itrt([1, 2, 3])
        assert iterator.position(lambda x: x > 10).is_nothing()
        assert iterator.next().is_nothing()  # iterator is exhausted
        ```
        """
        for i, item in builtins.enumerate(self):
            if pred(item):
                return _maybe.Maybe.make_just(i)
        return _maybe.Maybe.make_nothing()

    def reduce(self, func, /):
        """
        Reduce the elements of the iterator using the accumulation function `func` and returns a [`Maybe`][apfel.container.maybe.Maybe].
        The first element of the iterator is used as the initial accumulator value.
        If the iterator is empty, returns `Nothing`.

        See also [`fold`][apfel.core.iter.Iterator.fold] if an explicit initial value is needed.

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

    def scan(self, state, func):
        """
        Creates a new iterator that holds internal state, applying `func` to each element.
        `func` receives `state` and an element, and returns a
        [`Maybe`][apfel.container.maybe.Maybe]. Yields the unwrapped value while `func`
        returns `Just`; stops on `Nothing`.

        `state` is passed directly to `func` each iteration — pass a mutable container
        such as [`Value`][apfel.container.value.Value] if `func` needs to update it across iterations.

        ```python
        from apfel.container.maybe import just, nothing
        from apfel.container.value import Value
        from apfel.core.common import imperative

        state = Value(1)
        iterator = itrt([1, 2, 3, 4])
        result = iterator.scan(state, lambda s, x: imperative(
            s.update(lambda v: v * x),
            nothing() if s.done() > 6 else just(-s.done()),
        ))
        assert result.next().unwrap() == -1
        assert result.next().unwrap() == -2
        assert result.next().unwrap() == -6
        assert result.next().is_nothing()
        ```
        """

        def _gen():
            for item in self:
                result = func(state, item)
                if result.is_nothing():
                    return
                yield result.unwrap()

        return IteratorAdaptor(_gen())

    def skip(self, n: int, /):
        """
        Creates a new iterator that skips the first `n` elements of the original iterator.
        If the original iterator has fewer than `n` elements, all elements are skipped.

        Args:
            n (int): The number of elements to skip from the start of the iterator.

        Raises:
            ValueError: If `n` is negative.

        ```python
        iterator = itrt([1, 2, 3, 4, 5])
        skipped_iterator = iterator.skip(2)
        assert skipped_iterator.next().unwrap() == 3
        assert skipped_iterator.next().unwrap() == 4
        assert skipped_iterator.next().unwrap() == 5
        assert skipped_iterator.next().is_nothing()
        assert iterator.next().is_nothing()  # original iterator is also exhausted
        ```
        """
        if n < 0:
            raise ValueError("n must be non-negative")
        return IteratorAdaptor(_itertools.islice(self, n, None))

    def skip_while(self, pred, /):
        """
        Creates a new iterator that skips elements while the predicate `pred` returns `True`.
        Once the predicate returns `False`, all remaining elements are yielded.

        ```python
        iterator = itrt([1, 2, 3, 4, 1, 2])
        skipped_iterator = iterator.skip_while(lambda x: x < 4)
        assert skipped_iterator.next().unwrap() == 4
        assert skipped_iterator.next().unwrap() == 1
        assert skipped_iterator.next().unwrap() == 2
        assert skipped_iterator.next().is_nothing()
        ```
        """
        return IteratorAdaptor(_itertools.dropwhile(pred, self))

    def step_by(self, n: int, /):
        """
        Creates a new iterator that yields every `n`-th element of the original iterator.
        The first element (index 0) is always yielded.
        It does not guarantee the skipped elements are consumed before or after yielding the next element.

        ```python
        iterator = itrt([1, 2, 3, 4, 5, 6, 7, 8])
        stepped_iterator = iterator.step_by(2)
        assert stepped_iterator.next().unwrap() == 1
        assert stepped_iterator.next().unwrap() == 3
        assert stepped_iterator.next().unwrap() == 5
        assert stepped_iterator.next().unwrap() == 7
        assert stepped_iterator.next().is_nothing()
        ```
        """
        return IteratorAdaptor(_itertools.islice(self, 0, None, n))

    def take(self, n: int, /):
        """
        Creates a new iterator that stops after the first `n` elements of the original iterator.
        If the original iterator has fewer than `n` elements, all elements are yielded.

        Args:
            n (int): The number of elements to take from the start of the iterator.

        Raises:
            ValueError: If `n` is negative.

        ```python
        iterator = itrt([1, 2, 3, 4, 5])
        taken_iterator = iterator.take(3)
        assert taken_iterator.next().unwrap() == 1
        assert taken_iterator.next().unwrap() == 2
        assert taken_iterator.next().unwrap() == 3
        assert taken_iterator.next().is_nothing()
        assert iterator.next().unwrap() == 4  # original iterator continues from where take stopped
        ```
        """
        if n < 0:
            raise ValueError("n must be non-negative")
        return IteratorAdaptor(_itertools.islice(self, n))

    def tap(self, func, /):
        """
        Creates a new iterator that calls `func` on each element for side effects,
        passing the element through unchanged.

        ```python
        result = []
        iterator = itrt([1, 2, 3])
        tapped = iterator.tap(result.append)
        assert tapped.next().unwrap() == 1
        assert result == [1]
        assert tapped.next().unwrap() == 2
        assert result == [1, 2]
        assert tapped.next().unwrap() == 3
        assert result == [1, 2, 3]
        assert tapped.next().is_nothing()
        ```
        """

        def _gen():
            for item in self:
                func(item)
                yield item

        return IteratorAdaptor(_gen())

    def take_while(self, pred, /):
        """
        Creates a new iterator that yields elements while the predicate `pred` returns `True`.
        Once the predicate returns `False`, iteration stops.

        ```python
        iterator = itrt([1, 2, 3, 4, 1, 2])
        taken_iterator = iterator.take_while(lambda x: x < 4)
        assert taken_iterator.next().unwrap() == 1
        assert taken_iterator.next().unwrap() == 2
        assert taken_iterator.next().unwrap() == 3
        assert taken_iterator.next().is_nothing()
        assert iterator.next().unwrap() == 1  # elements after the predicate failed
        ```
        """
        return IteratorAdaptor(_itertools.takewhile(pred, self))

    def zip(self, *others):
        """
        Zips up this iterator with one or more other iterables into a single iterator of tuples.
        Iteration stops whenever an iterator or iterable is exhausted.

        The iterators are guaranteed to be consumed in the order they are passed in.

        Warning:
            The original iterators should not be pulled after being zipped together, as some
            of their elements may have been consumed and discarded during the zipping process.

        ```python
        iterator1 = itrt([1, 2, 3])
        iterator2 = itrt([4, 5, 6])
        zipped = iterator1.zip(iterator2)
        assert zipped.next().unwrap() == (1, 4)
        assert zipped.next().unwrap() == (2, 5)
        assert zipped.next().unwrap() == (3, 6)
        assert zipped.next().is_nothing()

        iterator1 = itrt([1, 2, 3])
        iterator2 = itrt(['a', 'b'])
        zipped = iterator1.zip(iterator2)
        assert zipped.next().unwrap() == (1, 'a')
        assert zipped.next().unwrap() == (2, 'b')
        assert zipped.next().is_nothing()
        assert iterator1.next().is_nothing() # 3 is consumed and discarded during zipping

        iterator = itrt([1, 2, 3])
        zipped = iterator.zip([4, 5, 6])
        assert zipped.next().unwrap() == (1, 4)
        assert zipped.next().unwrap() == (2, 5)
        assert zipped.next().unwrap() == (3, 6)
        assert zipped.next().is_nothing()
        ```
        """
        return IteratorAdaptor(builtins.zip(self, *others))


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
