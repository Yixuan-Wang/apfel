# type: ignore

import pytest


def test_function_object_init():
    from apfel.core.function_object import FunctionObject

    def f(x):
        """A simple function"""
        return x + 1

    f_obj = FunctionObject(f)
    assert (
        getattr(f_obj, "__wrapped__") is f
    ), "`FunctionObject.__wrapped__ `is not the original function"
    assert (
        getattr(f_obj, "__doc__") is f.__doc__
    ), "`FunctionObject.__doc__` is not the original function's docstring"
    assert (
        getattr(f_obj, "__name__") is f.__name__
    ), "`FunctionObject.__name__` is not the original function's name"


def test_function_object_call():
    from apfel.core.function_object import FunctionObject

    def f(x):
        """A simple function"""
        return x + 1

    f_obj = FunctionObject(f)
    assert f_obj(1) == f(
        1
    ), "`FunctionObject` does not call the original function correctly"


def test_func_decorator():
    from apfel.core.function_object import fob

    @fob
    def f(x):
        return x + 1

    assert f(1) == 2, "`@fob` decorator does not work correctly"


def test_func_batch_transform():
    from apfel.core.function_object import fob

    def f(x: int) -> int:
        return x + 1
    
    def g(x: str) -> str:
        return x * 2
    
    f, g = fob(f, g)
    assert f(1) == 2
    assert g("a") == "aa"


def test_function_object_function_application():
    from apfel.core.function_object import fob

    @fob
    def f(x):
        """A simple function"""
        return x + 1

    assert f | 1 == 2, "`FunctionObject.__or__` does not work correctly"
    assert f @ 1 == 2, "`FunctionObject.__matmul__` does not work correctly"
    assert 1 & f == 2, "`FunctionObject.__rand__` does not work correctly"

    @fob
    def g(x, y):
        return x + y

    with pytest.raises(TypeError):
        g | 1

    with pytest.raises(TypeError):
        g @ 1

    with pytest.raises(TypeError):
        1 & g

def test_function_object_application_pow():
    from apfel.core.function_object import fob

    @fob
    def f(x):
        """A simple function"""
        return x + 1

    @fob
    def g(x):
        return x * 2

    assert f ** g ** 1 == f(g(1)), "`FunctionObject.__pow__` does not work correctly"
    assert g ** f ** 1 == g(f(1)), "`FunctionObject.__pow__` does not work correctly"

def test_function_object_application_mod():
    from apfel.core.function_object import fob

    @fob
    def f(a, b, c):
        return a + b + c

    @fob
    def g(a, b = 2, c = 3):
        return a * b * c

    assert f % (1, 2, 3) == f(1, 2, 3)
    assert f % [1, 2, 3] == f(1, 2, 3)
    assert f % { "a": 1, "b": 2, "c": 3 } == f(a=1, b=2, c=3)
    assert f % { ...: (1, 2,), "c": 3 } == f(1, 2, c=3)
    assert f % { ...: (), "a": 1, "b": 2, "c": 3 } == f(1, 2, 3)
    assert f % ({...: (1, 2)} | { "c": 3 }) == f(1, 2, c=3)

    assert g % 1 == g % (1,)

    with pytest.raises(TypeError):
        f % 1

def test_function_object_precedence():
    from apfel.core.function_object import fob

    @fob
    def f(x):
        return x * 2
    
    assert f | 1 + 2 == f | (1 + 2)
    assert f @ 1 + 2 == (f @ 1) + 2
    assert 1 + 2 & f == (1 + 2) & f

    @fob
    def g(x):
        return x + 1

    assert g @ 1 * 3 == (g @ 1) * 3
    assert g | 1 * 3 == g | (1 * 3)
    assert 1 * 3 & g == (1 * 3) & g

    assert f | g @ 1 == f | (g @ 1)
    assert g @ 1 & f == (g @ 1) & f

    assert f | g @ 1 + 2 == f | ((g @ 1) + 2)
    
    assert f @ g ** 1 == f(g(1))
    assert f @ g ** 1 & 2 == f(g(1)) & 2

    assert f % g ** 1 == f(g(1))
    
    with pytest.raises(TypeError):
        f ** g @ 1

def test_function_object_typing(capsys):
    from apfel.core.function_object import fob
    from typing_extensions import reveal_type
    from apfel.core.function_object import reveal_fob

    @fob
    def f(x: int) -> int:
        return x + 1
    
    reveal_type(f)
    reveal_type(reveal_fob(f) | 1)
    reveal_type(reveal_fob(f) @ 1)
    reveal_type(1 & reveal_fob(f))
    reveal_type(reveal_fob(f) ** 1)
    reveal_type(reveal_fob(f) % (1,))

    @fob
    def g(a: int, b: str = "a", *, c: float = 1.0) -> str:
        return f"{a}{b}{c}"
    
    reveal_type(g)
    reveal_type(reveal_fob(g))
    reveal_type(reveal_fob(g) | 1)
    reveal_type(reveal_fob(g) @ 1)
    reveal_type(1 & reveal_fob(g))
    reveal_type(reveal_fob(g) ** 1)


def test_function_object_on_callables():
    from apfel.core.function_object import fob

    class A:
        def __call__(self, x):
            return x + 1
        
    a = fob(A())

    assert a | 1 == 2

    list_ = fob(list)
    map_ = fob(map)

    assert list_ | map_ % (lambda x: x + 1, [1, 2, 3]) == [2, 3, 4]
