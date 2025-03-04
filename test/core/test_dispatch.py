from apfel.core.dispatch import ABCDispatch, dispatch, impl
from abc import abstractmethod

import pytest

class TestSingleDispatch:
    class ITest(ABCDispatch):
        """
        A test ABC for ABCDispatch.
        """

        @abstractmethod
        def normal_method(self, *args, **kwargs):
            return {
                "type": "normal",
                "implementation": "(blanket)",
                "args": args,
                "kwargs": kwargs,
            }

        @classmethod
        @abstractmethod
        def class_method(cls, *args, **kwargs):
            return {
                "type": "class",
                "implementation": "(blanket)",
                "args": args,
                "kwargs": kwargs,
            }
        
        @staticmethod
        @abstractmethod
        def static_method(*args, **kwargs):
            return {
                "type": "static",
                "implementation": "(blanket)",
                "args": args,
                "kwargs": kwargs,
            }

    def test_dispatch_abc_blanket(self):
        """Check if the blanket implementation works."""

        # ABC behavior is unchanged.
        # If a class has abstract methods, it cannot be instantiated,
        # even if the abstract methods have blanket impl.

        with pytest.raises(TypeError):
            class TestNotInitiable(TestSingleDispatch.ITest):
                pass
            _ = TestNotInitiable()  # type: ignore

        # Given a class that neither subclasses nor registers any methods,
        # should raise NotImplementedError (instead of AttributeError)
        EmptyClass = type("EmptyClass", (), {})
        empty = EmptyClass()

        with pytest.raises(NotImplementedError):
            TestSingleDispatch.ITest.normal_method(empty) # type: ignore

        with pytest.raises(NotImplementedError):
            TestSingleDispatch.ITest.class_method[empty]() # type: ignore

        with pytest.raises(NotImplementedError):
            TestSingleDispatch.ITest.static_method[empty]() # type: ignore

    class A(ITest):
        def normal_method(self, *args, **kwargs):
            return {
                "type": "normal",
                "implementation": "A",
                "args": args,
                "kwargs": kwargs,
            }

        @classmethod
        def class_method(cls, *args, **kwargs):
            return {
                "type": "class",
                "implementation": "A",
                "args": args,
                "kwargs": kwargs,
            }
        
        @staticmethod
        def static_method(*args, **kwargs):
            return {
                "type": "static",
                "implementation": "A",
                "args": args,
                "kwargs": kwargs,
            }
    
    def test_dispatch_abc_inherit_normal(self):
        A = TestSingleDispatch.A
        a = A()
        
        # Using normal method call
        assert a.normal_method(1, a="a") == {
            "type": "normal",
            "implementation": "A",
            "args": (1,),
            "kwargs": {"a": "a"},
        }

        # Use qualified function call
        assert A.normal_method(a, 1, a="a") == {
            "type": "normal",
            "implementation": "A",
            "args": (1,),
            "kwargs": {"a": "a"},
        }

        # Using dynamic dispatch
        assert TestSingleDispatch.ITest.normal_method(a, 1, a="a") == {
            "type": "normal",
            "implementation": "A",
            "args": (1,),
            "kwargs": {"a": "a"},
        }

    def test_dispatch_abc_inherit_class(self):
        A = self.A
        a = A()
    
        assert a.class_method(1, a="a") == {
            "type": "class",
            "implementation": "A",
            "args": (1,),
            "kwargs": {"a": "a"},
        }
        assert A.class_method(1, a="a") == {
            "type": "class",
            "implementation": "A",
            "args": (1,),
            "kwargs": {"a": "a"},
        }
        assert TestSingleDispatch.ITest.class_method[a](1, a="a") == { # type: ignore
            "type": "class",
            "implementation": "A",
            "args": (1,),
            "kwargs": {"a": "a"},
        }
        assert TestSingleDispatch.ITest.class_method[A](1, a="a") == { # type: ignore
            "type": "class",
            "implementation": "A",
            "args": (1,),
            "kwargs": {"a": "a"},
        }


    def test_dispatch_abc_inherit_static(self):
        A = self.A
        a = A()

        assert a.static_method(1, a="a") == {
            "type": "static",
            "implementation": "A",
            "args": (1,),
            "kwargs": {"a": "a"},
        }
        assert A.static_method(1, a="a") == {
            "type": "static",
            "implementation": "A",
            "args": (1,),
            "kwargs": {"a": "a"},
        }

        # Using function call
        assert TestSingleDispatch.ITest.static_method[a](1, a="a") == { # type: ignore
            "type": "static",
            "implementation": "A",
            "args": (1,),
            "kwargs": {"a": "a"},
        }
        assert TestSingleDispatch.ITest.static_method[A](1, a="a") == { # type: ignore
            "type": "static",
            "implementation": "A",
            "args": (1,),
            "kwargs": {"a": "a"},
        }

    def test_dispatch_impl(self):
        @impl(TestSingleDispatch.ITest)
        class _(int):
            def normal_method(self, *args, **kwargs):
                return {
                    "type": "normal",
                    "implementation": "int",
                    "args": args,
                    "kwargs": kwargs,
                }

            @classmethod
            def class_method(cls, *args, **kwargs):
                return {
                    "type": "class",
                    "implementation": "int",
                    "args": args,
                    "kwargs": kwargs,
                }
            
            @staticmethod
            def static_method(*args, **kwargs):
                return {
                    "type": "static",
                    "implementation": "int",
                    "args": args,
                    "kwargs": kwargs,
                }
            
        i = 1
        assert TestSingleDispatch.ITest.normal_method(i, 1, a="a") == { # type: ignore
            "type": "normal",
            "implementation": "int",
            "args": (1,),
            "kwargs": {"a": "a"},
        }
        assert TestSingleDispatch.ITest.class_method[1](1, a="a") == { # type: ignore
            "type": "class",
            "implementation": "int",
            "args": (1,),
            "kwargs": {"a": "a"},
        }
        assert TestSingleDispatch.ITest.class_method[int](1, a="a") == { # type: ignore
            "type": "class",
            "implementation": "int",
            "args": (1,),
            "kwargs": {"a": "a"},
        }

class TestSingleDispatchFuncAPI:    
    def test_dispatch_func_api(self):
        from typing import Any

        @dispatch
        def f(x: Any) -> str:
            return str(x)

        # Empty registry before dispatch        
        assert f.__dispatch__.registry == {}

        # Fallback implementation used
        with pytest.raises(NotImplementedError):
            f(1/3)

        # Register an implementation
        @f.impl_for(float)
        def impl_float(x: float) -> str:
            return f"{x:.2f}"

        assert f.__dispatch__.registry == {float: impl_float}
        assert f(1/3) == "0.33"

        # Single-inheritance should work
        class MyFloat(float):
            pass

        assert f(MyFloat(1/3)) == "0.33"
