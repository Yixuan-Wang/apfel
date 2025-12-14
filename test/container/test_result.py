from typing import NoReturn, no_type_check
from apfel.container.result import Result, ok, err
import apfel.container.maybe as _maybe
from apfel.core.monad import Monad
import pytest

def test_make():
    a = Result[int, NoReturn].make_ok(10)
    b = Result[NoReturn, str].make_err("error")

    assert a.unwrap() == 10
    assert b.unwrap_err() == "error"

def test_and():
    result_1 = ok(1)
    result_2 = ok(2)
    result_err = err("error")

    assert (result_1.and_(result_2)).unwrap() == 2
    assert (result_1.and_(result_2)) is not result_2
    assert (result_1 & result_2).unwrap() == 2
    assert (result_1.and_(result_err)).is_err()
    assert (result_1 & result_err).is_err()
    assert (result_err.and_(result_1)).is_err()
    assert (result_err & result_1) is not result_err
    assert (result_err.and_(result_err)).is_err()
    assert (result_err & result_err) is not result_err

def test_and_then():
    result = ok(2)
    result_err = err("error")

    assert result.and_then(lambda x: ok(x * 3)).unwrap() == 6
    assert result.and_then(lambda x: err("failed")).unwrap_err() == "failed"
    assert result_err.and_then(lambda x: ok(x * 3)).unwrap_err() == "error"
    assert result_err.and_then(lambda x: ok(None)) is not result_err

    assert result.bind(lambda x: ok(x + 5)).unwrap() == 7
    assert Monad.bind(result, lambda x: err("failed")).unwrap_err() == "failed"  # type: ignore

def test_apply():
    result_func = ok(lambda x: x + 3)
    result_value = ok(7)
    result_err = err("error")

    assert result_value.apply(result_func).unwrap() == 10
    assert result_value.apply(err("failed")).unwrap_err() == "failed"
    assert result_err.apply(result_func).unwrap_err() == "error"
    assert result_err.apply(err("failed")).unwrap_err() == "error"

def test_done():
    a = ok[str](10)
    b = err[int]("error")

    assert a.done() == (10, None)
    assert b.done() == (None, "error")

def test_eq():
    a1 = ok[NoReturn](10)
    a2 = ok[NoReturn](10)
    a3 = ok[NoReturn](20)
    b1 = err[NoReturn]("error")
    b2 = err[NoReturn]("error")
    b3 = err[NoReturn]("different")

    assert a1 == a2
    assert a1 != a3
    assert b1 == b2
    assert b1 != b3
    assert a1 != b1

def test_err():
    result_ok = ok[int](10)
    result_err = err[str]("error")

    assert result_ok.err().is_nothing()
    assert result_err.err().unwrap() == "error"

def test_expect():
    a = ok[NoReturn](10)
    b = err[NoReturn]("error")

    assert a.expect("Should be ok") == 10

    with pytest.raises(ValueError) as excinfo:
        b.expect("Expected an error")
    assert excinfo.value.args[0] == "Expected an error"
    
    assert b.expect_err("Should be error") == "error"
    with pytest.raises(ValueError) as excinfo:
        a.expect_err("Expected an ok")
    assert excinfo.value.args[0] == "Expected an ok"

def test_flatten():
    a = ok(ok(10))
    b = ok(err("error"))
    c = err("outer error")

    assert a.flatten().unwrap() == 10
    assert b.flatten().unwrap_err() == "error"
    assert c.flatten().unwrap_err() == "outer error"

def test_hash():
    assert hash(ok[NoReturn](10)) == hash(ok[NoReturn](10))
    assert hash(err[NoReturn]("error")) == hash(err[NoReturn]("error"))
    assert hash(ok[NoReturn](10)) != hash(ok[NoReturn](20))
    assert hash(ok[NoReturn](10)) != hash(err[NoReturn](10))

def test_is():
    a = ok[NoReturn](10)
    b = err[NoReturn]("error")

    assert a.is_ok()
    assert not a.is_err()
    assert b.is_err()
    assert not b.is_ok()
    assert a
    assert not b

    assert a.is_ok_and(lambda x: x == 10)
    assert not a.is_ok_and(lambda x: x == 20)
    assert b.is_err_and(lambda e: e == "error")
    assert not b.is_err_and(lambda e: e == "different")

def test_map():
    result = ok(5)
    result_err = err("error")

    assert result.map(lambda x: x * 2).unwrap() == 10
    assert result_err.map(lambda x: x * 2).is_err()

    assert result.map_err(lambda e: f"{e}!").unwrap() == 5
    assert result_err.map_err(lambda e: f"{e}!").unwrap_err() == "error!"

    assert result.map_or(0, lambda x: x + 3) == 8
    assert result_err.map_or(0, lambda x: x + 3) == 0

    assert result.map_or_else(lambda e: len(e), lambda x: x + 4) == 9
    assert result_err.map_or_else(lambda e: len(e), lambda x: x + 4) == 5

@no_type_check
def test_match():
    result_ok = ok(10)
    result_err = err("error")

    match result_ok:
        case ok(val):
            assert val == 10
        case err(e):
            pytest.fail("Should not match err case")

    match result_err:
        case ok(val):
            pytest.fail("Should not match ok case")
        case err(e):
            assert e == "error"

def test_ok():
    result_ok = ok[int](10)
    result_err = err[str]("error")

    assert result_ok.ok().unwrap() == 10
    assert result_err.ok().is_nothing()

def test_or():
    result1 = ok(10)
    result2 = ok(20)
    result_err = err("error")

    assert result1.or_(result2).unwrap() == 10
    assert (result1 | result2).unwrap() == 10
    assert result1.or_(result2) is not result1
    assert result_err.or_(result2).unwrap() == 20
    assert result_err.or_(result2) is not result2
    assert (result_err | result2).unwrap() == 20
    assert result1.or_(result_err).unwrap() == 10
    assert (result1 | result_err).unwrap() == 10
    assert result_err.or_(result_err).is_err()
    assert (result_err | result_err) is not result_err

def test_or_else():
    result = ok(10)
    result_err = err("error")

    assert result.or_else(lambda e: ok(20)).unwrap() == 10
    assert result.or_else(lambda e: ok(20)) is not result
    assert result_err.or_else(lambda e: ok(20)).unwrap() == 20
    assert result_err.or_else(lambda e: err(f"{e}!")).unwrap_err() == "error!"

def test_pure():
    a = Result.pure(10)
    b = Monad.pure[Result](20) # type: ignore

    assert a.unwrap() == 10
    assert b.unwrap() == 20

def test_tap():
    result = ok(10)
    result_err = err("error")

    side_effects = []

    def tap_func(x):
        side_effects.append(x)
        return ok(...)

    result_tapped = result.tap(tap_func)
    result_err_tapped = result_err.tap(tap_func)

    assert result_tapped is result
    assert result_err_tapped is result_err
    assert side_effects == [10]

    result_tapped_err = result.tap_err(tap_func)
    result_err_tapped_err = result_err.tap_err(tap_func)
    assert result_tapped_err is result
    assert result_err_tapped_err is result_err
    assert side_effects == [10, "error"]

def test_throw():
    a = ok[NoReturn](10)
    b = err[NoReturn](ValueError("error"))

    assert a.throw() == 10

    with pytest.raises(ValueError) as excinfo:
        b.throw()
    assert excinfo.value.args[0] == "error"

def test_transpose():
    a = ok(_maybe.just(10))
    b = ok(_maybe.nothing())
    c = err("error")

    assert a.transpose().unwrap().unwrap() == 10
    assert b.transpose().is_nothing()
    assert c.transpose().unwrap().unwrap_err() == "error"

def test_unwrap():
    a = ok[NoReturn](10)
    b = err[NoReturn](10)

    assert a.unwrap() == 10
    assert b.unwrap_err() == 10

    with pytest.raises(ValueError):
        b.unwrap()

    with pytest.raises(ValueError):
        a.unwrap_err()

def test_caught():
    from apfel.container.result import caught
    from typing import reveal_type

    @caught[ZeroDivisionError]()
    def result_unchecked(value: float):
        if value == 1.0:
            raise ValueError("The value cannot be 1.0")
        return 1 / value

    @caught(ZeroDivisionError)
    def result_checked(value: float):
        if value == 1.0:
            raise ValueError("The value cannot be 1.0")
        return 1 / value

    assert isinstance(result_unchecked(0.0).unwrap_err(), ZeroDivisionError)
    assert isinstance(result_unchecked(1.0).unwrap_err(), ValueError)

    assert isinstance(result_checked(0.0).unwrap_err(), ZeroDivisionError)
    with pytest.raises(ValueError):
        result_checked(1.0)


    @caught(ZeroDivisionError, ValueError, TypeError)
    def result_multiple(value: float):
        if value == 2.0:
            raise ValueError("The value cannot be 2.0")
        if value == 3.0:
            raise TypeError("The value cannot be 3.0")
        if value == 1.0:
            raise RuntimeError("The value cannot be 1.0")
        return 1 / value

    reveal_type(result_multiple)
    assert isinstance(result_multiple(0.0).unwrap_err(), ZeroDivisionError)
    assert isinstance(result_multiple(2.0).unwrap_err(), ValueError)
    assert isinstance(result_multiple(3.0).unwrap_err(), TypeError)
    with pytest.raises(RuntimeError):
        result_multiple(1.0)


    @caught(ZeroDivisionError | ValueError | TypeError)
    def result_union(value: float):
        if value == 2.0:
            raise ValueError("The value cannot be 2.0")
        if value == 3.0:
            raise TypeError("The value cannot be 3.0")
        if value == 1.0:
            raise RuntimeError("The value cannot be 1.0")
        return 1 / value

    reveal_type(result_union)
    assert isinstance(result_union(0.0).unwrap_err(), ZeroDivisionError)
    assert isinstance(result_union(2.0).unwrap_err(), ValueError)
    assert isinstance(result_union(3.0).unwrap_err(), TypeError)
    with pytest.raises(RuntimeError):
        result_union(1.0)