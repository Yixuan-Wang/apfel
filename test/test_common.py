import apfel as apfel
import pytest

def test_identity():
    assert identity(1) == 1  # noqa: F821

def test_todo():
    with pytest.raises(NotImplementedError):
        todo() # noqa: F821

def test_unimplemented():
    with pytest.raises(NotImplementedError):
        unimplemented() # noqa: F821
