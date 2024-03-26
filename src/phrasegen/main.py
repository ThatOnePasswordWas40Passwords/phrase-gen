#!/usr/bin/env python

"""Module to genreate a list of all possible slices given an input."""

from argparse import Namespace
from typing import Generator, Iterator, Sequence

from phrasegen.cli import _cli  # pyright: ignore
from phrasegen.utils import load_file


def _find_ngrams(input_list: Sequence[str], n: int) -> Iterator[str]:
    return zip(*[input_list[i:] for i in range(n)])  # type: ignore


def gen_slices(
    input_material: str, args: Namespace
) -> Generator[Sequence[str], None, None]:
    """Generate all possible slices from a given string.

    Args:
        input_material (str): The input string to generate all slices for.
        args (Namespace): Passed CLI arguments to the program.

    Returns:
        Generator[Sequence[str], None, None]: Slice representing a generated phrase
        from the source material.
    """
    if args.only_size:
        yield from _find_ngrams(
            [x.strip() for x in input_material.split()], args.only_size
        )
    else:
        for chunk_size in range(1, args.max_size + 1):
            yield from _find_ngrams(
                [x.strip() for x in input_material.split()], chunk_size
            )


def format_phrase(args: Namespace) -> Generator[str, None, None]:
    """Wrap ngram generation for normalizing generated phrase according to CLI options.

    Args:
        args (Namespace): Passed CLI arguments.

    Yields:
        Generator[str, None, None]: A generator of strings represented formatted ngram
        phrases from the source material.
    """
    for line in gen_slices(args.input if args.input else load_file(args.file), args):
        if args.pascal_case:
            line = [word.title() for word in line]

        p = args.join_str.join(line)

        if args.lowercase:
            p = p.lower()
        elif args.uppercase:
            p = p.upper()

        if not args.no_strip_punc:
            p = p.translate(
                str.maketrans("", "", args.strip_punc.replace(args.join_str, ""))
            )
        if not p:
            continue
        yield p


def main() -> None:
    """Main module."""
    args = _cli()

    if args.output_file:
        with open(args.output_file, "w") as outfile:
            for p in format_phrase(args):
                outfile.write(p + "\n")
    else:
        for p in format_phrase(args):
            print(p)


if __name__ == "__main__":
    main()
