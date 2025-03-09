from apfel.core._common import identity, imperative, todo, unimplemented
import builtins

setattr(builtins, "identity", identity)
setattr(builtins, "imperative", imperative)
setattr(builtins, "todo", todo)
setattr(builtins, "unimplemented", unimplemented)

__all__ = ["identity", "imperative", "todo", "unimplemented"]
