from apfel import identity, todo, unimplemented
import pytest

def test_identity():
    assert identity(1) == 1

def test_todo():
    with pytest.raises(NotImplementedError):
        todo()

def test_unimplemented():
    with pytest.raises(NotImplementedError):
        unimplemented()
