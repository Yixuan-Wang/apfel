"""
Primitive for a container that can be written only once. Inspired by [`OnceCell`](https://doc.rust-lang.org/std/cell/struct.OnceCell.html){.ref .rs} and [`LazyCell`](https://doc.rust-lang.org/std/cell/struct.LazyCell.html){.ref .rs}.

# Implementation

| Reference [`OnceCell`](https://doc.rust-lang.org/std/cell/struct.OnceCell.html){ .ref .rs } | Counterpart |
| --- | --- |
| `get` | :material-close-circle: |
| `get_mut` | :material-minus-circle: |
| `get_mut_or_init` | :material-minus-circle: |
| `get_mut_or_try_init` | :material-minus-circle: |
| `get_or_init` | [:material-check-circle:][apfel.container.once.Once.get_or_init] |
| `get_or_try_init` | :material-close-circle: |
| `into_inner` | :material-close-circle: |
| `new` | :material-close-circle: |
| `set` | [:material-dots-horizontal-circle:][apfel.container.once.Once.set] |
| `take` | :material-close-circle: |
| `try_insert` | :material-close-circle: |

"""

from functools import wraps


class Once:
    """
    A container that can be written only once.
    See [`OnceCell`](https://doc.rust-lang.org/std/cell/struct.OnceCell.html){.ref .rs} for more information.
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

    def __class_getitem__(cls, value_type):
        return cls

    def __bool__(self):
        """
        Check if the `Once` container has been set.

        Returns:
            is_set (bool): `True` if the `Once` container has been set, `False` otherwise.
        """
        return self._has_value

    def set(self, value):
        """
        Set the inner value of the `Once` container.
        If a value has already been set, this method currently does nothing.

        Args:
            value (T): The value to set the `Once` container to.

        Experimental:
            This method will return a `Result` type in the future.
        """
        if self._has_value:
            return
        self._value = value
        self._has_value = True

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
    

def lazy_init(func):
    """
    Decorator to turn a function into a lazy initializer.
    The decorated function will be actually called only on the first call, and the result will be cached for consequent calls.
    See [`LazyCell`](https://doc.rust-lang.org/std/cell/struct.LazyCell.html){.ref .rs} for more information.

    Args:
        func (Callable[[], T]): The function to be lazily initialized.
    
    Returns:
        func (Callable[[], T]): The function that can be used as a getter.
    """
    is_called = False
    result = ...

    @wraps(func)
    def wrapper():
        nonlocal is_called, result

        if is_called:
            return result
        
        result = func()
        is_called = True
        return result
    
    return wrapper
