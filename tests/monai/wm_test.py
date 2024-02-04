import requests

url = 'http://localhost:5001/workflows'

# List all MONAI workflows
res = requests.get(url)

print(res.json())

# Create a new workflow

headers = {
    'accept': 'text/plain',
    'Content-Type': 'application/json-patch+json',
}

payload = '''{
                "name": "pixel-workflow",
                "version": "1.0.0",
                "description": "Attempt at making a workflow",
                "informatics_gateway": {
                    "ae_title": "MonaiSCU",
                    "data_origins": [
                        "MY_SCANNER"
                    ],
                    "export_destinations": [
                        "PROD_PACS"
                    ]
                },
                "tasks": [
                            {
                                "id": "aide-passing",
                                "description": "trigger simple argo workflow",
                                "type": "argo",
                                "args": {
                                    "namespace":"argo",
                                    "workflow_template_name": "aide-artifact-passing-j5ndx",
                                    "server_url": "https://localhost:2746",
                                    "allow_insecure": true
                                },
                                "artifacts": {
                                    "input": [
                                        {
                                            "name": "input-dicom",
                                            "value": "{{ context.input.dicom }}"
                                        }
                                    ],
                                    "output": [
                                        {
                                            "name": "report-pdf",
                                            "Mandatory": true
                                        }
                                    ]
                                }
                            }
                        ]
            }'''

res = requests.post(url, data=payload, headers=headers)

print(res.json())