"""MRI calibration assets."""
import ismrmrd
import numpy as np
from dagster import OpExecutionContext, job, op
from scanhub_libraries.resources.dag_config import DAGConfiguration
from scanhub_libraries.resources.notifier import DeviceManagerNotifier

from orchestrator.io.acquisition_data import AcquisitionData, acquisition_data_op
from orchestrator.utils.snr import signal_to_noise_ratio


@op
def frequency_calibration_op(
    context: OpExecutionContext,
    data: AcquisitionData,
    dag_config: DAGConfiguration,
    notigier_device_manager: DeviceManagerNotifier,
) -> None:
    """Perform frequency calibration."""
    context.log.info("AcquisitionData: %s", data)
    parameter = data.device_parameter
    context.log.info(f"Received device parameters (device id: {data.device_id}): {parameter}")

    with ismrmrd.File(data.mrd_path, "r") as f:
        ds = f[list(f.keys())[0]]
        header = ds.header
        acquisitions = ds.acquisitions

        num_acquisitions = len(acquisitions)
        if num_acquisitions > 1:
            context.log.warning(
                "Data is not 1D, got %s acquisition, processing first acquisition.",
                num_acquisitions,
            )

        # Only consider first acquisition and data from coil at index 0
        acq = acquisitions[0]
        acq_data = acq.data[0, ...]
        dwell_time = acq.sample_time_us * 1e-6
        data_fft = np.fft.fftshift(np.fft.fft(np.fft.fftshift(acq_data)))
        fft_freq = np.fft.fftshift(np.fft.fftfreq(acq_data.size, dwell_time))

        # Calculate SNR and FWHM
        bw_per_pixel = 1 / dwell_time / acq_data.size
        snr, fwhm_px = signal_to_noise_ratio(data_fft)
        fwhm_hz = round(fwhm_px*bw_per_pixel)
        context.log.info("SNR: %s dB, FWHM: %s Hz", str(round(snr, 2)), str(fwhm_hz))

        freq_offset = fft_freq[np.argmax(np.abs(data_fft))]

        # Get experiment larmor frequency
        f0 = header.experimentalConditions.H1resonanceFrequency_Hz
        context.log.info(
            "Frequency from acquisition: %s Hz, Larmor frequency offset: %s Hz",
            str(f0),
            str(freq_offset),
        )

    # Correct device parameter
    parameter["larmor_frequency"] = f0 + freq_offset
    notigier_device_manager.send_device_parameter_update(
        device_id=data.device_id, access_token=dag_config.user_access_token, parameter=parameter,
    )


# @op(ins={"start": In(Nothing), })
# def success_notify_op(context: OpExecutionContext, scanhub_notifier: BackendNotifier) -> None:
#     """Single, end-of-run success signal."""
#     scanhub_notifier.send_dag_success()
#     context.log.info("Backend notification send.")

@job(
    name="frequency_calibration",
    description="Read ismrmrd data and adjust Larmor frequency.",
)
def frequency_calibration_job() -> None:
    """Calibrate Larmor frequency."""
    data = acquisition_data_op()
    frequency_calibration_op(data)
    # done = frequency_calibration_op(data)
    # success_notify_op(start=done)
