from ._definition import Functor, Applicative, Monad

fmap = Functor.map

__all__ = ["Functor", "Applicative", "Monad", "fmap"]
