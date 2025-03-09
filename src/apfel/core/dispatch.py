"""
Dynamic dispatch facilities for Python.

This addresses the lack of **runtime-available**, **inheritance-free** interfaces in Python.
It partially resembles the [`extension`](https://kotlinlang.org/docs/extensions.html){ .ref .kt } and [`trait`](https://doc.rust-lang.org/book/ch10-02-traits.html){ .ref .rs }.

# Rationale

**Why not [`functools.singledispatch`](https://docs.python.org/3/library/functools.html#functools.singledispatch){ .ref .py }?**

- Runtime behavior based on type hints can be confusing.
- It's method variant [`functools.singledispatchmethod`](https://docs.python.org/3/library/functools.html#functools.singledispatchmethod){ .ref .py } dispatches methods based on the first non-`self` argument, which is very different from the single dispatch found in other object-oriented programming languages.

**Why not [`abc.ABC`](https://docs.python.org/3/library/abc.html#abc.ABC){ .ref .py }?**

- It does not enable [`virtual`](https://cppreference.com/w/cpp/language/virtual){ .ref .cpp }-like or [`dyn`](https://doc.rust-lang.org/book/ch18-02-trait-objects.html){ .ref .rs }-like dispatch.
An [`abstractmethod`](https://docs.python.org/3/library/abc.html#abc.abstractmethod){ .ref .py } in an abstract class will not forward the call to the concrete implementation based on the real type.
i.e., there is no facilities for implementation selection based on concrete types.
- Although [`ABCMeta.register`](https://docs.python.org/3/library/abc.html#abc.ABCMeta.register){ .ref .py } can be used to register non-child classes, it cannot inject implementations to the registered classes. 
Some classes do not allow monkey-patching and the implementations must be stored elsewhere, registering them to the ABC is logical error, as the implementations are not part of the concrete class.

Using [`ABCDispatch`][apfel.core.dispatch.ABCDispatch] defined in this module,

- All ABC features work out of the box. Supports static type checking (inheritance-based usages only), non-inheritance based runtime type checking, and `@abstractmethod`.
- Abstract methods defined in an `ABCDispatch` can **dynamically** forward the call to the concrete implementation based on the real type, and the implementations can be externally provided.
  For example, an `ABCDispatch` can be used to extend built-in classes.

# Usage

First, define a class that subclasses [`ABCDispatch`][apfel.core.dispatch.ABCDispatch].
This class will be semantically similar to [Rust traits](https://doc.rust-lang.org/book/ch10-02-traits.html){ .ref .rs }.
All interface functions defined in this method shall be decorated with [`@abc.abstractmethod`](https://docs.python.org/3/library/abc.html#abc.abstractmethod){ .ref .py }.
Class methods and static methods can also be defined with the same decorator.

Warning:
    The `@abstractmethod` decorator must be placed after the `@classmethod` or `@staticmethod` decorator.

```python
class Trait(ABCDispatch):
    @abstractmethod
    def method(self, f): ...

    @classmethod
    @abstractmethod
    def class_method(cls, f): ...

    @staticmethod
    @abstractmethod
    def static_method(f): ...
```

Then, we can implement the "trait" for a class by using the [`@impl`][apfel.core.dispatch.impl] decorator.
The implementor class is passed as the first argument to the decorator.
The implementation is written in the `class` syntax, with each trait method implemented as a method of the class.
The class name doesn't matter, but it should subclass the trait class.

```python
@impl(Class)
class _(Trait):
    def method(self, f): \"""Concrete implementation goes here\"""

    @classmethod
    def class_method(cls, f): \"""Concrete implementation goes here\"""

    @staticmethod
    def static_method(f): \"""Concrete implementation goes here\"""
```

In this case, `Class.method` does not exist during runtime so you may not call it, and calling `.method` on an instance of `Class` will also fail.
But you can call `Trait.method` on an instance of `Class` and it will dispatch to the concrete implementation defined in the `@impl` construct.

```python
c = Class()
Trait.method(c, f)  # Calls the implementation within the @impl
```

If you have control to the source code, you can add `Trait` to the base classes of `Class`,
so `Class.method(instance)` and `instance.method()` will work as expected, `Trait.method(instance, f)` shall also work.

Class methods and static methods shall be called with the generic syntax, as the concrete class is not inferrable from the function's call arguments.

```python
Trait.class_method[Class](f)
Trait.static_method[Class](f)
```

It's also possible to define a dispatchable function using the [`@dispatch`][apfel.core.dispatch.dispatch] decorator.
Then an method `impl_for` will be on the function, which can be used to register implementations.

```python
@dispatch
def f(x): ...

@f.impl_for(int)
def _(x: int):
    \"""Implementation for int goes here\"""
```

Example:
  You can check the [`Functor`][apfel.core.monad.Functor]'s source code as an example of how to use this module.

By default `ABCDispatch` and `@dispatch` defines a [single dispatch](https://en.wikipedia.org/wiki/Multiple_dispatch#Single_dispatch).
This means the runtime imlementation selection is based on **the concrete type** of **first argument** of the function, or of the **receiver** in the case of methods.

"""

from __future__ import annotations
from abc import ABCMeta
from collections.abc import Callable, Sequence
from functools import update_wrapper, WRAPPER_ASSIGNMENTS
from typing import Protocol
from types import FunctionType, MethodType

from apfel import unimplemented


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
    This behaves similarly to [`abc.ABC`](https://docs.python.org/3/library/abc.html#abc.ABC){ .ref .py } but with the added feature of dynamic concrete implementation selection under single dispatch.
    Stick to built-in [`abc.abstractmethod`](https://docs.python.org/3/library/abc.html#abc.abstractmethod){ .ref .py } to define abstract methods.

    See the [usage section][apfel.core.dispatch--usage] for more information.

    Example:
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
    A decorator for creating a single-dispatchable function.
    It will add an `impl_for` method to the function, which can be used to register implementations.
    Calling the function will dispatch to the correct implementation based on the type of the first argument.

    This is similar to [`functools.singledispatch`](https://docs.python.org/3/library/functools.html#functools.singledispatch){ .ref .py }, but does not use type hints for dispatching, and static type unions are not supported.

    Example:
        ```python
        @dispatch
        def show(x):
            ...

        @show.impl_for(int)
        def _(x: int):
            return f"int: {x}"

        @show.impl_for(str)
        def _(x: str):
            return f"str: {x}"
        
        show(1)       # "int: 1"
        show("hello") # "str: hello"
        ```
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
    Decorator for registering an implementation using the `class` syntax.

    See the [usage section][apfel.core.dispatch--usage] for more information.

    Example:
        Here `Class` is a concrete class and `Trait` is an [`ABCDispatch`][apfel.core.dispatch.ABCDispatch].
        ```python
        @impl(Class)
        class _(Trait):
            def method(self, f): \"""Concrete implementation goes here\"""

            @classmethod
            def class_method(cls, f): \"""Concrete implementation goes here\"""

            @staticmethod
            def static_method(f): \"""Concrete implementation goes here\"""
        ```
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
    For a declarative interface, use the [`@impl`][apfel.core.dispatch.impl] decorator.

    If the dispatchable class is an [`ABCDispatch`][apfel.core.dispatch.ABCDispatch] which does single dispatch,
    the `impl_for_args` param should be the type of the implementor class.

    Args:
        definition (type): The dispatchable class.
        impl (Mapping[str, Callable]): A mapping from method names to implementations.
        *impl_for_args: Arguments that the dispatch mechanism will use for selecting the implementation.
        **impl_for_kwargs: Keyword arguments that the dispatch mechanism will use for selecting the implementation.

    Example:
        ```python
        # The following imperative code ...
        add_impl(Trait, {"method": lambda self, f: f}, Class)

        # ... is equivalent to the following declarative code:
        @impl(Class)
        class _(Trait):
            def method(self, f): return f
        ```
    """
    for name, func in impl.items():
        getattr(definition, name).__dispatch__.add_impl(func, *impl_for_args, **impl_for_kwargs)
