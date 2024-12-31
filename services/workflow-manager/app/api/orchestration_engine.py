# Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

import os
import requests
from fastapi import HTTPException

class OrchestrationEngine:
    def __init__(self):
        self.engine = os.getenv("ORCHESTRATION_ENGINE")
        self.kestra_api_url = os.getenv("KESTRA_API_URL")
        self.airflow_api_url = os.getenv("AIRFLOW_API_URL")

    def trigger_workflow(self, workflow_id: str):
        if self.engine == "KESTRA":
            return self._trigger_kestra_workflow(workflow_id)
        elif self.engine == "AIRFLOW":
            return self._trigger_airflow_workflow(workflow_id)
        else:
            raise ValueError("Invalid orchestration engine specified")

    def _trigger_kestra_workflow(self, workflow_id: str):
        response = requests.post(
            f"{self.kestra_api_url}/executions",
            json={
                "namespace": "my_namespace",
                "flowId": "example_workflow",
                "inputs": {"workflow_id": workflow_id}
            }
        )
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to trigger Kestra workflow")
        return {"message": "Kestra workflow triggered successfully"}

    def _trigger_airflow_workflow(self, workflow_id: str):
        response = requests.post(
            f"{self.airflow_api_url}/dags/example_workflow/dagRuns",
            json={"conf": {"workflow_id": workflow_id}}
        )
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to trigger Airflow workflow")
        return {"message": "Airflow workflow triggered successfully"}

    def get_workflow_status(self, workflow_id: str):
        if self.engine == "KESTRA":
            return self._get_kestra_workflow_status(workflow_id)
        elif self.engine == "AIRFLOW":
            return self._get_airflow_workflow_status(workflow_id)
        else:
            raise ValueError("Invalid orchestration engine specified")

    def _get_kestra_workflow_status(self, workflow_id: str):
        response = requests.get(
            f"{self.kestra_api_url}/executions/{workflow_id}"
        )
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to get Kestra workflow status")
        return response.json()

    def _get_airflow_workflow_status(self, workflow_id: str):
        response = requests.get(
            f"{self.airflow_api_url}/dags/example_workflow/dagRuns/{workflow_id}"
        )
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to get Airflow workflow status")
        return response.json()