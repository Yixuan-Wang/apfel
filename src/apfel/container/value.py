"""
`apfel.container.value` provides a container that simply wraps a value
designed to aid chained method calls.

See also [`Identity`](https://hackage.haskell.org/package/base/docs/Data-Functor-Identity.html){ .ref .hs }.
"""

from apfel.core.monad import Monad


class Value(Monad):
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

    def apply(self, func, /):
        """
        Apply a function wrapped inside a `Value` to the inner value.
        Implementation of [`Applicative.apply`][apfel.core.monad.Applicative.apply].

        Args:
            func (Value[Callable[[T], R]]): A `Value` containing a function to apply.

        Returns:
            (Value[R]): A new `Value` containing the result of the function application.
        """
        return Value(func._value(self._value))  # pyright: ignore[reportAttributeAccessIssue]

    def bind(self, func, /):
        """
        Monadically bind a function that maps the inner value to a new `Value`.
        Implementation of [`Monad.bind`][apfel.core.monad.Monad.bind].

        Args:
            func (Callable[[T], Value[R]]): A function that takes the inner value and returns a `Value`.

        Returns:
            (Value[R]): A new `Value` containing the result of the function.
        """
        return func(self._value)

    def done(self):
        """
        Return the value wrapped inside the container.

        Unlike `unwrap` methods on other containers, this method will never raise
        exceptions.
        """
        return self._value

    def map(self, func, /):
        """
        Map a function over the `Value` container. Implementation of [`Functor.map`][apfel.core.monad.Functor.map].

        Args:
            func (Callable[[T], U]): A function to transform the inner value.

        Returns:
            (Value[U]): A new `Value` containing the transformed value.
        """
        return Value(func(self._value))

    def mutate(self, func, /):
        """
        Call a function to mutate the inner value in place.

        The function's return value is ignored, and the container keeps the
        original inner reference.
        This is similar to [`Value.tap`][apfel.container.value.Value.tap],
        just hinting the mutating intention of the function.

        Args:
            func (Callable[[T], Any]): A function that mutates the inner value.

        Returns:
            (Value[T]): The mutated container itself.
        """
        func(self._value)
        return self

    @classmethod
    def pure(cls, value, /):
        """
        Wrap a value into the `Value` container.
        Implementation of [`Applicative.pure`][apfel.core.monad.Applicative.pure].

        Args:
            value (T): The value to wrap.

        Returns:
            (Value[T]): A new instance of `Value` with the value wrapped.
        """
        return cls(value)

    def run(self, func, /):
        """
        Run a function to process the inner value, and return the result.

        Args:
            func (Callable[[T], R]): A function to process the value.

        Returns:
            (R): The result of the function.
        """
        return func(self._value)

    def tap(self, func, /):
        """
        Call a function over the inner value, ignore the return value,
        and return the original container.

        See also [`also`](https://kotlinlang.org/docs/scope-functions.html#also){ .ref .kt }.

        Warning:
            Pragmatically, the function shouldn't mutate the inner value.
            Use the [`Value.mutate`][apfel.container.value.Value.mutate] method instead.
        """

        func(self._value)
        return self

    def update(self, func, /):
        """
        Update the inner value with the result of a function.

        Warning:
            Compare to [`Value.map`][apfel.container.value.Value.map], this method
            mutates the container in place. No new container is created.
            Therefore, the function must return a result of the same type as the
            previous inner type of the container.

        Args:
            func (Callable[[T], T]): A function to transform the inner value.

        Returns:
            (Value[T]): The mutated container itself.
        """
        self._value = func(self._value)
        return self
