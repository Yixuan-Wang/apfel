"""
Dynamic dispatch for Python.

This address the lack of **runtime-available**, **inheritance-free** interfaces in Python.
It partially resembles the [`extension`](https://kotlinlang.org/docs/extensions.html){ .ref .kt } and [`trait`](https://doc.rust-lang.org/book/ch10-02-traits.html){ .ref .rs }.

# Rationale

**Why not [`functools.singledispatch`](https://docs.python.org/3/library/functools.html#functools.singledispatch){ .ref .py }?**
This API is added in Python 3.4, and it uses type hints to dispatch functions.
However, as Python develops, type hints are disentangled from concrete types.
Using type hints to dispatch functions can be error-prone.
Besides, its method counterpart [`functools.singledispatchmethod`](https://docs.python.org/3/library/functools.html#functools.singledispatchmethod){ .ref .py } dispatches methods based on the first non-first argument, which is very different from the single dispatch found in object-oriented programming.

**Why not [`abc.ABC`](https://docs.python.org/3/library/abc.html#abc.ABC){ .ref .py }?**
`abc.ABC` enables inheritance-free interfaces with the [`register`](https://docs.python.org/3/library/abc.html#abc.ABC.register){ .ref .py } method,
but it does not enable [`virtual`](https://cppreference.com/w/cpp/language/virtual){ .ref .cpp }-like dispatch.


# Usage

By default the utilities in `dispatch` module are for [single dispatch](https://en.wikipedia.org/wiki/Multiple_dispatch#Single_dispatch).
This means the dispatch is based on **the concrete type** of **first argument** of the function, or of the **receiver** in the case of methods.

"""

from __future__ import annotations
from abc import ABCMeta
from collections.abc import Callable
from functools import update_wrapper, WRAPPER_ASSIGNMENTS
from typing import Protocol
from types import FunctionType, MethodType


class ABCDispatchMeta(ABCMeta):
    def __new__(cls, name, bases, namespace, **kwargs):
        __dispatch_methods__ = set()
        for key, value in namespace.items():
            if isinstance(value, (FunctionType, classmethod, staticmethod)) and getattr(
                value, "__isabstractmethod__", False
            ):
                if isinstance(value, classmethod):
                    dispatch = DispatchRegistryForClassMethod(value)
                elif isinstance(value, staticmethod):
                    dispatch = DispatchRegistryForStaticMethod(value)
                else:
                    dispatch = DispatchRegistry(value)

                value = dispatch.decorate(value)
                value.__dispatch__ = dispatch  # type: ignore
                namespace[key] = value
                __dispatch_methods__.add(key)

        namespace["__dispatch_methods__"] = __dispatch_methods__

        self = super().__new__(cls, name, bases, namespace, **kwargs)

        for key in __dispatch_methods__:
            d = getattr(self, key)
            d.__dispatch__.enclosing_class = self

        return self

class IABCDispatch(Protocol):
    """
    A protocol for ABCs that supports dispatching regardless of dispatch flavor.
    """

    @property
    def __dispatch_methods__(self): ...

class ABCDispatch(metaclass=ABCDispatchMeta):
    """
    An `ABC` that enables single dispatch for its abstract methods.
    This behaves similarly to [`abc.ABC`](https://docs.python.org/3/library/abc.html#abc.ABC){ .ref .py } but with the added feature of single dispatch.
    Stick to built-in [`abc.abstractmethod`](https://docs.python.org/3/library/abc.html#abc.abstractmethod){ .ref .py } to define abstract methods.

    See the [usage section][apfel.core.dispatch--usage] for more information.

    !!! example
        ```python
        from abc import abstractmethod
        from apfel.core.dispatch import ABCDispatch

        class A(ABCDispatch):
            @abstractmethod
            def hi(self):
                print(self)

            @classmethod
            @abstractmethod
            def hey(cls):
                print(cls)

        a: A = some_instance()
        A.hi(a)
        ```
    """
    ...

class IDispatchRegistry(Protocol):
    """
    A protocol for dispatch registry.
    """

    def dispatch(self, *args, **kwargs):
        """
        Dispatch based on a given a set of arguments,
        i.e. decide which implementation should be used.
        Returns the implementation function.
        """
        ...
    
    def decorate(self, func):
        """
        Redirect the function to the polymorphic dispatch.
        This method should typically be implemented as a higher-order function,
        which returns a new function that wraps the original function with the dispatch logic.

        !!! example
            An example implementation of this method:
            ```python
            def decorate(self, func):
                def dyn(*args, **kwargs):
                    return self.dispatch(*args, **kwargs)(*args, **kwargs)
                
                update_wrapper(dyn, func)
                return dyn
            ```
        """
        ...

    def register(self, func, *args, **kwargs):
        """
        Dynamically add a new implementation to the registry.
        The interface of this method is not specified,
        except that the first argument should be the implementation.
        """
        ...

class DispatchRegistry(IDispatchRegistry):
    """
    Default [registry][apfel.core.dispatch.IDispatchRegistry] using single dispatch.
    """

    func: Callable
    """
    The original function or method.
    """

    registry: dict
    """
    A mapping from types to functions or methods.
    """

    enclosing_class: type | None
    """
    The class that the dispatched function is a method of.
    If it is not a method, this should be `None`.
    """
    
    decorate_assignments: list
    """
    What attributes to copy from the original function to the decorated function
    when calling the `decorate` method.
    """

    def __init__(self, func, *, enclosing_class=None, decorate_assignments=None):
        self.func = func
        self.registry = {}
        self.enclosing_class = enclosing_class
        self.decorate_assignments = decorate_assignments or [*WRAPPER_ASSIGNMENTS, "__isabstractmethod__"]

    def dispatch(self, *args, **kwargs):
        receiver, *args = args
        ty_receiver = type(receiver)
        if self.enclosing_class and isinstance(receiver, self.enclosing_class):
            return getattr(ty_receiver, self.func.__name__)

        for cls in ty_receiver.__mro__:
            if cls in self.registry:
                return self.registry[cls]
            
        return self.func
    
    def decorate(self, func):
        def dyn(*args, **kwargs):
            return self.dispatch(*args, **kwargs)(*args, **kwargs)

        update_wrapper(dyn, func, assigned=self.decorate_assignments)
        return MethodType(dyn, self.enclosing_class) if self.enclosing_class is not None else dyn
        

    def register(self, func, cls):
        self.registry[cls] = func

class DispatchRegistryForClassMethod(DispatchRegistry):
    def dispatch(self, *args, **kwargs):
        ty_or_receiver = args[0]

        ty = ty_or_receiver if isinstance(ty_or_receiver, type) else type(ty_or_receiver)
        if self.enclosing_class and issubclass(ty, self.enclosing_class):
            return getattr(ty, self.func.__name__)

        if not hasattr(ty, "__mro__"):
            ty = type(ty)

        for cls in ty.__mro__: # type: ignore
            if cls in self.registry:
                return self.registry[cls]
            
        return self.func
    
    def decorate(self, func):
        def dyn(*args, **kwargs):
            impl = self.dispatch(*args, **kwargs)
            receiver, *args = args
            # Here impl is of `method` type
            return impl.__get__(receiver)(*args, **kwargs)

        update_wrapper(dyn, func, assigned=self.decorate_assignments)
        return MethodType(dyn, self.enclosing_class) if self.enclosing_class is not None else dyn

class DispatchRegistryForStaticMethod(DispatchRegistryForClassMethod):
    # dispatch reuses the dispatch function of `DispatchRegistryForClassMethod`

    def decorate(self, func):
        def dyn(*args, **kwargs):
            impl = self.dispatch(*args, **kwargs)
            _, *args = args
            # Here impl is of `function` type
            return impl(*args, **kwargs)
        
        update_wrapper(dyn, func, assigned=self.decorate_assignments)
        return MethodType(dyn, self.enclosing_class) if self.enclosing_class is not None else dyn

def dispatch(func):
    """
    Decorator for single dispatch.
    """

    dispatch = DispatchRegistry(func)
    func = dispatch.decorate(func)
    setattr(func, "__dispatch__", dispatch)

    def impl_for(cls):
        def wrapper(impl):
            dispatch.register(impl, cls)
            return impl
        return wrapper
    setattr(func, "impl_for", impl_for)

    return func

def impl(definition):
    """
    Decorator for registering an implementation.
    """

    is_class = isinstance(definition, type)
    if not is_class:
        raise TypeError(f"{definition} of type {type(definition)} cannot dispatch")
    
    dispatchable_methods = getattr(definition, "__dispatch_methods__", set())

    def decorator(impl):
        if not isinstance(impl, type):
            raise TypeError(f"{impl} of type {type(impl)} cannot be an implementation")
        
        impl_for = impl.__base__

        if impl_for is None:
            raise ValueError(f"{impl} not subclassing any class is not a valid implementation")

        for name, func in vars(impl).items():
            if not isinstance(func, (FunctionType, classmethod, staticmethod)):
                continue

            if name not in dispatchable_methods:
                raise ValueError(f"{name} of {definition.__name__} does not support dispatching")
            
            getattr(definition, name).__dispatch__.register(func, impl_for)

        return impl

    return decorator