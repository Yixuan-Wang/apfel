from functools import partial as _partial
from inspect import (
    signature as _signature,
    Parameter as _Parameter,
)

def partial(func, *args, **kwargs):
    """An alternative implementation of functools.partial.

    Note that this implementation has a bug:
    ```python
    def f(a, b, c): ...

    partial(1, 2)(3)           # This will not work because 3 is passed as `a`
    functools.partial(1, 2)(3) # This works
    """
    sig = _signature(func)
    if args:
        _new_args = []
        for arg, param in zip(args, sig.parameters.values()):
            if param.kind == _Parameter.POSITIONAL_OR_KEYWORD:
                kwargs[param.name] = arg
            else:
                _new_args.append(arg)
        args = tuple(_new_args)
    
    return _partial(func, *args, **kwargs)
