from apfel.core.common import identity, imperative, not_none, todo, unimplemented
import builtins

setattr(builtins, "identity", identity)
setattr(builtins, "imperative", imperative)
setattr(builtins, "todo", todo)
setattr(builtins, "unimplemented", unimplemented)

__all__ = ["identity", "imperative", "not_none", "todo", "unimplemented"]
