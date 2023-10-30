from pytest import CaptureFixture
from apfel.effect.hook import Hook

hook1 = Hook("hook1")

@hook1.register
def func_hook1_1():
    print("foo", end="")

@hook1.register
def func_hook1_2():
    print("bar", end="")

def test_hook_lazy(capsys: CaptureFixture[str]):
    """Test the lazy hooks."""
    @hook1
    def func():
        print("baz", end="")
    
    func()
    captured = capsys.readouterr()
    assert captured.out == "foobarbaz"

hook2 = Hook("hook2")
global_state = 0

@hook2.register_eager
def func_hook2_eager():
    global global_state
    global_state = 1

@hook2.register
def func_hook2_lazy():
    global global_state
    global_state = 2

def test_hook_eager():
    assert global_state == 0
    @hook2
    def func():
        pass

    assert global_state == 1
    func()
    assert global_state == 2

hook3 = Hook("hook3")
@hook3.register_eager
def func_hook3_1():
    print("foo", end="")

@hook3.register
def func_hook3_2():
    print("bar", end="")

def test_hook_fire(capsys: CaptureFixture[str]):
    """Test the removal of hooks."""
    
    hook3.fire()
    captured = capsys.readouterr()
    assert captured.out == "bar"
