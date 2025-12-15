import pytest


def test_once():
    from apfel.container.once import Once

    once = Once[int]()
    assert not once
    with pytest.raises(ValueError):
        once.unwrap()

    ok = once.set(1)
    assert once
    assert ok.is_ok() and ok.unwrap() is None
    assert once.unwrap() == 1

    prev = once.set(2)
    assert once.unwrap() == 1
    assert prev.is_err() and prev.unwrap_err() == 1

    once = Once[int]()
    assert once.get().is_nothing()
    once.get_or_init(lambda: 1)
    assert once
    assert once.get().unwrap() == 1
    assert once.unwrap() == 1

    once.get_or_init(lambda: 2)
    assert once.get().unwrap() == 1
    assert once.unwrap() == 1


def test_once_of_type():
    from apfel.container.once import Once

    once = Once.of_hint(int)


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

    assert f.value() is obj  # the function `f` will not be called again.
    assert a == 1

    b = 0

    @Lazy[int]
    def g():
        nonlocal b
        b += 1
        return b

    assert g() == 1
    assert g() == 1


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


def test_once_lock():
    from apfel.container.once import OnceLock
    import random
    import time
    import concurrent.futures

    lock = OnceLock[int]()
    assert not lock
    assert lock.get().is_nothing()

    def init():
        time.sleep(random.random() / 10)
        return random.randint(1, 100)

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(lambda _: lock.get_or_init(init), range(20)))

    assert (lock_val := lock.get().unwrap()) is not None
    assert all(result == lock_val for result in results)

    lock = OnceLock[int]()
    with pytest.raises(ValueError):
        lock.unwrap()

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        results = list(
            executor.map(lambda _: lock.set(random.randint(1, 100)), range(20))
        )

    assert (lock_val := lock.unwrap()) is not None
    for result in results:
        if result.is_ok():
            assert result.unwrap() is None
        else:
            assert result.unwrap_err() == lock_val


def test_lazy_lock():
    from apfel.container.once import LazyLock
    import random
    import time
    import concurrent.futures

    @LazyLock
    def init():
        time.sleep(random.random() / 10)
        return random.randint(1, 100)

    assert not init

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(lambda _: init(), range(20)))

    assert (lock_val := init()) is not None
    assert all(result == lock_val for result in results)

    init = LazyLock[int](init)
    with pytest.raises(ValueError):
        init.unwrap()

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(lambda _: init(), range(20)))

    assert (lock_val := init.unwrap()) == init.value()
    assert all(result == lock_val for result in results)

    init = LazyLock[int](init)
    assert init.value() == init()
