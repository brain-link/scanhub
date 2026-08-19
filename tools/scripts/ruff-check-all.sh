#!/bin/bash
# Script to run ruff check on all services. Use option --fix to run ruff check --fix on all services.
# Can be run from anywhere; always operates relative to the repo root.

cd "$(dirname "${BASH_SOURCE[0]}")/../.." || exit 1

if [ "$1" == --fix ]
then
    fixornot=--fix
else
    fixornot=""
fi

set -x  # @echo on

(cd services/base/shared_libs && uv run ruff check $fixornot)
(cd services/device-manager && uv run ruff check $fixornot)
(cd services/protocol-manager && uv run ruff check $fixornot)
(cd services/patient-manager && uv run ruff check $fixornot)
(cd services/user-login-manager && uv run ruff check $fixornot)
(cd tools/device-sdk && uv run ruff check $fixornot)
