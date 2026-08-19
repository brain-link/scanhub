#!/bin/bash
# Script to run `uv sync` for all services, populating each service's own .venv
# with its full dependency set (all extras and groups: lint, test, docs, ...).
# Can be run from anywhere; always operates relative to the repo root.

cd "$(dirname "${BASH_SOURCE[0]}")/../.." || exit 1

set -x  # @echo on

(cd services/base/shared_libs && uv sync --all-extras --all-groups)
(cd services/device-manager && uv sync --all-extras --all-groups)
(cd services/protocol-manager && uv sync --all-extras --all-groups)
(cd services/patient-manager && uv sync --all-extras --all-groups)
(cd services/user-login-manager && uv sync --all-extras --all-groups)
(cd services/orchestration-engine && uv sync --all-extras --all-groups)
(cd tools/device-sdk && uv sync --all-extras --all-groups)
