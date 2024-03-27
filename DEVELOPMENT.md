# phrasegen development docs

## Requirements

* Python >= 3.9.x
* `pip`
    * `pre-commit`
* GNU utils (`make`, `sed`)
* bash
* Optionally, `direnv` to manage project-based venv

### Sourcing per-project venv if using `direnv`

After changing to this project's directory,

```bash
direnv allow .
```

Note that this requires the version currently laid out in the [.envrc](./.envrc) file;
thi can either be available via `pyenv` installed version, or directly via the `python3.xx`
command.

## Installing dependencies

```bash
make install-deps
```

## Building

```bash
make
```

## Testing

```bash
make test
```

## Submitting changes

Be sure to have installed the project's pre-commit hooks, and that all checks are passing
before commiting to a change PR:

```bash
pip install pre-commit
pre-commit install -c ./.pre-commit-config.yaml
pre-commit run --all-files
```
