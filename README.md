# safari-to-sqlite

[![PyPI](https://img.shields.io/pypi/v/safari-to-sqlite.svg)](https://pypi.org/project/safari-to-sqlite/)
[![Lint](https://github.com/hbmartin/safari-to-sqlite/actions/workflows/lint.yml/badge.svg)](https://github.com/hbmartin/safari-to-sqlite/actions/workflows/lint.yml)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Code style: black](https://img.shields.io/badge/🐧️-black-000000.svg)](https://github.com/psf/black)
[![Checked with pytype](https://img.shields.io/badge/🦆-pytype-437f30.svg)](https://google.github.io/pytype/)
[![Versions](https://img.shields.io/pypi/pyversions/safari-to-sqlite.svg)](https://pypi.python.org/pypi/safari-to-sqlite)
[![discord](https://img.shields.io/discord/823971286308356157?logo=discord&label=&color=323338)](https://discord.gg/EE7Hx4Kbny)
[![twitter](https://img.shields.io/badge/@hmartin-00aced.svg?logo=twitter&logoColor=black)](https://twitter.com/hmartin)

Save tabs from Safari to a SQLite database. Multiple devices can be synced with Turso. Search and explore with [Datasette](https://datasette.io/)!

- [How to install](#how-to-install)
- [Usage](#usage)
- [Authentication](#authentication)

## How to install

This package is available on PyPI and can be installed with pipx:

```bash
brew install pipx
pipx install safari-to-sqlite
```

## Usage

To save your Safari tabs to a SQLite database, run:

```bash
safari-to-sqlite
```

This will save the tabs to a file called `safari-tabs.db` in your current directory.

Or to specify a database file:

```bash
safari-to-sqlite tabs.db
```

## Authentication
Cross device sync is possible using a [Turso](https://turso.tech) account. 
You can configure your own database or allow this tool to automatically perform setup for you.
To authenticate, run:

```bash
safari-to-sqlite auth
```

If you don't have an existing Turso account or database, no problem!
This command will walk you through the setup process by installing the Turso CLI with brew and creating a new database for you.
Otherwise, you can manually enter your own database URL and token.

## Roadmap to 0.2
- Add scraping for when full page content is missing from Safari

## Development

Pull requests are very welcome! For major changes, please open an issue first to discuss what you would like to change.

### Setup

```bash
git clone git@github.com:hbmartin/safari-to-sqlite.git
cd safari-to-sqlite
> **Note:** Ensure that Python 3 is installed on your system before running these commands.

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m safari_to_sqlite
```

### Code Formatting

This project is linted with [ruff](https://docs.astral.sh/ruff/) and uses [Black](https://github.com/psf/black) code formatting.

## Authors

* [Harold Martin](https://www.linkedin.com/in/harold-martin-98526971/) - harold.martin at gmail

## License

© [Harold Martin](https://www.linkedin.com/in/harold-martin-98526971/) - released under [Apache-2.0 license](LICENSE.txt)

Safari is a registered trademark of Apple Inc.