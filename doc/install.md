# Installation


!!! warning
    This library is mainly personal and still in a very early stage. 
    We'll try to follow **Semantic Versioning**, but breaking changes should be expected. 
    If you are interested in using this library, please make sure to **lock** the version.


## Installation

This library is not published to PyPI.
You should install it directly from the GitHub repository.
Using `pyprojects.toml` and locking to a Git reference (e.g. a tag) is recommended.

### In `pyprojects.toml`

```toml
[package]
dependencies = [
    "apfel @ git+https://github.com/Yixuan-Wang/apfel.git@v{VERSION}"
]
```

### In `pyprojects.toml` with Poetry

```toml
[tool.poetry.dependencies]
apfel = { git = "https://github.com/Yixuan-Wang/apfel.git", tag = "v{VERSION}" }
```

### In `requirements.txt`

```plaintext
apfel @ git+https://github.com/Yixuan-Wang/apfel.git@v{VERSION}
```

### Direct Installation

```bash
pip install git+https://github.com/Yixuan-Wang/apfel.git@v{VERSION}
```
