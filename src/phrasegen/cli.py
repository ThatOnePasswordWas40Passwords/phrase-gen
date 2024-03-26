"""Command line parsing utilities."""

from argparse import ArgumentParser, ArgumentTypeError, Namespace
from os.path import exists
from string import punctuation


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


def _cli() -> Namespace:  # pyright: ignore
    parser = ArgumentParser(
        description="Generate ordered phrases from an input body of text.",
        add_help=True,
    )
    parser.add_argument(
        "--no-strip-punc",
        action="store_true",
        help="Don't remove all punctuation from source.",
    )
    parser.add_argument(
        "--strip-punc",
        default=punctuation,
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
    capitalization = parser.add_mutually_exclusive_group(required=False)
    capitalization.add_argument(
        "--pascal-case",
        action="store_true",
        help="Force generated phrases to BeJoinedWithPascalCase",
        default=False,
    )
    capitalization.add_argument(
        "--lowercase",
        action="store_true",
        help="Force all output to be lowercase",
        default=False,
    )
    capitalization.add_argument(
        "--uppercase",
        action="store_true",
        help="Force all output to be uppercase",
        default=False,
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
