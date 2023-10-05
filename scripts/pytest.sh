#!/usr/bin/env bash
set -e
set -x

source $(poetry env info --path)/bin/activate
pytest
