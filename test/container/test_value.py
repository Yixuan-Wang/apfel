from apfel.container.value import Value
from apfel import imperative


def test_value_apply():
    @Value
    def vf(x: int):
        return x + 1

    v: Value[int] = Value.pure(42)

    v2 = v.apply(vf)
    assert v2.done() == 43


def test_value_bind():
    def f(x: int):
        return Value(x + 1)

    v = Value(42)
    v2 = v.bind(f)
    assert v2.done() == 43

    v3 = v.bind(lambda x: Value(x * 2))
    assert v3.done() == 84


def test_value_method_done():
    v = Value(42)
    assert v.done() == 42

    v = Value(None)
    assert v.done() is None


def test_value_method_map():
    v = Value(42)
    v2 = v.map(lambda x: x + 1)

    assert v2.done() == 43
    assert v is not v2


def test_value_method_pipe():
    v = Value(42)
    v2 = v.pipe(lambda x: x + 1)

    assert v2.done() == 43
    assert v is v2

    v = Value([1, 2, 3])
    v2 = v.pipe(lambda x: x.append(4))
    assert v2.done() == [1, 2, 3, 4]


def test_value_method_run():
    v = Value(42)
    assert v.run(lambda x: x + 1) == 43


def test_value_method_tap():
    side_effects = []
    v = Value(42)

    result = v.tap(
        lambda x: imperative(
            side_effects.append(x),
            x + 1,
        )
    )

    assert result is v  # tap returns the original container
    assert v.done() == 42
    assert side_effects == [42]
