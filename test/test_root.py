import apfel
import builtins

def test_apfel_namespace():
    assert apfel.identity is getattr(builtins, "identity")
    assert apfel.imperative is getattr(builtins, "imperative")
    assert apfel.todo is getattr(builtins, "todo")
    assert apfel.unimplemented is getattr(builtins, "unimplemented")
