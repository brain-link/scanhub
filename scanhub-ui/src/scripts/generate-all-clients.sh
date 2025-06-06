#!/bin/bash
# filepath: /home/schote/code/scanhub/scanhub-ui/scripts/generate-clients.sh

set -e

# Delete existing generated client code
rm -rf src/generated-client

# Curl commands to fetch OpenAPI JSON files
curl https://localhost/api/v1/patient/openapi.json --cacert ../secrets/certificate.pem --output openapi-jsons/patient-openapi.json
curl https://localhost/api/v1/exam/openapi.json --cacert ../secrets/certificate.pem --output openapi-jsons/exam-openapi.json
curl https://localhost/api/v1/userlogin/openapi.json --cacert ../secrets/certificate.pem --output openapi-jsons/userlogin-openapi.json
curl https://localhost/api/v1/workflowmanager/openapi.json --cacert ../secrets/certificate.pem --output openapi-jsons/workflowmanager-openapi.json
curl https://localhost/api/v1/device/openapi.json --cacert ../secrets/certificate.pem --output openapi-jsons/device-openapi.json

# Generate TypeScript clients using OpenAPI Generator
openapi-generator-cli generate -i openapi-jsons/patient-openapi.json -g typescript-axios -o src/generated-client/patient --additional-properties=supportsES6=true,typescriptNullable=false
openapi-generator-cli generate -i openapi-jsons/exam-openapi.json -g typescript-axios -o src/generated-client/exam --additional-properties=supportsES6=true,typescriptNullable=false
openapi-generator-cli generate -i openapi-jsons/userlogin-openapi.json -g typescript-axios -o src/generated-client/userlogin --additional-properties=supportsES6=true,typescriptNullable=false
openapi-generator-cli generate -i openapi-jsons/workflowmanager-openapi.json -g typescript-axios -o src/generated-client/workflowmanager --additional-properties=supportsES6=true,typescriptNullable=false
openapi-generator-cli generate -i openapi-jsons/device-openapi.json -g typescript-axios -o src/generated-client/device --additional-properties=supportsES6=true,typescriptNullable=false

# Clean up
rm -rf openapi-jsons