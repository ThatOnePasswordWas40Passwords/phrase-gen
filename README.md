# phrasegen

> Generated sliding window ngrams of specified custommizations over a given body of text.
>
> Great for generating passphrase candidates with a focus on human memorization from a
> given source material.


## Why

Q: Many other tools for building wordlists from input material already exist, why bother
with this?

A: Sometimes less is more. When you _only_ want generated passphrases that maintain
original apperance ordering, this is the tool you want. A massive keyspace generated
by one of those other tools will contain these values, of course, but they also will
have many, many, many other non-interested in outputs.

## Installation

```bash
pip install phrasegen
```

## Usage

```bash
phrasegen -h
```

e.g Generating passphrases from a movie script, of exactly 4 phrases each, joined by a
`-` character, without having scrubbed any of the punctiation from the source material
before after joining, forcing all to lowercase, and storing in an output file `gen.txt`:

```bash
phrasegen --join-str "-" \
    --file movie_script.txt \
    --only-size 4 \
    --no-strip-punc \
    --lowercase \
    -o gen.txt
```
