#!/bin/bash
# Script to run mypy check on all services.
# Can be run from anywhere; always operates relative to the repo root.
#
# mypy has no config-inheritance mechanism (unlike ruff's `extend`), and needs each
# service's own synced environment to resolve imports, so each still gets its own
# invocation — but all point --config-file at the shared [tool.mypy] block in the
# root pyproject.toml, passing only their target dir (and, for device-sdk, --strict)
# as local overrides.

cd "$(dirname "${BASH_SOURCE[0]}")/../.." || exit 1

set -x  # @echo on

(cd services/base/shared_libs && uv run mypy --config-file ../../../pyproject.toml src)
(cd services/device-manager && uv run mypy --config-file ../../pyproject.toml app)
(cd services/protocol-manager && uv run mypy --config-file ../../pyproject.toml app)
(cd services/patient-manager && uv run mypy --config-file ../../pyproject.toml app)
(cd services/user-login-manager && uv run mypy --config-file ../../pyproject.toml app)
(cd device-sdk && uv run mypy --config-file ../pyproject.toml --strict src)
