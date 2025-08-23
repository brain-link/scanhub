#!/bin/bash
# Script to run ruff check on all services. Use option --fix to run ruff check --fix on all services.

if [ "$1" == --fix ]
then
    fixornot=--fix
else
    fixornot=""
fi

set -x  # @echo on

ruff check $fixornot services/base
ruff check $fixornot services/device-manager
ruff check $fixornot services/exam-manager
ruff check $fixornot services/patient-manager
ruff check $fixornot services/user-login-manager
ruff check $fixornot services/workflow-manager
ruff check $fixornot tools/device-sdk
