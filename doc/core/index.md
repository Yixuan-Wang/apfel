# Core 

Core utilities functions that are directly exposed by the `apfel` package.

These functions are injected to the `builtins` namespace and can be used directly
  as soon as the `apfel` package is imported.
If you are using Pyright, you can follow the [builtins extension](https://github.com/microsoft/pyright/blob/main/docs/builtins.md) documentation to enable autocompletion for these functions.

::: apfel
    options:
        members:
          - identity
          - todo
          - unimplemented
