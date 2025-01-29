#!/bin/bash
# Script to run all tests.

cd services/exam-manager
source .env/bin/activate
pytest
echo "Please consider that failed tests might in some cases leave database entries behind."
deactivate
