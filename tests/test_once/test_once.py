from apfel.effect.once import once


def test_once():
    x = 1

    @once
    def func():
        nonlocal x
        x += 1

    func()
    assert x == 2, "The first call is fired"
    func()
    assert x == 2, "The second call is not fired"
