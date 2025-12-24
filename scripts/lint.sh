#!/usr/bin/env bash

set -e
set -x

mypy fapi
ruff check fapi tests docs_src scripts
ruff format fapi tests --check
