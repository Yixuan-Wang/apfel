"""
Primitives for containers that can be written only once. Inspired by [`OnceCell`](https://doc.rust-lang.org/std/cell/struct.OnceCell.html){.ref .rs} and [`LazyCell`](https://doc.rust-lang.org/std/cell/struct.LazyCell.html){.ref .rs}.

The [`Once`][apfel.container.once.Once] and [`Lazy`][apfel.container.once.Lazy] classes, are exposed in the [:material-earth: package namespace](../prelude.md#package-namespace).

# Implementation

[`Once`][apfel.container.once.Once] takes reference from [`OnceCell`](https://doc.rust-lang.org/std/cell/struct.OnceCell.html){.ref .rs} and the current status is as follows:

| Reference [`OnceCell`](https://doc.rust-lang.org/std/cell/struct.OnceCell.html){ .ref .rs } | Counterpart |
| --- | --- |
| `get` | [:material-check-circle:][apfel.container.once.Once.get] |
| `get_mut` | :material-minus-circle: |
| `get_mut_or_init` | :material-minus-circle: |
| `get_mut_or_try_init` | :material-minus-circle: |
| `get_or_init` | [:material-check-circle:][apfel.container.once.Once.get_or_init] |
| `get_or_try_init` | :material-close-circle: |
| `into_inner` | :material-close-circle: |
| `new` | :material-close-circle: |
| `set` | [:material-check-circle:][apfel.container.once.Once.set] |
| `take` | :material-close-circle: |
| `try_insert` | :material-close-circle: |
"""

import apfel.container.maybe as _maybe
import apfel.container.result as _result


class Once:
    """
    A container that can be written only once.
    See [`OnceCell`](https://doc.rust-lang.org/std/cell/struct.OnceCell.html){.ref .rs} for more information.

    This class is exposed in the [:material-earth: package namespace](../prelude.md#package-namespace).
    """

    __slots__ = ("_value", "_has_value")

    def __init__(self):
        """
        Create an unpopulated `Once` container.

        Returns:
            container (Once): An unpopulated `Once` container.
        """
        self._value = ...
        self._has_value = False

    def __class_getitem__(cls, item):
        return cls

    @classmethod
    def of_hint(cls, type, /):
        """
        Create a `Once` container hinting the given type.

        Args:
            type (Type[T]): The type of the value to be stored in the `Once` container.

        Returns:
            container (Once[T]): A `Once` container hinting the given type.
        """
        return cls()

    def __bool__(self):
        """
        Check if the `Once` container has been set.

        Returns:
            is_set (bool): `True` if the `Once` container has been set, `False` otherwise.
        """
        return self._has_value

    def get(self):
        """
        Get the inner value of the `Once` container if it has been set.

        Returns:
            value (Maybe[T]): A `Just`-wrapped inner value of the `Once` container if it has been set, a `Nothing` otherwise.
        """
        if self._has_value:
            return _maybe.Maybe.make_just(self._value)
        return _maybe.Maybe.make_nothing()

    def get_or_init(self, f, /):
        """
        Get the inner value of the `Once` container, or initialize it with the given function if no value has been set.

        Args:
            f (Callable[[], T]): The function to initialize the `Once` container with if no value has been set.

        Returns:
            value (T): The inner value (maybe newly set) of the `Once` container.
        """
        if not self._has_value:
            self._value = f()
            self._has_value = True

        return self._value

    def set(self, value):
        """
        Set the inner value of the `Once` container.
        If a value has already been set, this method returns an `Err` containing the existing value.

        Args:
            value (T): The value to set the `Once` container to.

        Returns:
            result (Result[None, T]):
                `Ok(None)` if the value was set successfully.
                `Err(value)` if the value has already been set, containing the existing value.
        """
        if self._has_value:
            return _result.err(self._value)
        self._value = value
        self._has_value = True
        return _result.ok(None)

    def unwrap(self):
        """
        Get the inner value of the `Once` container.
        If no value has been set, this method raises a `ValueError`.

        Returns:
            value (T): The inner value of the `Once` container.

        Raises:
            ValueError: If no value has been set.
        """
        if not self._has_value:
            raise ValueError("called `Once.unwrap()` on an unset value.")

        return self._value


class OnceLock:
    """
    A thread-safe version of [`Once`][apfel.container.once.Once].
    See [`OnceLock`](https://doc.rust-lang.org/std/sync/struct.OnceLock.html){.ref .rs} for more information.
    """

    __slots__ = ("_value", "_has_value", "_lock")

    def __init__(self):
        """
        Create an unpopulated `OnceLock` container.

        Returns:
            container (OnceLock): An unpopulated `OnceLock` container.
        """
        import threading

        self._value = ...
        self._has_value = False
        self._lock = threading.Lock()

    def __class_getitem__(cls, item):
        return cls

    def __bool__(self):
        """
        Check if the `OnceLock` container has been set.

        Returns:
            is_set (bool): `True` if the `OnceLock` container has been set, `False` otherwise.
        """
        with self._lock:
            return self._has_value

    def get(self):
        """
        Get the inner value of the `OnceLock` container if it has been set.

        Returns:
            value (Maybe[T]): A `Just`-wrapped inner value of the `OnceLock` container if it has been set, a `Nothing` otherwise.
        """
        with self._lock:
            if self._has_value:
                return _maybe.Maybe.make_just(self._value)
            return _maybe.Maybe.make_nothing()

    def get_or_init(self, f, /):
        """
        Get the inner value of the `OnceLock` container, or initialize it with the given function if no value has been set.

        Args:
            f (Callable[[], T]): The function to initialize the `OnceLock` container with if no value has been set.

        Returns:
            value (T): The inner value (maybe newly set) of the `OnceLock`
        """
        with self._lock:
            if not self._has_value:
                self._value = f()
                self._has_value = True

            return self._value

    def set(self, value):
        """
        Set the inner value of the `OnceLock` container.
        If a value has already been set, this method returns an `Err` containing the existing value.

        Args:
            value (T): The value to set the `OnceLock` container to.

        Returns:
            result (Result[None, T]):
                `Ok(None)` if the value was set successfully.
                `Err(value)` if the value has already been set, containing the existing value.
        """
        with self._lock:
            if self._has_value:
                return _result.err(self._value)
            self._value = value
            self._has_value = True
            return _result.ok(None)

    def unwrap(self):
        """
        Get the inner value of the `OnceLock` container.
        If no value has been set, this method raises a `ValueError`.

        Returns:
            value (T): The inner value of the `OnceLock` container.

        Raises:
            ValueError: If no value has been set.
        """
        with self._lock:
            if not self._has_value:
                raise ValueError("called `OnceLock.unwrap()` on an unset value.")
            return self._value


class Lazy:
    """
    A container that can be lazily initialized only once.
    The stored function will be actually called only on the first retrieval, and the result will be cached for consequent calls.
    See [`LazyCell`](https://doc.rust-lang.org/std/cell/struct.LazyCell.html){.ref .rs} for more information.

    This class is exposed in the [:material-earth: package namespace](../prelude.md#package-namespace).

    Example:
        ```python
        from apfel.container.once import Lazy

        @Lazy
        def f():
            print("called")
            return object()

        obj = f.value()
        # print "called"
        # here, the function `f` will be called and the result will be cached.

        f.value() is obj # the function `f` will not be called again.
        ```
    """

    __slots__ = ("_value", "_has_value", "_init")

    def __init__(self, f, /):
        """
        Create a lazily initialized `Lazy` container.

        Args:
            f (Callable[[], T]): The function to be lazily initialized.
        """
        self._value = ...
        self._has_value = False
        self._init = f

    def __class_getitem__(cls, item):
        return cls

    def __bool__(self):
        return self._has_value

    def __call__(self):
        """
        An alias for [`Lazy.value`][apfel.container.once.Lazy.value].
        Notice that this operator overloading might be slower than calling `value` directly.

        Example:
            ```python
            @Lazy
            def f():
                return object()

            obj = f()
            assert f() is obj
            ```
        """
        if self._has_value:
            return self._value

        self._value = self._init()
        self._has_value = True
        return self._value

    def unwrap(self):
        """
        Get the inner value of the `Lazy` container.
        If no value has been set, this method raises a `ValueError`.

        Returns:
            value (T): The lazily initialized value of the `Lazy` container.

        Raises:
            ValueError: If no value has been set.
        """
        if not self._has_value:
            raise ValueError("Called `Lazy.unwrap()` on an uninitialized value.")

        return self._value

    def value(self):
        """
        Get the inner value of the `Lazy` container.
        If no value has been set, this method initializes the value with the stored function.

        Returns:
            value (T): The lazily initialized value of the `Lazy` container.
        """
        if self._has_value:
            return self._value

        self._value = self._init()
        self._has_value = True
        return self._value


class LazyLock:
    """
    A thread-safe version of [`Lazy`][apfel.container.once.Lazy].
    See [`LazyCell`](https://doc.rust-lang.org/std/cell/struct.LazyCell.html){.ref .rs} for more information.
    """

    __slots__ = ("_value", "_has_value", "_init", "_lock")

    def __init__(self, f, /):
        """
        Create a thread-safe lazily initialized `LazyLock` container.

        Args:
            f (Callable[[], T]): The function to be lazily initialized.
        """
        import threading

        self._value = ...
        self._has_value = False
        self._init = f
        self._lock = threading.Lock()

    def __class_getitem__(cls, item):
        return cls

    def __bool__(self):
        with self._lock:
            return self._has_value

    def __call__(self):
        """
        An alias for [`LazyLock.value`][apfel.container.once.LazyLock.value].
        Notice that this operator overloading might be slower than calling `value` directly.

        Example:
            ```python
            from apfel.container.once import LazyLock

            lazy_lock = LazyLock(lambda: object())
            obj = lazy_lock()
            assert lazy_lock() is obj
            ```
        """
        with self._lock:
            if self._has_value:
                return self._value

            self._value = self._init()
            self._has_value = True
            return self._value

    def unwrap(self):
        """
        Get the inner value of the `LazyLock` container.
        If no value has been set, this method raises a `ValueError`.

        Returns:
            value (T): The inner value of the `LazyLock` container.

        Raises:
            ValueError: If no value has been set.
        """
        with self._lock:
            if not self._has_value:
                raise ValueError("called `LazyLock.unwrap()` on an unset value.")
            return self._value

    def value(self):
        """
        Get the inner value of the `LazyLock` container.
        If no value has been set, this method initializes the value with the stored function.

        Returns:
            value (T): The lazily initialized value of the `LazyLock` container.
        """
        with self._lock:
            if self._has_value:
                return self._value

            self._value = self._init()
            self._has_value = True
            return self._value
