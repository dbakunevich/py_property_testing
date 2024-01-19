#! /bin/bash

set -e

poetry run black property_testing/. --check
poetry run black tests/. --check

poetry run mypy property_testing/.
poetry run mypy tests/.

poetry run flake8 property_testing/.
poetry run flake8 tests/.

PROPERTY_TESTING=1 poetry run pytest

# PROPERTY_TESTING=1 poetry run python examples/
