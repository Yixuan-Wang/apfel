from types import BuiltinFunctionType, FunctionType

from apfel.core.dispatch import impl, add_impl
from . import Functor, Applicative, Monad


def do_impl_for_list():
    @impl(Functor)
    class _(list):
        def map(self, f):
            return [f(x) for x in self]

    @impl(Applicative)
    class _(list):
        @classmethod
        def pure(cls, x):
            return [x]

        def apply(self, f):
            return [f1(x) for f1 in f for x in self]

    @impl(Monad)
    class _(list):
        def bind(self, f):
            return [y for x in self for y in f(x)]


def do_impl_for_tuple():
    @impl(Functor)
    class _(tuple):
        def map(self, f):
            return tuple(f(x) for x in self)

    @impl(Applicative)
    class _(tuple):
        @classmethod
        def pure(cls, x):
            return (x,)

        def apply(self, f):
            return tuple(f1(x) for f1 in f for x in self)

    @impl(Monad)
    class _(tuple):
        def bind(self, f):
            return tuple(y for x in self for y in f(x))


def do_impl_for_set():
    @impl(Functor)
    class _(set):
        def map(self, f):
            return {f(x) for x in self}

    @impl(Applicative)
    class _(set):
        @classmethod
        def pure(cls, x):
            return {x}

        def apply(self, f):
            return {f1(x) for f1 in f for x in self}

    @impl(Monad)
    class _(set):
        def bind(self, f):
            return {y for x in self for y in f(x)}


def do_impl_for_dict():
    @impl(Functor)
    class _(dict):
        def map(self, f):
            return {k: f(v) for k, v in self.items()}


def do_impl_for_function():
    def map(self, f):
        return lambda *args, **kwargs: f(self(*args, **kwargs))
    
    def pure(cls, x):
        return lambda *_args, **_kwargs: x
    
    def apply(self, f):
        return lambda *args, **kwargs: f(*args, **kwargs)(self(*args, **kwargs))
    
    def bind(self, f):    
        return lambda *args, **kwargs: f(self(*args, **kwargs))(*args, **kwargs)

    add_impl(Functor, {
        "map": map,
    }, FunctionType)
    Functor.register(FunctionType)

    add_impl(Applicative, {
        "pure": pure,
        "apply": apply,
    }, FunctionType)
    Applicative.register(FunctionType)

    add_impl(Monad, {
        "bind": bind,
    }, FunctionType)
    Monad.register(FunctionType)


    # Built-in functions are treated as functions
    # which will be transformed into functions
    add_impl(Functor, {
        "map": map,
    }, BuiltinFunctionType)
    Functor.register(BuiltinFunctionType)

    add_impl(Applicative, {
        "pure": pure,
        "apply": apply,
    }, BuiltinFunctionType)
    Applicative.register(BuiltinFunctionType)

    add_impl(Monad, {
        "bind": bind,
    }, BuiltinFunctionType)
    Monad.register(BuiltinFunctionType)

    # type is also used as a constructor function
    add_impl(Functor, {
        "map": map,
    }, type)
    Functor.register(type)

    add_impl(Applicative, {
        "pure": pure,
        "apply": apply,
    }, type)
    Applicative.register(type)

    add_impl(Monad, {
        "bind": bind,
    }, type)
    Monad.register(type)
