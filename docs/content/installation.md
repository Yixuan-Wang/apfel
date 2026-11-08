---
title: Installation
description: Instructions on installing the apfel package.
---

:::caution
Apfel is mainly personal and still at an early stage. The project aims to follow Semantic Versioning, but breaking changes should be expected. If you use it, lock the version.
:::

## Dependencies

Apfel requires Python 3.11 or later and depends on [`typing-extensions`](https://pypi.org/project/typing-extensions/).

## Install from PyPI

Apfel is published to PyPI as `apfel`. Install it with `pip`, `uv`, or another modern Python package manager.

```bash
pip install apfel
# or
uv add apfel
```

## Install from GitHub

Install directly from the GitHub repository when needed. Use `pyproject.toml` and lock a Git reference, such as a tag, whenever possible.

### pip

This is not recommended because `pip` does not lock the version.

```bash
pip install git+https://github.com/Yixuan-Wang/apfel.git@v{VERSION}
```

### uv

```bash
uv add git+https://github.com/Yixuan-Wang/apfel.git --tag "v{VERSION}"

# or

uv add git+https://github.com/Yixuan-Wang/apfel.git --ref "{COMMIT_SHA}"
```

### pdm

```bash
pdm add "apfel @ git+https://github.com/Yixuan-Wang/apfel.git@v{VERSION}"
```

### pyproject.toml

```toml
[project]
dependencies = [
    "apfel @ git+https://github.com/Yixuan-Wang/apfel.git@v{VERSION}"
]
```

### pyproject.toml with Poetry

```toml
[tool.poetry.dependencies]
apfel = { git = "https://github.com/Yixuan-Wang/apfel.git", tag = "v{VERSION}" }
```

### requirements.txt

```plaintext
apfel @ git+https://github.com/Yixuan-Wang/apfel.git@v{VERSION}
```
