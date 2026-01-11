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
    | `filter`             | :material-close-circle: |
    | `filter_map`         | :material-close-circle: |
    | `find`               | :material-close-circle: |
    | `find_map`           | :material-close-circle: |
    | `flat_map`           | :material-close-circle: |
    | `flatten`            | :material-close-circle: |
    | `fold`               | :material-close-circle: |
    | `for_each`           | :material-close-circle: |
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
    | `map`                | :material-close-circle: |
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
    | `reduce`             | :material-close-circle: |
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

import collections.abc as _collections_abc

from ._iterator import Iterator


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


def itrt(it):
    """
    Create an `Iterator` from a standard Python `Iterator` or `Iterable`.

    Args:
        it: A Python standard `collections.abc.Iterator` or `collections.abc.Iterable`.

    Returns:
        An iterator that guarantees the apfel `Iterator` interface.

    Raises:
        TypeError: If the input is neither an `Iterator` nor an `Iterable`.
    """
    if isinstance(it, Iterator):
        return it
    elif isinstance(it, _collections_abc.Iterator):
        return IteratorAdaptor(it)
    elif isinstance(it, _collections_abc.Iterable):
        iterator = iter(it)
        return IteratorAdaptor(iterator)
    else:
        raise TypeError(f"Cannot convert type {type(it)} to Iterator")


__all__ = ["Iterator", "itrt"]
