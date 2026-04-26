import pytest
from apfel import identity
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

def test_iterator_chain():
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

def test_iterator_enumerate():
    iterator = itrt(['a', 'b', 'c'])
    enumerated_iterator = iterator.enumerate()
    assert enumerated_iterator.next().unwrap() == (0, 'a')
    assert enumerated_iterator.next().unwrap() == (1, 'b')
    assert enumerated_iterator.next().unwrap() == (2, 'c')
    assert enumerated_iterator.next().is_nothing()
    
    iterator = itrt(['a'])
    assert iterator.enumerate(1).next().unwrap() == (1, 'a')

def test_iterator_filter():
    iterator = itrt([1, 2, 3, 4, 5])
    filtered_iterator = iterator.filter(lambda x: x % 2 == 0)
    assert filtered_iterator.next().unwrap() == 2
    assert filtered_iterator.next().unwrap() == 4
    assert filtered_iterator.next().is_nothing()
    assert iterator.next().is_nothing()  # original iterator is also exhausted

def test_iterator_filter_map():
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

    iterator = itrt(["a", "b"])
    assert iterator.filter_map(try_parse).next().is_nothing()

    iterator = itrt([])
    assert iterator.filter_map(try_parse).next().is_nothing()

def test_iterator_find():
    iterator = itrt([1, 2, 3, 4, 5])
    assert iterator.find(lambda x: x % 2 == 0).unwrap() == 2
    assert iterator.find(lambda x: x <= 3).unwrap() == 3  # 1, 2 have been consumed
    assert iterator.find(lambda x: x > 10).is_nothing()  # no such element exists
    assert iterator.next().is_nothing()  # iterator is exhausted

def test_iterator_find_map():
    from apfel.container.maybe import Maybe

    def try_parse(s):
        try:
            return Maybe.make_just(int(s))
        except ValueError:
            return Maybe.make_nothing()

    iterator = itrt(["lol", "NaN", "2", "5"])
    assert iterator.find_map(try_parse).unwrap() == 2
    assert iterator.next().unwrap() == "5"  # "2" consumed, "5" remains

    iterator = itrt(["a", "b", "c"])
    assert iterator.find_map(try_parse).is_nothing()
    assert iterator.next().is_nothing()  # iterator is exhausted

    iterator = itrt([])
    assert iterator.find_map(try_parse).is_nothing()

def test_iterator_flat_map():
    iterator = itrt([1, 2, 3])
    result = iterator.flat_map(lambda x: [x, x * 10])
    assert result.next().unwrap() == 1
    assert result.next().unwrap() == 10
    assert result.next().unwrap() == 2
    assert result.next().unwrap() == 20
    assert result.next().unwrap() == 3
    assert result.next().unwrap() == 30
    assert result.next().is_nothing()

    iterator = itrt([[1, 2], [3], [4, 5]])
    result = iterator.flat_map(identity)
    assert result.next().unwrap() == 1
    assert result.next().unwrap() == 2
    assert result.next().unwrap() == 3
    assert result.next().unwrap() == 4
    assert result.next().unwrap() == 5
    assert result.next().is_nothing()

    iterator = itrt([])
    assert iterator.flat_map(lambda x: itrt([x])).next().is_nothing()

def test_iterator_flatten():
    iter1 = iter([1, 2])
    iter2 = itrt([3, 4])
    iter3 = iter([5, 6])
    nested_iterator = itrt([iter1, iter2, iter3])
    flattened_iterator = nested_iterator.flatten()

    assert flattened_iterator.next().unwrap() == 1
    assert flattened_iterator.next().unwrap() == 2
    assert flattened_iterator.next().unwrap() == 3
    assert flattened_iterator.next().unwrap() == 4
    assert flattened_iterator.next().unwrap() == 5
    assert flattened_iterator.next().unwrap() == 6
    assert flattened_iterator.next().is_nothing()

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

def test_iterator_hint():
    iterator = itrt([1, 2, 3])
    hinted_iterator = iterator.hint(int)
    assert hinted_iterator.next().unwrap() == 1
    assert hinted_iterator.next().unwrap() == 2
    assert hinted_iterator.next().unwrap() == 3
    assert hinted_iterator.next().is_nothing()
    assert iterator.next().is_nothing()  # original iterator is also exhausted

def test_iterator_last():
    iterator = itrt([1, 2, 3, 4, 5])
    assert iterator.last().unwrap() == 5
    assert iterator.next().is_nothing()  # iterator is exhausted

    iterator = itrt([])
    assert iterator.last().is_nothing()

def test_iterator_map():
    iterator = itrt([1, 2, 3])
    mapped_iterator = iterator.map(lambda x: x * 2)
    assert mapped_iterator.next().unwrap() == 2
    assert mapped_iterator.next().unwrap() == 4
    assert mapped_iterator.next().unwrap() == 6
    assert mapped_iterator.next().is_nothing()
    assert iterator.next().is_nothing()  # original iterator is also exhausted

def test_iterator_map_while():
    from apfel.container.maybe import Maybe

    def checked_double(x):
        if x < 4:
            return Maybe.make_just(x * 2)
        return Maybe.make_nothing()

    iterator = itrt([1, 2, 3, 4, 5])
    result = iterator.map_while(checked_double)
    assert result.next().unwrap() == 2
    assert result.next().unwrap() == 4
    assert result.next().unwrap() == 6
    assert result.next().is_nothing()

    iterator = itrt([4, 5, 6])
    result = iterator.map_while(checked_double)
    assert result.next().is_nothing()

    iterator = itrt([])
    assert iterator.map_while(checked_double).next().is_nothing()

    iterator = itrt([1, 2, 3])
    result = iterator.map_while(Maybe.make_just)
    assert result.next().unwrap() == 1
    assert result.next().unwrap() == 2
    assert result.next().unwrap() == 3
    assert result.next().is_nothing()

def test_iterator_nth():
    iterator = itrt([1, 2, 3, 4, 5])
    assert iterator.nth(2).unwrap() == 3
    assert iterator.next().unwrap() == 4
    
    iterator = itrt([1, 2])
    assert iterator.nth(5).is_nothing()

def test_iterator_pipe():
    iterator = itrt([1, 2, 3, 4, 5])
    result = iterator.pipe(sum, 10) # ty: ignore[no-matching-overload]
    assert result == 25  # 10 + 1 + 2 + 3 + 4 + 5

    iterator = itrt([1, 2, 3])
    result = iterator.pipe(max)
    assert result == 3

    iterator = itrt([1, 2, 3, 4])
    result = iterator.map(str).pipe("-".join)
    assert result == "1-2-3-4"

def test_iterator_position():
    iterator = itrt([1, 2, 3, 4, 5])
    assert iterator.position(lambda x: x % 2 == 0).unwrap() == 1
    assert iterator.next().unwrap() == 3  # 1, 2 have been consumed

    iterator = itrt([1, 2, 3])
    assert iterator.position(lambda x: x > 10).is_nothing()
    assert iterator.next().is_nothing()  # iterator is exhausted

    iterator = itrt([])
    assert iterator.position(lambda x: True).is_nothing()

    iterator = itrt([5, 3, 1])
    assert iterator.position(lambda x: x == 5).unwrap() == 0  # first element matches

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

def test_iterator_skip():
    iterator = itrt([1, 2, 3, 4, 5])
    skipped_iterator = iterator.skip(2)
    assert skipped_iterator.next().unwrap() == 3
    assert skipped_iterator.next().unwrap() == 4
    assert skipped_iterator.next().unwrap() == 5
    assert skipped_iterator.next().is_nothing()
    assert iterator.next().is_nothing()
    
    iterator = itrt([1, 2])
    skipped_iterator = iterator.skip(5)
    assert skipped_iterator.next().is_nothing()
    assert iterator.next().is_nothing()
    
    with pytest.raises(ValueError):
        iterator = itrt([1, 2, 3])
        skipped_iterator = iterator.skip(-1)

def test_iterator_skip_while():
    iterator = itrt([1, 2, 3, 4, 1, 2])
    skipped_iterator = iterator.skip_while(lambda x: x < 4)
    assert skipped_iterator.next().unwrap() == 4
    assert skipped_iterator.next().unwrap() == 1
    assert skipped_iterator.next().unwrap() == 2
    assert skipped_iterator.next().is_nothing()

def test_iterator_step_by():
    iterator = itrt([1, 2, 3, 4, 5, 6, 7, 8])
    stepped_iterator = iterator.step_by(2)
    assert stepped_iterator.next().unwrap() == 1
    assert stepped_iterator.next().unwrap() == 3
    assert stepped_iterator.next().unwrap() == 5
    assert stepped_iterator.next().unwrap() == 7
    assert stepped_iterator.next().is_nothing()
    assert iterator.next().is_nothing()  # original iterator is also exhausted
    
    iterator = itrt([10, 20, 30])
    stepped_iterator = iterator.step_by(3)
    assert stepped_iterator.next().unwrap() == 10
    assert stepped_iterator.next().is_nothing()
    assert iterator.next().is_nothing()  # original iterator is also exhausted

    with pytest.raises(ValueError):
        iterator = itrt([1, 2, 3])
        stepped_iterator = iterator.step_by(0)

def test_iterator_take():
    iterator = itrt([1, 2, 3, 4, 5])
    taken_iterator = iterator.take(3)
    assert taken_iterator.next().unwrap() == 1
    assert taken_iterator.next().unwrap() == 2
    assert taken_iterator.next().unwrap() == 3
    assert taken_iterator.next().is_nothing()
    assert iterator.next().unwrap() == 4  # original iterator continues from where take stopped

    iterator = itrt([1, 2])
    taken_iterator = iterator.take(5)
    assert taken_iterator.next().unwrap() == 1
    assert taken_iterator.next().unwrap() == 2
    assert taken_iterator.next().is_nothing()
    assert iterator.next().is_nothing()  # original iterator is also exhausted
    
    with pytest.raises(ValueError):
        iterator = itrt([1, 2, 3])
        taken_iterator = iterator.take(-1)

def test_iterator_take_while():
    iterator = itrt([2, 4, 6, 7, 8])
    taken_iterator = iterator.take_while(lambda x: x % 2 == 0)
    assert taken_iterator.next().unwrap() == 2
    assert taken_iterator.next().unwrap() == 4
    assert taken_iterator.next().unwrap() == 6
    assert taken_iterator.next().is_nothing()
    assert iterator.next().unwrap() == 8  # original iterator continues from where take_while stopped

    iterator = itrt([1, 3, 5])
    taken_iterator = iterator.take_while(lambda x: x % 2 == 0)
    assert taken_iterator.next().is_nothing()
    assert iterator.next().unwrap() == 3 # original iterator is shifted once

def test_iterator_tap():
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

    counts = []
    tapped = itrt([10, 20, 30]).tap(counts.append).map(lambda x: x * 2)
    assert list(tapped) == [20, 40, 60]
    assert counts == [10, 20, 30]

    assert itrt([]).tap(lambda x: None).next().is_nothing()

def test_iterator_zip():
    iterator1 = itrt([1, 2, 3])
    iterator2 = itrt([4, 5, 6])
    zipped = iterator1.zip(iterator2)
    assert zipped.next().unwrap() == (1, 4)
    assert zipped.next().unwrap() == (2, 5)
    assert zipped.next().unwrap() == (3, 6)
    assert zipped.next().is_nothing()

    iterator1 = itrt([1, 2, 3])
    iterator2 = itrt([4, 5])
    zipped = iterator1.zip(iterator2)
    assert zipped.next().unwrap() == (1, 4)
    assert zipped.next().unwrap() == (2, 5)
    assert zipped.next().is_nothing()
    assert iterator1.next().is_nothing()  # original iterator1 is also exhausted

    iterator1 = itrt([1, 2, 3])
    iterator2 = itrt([4, 5, 6, 7])
    zipped = iterator1.zip(iterator2)
    assert zipped.next().unwrap() == (1, 4)
    assert zipped.next().unwrap() == (2, 5)
    assert zipped.next().unwrap() == (3, 6)
    assert zipped.next().is_nothing()
    assert iterator1.next().is_nothing()  # original iterator1 is also exhausted
    assert iterator2.next().unwrap() == 7  # original iterator2 continues from where zip stopped

    iterator = itrt([1, 2, 3])
    zipped = iterator.zip([4, 5, 6])
    assert zipped.next().unwrap() == (1, 4)
    assert zipped.next().unwrap() == (2, 5)
    assert zipped.next().unwrap() == (3, 6)
    assert zipped.next().is_nothing()

    iterator = itrt([1, 2, 3])
    zipped = iterator.zip([4, 5, 6], [7, 8, 9])
    assert zipped.next().unwrap() == (1, 4, 7)
    assert zipped.next().unwrap() == (2, 5, 8)
    assert zipped.next().unwrap() == (3, 6, 9)
    assert zipped.next().is_nothing()

    iterator = itrt([])
    assert iterator.zip([1, 2, 3]).next().is_nothing()