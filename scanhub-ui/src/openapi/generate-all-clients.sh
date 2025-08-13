#!/bin/bash
# filepath: /home/schote/code/scanhub/scanhub-ui/scripts/generate-clients.sh

set -e

echo "Deleting existing generated client code..."
rm -rf src/openapi/generated-client

echo "Creating directory for OpenAPI JSON files..."
mkdir -p src/openapi/openapi-jsons

echo "Fetching OpenAPI JSON files from API endpoints..."
# Use curl with custom port (8443) if your API is running on that port, used for development
curl https://localhost:8443/api/v1/patient/openapi.json \
    --cacert ../secrets/certificate.pem \
    --output src/openapi/openapi-jsons/patient-openapi.json
curl https://localhost:8443/api/v1/exam/openapi.json \
    --cacert ../secrets/certificate.pem \
    --output src/openapi/openapi-jsons/exam-openapi.json
curl https://localhost:8443/api/v1/userlogin/openapi.json \
    --cacert ../secrets/certificate.pem \
    --output src/openapi/openapi-jsons/userlogin-openapi.json
curl https://localhost:8443/api/v1/workflowmanager/openapi.json \
    --cacert ../secrets/certificate.pem \
    --output src/openapi/openapi-jsons/workflowmanager-openapi.json
curl https://localhost:8443/api/v1/device/openapi.json \
    --cacert ../secrets/certificate.pem \
    --output src/openapi/openapi-jsons/device-openapi.json


echo "Generating TypeScript clients using OpenAPI Generator..."
openapi-generator-cli generate \
    -i src/openapi/openapi-jsons/patient-openapi.json \
    -g typescript-axios \
    -o src/openapi/generated-client/patient \
    -t src/openapi/templates/typescript-axios \
    --additional-properties=supportsES6=true,typescriptNullable=false
openapi-generator-cli generate \
    -i src/openapi/openapi-jsons/exam-openapi.json \
    -g typescript-axios \
    -o src/openapi/generated-client/exam \
    -t src/openapi/templates/typescript-axios \
    --additional-properties=supportsES6=true,typescriptNullable=false
openapi-generator-cli generate \
    -i src/openapi/openapi-jsons/userlogin-openapi.json \
    -g typescript-axios \
    -o src/openapi/generated-client/userlogin \
    -t src/openapi/templates/typescript-axios \
    --additional-properties=supportsES6=true,typescriptNullable=false
openapi-generator-cli generate \
    -i src/openapi/openapi-jsons/workflowmanager-openapi.json \
    -g typescript-axios \
    -o src/openapi/generated-client/workflowmanager \
    -t src/openapi/templates/typescript-axios \
    --additional-properties=supportsES6=true,typescriptNullable=false
openapi-generator-cli generate \
    -i src/openapi/openapi-jsons/device-openapi.json \
    -g typescript-axios \
    -o src/openapi/generated-client/device \
    -t src/openapi/templates/typescript-axios \
    --additional-properties=supportsES6=true,typescriptNullable=false

echo "Cleaning up temporary OpenAPI JSON files..."
rm -rf src/openapi/openapi-jsons

echo "Client generation complete."


# echo "Patching client barrels for default forwarding..."
# ./src/openapi/patch-client-barrels.sh