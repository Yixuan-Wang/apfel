import pytest

from apfel.core.iter import Iterator, itrt


def test_iter_dispatch():
    iterator = iter([1, 2, 3])
    assert Iterator.next(iterator).unwrap() == 1
    assert next(iterator) == 2
    assert Iterator.next(iterator).unwrap() == 3
    assert Iterator.next(iterator).is_nothing()


def test_iterator_next():
    iterator = itrt([1, 2, 3])

    assert iterator.next().unwrap() == 1
    assert iterator.next().unwrap() == 2
    assert iterator.next().unwrap() == 3
    assert iterator.next().is_nothing()


def test_iterator_advance_by():
    iterator = itrt([1, 2, 3, 4, 5])
    assert iterator.advance_by(2).is_ok()
    assert iterator.next().unwrap() == 3
    assert iterator.advance_by(6).unwrap_err() == 4


def test_iterator_all():
    iterator = itrt([2, 4, 6])
    assert iterator.all(lambda x: x % 2 == 0)
    assert iterator.next().is_nothing()

    iterator = itrt([2, 3, 6])
    assert not iterator.all(lambda x: x % 2 == 0)
    assert iterator.next().unwrap() == 6


def test_iterator_any():
    iterator = itrt([1, 3, 5])
    assert not iterator.any(lambda x: x % 2 == 0)
    assert iterator.next().is_nothing()

    iterator = itrt([1, 2, 3])
    assert iterator.any(lambda x: x % 2 == 0)
    assert iterator.next().unwrap() == 3


def test_iterator_count():
    iterator = itrt([10, 20, 30, 40])
    assert iterator.count() == 4
    assert iterator.next().is_nothing()

def test_iterator_eq():
    iterator1 = itrt([1, 2, 3])
    iterator2 = itrt([1, 2, 3])
    assert iterator1.eq(iterator2)

    iterator1 = itrt([1, 2, 3])
    iterator3 = itrt([1, 2, 4])
    assert not iterator1.eq(iterator3)

    iterator1 = itrt([1, 2, 3])
    iterator4 = itrt([1, 2])
    assert not iterator1.eq(iterator4)

    iterator1 = itrt([1, 2, 3, 4])
    iterator5 = itrt([1, 2, 3])
    assert not iterator1.eq(iterator5)

    iterator1 = itrt([1, 2, 3])
    iterator2 = itrt([1, 2, 3])
    assert iterator1 == iterator2

    iterator1 = itrt([1, 2, 3])
    iterator3 = itrt([1, 2, 4])
    assert iterator1 != iterator3

    iterator1 = itrt([1, 2, 3])
    iterator4 = itrt([1, 2])
    assert iterator1 != iterator4

    iterator1 = itrt([1, 2, 3])
    raw_iterator2 = iter([1, 2, 3])
    assert iterator1.eq(raw_iterator2)

    iterator1 = itrt([1, 2, 3])
    raw_iterator2 = iter([1, 2, 3])
    assert raw_iterator2 == iterator1

    iterator1 = itrt([1, 2, 3])
    lst = [1, 2, 3]
    assert iterator1 != lst

def test_iterator_find():
    iterator = itrt([1, 2, 3, 4, 5])
    assert iterator.find(lambda x: x % 2 == 0).unwrap() == 2
    assert iterator.find(lambda x: x <= 3).unwrap() == 3  # 1, 2 have been consumed
    assert iterator.find(lambda x: x > 10).is_nothing()  # no such element exists
    assert iterator.next().is_nothing()  # iterator is exhausted

def test_iterator_fold():
    iterator = itrt([1, 2, 3, 4, 5])
    result = iterator.fold(0, lambda acc, x: acc + x)
    assert result == 15
    assert iterator.next().is_nothing()  # iterator is exhausted

    iterator = itrt([])
    result = iterator.fold(10, lambda acc, x: acc + x)
    assert result == 10

def test_iterator_for_each(capsys):
    iterator = itrt([1, 2, 3])
    result = []
    iterator.for_each(lambda x: result.append(x * 2))
    assert result == [2, 4, 6]
    assert iterator.next().is_nothing()  # iterator is exhausted

    iterator = itrt([1, 2, 3, 4, 5])
    iterator.for_each(print)
    captured = capsys.readouterr()
    assert captured.out == "1\n2\n3\n4\n5\n"
    assert iterator.next().is_nothing()  # iterator is exhausted

def test_iterator_reduce():
    iterator = itrt([1, 2, 3, 4, 5])
    result = iterator.reduce(lambda acc, x: acc + x)
    assert result.unwrap() == 15
    assert iterator.next().is_nothing()  # iterator is exhausted

    iterator = itrt([42])
    result = iterator.reduce(lambda acc, x: acc + x)
    assert result.unwrap() == 42
    assert iterator.next().is_nothing()  # iterator is exhausted

    iterator = itrt([])
    result = iterator.reduce(lambda acc, x: acc + x)
    assert result.is_nothing()  # no elements to reduce