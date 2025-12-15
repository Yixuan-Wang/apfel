import builtins

from apfel.core.common import identity, imperative, not_none, todo, unimplemented
from apfel.container.maybe import Maybe, just, nothing, some
from apfel.container.result import Result, ok, err, caught
from apfel.container.once import Once, Lazy

setattr(builtins, "identity", identity)
setattr(builtins, "imperative", imperative)
setattr(builtins, "todo", todo)
setattr(builtins, "unimplemented", unimplemented)

__all__ = [
    "identity", "imperative", "not_none", "todo", "unimplemented",
    "Maybe", "just", "nothing", "some",
    "Result", "ok", "err", "caught",
    "Once", "Lazy",
]
