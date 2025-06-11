#!/bin/bash
# filepath: /home/schote/code/scanhub/scanhub-ui/scripts/generate-clients.sh

set -e

echo "Deleting existing generated client code..."
rm -rf src/generated-client

echo "Creating directory for OpenAPI JSON files..."
mkdir -p openapi-jsons

echo "Fetching OpenAPI JSON files from API endpoints..."
# Use curl with default https port (443) if not using a custom port
# curl https://localhost/api/v1/patient/openapi.json --cacert ../secrets/certificate.pem --output openapi-jsons/patient-openapi.json
# curl https://localhost/api/v1/exam/openapi.json --cacert ../secrets/certificate.pem --output openapi-jsons/exam-openapi.json
# curl https://localhost/api/v1/userlogin/openapi.json --cacert ../secrets/certificate.pem --output openapi-jsons/userlogin-openapi.json
# curl https://localhost/api/v1/workflowmanager/openapi.json --cacert ../secrets/certificate.pem --output openapi-jsons/workflowmanager-openapi.json
# curl https://localhost/api/v1/device/openapi.json --cacert ../secrets/certificate.pem --output openapi-jsons/device-openapi.json
# Use curl with custom port (8443) if your API is running on that port, used for development
curl https://localhost:8443/api/v1/patient/openapi.json --cacert ../secrets/certificate.pem --output openapi-jsons/patient-openapi.json
curl https://localhost:8443/api/v1/exam/openapi.json --cacert ../secrets/certificate.pem --output openapi-jsons/exam-openapi.json
curl https://localhost:8443/api/v1/userlogin/openapi.json --cacert ../secrets/certificate.pem --output openapi-jsons/userlogin-openapi.json
curl https://localhost:8443/api/v1/workflowmanager/openapi.json --cacert ../secrets/certificate.pem --output openapi-jsons/workflowmanager-openapi.json
curl https://localhost:8443/api/v1/device/openapi.json --cacert ../secrets/certificate.pem --output openapi-jsons/device-openapi.json


echo "Generating TypeScript clients using OpenAPI Generator..."
openapi-generator-cli generate -i openapi-jsons/patient-openapi.json -g typescript-axios -o src/generated-client/patient --additional-properties=supportsES6=true,typescriptNullable=false
openapi-generator-cli generate -i openapi-jsons/exam-openapi.json -g typescript-axios -o src/generated-client/exam --additional-properties=supportsES6=true,typescriptNullable=false
openapi-generator-cli generate -i openapi-jsons/userlogin-openapi.json -g typescript-axios -o src/generated-client/userlogin --additional-properties=supportsES6=true,typescriptNullable=false
openapi-generator-cli generate -i openapi-jsons/workflowmanager-openapi.json -g typescript-axios -o src/generated-client/workflowmanager --additional-properties=supportsES6=true,typescriptNullable=false
openapi-generator-cli generate -i openapi-jsons/device-openapi.json -g typescript-axios -o src/generated-client/device --additional-properties=supportsES6=true,typescriptNullable=false

echo "Cleaning up temporary OpenAPI JSON files..."
rm -rf openapi-jsons

echo "Client generation complete."