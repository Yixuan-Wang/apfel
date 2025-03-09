import pytest


def test_once():
    from apfel.container.once import Once

    once = Once[int]()
    assert not once

    once.set(1)
    assert once
    assert once.unwrap() == 1

    once.set(2)
    assert once.unwrap() == 1

    once = Once[int]()
    once.get_or_init(lambda: 1)
    assert once
    assert once.unwrap() == 1

    once.get_or_init(lambda: 2)
    assert once.unwrap() == 1

def test_lazy():
    from apfel.container.once import Lazy

    a = 0
    @Lazy
    def f():
        nonlocal a
        a += 1
        return object()
    
    obj = f.value()
    assert a == 1

    assert f.value() is obj # the function `f` will not be called again.
    assert a == 1

def test_lazy_bool():
    from apfel.container.once import Lazy

    l = Lazy(lambda: 42)
    assert not l
    
    l()
    assert l

def test_lazy_unwrap():
    from apfel.container.once import Lazy

    l = Lazy(lambda: 42)
    
    with pytest.raises(ValueError):
        l.unwrap()
    
    l()
    assert l.unwrap() == 42

def test_lazy_value():
    from apfel.container.once import Lazy

    @Lazy
    def f():
        return object()
    
    obj = f.value()
    assert f.value() is obj
