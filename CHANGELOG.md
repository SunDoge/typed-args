# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.10.0]

- Add `Arg(positional=True)`, which forces a field to be a positional argument even when
  it has a default. Previously a field with a default and no option strings was always
  routed to a `--flag` (the `foo: int = 5` → `--foo` idiom), so an optional positional
  with its own fallback could not be expressed — the default had to be handled out of
  band. `path: Annotated[str, Arg(nargs="?", positional=True)] = "fallback"` now yields a
  positional that argparse honours the default for when omitted. Existing behaviour is
  unchanged: fields without `positional=True` keep the flag idiom.

## [0.6.4]

- Parse doc for class as description.
- Parse doc for class attributes as help.

## [0.6.3]

- Update `class TypedArgs`.

## [0.6.2]

- Add `ta.TypedArgs` for better intellisense.

## [0.6.1]

- Add `@overload` for API.

## [0.6.0]

- Support `add_argument_group`
- Support `add_subparsers`
- Rename `from_args`, `from_known_args` to `parse_args` and `parse_known_args` because `Args` is now a `ArgumentParser`.

## [0.5.2]

- Don't remmber what I changed.


## [0.5.1]

- Fix default argument. `add_argument(default=[])` now init the correct `[]` for dataclass.

## [0.5.0]

- Function `add_argument` accepts `type` now and we don't check the type annotations in dataclass fields. This make `typed-args` less strict but more easy to use.
- Python 3.6 is supported now. Python 3.5 should work but I didn't test it.

## [0.4.2]

- make `@classmethod` return correct type

## [0.4.1]

- Add `__repr__`.
- Add a comparison between `argparse` and `TypedArgs`.
- Fix NotImplementedError.

## [0.4.0]

- Use `parser_factory()` to create `parser`.
- Support optional parsing. If not using `add_argument` function, attributes will not be parsed.

## [0.3.7]

- Fix `repr`.

## [0.3.6]

- Support `pickle`.

## [0.3.0]

- Assign attributes by name and type
- `parser` is initialized inside class.

## [0.2.0]

- Define `parser` as a local variable.

## [0.1.0]

- Define `parser` as a global varaible.
- Replace attributes by name

[unreleased]: https://github.com/SunDoge/typed-args
[0.10.0]: https://github.com/SunDoge/typed-args/tree/v0.10.0
[0.6.4]: https://github.com/SunDoge/typed-args/tree/v0.6.4
[0.6.3]: https://github.com/SunDoge/typed-args/tree/v0.6.3
[0.6.2]: https://github.com/SunDoge/typed-args/tree/v0.6.2
[0.6.1]: https://github.com/SunDoge/typed-args/tree/v0.6.1
[0.6.0]: https://github.com/SunDoge/typed-args/tree/v0.6.0
[0.5.2]: https://github.com/SunDoge/typed-args/tree/v0.5.2
[0.5.1]: https://github.com/SunDoge/typed-args/tree/v0.5.1
[0.5.0]: https://github.com/SunDoge/typed-args/tree/v0.5.0
[0.4.2]: https://github.com/SunDoge/typed-args/tree/v0.4.2
[0.4.1]: https://github.com/SunDoge/typed-args/tree/v0.4.1
[0.4.0]: https://github.com/SunDoge/typed-args/tree/v0.4.0
[0.3.7]: https://github.com/SunDoge/typed-args/tree/v0.3.7
[0.3.6]: https://github.com/SunDoge/typed-args/tree/v0.3.6
[0.3.0]: https://github.com/SunDoge/typed-args/tree/v0.3
[0.2.0]: https://github.com/SunDoge/typed-args/tree/v0.2
[0.1.0]: https://github.com/SunDoge/typed-args/tree/v0.1
