---
title: Introduction
description: Motivation and design goals of the package.
---

:::note[Trivia]
[Apfel](https://en.wiktionary.org/wiki/Apfel#German) is the German word for apple.
:::

## Motivation

Python is not inherently a functional programming language. However, a functional style can often lead to clearer and more concise code.

Apfel is a small personal toolkit for research-oriented, iterative, and exploratory work. It provides helpers, data types, and containers that address practical gaps in Python while avoiding less-maintained or less-documented third-party dependencies. Expect extensive use of metaprogramming, type hints, and functional programming techniques.

## Design goals

- **Unpythonic.** Apfel borrows best practices and API naming conventions from [:rust Rust](https://doc.rust-lang.org/stable/std), [:haskell Haskell](https://hoogle.haskell.org/?scope=set%3Aincluded-with-ghc), [:rlang R](https://www.rdocumentation.org/), and [:julia Julia](https://docs.julialang.org/en/v1) to mitigate Python's limitations. [:golang Go](https://go.dev/) is another useful reference for simplicity and readability.
- **Type safe.** Add expressive and sound type hints whenever possible.
- **Low-cost abstraction.** Use the most efficient underlying implementation where practical.
- **Minimal dependencies.** Keep the library almost self-contained, apart from its [runtime dependency](https://pypi.org/project/typing-extensions/).

## Acknowledgement

The apple logo uses the [Noto Color Emoji](https://fonts.google.com/specimen/Noto+Color+Emoji) font by Google.
