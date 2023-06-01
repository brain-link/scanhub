"""Utility function to create a sequence plot with plotly."""
import numpy as np
from pypulseq import Sequence
import plotly.graph_objects as go
from pydantic_numpy import NumpyModel, NDArrayFp32



def cast_data(x):
    return np.round(x, 2).astype(float)


class TraceData(NumpyModel):
    """Numpy model for trace data."""

    x: NDArrayFp32
    y: NDArrayFp32
    name: str


def get_sequence_plot(seq: Sequence, time_range: tuple[float, float] = (0., np.inf), time_factor=1e3):
    """Computes a sequence dictionary from pulseq sequence object.

    Parameters
    ----------
    seq
        pypulseq sequence object
    time_range, optional
        time span of the sequence plot, by default (0., np.inf)
    time_factor, optional
        time prefix, by default 1e3

    Returns
    -------
        list of plot data models
    """
    # Empty lists for RX and TX channel: [Time, Magnitude, Phase]
    # rx: list[list] = [[], [], []]
    # tx: list[list] = [[], [], []]
    rx = [np.array([]), np.array([]), np.array([])]
    tx = [np.array([]), np.array([]), np.array([])]

    # Empty gradient channel dictionary: {channel: [Time, Magnitude]}
    # gradients: dict[str, list[list]] = {channel: [[], []] for channel in ['gx', 'gy', 'gz']}
    gradients = {channel: [np.array([]), np.array([])] for channel in ['gx', 'gy', 'gz']}

    t0 = 0.

    for idx in range(len(seq.block_events.keys())):
        block = seq.get_block(idx+1)
        is_valid = time_range[0] <= t0 <= time_range[1]
        if is_valid:

            # ADC event
            if block.adc:
                adc = block.adc
                # From Pulseq: According to the information from Klaus Scheffler and indirectly from Siemens this
                # is the present convention - the samples are shifted by 0.5 dwell
                t = adc.delay + (np.arange(int(adc.num_samples)) + 0.5) * adc.dwell
                # rx[0].append(np.round(time_factor * (t0 + t), 2).astype(float))
                # rx[1].append(np.ones(len(t), dtype=float))
                # rx[2].append(np.round(np.angle(
                #     np.exp(1j * adc.phase_offset) * np.exp(1j * 2 * np.pi * t * adc.freq_offset)
                # ), 2).astype(float))
                rx[0] = np.append(rx[0], time_factor * (t0 + t))
                rx[1] = np.append(rx[1], np.ones(len(t)))
                rx[2] = np.append(rx[2], np.angle(
                    np.exp(1j * adc.phase_offset) * np.exp(1j * 2 * np.pi * t * adc.freq_offset)
                ))
                
            # RF event
            if block.rf:
                rf = block.rf
                t = rf.t + rf.delay
                # tx[0].append(np.round(time_factor * (t0 + t), 2).astype(float))
                # tx[1].append(np.round(np.abs(rf.signal), 2).astype(float))
                # tx[2].append(np.round(np.angle(
                #     rf.signal * np.exp(1j * rf.phase_offset) * np.exp(1j * 2 * np.pi * rf.t * rf.freq_offset)
                # ), 2).astype(float))
                tx[0] = np.append(tx[0], time_factor * (t0 + t))
                tx[1] = np.append(tx[1], np.abs(rf.signal))
                tx[2] = np.append(tx[2], np.angle(
                    rf.signal * np.exp(1j * rf.phase_offset) * np.exp(1j * 2 * np.pi * rf.t * rf.freq_offset)
                ))

            # Gradient event
            for ch in gradients.keys():
                if gb := getattr(block, ch):
                    if gb.type == 'grad':
                        # In place unpacking of grad.t with the starred expression
                        t = gb.delay + [0, *(gb.tt+(gb.tt[1]-gb.tt[0])/2), gb.tt[-1]+gb.tt[1]-gb.tt[0]]
                        waveform = 1e-3 * np.array((gb.first, *gb.waveform, gb.last))
                    else:
                        t = np.cumsum([0, gb.delay, gb.rise_time, gb.flat_time, gb.fall_time])
                        waveform = 1e-3 * gb.amplitude * np.array([0, 0, 1, 1, 0])

                    # gradients[ch][0].append(np.round(time_factor * (t0 + t), 2).astype(float))
                    # gradients[ch][1].append(np.round(waveform, 2).astype(float))
                    gradients[ch][0] = np.append(gradients[ch][0], time_factor * (t0 + t))
                    gradients[ch][1] = np.append(gradients[ch][1], waveform)

        # Update current time offset
        t0 += seq.block_durations[idx]

    traces = [
        TraceData(x=cast_data(tx[0]), y=cast_data(tx[1]), name="Tx"),
        TraceData(x=cast_data(rx[0]), y=cast_data(rx[1]), name="Rx"),
        TraceData(x=cast_data(gradients["gx"][0]), y=cast_data(gradients["gx"][1]), name="Gx"),
        TraceData(x=cast_data(gradients["gy"][0]), y=cast_data(gradients["gy"][1]), name="Gy"),
        TraceData(x=cast_data(gradients["gz"][0]), y=cast_data(gradients["gz"][1]), name="Gz")
    ]

    fig = go.Figure()
    for k, trace in enumerate(traces):
        fig.add_trace(go.Scatter(
            x=trace.x,
            y=trace.y,
            name=trace.name,
            yaxis=f"y{len(traces)-k}",
            mode="lines",
        ))

    fig.update_layout(
        autosize=True,
        xaxis=dict(ticks="outside", title="Time (ms)", rangeslider=dict(autorange=True)),
        yaxis=dict(domain=[0.0, 0.15]),
        yaxis2=dict(domain=[0.2, 0.35]),
        yaxis3=dict(domain=[0.4, 0.55]),
        yaxis4=dict(domain=[0.6, 0.75]),
        yaxis5=dict(domain=[0.8, 0.95]),
    )

    return fig
