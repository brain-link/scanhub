# orchestrator/resources/notifier.py
import logging

import httpx
from dagster import ConfigurableResource

_log = logging.getLogger(__name__)


class ProtocolManagerNotifier(ConfigurableResource):
    """Notifies protocol manager about Dagster job outcomes."""

    base_url: str
    timeout: float = 5.0

    def create_blank_result(self, task_id: str, access_token: str) -> str:
        """Create an empty result placeholder and return its ID."""
        headers = {"Authorization": "Bearer " + access_token}
        url = self.base_url.rstrip("/") + "/result"
        with httpx.Client(timeout=self.timeout) as client:
            response = client.post(url, params={"task_id": task_id}, headers=headers)
            response.raise_for_status()
        return str(response.json()["id"])

    def set_result(
        self,
        result_id: str,
        result_type: str,
        directory: str,
        files: list[str],
        access_token: str,
    ) -> None:
        """Populate a blank result entry with actual data."""
        headers = {"Authorization": "Bearer " + access_token}
        url = self.base_url.rstrip("/") + f"/result/{result_id}"
        with httpx.Client(timeout=self.timeout) as client:
            response = client.put(
                url,
                json={"type": result_type, "directory": directory, "files": files},
                headers=headers,
            )
            response.raise_for_status()

    def update_task_status(self, task_id: str, status: str, access_token: str) -> None:
        """Update task status in the protocol manager."""
        headers = {"Authorization": "Bearer " + access_token}
        url = self.base_url.rstrip("/") + f"/task/{task_id}/status"
        with httpx.Client(timeout=self.timeout) as client:
            response = client.put(url, params={"status": status}, headers=headers)
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

    def push_task_event(
        self,
        task_id: str,
        source: str,
        task_status: str,
        progress: int = 0,
        message: str = "",
    ) -> None:
        """Push a real-time status event to all SSE subscribers watching a task.

        source: identifies the emitting component, e.g. 'device' or 'pipeline'.
        task_status: one of the known display statuses (INPROGRESS, FINISHED, FAILED, …).
        Failures are non-fatal — if no browser is subscribed the call still succeeds.
        """
        payload = {
            "source": source,
            "task_status": task_status,
            "progress": progress,
            "message": message,
        }
        url = self.base_url.rstrip("/") + f"/task/{task_id}/push-event"
        try:
            with httpx.Client(timeout=self.timeout) as client:
                client.post(url, json=payload).raise_for_status()
        except Exception as exc:  # noqa: BLE001
            _log.warning("SSE push for task %s failed (best-effort): %s", task_id, exc)
