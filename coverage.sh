#!/usr/bin/env bash
set -euo pipefail

pipenv run pytest -v \
  --cov=src/application/use_cases \
  --cov-report=term-missing \
  --cov-report=html \
  --cov-fail-under=90 \
  tests/
