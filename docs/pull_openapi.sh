#!/bin/bash
# filepath: /home/schote/code/scanhub/scanhub-ui/scripts/generate-clients.sh

set -e

echo "Deleting existing json files..."
rm -rf source/_openapi

echo "Creating directory for OpenAPI JSON files..."
mkdir -p source/_openapi


echo "Fetching OpenAPI JSON files from API endpoints..."
# Use curl with custom port (8443) if your API is running on that port, used for development
curl https://localhost:8443/api/v1/patient/openapi.json \
    --cacert ../secrets/certificate.pem \
    --output source/_openapi/patient_openapi.json
curl https://localhost:8443/api/v1/protocol/openapi.json \
    --cacert ../secrets/certificate.pem \
    --output source/_openapi/protocol_openapi.json
curl https://localhost:8443/api/v1/userlogin/openapi.json \
    --cacert ../secrets/certificate.pem \
    --output source/_openapi/userlogin_openapi.json
curl https://localhost:8443/api/v1/device/openapi.json \
    --cacert ../secrets/certificate.pem \
    --output source/_openapi/device_openapi.json

echo "Done."
