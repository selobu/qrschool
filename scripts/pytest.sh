#!/usr/bin/env bash

set -e
set -x

poetry shell
pytest
