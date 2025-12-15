# Prelude

`apfel` comes with a set of predefined namespace tricks to help you use the library more effectively.

## Package Namespace

Shown as :material-earth: in the documentation.

Some common utilities are re-exported to the package-top `apfel` namespace.
These can be directly imported from the `apfel` package.

!!! Tip
    The package namespace is properly typed, so it's best to explicitly use these instead of relying on [builtins namespace](#builtins-namespace).

## Builtins Namespace

Shown as :material-airballoon: in the documentation.

Some extremely common utilities are injected to the `builtins` namespace as module-level side effects.
These can be used directly in the code as soon as the `apfel` package is imported.

!!! Tip
    It is recommended only to use these in REPL or other interactive environments, as patched builtins may cause confusion in toolchains and collaborators.


If you are using Pyright, you can follow the [builtins extension](https://github.com/microsoft/pyright/blob/main/docs/builtins.md) documentation to enable autocompletion for these functions.

## Catalog

### Functions

| Module | Function | Package? | Builtins? |
| : --- | :--- | :--: | :--: |
| `core.common` | [`identity`][apfel.core.common.identity] | :material-earth: | :material-airballoon: |
| `core.common` | [`imperative`][apfel.core.common.imperative] | :material-earth: | :material-airballoon: |
| `core.common` | [`not_none`][apfel.core.common.not_none] | :material-earth: |  |
| `core.common` | [`todo`][apfel.core.common.todo] | :material-earth: | :material-airballoon: |
| `core.common` | [`unimplemented`][apfel.core.common.unimplemented] | :material-earth: |:material-airballoon: |
| `container.maybe` | [`just`][apfel.container.maybe.just] | :material-earth: |  |
| `container.maybe` | [`nothing`][apfel.container.maybe.nothing] | :material-earth: |  |
| `container.maybe` | [`some`][apfel.container.maybe.some] | :material-earth: |  |
| `container.result` | [`ok`][apfel.container.result.ok] | :material-earth: |  |
| `container.result` | [`err`][apfel.container.result.err] | :material-earth: |  |
| `container.result` | [`caught`][apfel.container.result.caught] | :material-earth: |  |

### Classes

| Module | Class | Package? | Builtins? |
| : --- | :--- | :--: | :--: |
| `container.maybe` | [`Maybe`][apfel.container.maybe.Maybe] | :material-earth: |  |
| `container.result` | [`Result`][apfel.container.result.Result] | :material-earth: |  |
| `container.once` | [`Once`][apfel.container.once.Once] | :material-earth: |  |
| `container.once` | [`Lazy`][apfel.container.once.Lazy] | :material-earth: |  |
