#!/usr/bin/env python

"""Module to genreate a list of all possible slices given an input."""

import string
from argparse import ArgumentParser, ArgumentTypeError, Namespace
from os.path import exists
from typing import Generator, Iterator, Sequence


def valid_file(file_path: str) -> str:
    """Check whether a given path is an existent file.

    If not, raises and ArgumentTypeError, as the intended purpose of
    this helper utility is a type for an argparse argument.

    Args:
        file_path (str): The path to the file to check exists.
    """
    if not exists(file_path):
        raise ArgumentTypeError(f"{file_path} does not exist")
    return file_path


def _cli():
    parser = ArgumentParser(
        description="Generate ordered phrases from an input body of text.",
        add_help=True,
    )
    parser.add_argument(
        "--lowercase", action="store_true", help="Force all output to be lowercase"
    )
    parser.add_argument(
        "--no-strip-punc",
        action="store_true",
        help="Don't remove all punctuation from source.",
    )
    parser.add_argument(
        "--strip-punc",
        default=string.punctuation,
        help=(
            "Remove all punctuation in the specified set from source; "
            + "by default is all of 'string.punctuation'"
        ),
    )
    parser.add_argument(
        "--max-size",
        type=int,
        default=0,
        help="Maximum number of words in generated phrases; default unlimited",
    )
    parser.add_argument(
        "--only-size",
        type=int,
        help="If specified, will _only_ output generated phrases of this size.",
    )
    parser.add_argument(
        "--join-str",
        default="",
        help=(
            "Char/string to join the individual words from the source with. "
            + "By default, is ''"
        ),
    )
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument(
        "--file",
        type=valid_file,
        help="Path to local file to use as input.",
    )
    source.add_argument(
        "--input", type=str, help="Input sentence to generate phrases from"
    )
    parser.add_argument(
        "--output-file",
        "-o",
        help="output file to write to. If not specified, will write to STDOUT.",
    )
    return parser.parse_args()


def _find_ngrams(input_list: Sequence[str], n: int) -> Iterator[str]:
    return zip(*[input_list[i:] for i in range(n)])


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
        p = (
            args.join_str.join(line).lower()
            if args.lowercase
            else args.join_str.join(line)
        )
        if not args.no_strip_punc:
            p = p.translate(
                str.maketrans("", "", args.strip_punc.replace(args.join_str, ""))
            )
        if not p:
            continue
        yield p


def load_file(fname: str) -> str:
    """Load and return a local file as a string."""
    with open(fname) as infile:
        return infile.read().strip()


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
