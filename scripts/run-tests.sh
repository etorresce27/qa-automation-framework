#!/usr/bin/env bash
set -e

SUITE="${1:-smoke}"

mkdir -p artifacts test-results
touch artifacts/.keep
echo "Running suite: $SUITE"
pytest -m "$SUITE" --junitxml="test-results/results.xml" -q
