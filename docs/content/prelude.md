---
title: Prelude
description: Understand Apfel's package and builtins namespaces.
---

Apfel includes predefined namespace conveniences that make the library easier to use.

## Package namespace

Some common utilities are re-exported from the top-level `apfel` package and can be imported directly.

:::tip
The package namespace is properly typed. Prefer explicit imports from it instead of relying on the [builtins namespace](#builtins-namespace).
:::

## Builtins namespace

Some extremely common utilities are injected into Python's `builtins` namespace as module-level side effects. They are available after importing `apfel`.

:::caution
Use patched builtins only in a REPL or another interactive environment. They can confuse toolchains and collaborators.
:::

If you use Pyright, follow its [builtins extension documentation](https://github.com/microsoft/pyright/blob/main/docs/builtins.md) to enable autocompletion for these functions.

## Catalog

### Functions

| Module             | Function                                                                   | Package | Builtins |
| :----------------- | :------------------------------------------------------------------------- | :-----: | :------: |
| `core.common`      | [`apply`](/reference/core/common/#apfel.core.common.apply)                 |   Yes   |   Yes    |
| `core.common`      | [`identity`](/reference/core/common/#apfel.core.common.identity)           |   Yes   |   Yes    |
| `core.common`      | [`imperative`](/reference/core/common/#apfel.core.common.imperative)       |   Yes   |   Yes    |
| `core.common`      | [`not_none`](/reference/core/common/#apfel.core.common.not_none)           |   Yes   |          |
| `core.common`      | [`pipe`](/reference/core/common/#apfel.core.common.pipe)                   |   Yes   |   Yes    |
| `core.common`      | [`todo`](/reference/core/common/#apfel.core.common.todo)                   |   Yes   |   Yes    |
| `core.common`      | [`unimplemented`](/reference/core/common/#apfel.core.common.unimplemented) |   Yes   |   Yes    |
| `core.iter`        | [`itrt`](/reference/core/iter/#apfel.core.iter.itrt)                       |   Yes   |          |
| `container.maybe`  | [`just`](/reference/container/maybe/#apfel.container.maybe.just)           |   Yes   |          |
| `container.maybe`  | [`nothing`](/reference/container/maybe/#apfel.container.maybe.nothing)     |   Yes   |          |
| `container.maybe`  | [`some`](/reference/container/maybe/#apfel.container.maybe.some)           |   Yes   |          |
| `container.result` | [`ok`](/reference/container/result/#apfel.container.result.ok)             |   Yes   |          |
| `container.result` | [`err`](/reference/container/result/#apfel.container.result.err)           |   Yes   |          |
| `container.result` | [`caught`](/reference/container/result/#apfel.container.result.caught)     |   Yes   |          |

### Classes

| Module             | Class                                                                  | Package | Builtins |
| :----------------- | :--------------------------------------------------------------------- | :-----: | :------: |
| `core.iter`        | [`Iterator`](/reference/core/iter/#apfel.core.iter.Iterator)           |   Yes   |          |
| `container.maybe`  | [`Maybe`](/reference/container/maybe/#apfel.container.maybe.Maybe)     |   Yes   |          |
| `container.result` | [`Result`](/reference/container/result/#apfel.container.result.Result) |   Yes   |          |
| `container.once`   | [`Once`](/reference/container/once/#apfel.container.once.Once)         |   Yes   |          |
| `container.once`   | [`Lazy`](/reference/container/once/#apfel.container.once.Lazy)         |   Yes   |          |
