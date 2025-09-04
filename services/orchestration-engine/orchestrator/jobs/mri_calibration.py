"""MRI calibration assets."""
import ismrmrd
from dagster import In, Nothing, OpExecutionContext, job, op, In, AssetKey
from scanhub_libraries.resources.notifier import BackendNotifier

from orchestrator.io.acquisition_data import AcquisitionData, acquisition_data_op


@op
def frequency_calibration_op(
    context: OpExecutionContext,
    data: AcquisitionData,
    scanhub_notifier: BackendNotifier,
) -> None:
    """Perform frequency calibration."""
    context.log.info("AcquisitionData: %s", data)
    parameter = data.device_parameter
    context.log.info(f"Received device parameters (device id: {data.device_id}): {parameter}")

    with ismrmrd.File(data.mrd_path, "r") as f:
        ds = f[list(f.keys())[0]]
        header = ds.header
        acquisitions = ds.acquisitions[:]

    f0 = header.experimentalConditions.H1resonanceFrequency_Hz
    context.log.info(f"Larmor frequency from ismrmrd file: {f0}")
    context.log.info(f"Number of readouts: {len(acquisitions)}")

    parameter["larmor_frequency"] = f0
    scanhub_notifier.send_device_parameter_update(device_id=data.device_id, parameter=parameter)


@op(ins={"start": In(Nothing), })
def success_notify_op(context: OpExecutionContext, scanhub_notifier: BackendNotifier) -> None:
    """Single, end-of-run success signal."""
    scanhub_notifier.send_dag_success()
    context.log.info("Backend notification send.")

@job(
    name="frequency_calibration",
    description="Read ismrmrd data and adjust Larmor frequency.",
)
def frequency_calibration_job() -> None:
    """Calibrate Larmor frequency."""
    data = acquisition_data_op()
    done = frequency_calibration_op(data)
    success_notify_op(start=done)
