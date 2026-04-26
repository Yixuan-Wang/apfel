import builtins as _builtins

from apfel.core.common import apply, identity, imperative, not_none, pipe, todo, unimplemented
from apfel.core.iter import Iterator, itrt
from apfel.container.maybe import Maybe, just, nothing, some
from apfel.container.result import Result, ok, err, caught
from apfel.container.once import Once, Lazy

setattr(_builtins, "apply", apply)
setattr(_builtins, "identity", identity)
setattr(_builtins, "imperative", imperative)
setattr(_builtins, "pipe", pipe)
setattr(_builtins, "todo", todo)
setattr(_builtins, "unimplemented", unimplemented)

__all__ = [
    "apply", "identity", "imperative", "not_none", "pipe", "todo", "unimplemented",
    "Iterator", "itrt",
    "Maybe", "just", "nothing", "some",
    "Result", "ok", "err", "caught",
    "Once", "Lazy",
]
