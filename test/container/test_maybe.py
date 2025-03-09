from typing import Any
from weakref import ref
from apfel.container.maybe import Maybe, just, nothing, some
import pytest

def fail():
    assert False

def test_maybe_match_stmt():
    j = just(1)
    n = nothing()

    assert type(j) is Maybe[int]
    assert type(n) is Maybe[Any]

    # not a subclass
    assert type(j) is not just
    assert type(n) is not nothing

    match j:
        case just(x):
            assert x == 1
        case nothing():
            assert False

    match n:
        case just(x):
            assert False
        case nothing():
            assert True

def test_maybe_constructor_just():
    j1 = Maybe.just(1)
    assert j1.is_just()

    j2 = just(1)
    assert j2.is_just()

    assert j1 == j2

    jn = just(None)
    assert jn.is_just()

def test_maybe_constructor_nothing():
    n1 = Maybe.nothing()
    assert n1.is_nothing()

    n2 = nothing()
    assert n2.is_nothing()

    assert n1 == n2

def test_maybe_constructor_some():
    j = Maybe.some(1)
    assert j.is_just()

    j = some(1)
    assert j.is_just()

    n = Maybe.some(None)
    assert n.is_nothing()

    n = some(None)
    assert n.is_nothing()

def test_maybe_constructor_duplicate():
    j = just(42)
    n = nothing()

    j1 = Maybe.duplicate(j)
    assert j1 is not j

    n1 = Maybe.duplicate(n)
    assert n1 is not n

def test_maybe_method_and():
    j1 = just[int](42)
    j2 = just[bool](True)

    assert j1.and_(j2).unwrap()
    assert j1.and_(nothing[bool]()).is_nothing()
    assert nothing[int]().and_(j2).is_nothing()

    assert (j1 & j2).unwrap()
    assert (j1 & nothing[bool]()).is_nothing()
    assert (nothing[int]() & j2).is_nothing()

    j1 = just(1)
    j2 = just(2)
    n = nothing()

    assert j1.and_(j2) == j2
    assert j1.and_(n).is_nothing()
    assert j1.and_(n) is not n

    assert n.and_(j1).is_nothing()
    assert n.and_(j1) is not n

    assert n.and_(n).is_nothing()
    assert n.and_(n) is not n

def test_maybe_method_and_then():
    j = just[int](114514)

    assert j.and_then(lambda x: some(x + 1805296)).unwrap() == 1919810
    assert j.and_then(lambda x: nothing()).is_nothing()

    n = nothing[int]()
    assert n.and_then(lambda x: some(x + 1805296)).is_nothing()
    assert n.and_then(lambda x: fail()).is_nothing()

def test_maybe_method_apply():
    from collections.abc import Callable
    j = just[int](42)
    f = just[Callable[[int], str]](str)

    assert j.apply(f).unwrap() == '42'
    assert nothing[int]().apply(f).is_nothing()
    assert j.apply(nothing[Callable[[int], str]]()).is_nothing()
    assert nothing[int]().apply(nothing[Callable[[int], str]]()).is_nothing()

def test_maybe_method_bind():
    """
    The `bind` method is the same as `and_then`.
    """
    j = just[int](114514)

    assert j.bind(lambda x: some(x + 1805296)).unwrap() == 1919810
    assert j.bind(lambda x: nothing()).is_nothing()

    n = nothing[int]()
    assert n.bind(lambda x: some(x + 1805296)).is_nothing()
    assert n.bind(lambda x: nothing()).is_nothing()

def test_maybe_method_bool():
    assert just(1)
    assert not nothing()

def test_maybe_method_eq():
    assert just(1) == just(1)
    assert not just(1) == nothing()
    assert not nothing() == just(1)
    assert nothing() == nothing()

    assert not nothing() == False # noqa: E712
    assert not nothing() == None # noqa: E711

def test_maybe_method_expect():
    j = just(1)
    assert j.expect('error') == 1

    n = nothing()
    try:
        n.expect('error')
    except ValueError as e:
        assert str(e) == 'error'

def test_maybe_method_filter():
    j = just[int](42)
    assert j.filter(lambda x: x > 0).unwrap() == 42
    assert j.filter(lambda x: x < 0).is_nothing()

    j = just(1)
    assert j.filter(lambda x: x == 1) == j
    assert j.filter(lambda x: x == 2).is_nothing()

    n = nothing()
    assert n.filter(lambda x: x == 1).is_nothing()
    assert n.filter(lambda x: fail()).is_nothing()

def test_maybe_method_flatten():
    j = just[Maybe[int]](just(42))
    assert j.flatten() == just(42)

    j2 = just[Maybe[Maybe[int]]](just(just(42)))
    assert j2.flatten() == just(just(42))
    assert j2.flatten().flatten() == just(42)

    n = just[Maybe[int]](nothing())
    assert n.flatten().is_nothing()

    noop = just(42)
    assert noop.flatten() == just(42)

def test_maybe_method_get_or_insert():
    j = just[int](42)
    assert j.get_or_insert(114514) == 42
    assert j == just(42)

    n = nothing[int]()
    assert n.get_or_insert(114514) == 114514
    assert n == just(114514)

def test_maybe_method_get_or_insert_with():
    j = just[int](42)
    assert j.get_or_insert_with(lambda: 114514) == 42
    assert j.get_or_insert_with(lambda: fail()) == 42
    assert j == just(42)

    n = nothing[int]()
    assert n.get_or_insert_with(lambda: 114514) == 114514
    assert n == just(114514)

def test_maybe_method_hash():
    assert hash(just(1)) == hash(just(1))
    assert hash(just(1)) != hash(just(2))
    assert hash(nothing()) == hash(nothing())

def test_maybe_method_insert():
    j = just[int](42)
    assert j.insert(114514) == 114514
    assert j == just(114514)

    n = nothing[int]()
    assert n.insert(114514) == 114514
    assert n == just(114514)

def test_maybe_method_is_just():
    assert just(1).is_just()
    assert not nothing().is_just()

def test_maybe_method_is_just_and():
    j = just(42)
    assert j.is_just_and(lambda x: x == 42)
    assert not j.is_just_and(lambda x: x == 43)
    assert not nothing().is_just_and(lambda x: x == 42)
    assert not nothing().is_just_and(lambda x: fail())

def test_maybe_method_is_nothing():
    assert not just(1).is_nothing()
    assert not just(None).is_nothing()
    assert nothing().is_nothing()

def test_maybe_method_len():
    assert len(just(1)) == 1
    assert len(nothing()) == 0

def test_maybe_method_map():
    j = just[int](42)
    assert j.map(lambda x: x + 1) == just(43)

    n = nothing[int]()
    assert n.map(lambda x: x + 1) == nothing()

    n = nothing()
    assert n.map(lambda _: fail()) == nothing()

def test_maybe_method_map_or():
    j = just[int](42)
    n = nothing[int]()

    assert j.map_or(0, lambda x: x + 1) == 43
    assert n.map_or(0, lambda x: x + 1) == 0
    assert n.map_or(0, lambda x: fail()) == 0

def test_maybe_method_map_or_else():
    j = just[int](42)
    n = nothing[int]()

    assert j.map_or_else(lambda: 0, lambda x: x + 1) == 43
    assert n.map_or_else(lambda: 0, lambda x: x + 1) == 0
    assert j.map_or_else(lambda: fail(), lambda x: x + 1) == 43
    assert n.map_or_else(lambda: 0, lambda x: fail()) == 0

def test_maybe_method_or():
    j1 = just[int](42)
    j2 = just[int](114514)

    or_1 = j1.or_(j2)
    or_2 = j1.or_(nothing[int]())
    or_3 = nothing[int]().or_(j2)

    assert or_1.unwrap() == 42
    assert or_2.unwrap() == 42
    assert or_3.unwrap() == 114514

    assert or_1 is not j1
    assert or_2 is not j1
    assert or_3 is not j2

    assert j1 | j2 == j1

def test_maybe_method_or_else():
    j = just[int](42)
    n = nothing[int]()

    jo = j.or_else(lambda: fail())
    no = n.or_else(lambda: just(1))

    assert jo is not j
    assert jo.unwrap() == 42
    assert no.unwrap() == 1

def test_pure():
    assert Maybe.pure(1) == just(1)

def test_maybe_method_replace():
    j = just[int](42)
    old = j.replace(114514)
    assert j == just(114514)
    assert old == just(42)

    n = nothing[int]()
    old = n.replace(1919810)
    assert n == just(1919810)
    assert old == nothing()

def test_maybe_method_take():
    j = just[int](42)
    out = j.take()
    assert j.is_nothing()
    assert out == just(42)

    j = just(42)
    assert j.take() == just(42)
    assert j == nothing()

    n = nothing()
    assert n.take() == nothing()
    assert n == nothing()

def test_maybe_method_take_if():
    j = just[int](42)
    out = j.take_if(lambda x: x > 0)
    assert j.is_nothing()
    assert out == just(42)

    j = just[int](42)
    out = j.take_if(lambda x: x < 0)
    assert j.is_just()
    assert out == nothing()

def test_tap(capfd):
    just(42).tap(print)
    out, _ = capfd.readouterr()
    assert out == '42\n'

    nothing().tap(print)
    out, _ = capfd.readouterr()
    assert out == ''

def test_maybe_method_unwrap():
    assert just(42).unwrap() == 42
    assert just(None).unwrap() is None

    with pytest.raises(ValueError):
        nothing().unwrap()

def test_maybe_method_unwrap_or():
    j = just[int](42)
    n = nothing[int]()
    assert j.unwrap_or(0) == 42
    assert n.unwrap_or(0) == 0

def test_maybe_method_unwrap_or_else():
    j = just[int](42)
    n = nothing[int]()
    assert j.unwrap_or_else(lambda: fail()) == 42
    assert n.unwrap_or_else(lambda: 0) == 0

def test_maybe_method_unwrap_unchecked():
    assert just(42).unwrap_unchecked() == 42

def test_maybe_method_xor():
    j1 = just(1)
    j2 = just(2)
    n = nothing()

    assert j1.xor(j2) == n
    
    assert j1.xor(n) == j1
    assert j1.xor(n) is not j1

    assert n.xor(j1) == j1
    assert n.xor(j1) is not j1
    
    assert n.xor(n) == n
    assert n.xor(n) is not n

def test_maybe_method_zip():
    j1 = just[int](42)
    j2 = just[int](114514)
    assert j1.zip().unwrap() == (42, )
    assert j1.zip(j2).unwrap() == (42, 114514)

    n = nothing[int]()
    assert j1.zip(n).is_nothing()
    assert n.zip(j1).is_nothing()
