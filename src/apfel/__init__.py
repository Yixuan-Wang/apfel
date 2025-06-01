from apfel.core._common import not_none, identity, imperative, todo, unimplemented
import builtins

setattr(builtins, "not_none", not_none)
setattr(builtins, "identity", identity)
setattr(builtins, "imperative", imperative)
setattr(builtins, "todo", todo)
setattr(builtins, "unimplemented", unimplemented)

__all__ = ["not_none", "identity", "imperative", "todo", "unimplemented"]
