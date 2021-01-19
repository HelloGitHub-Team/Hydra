#!/usr/bin/env bash

set -e
set -x

pytest -s --cov=hydra --cov-report=term-missing hydra/tests
