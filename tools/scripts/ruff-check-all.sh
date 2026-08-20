#!/bin/bash
# Script to run ruff check across every service. Use option --fix to run ruff check --fix.
# Can be run from anywhere; always operates relative to the repo root.
#
# A single invocation is enough: ruff resolves each file's config from the nearest
# pyproject.toml (which extends the shared [tool.ruff] base in the root pyproject.toml),
# so this already respects each service's own overrides without looping per directory.

cd "$(dirname "${BASH_SOURCE[0]}")/../.." || exit 1

if [ "$1" == --fix ]
then
    fixornot=--fix
else
    fixornot=""
fi

set -x  # @echo on

uv run ruff check $fixornot services/base/shared_libs/src services/device-manager/app services/protocol-manager/app services/patient-manager/app services/user-login-manager/app
(cd tools/device-sdk && uv run ruff check $fixornot src)
