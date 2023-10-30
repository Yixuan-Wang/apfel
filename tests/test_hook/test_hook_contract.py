from inspect import isclass
from typing import Generator, cast, TypeVar

import apfel.effect.hook as module_hook
from apfel.effect.hook import HookLike


def all_hook_like() -> Generator[type[HookLike], None, None]:
    return (
        cast(type[HookLike], obj)
        for name in dir(module_hook)
        if (obj := getattr(module_hook, name))
        and isclass(obj)
        and obj != HookLike
        and issubclass(obj, HookLike)
    )


def init_hook_like(cls: type[HookLike]) -> HookLike:
    if cls is module_hook.Hook:
        return module_hook.Hook("test")
    else:
        raise NotImplementedError


def test_hook_register_identity():
    for cls in all_hook_like():
        instance = init_hook_like(cls)

        def func():
            pass

        assert instance.register(func) is func
