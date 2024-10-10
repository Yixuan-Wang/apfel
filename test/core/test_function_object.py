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
    from apfel.core.function_object import func

    @func
    def f(x):
        """A simple function"""
        return x + 1

    assert f(1) == 2, "`@func` decorator does not work correctly"


def test_function_object_function_apply():
    from apfel.core.function_object import func

    @func
    def f(x):
        """A simple function"""
        return x + 1

    assert f | 1 == 2, "`FunctionObject.__or__` does not work correctly"

    @func
    def g(x, y):
        return x + y

    with pytest.raises(TypeError):
        g | 1


def test_function_object_function_apply_reverse():
    from apfel.core.function_object import func

    @func
    def f(x):
        """A simple function"""
        return x + 1

    assert 1 & f == 2, "`FunctionObject.__rand__` does not work correctly"

    @func
    def g(x, y):
        return x + y

    with pytest.raises(TypeError):
        1 & g


def test_function_object_composition():
    from apfel.core.function_object import func

    @func
    def f(x):
        """A simple function"""
        return x + 1

    @func
    def g(x):
        return x * 2

    assert (f**g)(1) == f(g(1)), "`FunctionObject.__pow__` does not work correctly"
    assert (g**f)(1) == g(f(1)), "`FunctionObject.__pow__` does not work correctly"


def test_function_object_curry_or_call():
    from apfel.core.function_object import func

    @func
    def single_argument(x):
        return x + 1

    # for single argument functions, call directly
    assert single_argument @ 1 == 2

    @func
    def single_position_only_argument(x, /):
        return x + 1

    # for single argument functions, call directly
    assert single_position_only_argument @ 1 == 2

    @func
    def double_argument(x, y):
        return x + y

    # for multiple argument functions, curry
    assert (double_argument @ 1)(2) == 3
    assert (double_argument @ 1 @ 2) == 3

    @func
    def double_position_only_argument(x, y, /):
        return x + y

    assert (double_position_only_argument @ 1)(2) == 3
    assert (double_position_only_argument @ 1 @ 2) == 3

    @func
    def single_argument_with_kwarg(x, *, y):
        return x + y

    with pytest.raises(TypeError):
        single_argument_with_kwarg @ 1

    @func
    def single_with_kwargs(x, **kwargs):
        return x + sum(kwargs.values())

    assert single_with_kwargs @ 1 == 1

    @func
    def double_with_kwargs(x, y, **kwargs):
        return x + y + sum(kwargs.values())

    assert (double_with_kwargs @ 1 @ 2) == 3

    @func
    def single_with_args(x, *args):
        return x + sum(args)

    assert single_with_args @ 1 == 1

    @func
    def double_with_args(x, y, *args):
        return x + y + sum(args)

    assert (double_with_args @ 1 @ 2) == 3

    @func
    def triple(x, y, z):
        return x + y + z

    assert (triple @ 1 @ 2 @ 3) == 6

    @func
    def zero():
        return 0

    assert zero @ ... == 0

    @func
    def zero_with_args(*args):
        return sum(args)

    assert zero_with_args @ 1 @ 2 @ 3 | 4 == 10

    @func
    def zero_with_kwargs(**kwargs):
        return sum(kwargs.values())

    assert zero_with_kwargs @ ... == 0

    @func
    def zero_with_args_and_kwargs(*args, **kwargs):
        return sum(args) + sum(kwargs.values())

    assert zero_with_args_and_kwargs @ 1 @ 2 @ 3 | 4 == 10

def test_function_object_partial():
    from apfel.core.function_object import func

    @func
    def f(a, b, c):
        return a + b + c

    g = f % (1, 2)
    assert g(3) == 6, "`FunctionObject.__mod__` does not work correctly"

    g = f % {"a": 1, "b": 2}
    assert g(c=3) == 6, "`FunctionObject.__mod__` does not work correctly"

    with pytest.raises(TypeError):
        f % 1