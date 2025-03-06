"""
This module provides a low-level hook mechanism to transform the source code of a package or module during its import.
It must be imported **before** any other packages and modules that you want to hook.

!!! warning "Effectful"
    This package has an effectful behavior: modifying the `sys.meta_path` finder list, which will affect **the import process**, and is **sensitive to the order of imports**.

Normally you would use adapters defined in the `impt` package, instead of directly using the low level [`register_transform_hook`][apfel.impt.transform.register_transform_hook] function.
"""

import sys
import _io
import _frozen_importlib_external

PYCACHE_SUFFIX = ".pyc"


class TransformSourceFileLoader(_frozen_importlib_external.SourceFileLoader):
    """
    A subclass of [`importlib.machinery.SourceFileLoader`](https://docs.python.org/3/library/importlib.html#importlib.machinery.SourceFileLoader){ .ref .py }
    that applies all registered hooks to the source code of a module or package during import.

    !!! note "Implementation"
        This loader will directly read the source code from the `.py` file, completely ignoring the `.pyc` file.
        The transformed source code will not have a bytecode cache (`.pyc`) generated.
        If your file system has high latency, this may slow down the import process.
    """

    def __init__(self, fullname, path, *, hook) -> None:
        super().__init__(fullname, path)
        self.hook = hook

    def get_data(self, path: str) -> bytes:
        if path.endswith(PYCACHE_SUFFIX):
            path = _frozen_importlib_external.source_from_cache(path)

        with _io.open(path, "r") as f:
            source = f.read()
            for hook in self.hook:
                source = hook(source)
        return source.encode("utf-8")

    def set_data(self, path, data, *, _mode: int = 0o666):
        pass


class TransformPathFinder(_frozen_importlib_external.PathFinder):
    """
    A subclass of [`importlib.machinery.PathFinder`](https://docs.python.org/3/library/importlib.html#importlib.machinery.PathFinder){ .ref .py }
    that injects [`TransformSourceFileLoader`][apfel.impt.transform.TransformSourceFileLoader] to the import process.
    """
    _hook_registry = {}

    @classmethod
    def find_spec(cls, fullname, path=None, target=None):
        if fullname not in cls._hook_registry:
            return None

        spec = super().find_spec(fullname, path, target)
        if (
            spec is not None
            and spec.origin is not None
            and isinstance(spec.loader, _frozen_importlib_external.SourceFileLoader)
        ):
            spec.loader = TransformSourceFileLoader(
                fullname, spec.origin, hook=cls._hook_registry[spec.name]
            )
        else:
            raise ImportError(
                f"Cannot hook {fullname}, as no valid source file is found.", fullname
            )

        return spec


def register_transform_hook(name, hook):
    """
    Register a hook function to replace the source code of a module or package.

    Args:
        name (str): The name of the module or package to hook.
        hook (Callable[[str], str]): The hook function that takes the original source code as input and returns the transformed source code. 
    """
    if name not in TransformPathFinder._hook_registry:
        TransformPathFinder._hook_registry[name] = []
    TransformPathFinder._hook_registry[name].append(hook)


# Register the hook path finder
sys.meta_path.insert(0, TransformPathFinder)

__all__ = [
    "TransformSourceFileLoader",
    "TransformPathFinder",
    "register_transform_hook",
]
