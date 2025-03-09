import importlib
import importlib.machinery
from collections.abc import Sequence, Callable
from types import ModuleType

class TransformSourceFileLoader(importlib.machinery.SourceFileLoader):
    def __init__(self, fullname: str, path: str, *, hook: Sequence[Callable[[str], str]]) -> None: ...
    def get_data(self, path: str) -> bytes: ...

    # set_data is deliberately not typed, as it is wiped out as a no-op

class TransformPathFinder(importlib.machinery.PathFinder):
    _hook_registry: dict[str, list[Callable[[str], str]]]

    @classmethod
    def find_spec(
        cls, fullname: str, path: Sequence[str] | None = None, target: ModuleType | None = None
    ) -> importlib.machinery.ModuleSpec | None: ...

def register_transform_hook(name: str, hook: Callable[[str], str]) -> None: ...
