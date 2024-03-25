"""Generic and misc. utilities."""


def load_file(fname: str) -> str:
    """Load and return a local file as a string."""
    with open(fname) as infile:
        return infile.read().strip()
