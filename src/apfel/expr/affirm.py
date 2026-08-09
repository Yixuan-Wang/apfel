"""
The expression form of [:python `assert`](https://docs.python.org/3/reference/simple_stmts.html#the-assert-statement),
and related helper functions.

Also see [:rust `assert!`](https://doc.rust-lang.org/std/macro.assert.html).

## Usage

[`affirm`][apfel.expr.affirm.affirm] allows asserting a value according to a predicate,
  returning the value if the assertion is satisfied,
  or raising an `AssertionError` with detailed information if not.

Similar to the builtin [:python `assert`](https://docs.python.org/3/reference/simple_stmts.html#the-assert-statement),
  the `affirm` function will be a no-op when Python is run with optimizations (the [:python `-O` flag](https://docs.python.org/3/using/cmdline.html#cmdoption-O), or setting [:python `__debug__`](https://docs.python.org/3/library/constants.html#debug__) to `False`).


Tip:
    Specifically, the `AssertionError` message will include the full expression passed to `affirm`,
      not just the evaluated value.
    Different predicates can customize the error message to provide more context.

    ```python
    >>> affirm(operator.mul(2, 3), lambda x: x % 2)
    AssertionError: `operator.mul(2, 3)` evals to 6, which does not satisfy `lambda x: x % 2`.
    >>> affirm(1 or None, type[bool, str])
    AssertionError: `1 or None` evals to 1, which is of type int, expected one of [bool, str].
    ```

Some available forms of predicates:

- **Unspecified or `None`**: evaluate the truthiness of the value.
  ```python
  affirm(1)  # OK, 1
  affirm(0)  # raises AssertionError
  ```
- **Callable**: a function that takes the value and returns a boolean.
  If a `lambda` function is used, its source code will be included in the error message.
  ```python
  affirm(5, lambda x: x > 0)   # OK, 5
  affirm(-3, lambda x: x > 0)  # raises AssertionError
  ```
- **An [`AffirmPredicate`][apfel.expr.affirm.AffirmPredicate]**: a more complex predicate that can customize the failure message.
  ```python
  affirm(True, type[int])  # OK, True (bool is a subclass of int)
  affirm(True, type[str])  # raises AssertionError
  ```
- **Boolean**: an expression that is directly evaluated to a boolean.
  Any value that can be converted to boolean is accepted.
  ```python
  affirm(False, True)    # OK, False
  affirm(True, False)    # raises AssertionError
  ```

Tip:
    If you want to assert a value is not `None`, which is a much more common use case,
    use the [`apfel.not_none`][apfel.core.common.not_none] function instead.

    If you do not want an exception to be raised, use [`apfel.container.Maybe`][apfel.container.maybe.Maybe]:
    ```python
    just(value).filter(predicate)
    ```

"""

from abc import abstractmethod
import ast
from functools import lru_cache
import sys
import textwrap
from types import FunctionType, GenericAlias

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override

from apfel.core.dispatch import ABCDispatch, impl
from apfel.experimental.introspect import call_expr


def affirm(value, predicate=None):
    """
    Assert the value according to the predicate, return it if it is true.
    This is the expression form of [:python `assert`](https://docs.python.org/3/reference/simple_stmts.html#the-assert-statement).

    See module-level documentation for detailed usage.

    Args:
        value (T): The value to be asserted.
        predicate (Callable[[T], bool] | bool | None): The predicate to be used for assertion. If None, evaluate the truthiness of the value.

    Returns:
        T: The value asserted.

    Raises:
        AssertionError: If the value is not true.
    """

    if __debug__:
        if predicate is None:
            predicate = bool

        # Run the predicate on the value
        ok = True
        if isinstance(predicate, AffirmPredicate):
            if not AffirmPredicate.test(predicate, value):
                ok = False
        elif callable(predicate):
            if not predicate(value):
                ok = False
        else:
            if not predicate:
                ok = False

        # If the assertion fails, detail the reason
        if not ok:
            # Get the string representation of the value
            _args = call_expr()
            argument_expr = _args[0] if _args and len(_args) > 0 else None

            fail_message = ""
            if predicate is bool:
                fail_message = (
                    "{argument_expr} evals to {value_str}, which is not true."
                )
            elif callable(predicate):
                if (
                    isinstance(predicate, FunctionType)
                    and predicate.__name__ == "<lambda>"
                ):
                    if _args and len(_args) > 1:
                        node_predicate = _args[1]
                        if isinstance(node_predicate, ast.Lambda):
                            arg_predicate = ast.unparse(node_predicate)
                            fail_message = f"{{argument_expr}} evals to {{value_str}}, which does not satisfy `{arg_predicate}`."
                elif isinstance(predicate, AffirmPredicate):
                    fail_message = AffirmPredicate.fail_message(
                        predicate, argument_expr=argument_expr, value=value
                    )
                else:
                    fail_message = f"{{argument_expr}} evals to {{value_str}}, which does not satisfy `{predicate.__name__}`."
            else:
                if _args and len(_args) > 1:
                    arg_predicate = ast.unparse(_args[1])
                    fail_message = f"{{argument_expr}} evals to {{value_str}}, which does not satisfy `{arg_predicate}`."
                else:
                    fail_message = f"{{argument_expr}} evals to {{value_str}}, which does not satisfy `{predicate!r}`."

            if fail_message == "":
                fail_message = "{argument_expr} evals to {value_str}, which does not satisfy the predicate."

            fail_message = fail_message.format(
                argument_expr="`{}`".format(
                    ast.unparse(argument_expr)
                    if argument_expr is not None
                    else "<unknown>"
                ),
                value_str=textwrap.shorten(repr(value), width=80, placeholder="..."),
                value=value,
                predicate=predicate,
            )
            exc = AssertionError(fail_message)
            raise exc

    # The assertion is satisfied
    return value


class AffirmPredicate(ABCDispatch):
    """
    An abstract base class for complex predicates within the `affirm` function.
    """

    @abstractmethod
    def test(self, value) -> bool:
        """
        Test if the value satisfies the predicate.

        Args:
            value (T): The value to be tested.

        Returns:
            bool: Whether the value satisfies the predicate.
        """
        return True

    def __call__(self, value) -> bool:
        """
        Test if the value satisfies the predicate.
        This function enforces returning a boolean value.

        Args:
            value (T): The value to be tested.

        Returns:
            bool: Whether the value satisfies the predicate.
        """
        return bool(self.test(value))

    @abstractmethod
    def fail_message(self, *, argument_expr: ast.expr | None, value) -> str:
        """
        When the predicate fails, convert inputs to a formattable string explaining the reason.

        Args:
            argument_expr (ast.expr | None): The AST expression of the argument passed to `affirm`, before evaluation. May be `None` if not available.
            value (T): The actual value being affirmed.

        Returns:
            str: A string explaining the reason for failure.
        """
        return "{argument_expr} evals to {value_str}, which does not satisfy {predicate!r}."


def _visualize_type(ty: type) -> str:
    if hasattr(ty, "__module__") and ty.__module__ != "builtins":
        return f"{ty.__module__}.{ty.__qualname__}"
    else:
        return ty.__qualname__


@impl(AffirmPredicate)
class _(GenericAlias):
    def test(self, value):
        if self.__origin__ is not type:
            raise NotImplementedError(
                "Only type[...] GenericAlias is supported as `affirm` predicate."
            )

        return isinstance(value, self.__args__)

    def fail_message(self, *, argument_expr: ast.expr | None, value) -> str:
        if len(self.__args__) == 1:
            ty = self.__args__[0]
            return f"{{argument_expr}} evals to {{value_str}}, which is of type {_visualize_type(type(value))}, expected {_visualize_type(ty)}."
        else:
            ty_names = [_visualize_type(ty) for ty in self.__args__]
            ty_names = f"[{', '.join(ty_names)}]"
            return f"{{argument_expr}} evals to {{value_str}}, which is of type {_visualize_type(type(value))}, expected one of {ty_names}."


class is_type(AffirmPredicate):
    """
    Assert whether the value is exactly the specified type.
    """

    ty = object

    @override
    def test(self, value) -> bool:
        return type(value) is self.ty

    @override
    def __call__(self, value) -> bool:
        return type(value) is self.ty

    @classmethod
    @lru_cache
    def type(cls, ty):
        instance = cls()
        instance.ty = ty
        return instance

    def __class_getitem__(cls, item):
        if isinstance(item, type):
            return cls.type(item)
        else:
            raise TypeError(f"Expected a type within ty[...], got {type(item)}.")

    @override
    def fail_message(self, *, argument_expr: ast.expr | None, value) -> str:
        return f"{{argument_expr}} evals to {{value_str}}, which is of type {_visualize_type(type(value))}, expected {_visualize_type(self.ty)}."
