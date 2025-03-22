"""
`apfel.container.value` provides a container that simply wraps a value
designed to aid chained method calls.
"""

from apfel.core.monad import Functor

class Value(Functor):
    __slots__ = ("_value", )

    def __init__(self, value):
        self._value = value
        
        if hasattr(value, "__doc__"):
            self.__doc__ = value.__doc__

    def __class_getitem__(cls, item):
        return cls

    def __str__(self):
        return self._value.__str__()

    def __repr__(self):
        return f"<Value {self._value!r} at {hex(id(self))}>"

    def done(self):
        """
        Return the value wrapped inside the container.

        Unlike `unwrap` methods on other containers, this method will never raise
        exceptions.
        """
        return self._value

    def map(self, func):
        """
        Map a function over the `Value` container.
        """
        return Value(func(self._value))

    def mutate(self, func):
        """
        Call a function over the inner value, ignore the return value,
        and return the original container.

        The behavior is same as [`Value.tap`][apfel.container.value.Value.tap],
        just that the inner value is pragmatically allowed to
        be mutated in place.
        """

        func(self._value)
        return self

    def pipe(self, func):
        """
        Run the function to process the inner value, and place the
        result back to the container.

        Args:
            func (Callable[[T], R]): A function to mutate the value.

        Returns:
            (Value[R]): The mutated container itself.
        """
        self._value = func(self._value)
        return self

    def tap(self, func):
        """
        Call a function over the inner value, ignore the return value,
        and return the original container.

        See also [`also`](https://kotlinlang.org/docs/scope-functions.html#also){ .ref .kt }.

        Warning:
            Pragmatically, the function shall not mutate the inner value.
            If mutating the inner value is desired, see [`Value.mutate`][apfel.container.value.Value.mutate].
        """

        func(self._value)
        return self

