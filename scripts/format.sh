#!/usr/bin/env bash
set -x

ruff check fapi tests docs_src scripts --fix
ruff format fapi tests docs_src scripts
