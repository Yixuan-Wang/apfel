from apfel.core._common import identity, todo, unimplemented
import builtins

setattr(builtins, "identity", identity)
setattr(builtins, "todo", todo)
setattr(builtins, "unimplemented", unimplemented)

__all__ = ["identity", "todo", "unimplemented"]
