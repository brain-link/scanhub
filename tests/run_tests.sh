#!/bin/bash
# Script to run all tests.

cd services/exam-manager
source .env/bin/activate
pytest
deactivate
