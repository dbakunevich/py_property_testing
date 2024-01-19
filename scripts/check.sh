#! /bin/bash

set -e

poetry run black property_testing/. --check
poetry run black tests/. --check

poetry run mypy property_testing/.
poetry run mypy tests/.

poetry run flake8 property_testing/.
poetry run flake8 tests/.

poetry run pytest