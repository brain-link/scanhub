# Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Orchestration engine file for the workflow manager service."""

import os
from typing import Dict

import requests
from fastapi import HTTPException
from datetime import datetime
from typing import Dict


class OrchestrationEngine:
    """OrchestrationEngine is responsible for interacting with different orchestration engines."""

    def __init__(self):
        """Initialize the OrchestrationEngine with environment variables."""
        self.engine = os.getenv("ORCHESTRATION_ENGINE")
        self.kestra_api_url = os.getenv("KESTRA_API_URL")
        self.airflow_api_url = os.getenv("AIRFLOW_API_URL")

    def get_available_tasks(self):
        """Retrieve the available tasks from the orchestration engine.

        Currently, only Airflow is supported.

        Returns
        -------
            list: A list of available tasks (DAGs) for Airflow.

        Raises
        ------
            ValueError: If the orchestration engine is not Airflow.
        """
        if self.engine == "AIRFLOW":
            return self._get_airflow_dags()
        else:
            raise ValueError("Task listing is only supported for Airflow")

    def _get_airflow_dags(self):
        """Get the list of Airflow DAGs.

        Returns
        -------
            dict: A dictionary containing the list of Airflow DAGs.

        Raises
        ------
            HTTPException: If the request to Airflow API fails.
        """
        print(f"{self.airflow_api_url}/api/v1/dags")

        # TBD: Authentication should be handled in a more secure way
        response = requests.get(
            url=f"{self.airflow_api_url}/api/v1/dags",
            auth=("airflow", "airflow"),
            timeout=5
        )
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to retrieve Airflow DAGs")
        return response.json()

    def trigger_task(self, task_id: str, conf: Dict[str, str] = None):
        """
        Triggers a task in the orchestration engine.
        Currently, only Airflow is supported.

        Args:
            task_id (str): The ID of the task to be triggered.
            conf (Dict[str, str]): Additional configuration parameters to pass to the DAG.

        Returns:
            dict: A dictionary containing a success message.

        Raises:
            HTTPException: If the request to Airflow API fails.
        """
        if self.engine == "AIRFLOW":
            return self._trigger_airflow_task(task_id, conf)
        else:
            raise ValueError("Task triggering is only supported for Airflow")

    def _trigger_airflow_task(self, task_id: str, conf: Dict[str, str] = None):
        """
        Trigger an Airflow task.

        Args:
            task_id (str): The ID of the task to be triggered.
            conf (Dict[str, str]): Additional configuration parameters to pass to the DAG.

        Returns:
            dict: A dictionary containing a success message.

        Raises:
            HTTPException: If the request to Airflow API fails.
        """
        print(f"{self.airflow_api_url}/api/v1/dags/{task_id}/dagRuns")

        payload = {
            "conf": conf or {},
            "dag_run_id": task_id,
            "data_interval_end": datetime.utcnow().isoformat() + "Z",
            "data_interval_start": datetime.utcnow().isoformat() + "Z",
            "logical_date": datetime.utcnow().isoformat() + "Z",
            "note": "Triggered via API"
        }

        print(payload)

        response = requests.post(
            url=f"{self.airflow_api_url}/api/v1/dags/{task_id}/dagRuns",
            auth=("airflow", "airflow"),
            json=payload,
            timeout=5
        )

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to trigger Airflow task")
        return {"message": "Airflow task triggered successfully"}

    def get_task_status(self, task_id: str):
        """Retrieve the status of a task in the orchestration engine.

        Currently, only Airflow is supported.

        Args:
            task_id (str): The ID of the task whose status is to be retrieved.

        Returns
        -------
            dict: A dictionary containing the task status.

        Raises
        ------
            ValueError: If the orchestration engine is not Airflow.
        """
        if self.engine == "AIRFLOW":
            return self._get_airflow_task_status(task_id)
        else:
            raise ValueError("Task status is only supported for Airflow")

    def _get_airflow_task_status(self, task_id: str):
        """Get the status of an Airflow task.

        Args:
            task_id (str): The ID of the task whose status is to be retrieved.

        Returns
        -------
            dict: A dictionary containing the task status.

        Raises
        ------
            HTTPException: If the request to Airflow API fails.
        """
        response = requests.get(
            f"{self.airflow_api_url}/dags/example_workflow/dagRuns/{task_id}",
            auth=("airflow", "airflow"),
            timeout=5
        )
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to get Airflow task status")
        return response.json()
