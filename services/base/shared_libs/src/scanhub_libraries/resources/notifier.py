# orchestrator/resources/notifier.py
import httpx
from dagster import ConfigurableResource


class BackendNotifier(ConfigurableResource):
    """Backend notifier."""

    success_callback_url: str | None = None
    devicemanager_url: str | None = None
    access_token: str | None = None
    timeout: float = 5.0

    def send_dag_success(self, success: bool = True) -> None:
        """Notify backend about successful execution of dagster job/dag."""
        if self.success_callback_url is None:
            raise AttributeError
        if self.access_token is None:
            raise AttributeError
        headers = {"Authorization": "Bearer " + self.access_token}
        payload = {"success": success}
        with httpx.Client(timeout=self.timeout) as client:
            response = client.post(self.success_callback_url, json=payload, headers=headers)
            response.raise_for_status()

    def send_device_parameter_update(self, device_id: str, parameter: dict) -> None:
        """Notify backend about device parameter update and send parameters."""
        if self.devicemanager_url is None:
            raise AttributeError
        if self.access_token is None:
            raise AttributeError
        headers = {"Authorization": "Bearer " + self.access_token}
        url = self.devicemanager_url.rstrip("/") + f"/{device_id}"
        with httpx.Client(timeout=self.timeout) as client:
            response = client.put(url, json=parameter, headers=headers)
            response.raise_for_status()
