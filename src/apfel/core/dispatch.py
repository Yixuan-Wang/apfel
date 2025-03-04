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
`abc.ABC` enables inheritance-free interfaces with the [.add_impl`](https://docs.python.org/3/library/abc.html#abc.ABC.add_impl){ .ref .py } method,
but it does not enable [`virtual`](https://cppreference.com/w/cpp/language/virtual){ .ref .cpp }-like dispatch.


# Usage

By default the utilities in `dispatch` module are for [single dispatch](https://en.wikipedia.org/wiki/Multiple_dispatch#Single_dispatch).
This means the dispatch is based on **the concrete type** of **first argument** of the function, or of the **receiver** in the case of methods.

"""

from __future__ import annotations
from abc import ABCMeta
from collections.abc import Callable, Sequence
from functools import update_wrapper, WRAPPER_ASSIGNMENTS
from typing import Protocol
from types import FunctionType, MethodType

from apfel.core.function import unimplemented


class ABCDispatchMeta(ABCMeta):
    def __new__(cls, name, bases, namespace, **kwargs):
        __dispatch_methods__ = set()
        for key, value in namespace.items():
            if isinstance(value, (FunctionType, classmethod, staticmethod)) and getattr(
                value, "__isabstractmethod__", False
            ):
                if isinstance(value, classmethod):
                    dispatch_registry = DispatchRegistryForClassMethod(value)
                elif isinstance(value, staticmethod):
                    dispatch_registry = DispatchRegistryForStaticMethod(value)
                else:
                    dispatch_registry = DispatchRegistry(value)

                value = dispatch_registry.make_dispatch_func(value)
                value.__dispatch__ = dispatch_registry  # type: ignore
                value.__isabstractmethod__ = True  # type: ignore
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
    A dispatch registry is a collection of implementations of a
      polymorphic function or method.
    """

    def decide_impl(self, *args, **kwargs):
        """
        ```python
        def decide_impl(self, *args: P.args, **kwargs: R.args) -> Callable[P, R]
        ```
        Decide which implementation should be used based on
        the arguments.

        This method should not call the implementation directly,
        but return a reference to it.

        Returns:
            (Callable): The implementation to be used.
        """
        ...

    def make_dispatch_func(self, func):
        """
        ```python
        def make_dispatch_func(self, func: Callable[P, R]) -> Callable[P, R]
        ```
        Make a function or callable that uses this registry to perform dynamic dispatch.

        Notes:
            This method should typically be implemented as a higher-order function,
            which returns a new function that wraps the original function with the
            dispatch logic.
            An example implementation of this method:
            ```python
            def make_dispatch_func(self, func):
                def dyn(*args, **kwargs):
                    return self.decide_impl(*args, **kwargs)(*args, **kwargs)

                functools.update_wrapper(dyn, func)
                return dyn
            ```
        """
        ...

    def add_impl(self, func, *args, **kwargs):
        """
        ```python
        def add_impl(self, func: Callable[P, R], *args: K.args, **kwargs: K.kwargs)
        ```
        Add a new implementation to the registry.

        Args:
            func (Callable[P, R]): The implementation to be added.
            ... (K): The implementor of the implementation added.
        """
        ...

    def get_impl(self, *args, **kwargs):
        """
        ```python
        def get_impl(self, *args: K.args, **kwargs: K.kwargs) -> Callable raise KeyError
        ```
        Get an implementation from the registry.

        Args:
            ... (K): The implementor of the implementation.

        Returns:
            (Callable[Self.P, Self.R]): The implementation.

        Raises:
            KeyError: If no such implementation is found.
        """
        ...


class DispatchRegistry(IDispatchRegistry):
    """
    Default [dispatch registry][apfel.core.dispatch.IDispatchRegistry] using single dispatch.
    """

    function: Callable
    """
    The fallback function or method.
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

    decorate_assignments: Sequence[str]
    """
    What attributes to copy from the original function to the decorated function
    when calling the `make_dispatch_func` method.
    """

    def __init__(self, func=None, *, enclosing_class=None, decorate_assignments=None):
        self.function = func or unimplemented
        self.registry = {}
        self.enclosing_class = enclosing_class
        self.decorate_assignments = decorate_assignments or WRAPPER_ASSIGNMENTS

    def decide_impl(self, *args, **kwargs):
        receiver, *args = args
        ty_receiver = type(receiver)
        if (
            self.enclosing_class
            and isinstance(receiver, self.enclosing_class)
            and (impl := getattr(ty_receiver, self.function.__name__, None)) is not None
        ):
            return impl 

        for cls in ty_receiver.__mro__:
            if cls in self.registry:
                return self.registry[cls]

        raise NotImplementedError(
            "No implementation {enclosing_class}found for {ty_receiver}".format(
                enclosing_class=f"of {self.enclosing_class.__name__} "
                if self.enclosing_class
                else "",
                ty_receiver=ty_receiver.__name__,
            )
        )

    def make_dispatch_func(self, func):
        def dyn(*args, **kwargs):
            return self.decide_impl(*args, **kwargs)(*args, **kwargs)

        update_wrapper(dyn, func, assigned=self.decorate_assignments)
        return (
            MethodType(dyn, self.enclosing_class)
            if self.enclosing_class is not None
            else dyn
        )

    def add_impl(self, func, *args, **kwargs):
        if len(args) != 1:
            raise ValueError("Single dispatch only supports one argument")
        ty = args[0]
        if not isinstance(ty, type):
            raise ValueError("Single dispatch only supports dispatching based on types")

        self.registry[ty] = func

    def get_impl(self, *args, **kwargs):
        if len(args) != 1:
            raise ValueError("Single dispatch only supports one argument")
        ty = args[0]
        if not isinstance(ty, type):
            raise ValueError("Single dispatch only supports dispatching based on types")

        return self.registry.get(ty, self.function)


class DispatchRegistryForClassMethod(DispatchRegistry):
    def decide_impl(self, *args, **kwargs):
        ty_or_receiver = args[0]

        ty = (
            ty_or_receiver if isinstance(ty_or_receiver, type) else type(ty_or_receiver)
        )
        if (
            self.enclosing_class
            and issubclass(ty, self.enclosing_class)
            and (impl := getattr(ty, self.function.__name__, None)) is not None
        ):
            return impl

        if not hasattr(ty, "__mro__"):
            ty = type(ty)

        for cls in ty.__mro__:  # type: ignore
            if cls in self.registry:
                return self.registry[cls]

        raise NotImplementedError(
            "No implementation {enclosing_class}found for {ty}".format(
                enclosing_class=f"of {self.enclosing_class.__name__} "
                if self.enclosing_class
                else "",
                ty=ty.__name__,
            )
        )

    def make_dispatch_func(self, func):
        # Create a callable class dyn
        # where dyn[cls] will return the implementation for cls

        # here `func` might be a descriptor

        class dyn:
            def __class_getitem__(cls, key):
                impl = self.decide_impl(key)
                return impl.__get__(key)

            def __new__(cls, *args, **kwargs):
                return self.function.__get__(cls)(*args, **kwargs)

        update_wrapper(dyn, func, assigned=self.decorate_assignments, updated=())
        return (
            MethodType(dyn, self.enclosing_class)
            if self.enclosing_class is not None
            else dyn
        )

    def add_impl(self, func, *args, **kwargs):
        if not isinstance(func, classmethod):
            func = classmethod(func)
        return super().add_impl(func, *args, **kwargs)


class DispatchRegistryForStaticMethod(DispatchRegistryForClassMethod):
    def make_dispatch_func(self, func):
        class dyn:
            def __class_getitem__(cls, key):
                return self.decide_impl(key)

            def __new__(cls, *args, **kwargs):
                return self.function(*args, **kwargs)

        update_wrapper(dyn, func, assigned=self.decorate_assignments, updated=())
        # static methods will not use MethodType
        return dyn

    def add_impl(self, func, *args, **kwargs):
        if not isinstance(func, staticmethod):
            func = staticmethod(func)
        return super().add_impl(func, *args, **kwargs)


def dispatch(func):
    """
    Decorator for single dispatch.
    """

    dispatch = DispatchRegistry(func)
    func = dispatch.make_dispatch_func(func)
    setattr(func, "__dispatch__", dispatch)

    def impl_for(cls):
        def wrapper(impl):
            dispatch.add_impl(impl, cls)
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
            raise ValueError(
                f"{impl} not subclassing any class is not a valid implementation"
            )

        for name, func in vars(impl).items():
            if not isinstance(func, (FunctionType, classmethod, staticmethod)):
                continue

            if name not in dispatchable_methods:
                raise ValueError(
                    f"{name} of {definition.__name__} does not support dispatching"
                )

            getattr(definition, name).__dispatch__.add_impl(func, impl_for)

        try:
            for name, func in vars(impl).items():
                if not isinstance(func, (FunctionType, classmethod, staticmethod)):
                    continue

                setattr(impl, name, func)
        except AttributeError:
            pass
        
        if isinstance(definition, ABCMeta):
            definition.register(impl_for)

        return impl

    return decorator


def add_impl(definition, impl, *impl_for_args, **impl_for_kwargs):
    """
    An imperative interface for adding implementations to a dispatchable class.
    """
    for name, func in impl.items():
        getattr(definition, name).__dispatch__.add_impl(func, *impl_for_args, **impl_for_kwargs)
