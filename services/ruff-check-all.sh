#!/bin/bash
# Script to run ruff check on all services. Use option --fix to run ruff check --fix on all services.

source .env/bin/activate

if [ "$1" == --fix ]
then
    fixornot=--fix
else
    fixornot=""
fi

set -x  # @echo on

ruff check $fixornot base
ruff check $fixornot device-manager
ruff check $fixornot exam-manager
ruff check $fixornot mri/recos
ruff check $fixornot mri/sequence-manager
ruff check $fixornot patient-manager
ruff check $fixornot user-login-manager
ruff check $fixornot workflow-manager
