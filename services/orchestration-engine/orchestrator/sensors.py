# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Run-status sensors that report job outcomes directly to the protocol manager."""
from pathlib import Path

from dagster import DagsterRunStatus, DefaultSensorStatus, RunStatusSensorContext, run_status_sensor
from scanhub_libraries.resources import DAG_CONFIG_KEY
from scanhub_libraries.resources.notifier import ProtocolManagerNotifier


def _get_dag_config_from_run(context: RunStatusSensorContext) -> dict:
    """Extract the DAG configuration dictionary from a RunStatusSensorContext."""
    run_config = getattr(context.dagster_run, "run_config", None)
    if not isinstance(run_config, dict):
        return {}
    return run_config.get("resources", {}).get(DAG_CONFIG_KEY, {}).get("config", {})


@run_status_sensor(
    run_status=DagsterRunStatus.SUCCESS,
    default_status=DefaultSensorStatus.RUNNING,
    monitor_all_code_locations=True,
    minimum_interval_seconds=5,
)
def on_run_success(context: RunStatusSensorContext, notifier_protocol: ProtocolManagerNotifier) -> None:
    """On successful reconstruction: collect DICOM output files and register a result in the protocol manager."""
    dag_config = _get_dag_config_from_run(context)
    task_dir = dag_config.get("task_dir", "")
    task_id = dag_config.get("task_id", "")
    access_token = dag_config.get("user_access_token", "")
    run_id = context.dagster_run.run_id

    if not (task_dir and task_id and access_token):
        context.log.info(
            "Run succeeded but missing task_dir/task_id/access_token — skipping protocol-manager notification."
        )
        return

    dcm_files = sorted(
        p.name for p in Path(task_dir).iterdir()
        if p.is_file() and p.name.startswith(run_id) and p.suffix.lower() == ".dcm"
    )

    try:
        notifier_protocol.create_dicom_result(
            task_id=task_id,
            directory=task_dir,
            files=dcm_files,
            run_id=run_id,
            access_token=access_token,
        )
        notifier_protocol.update_task_status(task_id, "FINISHED", access_token)
        context.log.info(
            "%s succeeded (run_id=%s) — registered %d DICOM file(s).",
            context.dagster_run.job_name, run_id, len(dcm_files),
        )
    except Exception as exc:
        context.log.error("Failed to notify protocol manager on success: %s", exc)


@run_status_sensor(
    run_status=DagsterRunStatus.FAILURE,
    default_status=DefaultSensorStatus.RUNNING,
    monitor_all_code_locations=True,
    minimum_interval_seconds=5,
)
def on_run_failure(context: RunStatusSensorContext, notifier_exam_manager: ProtocolManagerNotifier) -> None:
    """On failed reconstruction: mark the task as ERROR in the protocol manager."""
    dag_config = _get_dag_config_from_run(context)
    task_id = dag_config.get("task_id", "")
    access_token = dag_config.get("user_access_token", "")

    if not (task_id and access_token):
        context.log.info("Run failed but missing task_id/access_token — skipping protocol-manager notification.")
        return

    try:
        notifier_exam_manager.update_task_status(task_id, "ERROR", access_token)
        context.log.info("%s failed (run_id=%s).", context.dagster_run.job_name, context.dagster_run.run_id)
    except Exception as exc:
        context.log.error("Failed to notify protocol manager on failure: %s", exc)


@run_status_sensor(
    run_status=DagsterRunStatus.CANCELED,
    default_status=DefaultSensorStatus.RUNNING,
    monitor_all_code_locations=True,
    minimum_interval_seconds=5,
)
def on_run_canceled(context: RunStatusSensorContext, notifier_exam_manager: ProtocolManagerNotifier) -> None:
    """On canceled reconstruction: mark the task as ERROR in the protocol manager."""
    dag_config = _get_dag_config_from_run(context)
    task_id = dag_config.get("task_id", "")
    access_token = dag_config.get("user_access_token", "")

    if not (task_id and access_token):
        context.log.info("Run canceled but missing task_id/access_token — skipping protocol-manager notification.")
        return

    try:
        notifier_exam_manager.update_task_status(task_id, "ERROR", access_token)
        context.log.info("%s canceled (run_id=%s).", context.dagster_run.job_name, context.dagster_run.run_id)
    except Exception as exc:
        context.log.error("Failed to notify protocol manager on cancellation: %s", exc)
