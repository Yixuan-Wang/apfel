def test_once():
    from apfel.effect.once import Once

    once = Once[int]()
    assert not once.is_set()

    once.set(1)
    assert once.is_set()
    assert once.get() == 1

    once.set(2)
    assert once.get() == 1

    once = Once[int]()
    once.get_or_init(lambda: 1)
    assert once.is_set()
    assert once.get() == 1

    once.get_or_init(lambda: 2)
    assert once.get() == 1

def test_lazy_init():
    from apfel.effect.once import lazy_init

    @lazy_init
    def f():
        return object()
    
    obj = f()

    assert f() is obj
