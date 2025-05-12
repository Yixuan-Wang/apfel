"""
`apfel.container.value` provides a container that simply wraps a value
designed to aid chained method calls.
"""

from apfel.core.monad import Functor


class Value(Functor):
    __slots__ = ("_value",)

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

    def pipe(self, func):
        """
        Run a function to process the inner value.
        If a result is produced, the result will be put back to the container.
        Otherwise, the original reference within the container will be kept.


        Warning:
            Compare to [`Value.map`][apfel.container.value.Value.map], this method
            mutates the container in place. No new container is created.
            Therefore, the function must return a result of the same type as the
            previous inner type of the container, or return `None`.

        Args:
            func (Callable[[T], T] | Callable[[T], None]): A function to process the value.

        Returns:
            (Value[T]): The mutated container itself.
        """
        val = func(self._value)
        self._value = val if val is not None else self._value
        return self

    def run(self, func):
        """
        Run a function to process the inner value, and return the result.

        Args:
            func (Callable[[T], R]): A function to process the value.

        Returns:
            (R): The result of the function.
        """
        return func(self._value)

    def tap(self, func):
        """
        Call a function over the inner value, ignore the return value,
        and return the original container.

        See also [`also`](https://kotlinlang.org/docs/scope-functions.html#also){ .ref .kt }.

        Warning:
            Pragmatically, the function shouldn't mutate the inner value.
            Use the [`Value.pipe`][apfel.container.value.Value.pipe] method instead.
        """

        func(self._value)
        return self
