# orchestrator/resources/notifier.py
import httpx
from dagster import ConfigurableResource


class ExamManagerNotifier(ConfigurableResource):
    """Notifies exam manager about Dagster job outcomes."""

    base_url: str
    timeout: float = 5.0

    def create_dicom_result(
        self,
        task_id: str,
        directory: str,
        files: list[str],
        run_id: str,
        access_token: str,
    ) -> None:
        """Create a DICOM result entry in the exam manager after successful reconstruction."""
        headers = {"Authorization": "Bearer " + access_token}
        payload = {
            "type": "DICOM",
            "directory": directory,
            "files": files,
            "meta": {"run_id": run_id},
        }
        url = self.base_url.rstrip("/") + f"/result/dicom/{task_id}"
        with httpx.Client(timeout=self.timeout) as client:
            response = client.post(url, json=payload, headers=headers)
            response.raise_for_status()

    def update_task_status(self, task_id: str, status: str, access_token: str) -> None:
        """Update task status in the exam manager."""
        headers = {"Authorization": "Bearer " + access_token}
        url = self.base_url.rstrip("/") + f"/task/{task_id}/status"
        with httpx.Client(timeout=self.timeout) as client:
            response = client.put(url, json={"status": status}, headers=headers)
            response.raise_for_status()


class DeviceManagerNotifier(ConfigurableResource):
    """Notifies device manager."""

    base_url: str
    timeout: float = 5.0

    def send_device_parameter_update(self, device_id: str, access_token: str, parameter: dict) -> None:
        """Notify backend about device parameter update and send parameters."""
        headers = {"Authorization": "Bearer " + access_token}
        url = self.base_url.rstrip("/") + f"/parameter/{device_id}"
        with httpx.Client(timeout=self.timeout) as client:
            response = client.put(url, json=parameter, headers=headers)
            response.raise_for_status()
