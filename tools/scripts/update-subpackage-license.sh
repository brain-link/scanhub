#!/usr/bin/env bash
set -euo pipefail

# Run from repo root, where LICENSE files are
REPO_ROOT="$(pwd)"

# License files at repo root
LICENSE_FILES=(
  "LICENSE"
  "LICENSE.GPL3"
  "LICENSE.GPL3-EXCEPT"
)

# Verify license files exist
for lf in "${LICENSE_FILES[@]}"; do
  if [ ! -f "$REPO_ROOT/$lf" ]; then
    echo "X Missing required license file: $lf"
    exit 1
  fi
done

# Explicit list of subpackage directories
SUBPACKAGES=(
  "services/base/shared_libs"
  "services/device-manager"
  "services/exam-manager"
  "services/orchestration-engine"
  "services/patient-manager"
  "services/user-login-manager"
  "services/workflow-manager"
  "tools/device-sdk"
)

# Copy license files into each listed subpackage
for subpkg in "${SUBPACKAGES[@]}"; do
  if [ -d "$REPO_ROOT/$subpkg" ]; then
    echo "- Copying license files into $subpkg"
    for lf in "${LICENSE_FILES[@]}"; do
      cp "$REPO_ROOT/$lf" "$REPO_ROOT/$subpkg/"
    done
  else
    echo "~ Skipping $subpkg (not found)"
  fi
done

echo "Done, license files copied to all subpackages."