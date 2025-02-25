from apfel.core.dispatch import impl
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
