#!/usr/bin/env bash

autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place hydra --exclude=__init__.py
black hydra
isort --recursive --apply hydra