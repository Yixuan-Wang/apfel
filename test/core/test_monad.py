# type: ignore

from __future__ import annotations
from typing import Any

from apfel.core.monad import Functor, Applicative, Monad

class MyMaybe(Monad):
    value: Any
    is_nothing: bool

    def __init__(self, value = None):
        if value is None:
            self.is_nothing = True
        else:
            self.value = value
            self.is_nothing = False

    @classmethod
    def pure(cls, x):
        return cls(x)
    
    def bind(self, f):
        if self.is_nothing:
            return self
        return f(self.value)
    
    def __eq__(self, other):
        return isinstance(other, MyMaybe) and self.is_nothing == other.is_nothing and self.value == other.value


def test_monad_maybe():
    assert MyMaybe.__abstractmethods__ == set()

    maybe = MyMaybe(42)
    
    assert maybe.map(lambda x: x + 1) == MyMaybe(43) # type: ignore
    assert maybe.apply(MyMaybe(lambda x: x + 1)) == MyMaybe(43) # type: ignore
    assert maybe.bind(lambda x: MyMaybe(x + 1)) == MyMaybe(43) # type: ignore

def test_monad_impl_list():
    assert issubclass(list, Functor)
    assert issubclass(list, Applicative)
    assert issubclass(list, Monad)

    lst = [1, 2, 3]

    import operator
    from functools import partial

    def add(x):
        return partial(operator.add, x)

    assert Functor.map(lst, add(1)) == [2, 3, 4]
    assert Applicative.pure[list](42) == [42]
    assert Applicative.apply(lst, [add(1), add(2)]) == [2, 3, 4, 3, 4, 5]
    assert Monad.bind(lst, lambda x: [x, x + 1]) == [1, 2, 2, 3, 3, 4]

def test_monad_impl_tuple():
    assert issubclass(tuple, Functor)
    assert issubclass(tuple, Applicative)
    assert issubclass(tuple, Monad)

    tpl = (1, 2, 3)

    import operator
    from functools import partial

    def add(x):
        return partial(operator.add, x)

    assert Functor.map(tpl, add(1)) == (2, 3, 4)
    assert Applicative.pure[tuple](42) == (42,)
    assert Applicative.apply(tpl, (add(1), add(2))) == (2, 3, 4, 3, 4, 5)
    assert Monad.bind(tpl, lambda x: (x, x + 1)) == (1, 2, 2, 3, 3, 4)

def test_monad_impl_set():
    assert issubclass(set, Functor)
    assert issubclass(set, Applicative)
    assert issubclass(set, Monad)

    st = {1, 2, 3}

    import operator
    from functools import partial

    def add(x):
        return partial(operator.add, x)

    assert Functor.map(st, add(1)) == {2, 3, 4}
    assert Applicative.pure[set](42) == {42}
    assert Applicative.apply(st, {add(1), add(2)}) == {2, 3, 4, 5}
    assert Monad.bind(st, lambda x: {x, x + 1}) == {1, 2, 3, 4}

def test_monad_impl_dict():
    assert issubclass(dict, Functor)
    assert not issubclass(dict, Applicative)
    assert not issubclass(dict, Monad)

    dct = {1: 2, 3: 4}

    import operator
    from functools import partial

    def add(x):
        return partial(operator.add, x)

    assert Functor.map(dct, add(1)) == {1: 3, 3: 5}

def test_monad_impl_function():
    from types import FunctionType

    assert issubclass(FunctionType, Functor)
    assert issubclass(FunctionType, Applicative)
    assert issubclass(FunctionType, Monad)

    def f(x):
        return x + 1
    
    def add(x):
        return lambda y: f"{x}{y}"

    assert Functor.map(f, add(1))(42) == (lambda x: add(1)(x + 1))(42)
    assert Applicative.pure[FunctionType](42)() == 42
    assert Applicative.apply(f, lambda x: add(x))(42) == (lambda x: add(x)(x + 1))(42) == "4243"
    assert Monad.bind(f, lambda x: add(x))(42) == (lambda x: add(x + 1)(x))(42) == "4342"

def test_monad_impl_function_ext():
    """
    Test the implementation on BuiltinFunctionType and types
    """

    assert Functor.map(map, list)(lambda x: x + 1, [1, 2, 3, 4]) == list(map(lambda x: x + 1, [1, 2, 3, 4]))
    assert Functor.map(str, list)(1) == ["1"]
