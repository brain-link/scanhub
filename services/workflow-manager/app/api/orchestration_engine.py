# Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Orchestration engine file for the workflow manager service."""

import os

import requests
from fastapi import HTTPException


class OrchestrationEngine:
    """
    OrchestrationEngine is responsible for interacting with different orchestration engines
    like Airflow and Kestra to manage tasks and workflows.
    """

    def __init__(self):
        """Initializes the OrchestrationEngine with environment variables."""
        self.engine = os.getenv("ORCHESTRATION_ENGINE")
        self.kestra_api_url = os.getenv("KESTRA_API_URL")
        self.airflow_api_url = os.getenv("AIRFLOW_API_URL")

    def get_available_tasks(self):
        """Retrieves the available tasks from the orchestration engine.
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
        """Helper method to get the list of Airflow DAGs.

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
            auth=("airflow", "airflow")
        )
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to retrieve Airflow DAGs")
        return response.json()

    def trigger_task(self, task_id: str):
        """Triggers a task in the orchestration engine.
        Currently, only Airflow is supported.

        Args:
            task_id (str): The ID of the task to be triggered.

        Returns
        -------
            dict: A dictionary containing a success message.

        Raises
        ------
            ValueError: If the orchestration engine is not Airflow.
        """
        if self.engine == "AIRFLOW":
            return self._trigger_airflow_task(task_id)
        else:
            raise ValueError("Task triggering is only supported for Airflow")

    def _trigger_airflow_task(self, task_id: str):
        """Helper method to trigger an Airflow task.

        Args:
            task_id (str): The ID of the task to be triggered.

        Returns
        -------
            dict: A dictionary containing a success message.

        Raises
        ------
            HTTPException: If the request to Airflow API fails.
        """
        print(f"{self.airflow_api_url}/api/v1/dags/{task_id}/dagRuns")

        payload = {}

        print(payload)

        response = requests.post(
            url=f"{self.airflow_api_url}/api/v1/dags/{task_id}/dagRuns",
            auth=("airflow", "airflow"),
            json=payload
        )

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to trigger Airflow task")
        return {"message": "Airflow task triggered successfully"}

    def get_task_status(self, task_id: str):
        """Retrieves the status of a task in the orchestration engine.
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
        """Helper method to get the status of an Airflow task.

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
            auth=("airflow", "airflow")
        )
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to get Airflow task status")
        return response.json()
