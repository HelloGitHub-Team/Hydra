#!/usr/bin/env bash
set -x
# 只检测不自动修改
#mypy --config-file .mypy.ini hydra
black hydra --check
isort --recursive --check-only hydra
flake8 --config .flake8 hydra