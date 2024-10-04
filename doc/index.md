# Apfel

🍎 `apfel` stands for A Personal Functional Extension Library, which provides a set of basic utilities designed for academic experiments.

!!! note ""
    [Apfel](https://en.wiktionary.org/wiki/Apfel#German) is the Deutsch word for apple.

## Motivation

Originally, the word 'functional' comes from the functional programming paradigm.
However, Python is not inherently a functional programming language,
and it is functional incomplete in many aspects.

To fulfill my personal needs of writing elegant (and possibly efficient) code for 
academic experiments evolving in an agile way,
and to avoid pulling in less-maintained or less-documented third-party libraries,
a personal toolkit is a better choice.

It provides common helper functions, data types and sublanguages
that aim to counter the missing features and design flaws of Python language itself.
Heavy use of meta-programming, type hints and functional programming techniques
are expected.

## Design Goals

- **Unpythonic**.
  Use best practices and API naming conventions from other languages,
  especially [:simple-rust: Rust](https://doc.rust-lang.org/stable/std),
  [:simple-haskell: Haskell](https://hoogle.haskell.org/?scope=set%3Aincluded-with-ghc)
  and [:simple-julia: Julia](https://docs.julialang.org/en/v1) to mitigate Python's limitations.

- **Type safe**.
  Add expressive and sound type hints whenever possible.

- **Low cost abstraction**.
  Try to use the most efficient underlying implementation.

- **Minimal dependencies**.
  The library is kept (almost) self-contained, except those listed inside [dependencies](/install#dependencies).