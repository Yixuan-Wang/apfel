# Apfel

🍎 `apfel` stands for A Python Functional Extras Library, which provides a set of quality-of-life utilities designed for agile experiments.

!!! note "Trivia"
    [Apfel](https://en.wiktionary.org/wiki/Apfel#German) is the Deutsch word for apple.

## Motivation

Python is not inherently a functional programming language. However, functional style
can often lead to clearer and more concise code.

To fulfill my personal needs of writing elegant (and possibly efficient) code for 
evolving in an agile way (i.e. research oriented, iterative, and exploratory),
and to avoid pulling in less-maintained or less-documented third-party libraries,
a personal small toolkit is a better choice.

It provides common helper functions, data types and containers
that aim to counter the missing features and design flaws of Python language itself.
Heavy use of meta-programming, type hints and of course, functional programming techniques,
are expected.

## Design Goals

- **Unpythonic**.
  Use best practices and API naming conventions from other languages,
  especially <a class="ref rust" href="https://doc.rust-lang.org/stable/std">Rust</a>,
  <a class="ref haskell" href="https://hoogle.haskell.org/?scope=set%3Aincluded-with-ghc">Haskell</a>,
  <a class="ref rlang" href="https://www.rdocumentation.org/">R</a>,
  and <a class="ref julia" href="https://docs.julialang.org/en/v1">Julia</a> to mitigate Python's limitations.
  <a class="ref golang" href="https://go.dev/">Go</a> is also a good reference for simplicity and readability comparable to Python.

- **Type safe**.
  Add expressive and sound type hints whenever possible.

- **Low cost abstraction**.
  Try to use the most efficient underlying implementation.

- **Minimal dependencies**.
  The library is kept (almost) self-contained, except those listed inside [dependencies](install.md#dependencies).

## Acknowledgement

The apple logo used in the document is from the [Noto Color Emoji](https://fonts.google.com/specimen/Noto+Color+Emoji) font by Google.
