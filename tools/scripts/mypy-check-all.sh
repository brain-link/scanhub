#!/bin/bash
# Script to run mypy check on all services.
# Can be run from anywhere; always operates relative to the repo root.

cd "$(dirname "${BASH_SOURCE[0]}")/../.." || exit 1

set -x  # @echo on

(cd services/base/shared_libs && uv run mypy)
(cd services/device-manager && uv run mypy)
(cd services/protocol-manager && uv run mypy)
(cd services/patient-manager && uv run mypy)
(cd services/user-login-manager && uv run mypy)
(cd tools/device-sdk && uv run mypy)
