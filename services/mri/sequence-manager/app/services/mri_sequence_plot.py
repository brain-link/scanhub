# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
# %%
"""Utility function to create a sequence plot with plotly."""

import numpy as np
from pypulseq import Sequence
import plotly.graph_objects as go
from pydantic import BaseModel


class TraceData(BaseModel):
    """Numpy model for trace data."""

    x: list[float]
    y: list[float]
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
    rx: list[list] = [[0.], [0.], [0.]]
    tx: list[list[float]] = [[0.], [0.], [0.]]

    # Empty gradient channel dictionary: {channel: [Time, Magnitude]}
    gradients: dict[str, list[list]] = {channel: [[0.], [0.]] for channel in ['gx', 'gy', 'gz']}

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
                # t = adc.delay + (np.arange(int(adc.num_samples)) + 0.5) * adc.dwell
                # rx[0] += list(np.round(time_factor * (t0 + t), 2).astype(float))
                # rx[1] += list(np.ones(len(t), dtype=float))
                # rx[2] += list(np.round(np.angle(
                #     np.exp(1j * adc.phase_offset) * np.exp(1j * 2 * np.pi * t * adc.freq_offset)
                # ), 2).astype(float))
                adc_duration = adc.dwell * (adc.num_samples + 0.5)
                rx[0] += list(np.cumsum([t0, adc.delay, 0, adc_duration, 0]) * time_factor)
                rx[1] += [0., 0., 1., 1., 0.]

            # RF event
            if block.rf:
                rf = block.rf
                t = rf.t + rf.delay
                tx[0] += list(np.round(time_factor * (t0 + t), 2).astype(float))
                tx[1] += list(np.round(np.abs(rf.signal), 2).astype(float))
                tx[2] += list(np.round(np.angle(
                    rf.signal * np.exp(1j * rf.phase_offset) * np.exp(1j * 2 * np.pi * rf.t * rf.freq_offset)
                ), 2).astype(float))

            # Gradient event
            for ch in gradients.keys():
                if gb := getattr(block, ch):
                    if gb.type == 'grad':
                        # In place unpacking of grad.t with the starred expression -- produces weird shapes
                        # t = gb.delay + [0, *(gb.tt+(gb.tt[1]-gb.tt[0])/2), gb.tt[-1]+gb.tt[1]-gb.tt[0]]
                        # Double check: Is this the correct way to unwrap arbitrary waveform?
                        t = np.array([gb.delay, *gb.tt + gb.delay, gb.shape_dur])
                        waveform = 1e-3 * np.array((gb.first, *gb.waveform, gb.last))
                    else:
                        t = np.cumsum([0, gb.delay, gb.rise_time, gb.flat_time, gb.fall_time])
                        waveform = 1e-3 * gb.amplitude * np.array([0, 0, 1, 1, 0])

                    gradients[ch][0] += list(np.round(time_factor * (t0 + t), 2).astype(float))
                    gradients[ch][1] += list(np.round(waveform, 2).astype(float))

        # Update current time offset
        t0 += float(seq.block_durations[idx])

    # Set all channels back to zero
    tx[0] += [tx[0][-1], seq.duration()[0] * time_factor]
    tx[1] += [0., 0.]
    rx[0] += [rx[0][-1], seq.duration()[0] * time_factor]
    rx[1] += [0., 0.]
    for grad in gradients.values():
        grad[0] += [grad[0][-1], seq.duration()[0] * time_factor]
        grad[1] += [0., 0.]

    traces = [
        TraceData(x=tx[0], y=tx[1], name="Tx"),
        TraceData(x=rx[0], y=rx[1], name="Rx"),
        TraceData(x=gradients["gx"][0], y=gradients["gx"][1], name="Gx"),
        TraceData(x=gradients["gy"][0], y=gradients["gy"][1], name="Gy"),
        TraceData(x=gradients["gz"][0], y=gradients["gz"][1], name="Gz"),
    ]

    fig = go.Figure()
    for k, trace in enumerate(traces):
        fig.add_trace(go.Scatter(
            x=trace.x,
            y=trace.y,
            name=trace.name,
            yaxis=f"y{len(traces)-k}",
            mode="lines"
        ))

    fig.update_layout(
        autosize=True,
        xaxis=dict(
            ticks="outside", 
            title="Time (ms)", 
            rangeslider=dict(autorange=True)
        ),
        yaxis=dict(domain=[0.0, 0.15]),
        yaxis2=dict(domain=[0.2, 0.35]),
        yaxis3=dict(domain=[0.4, 0.55]),
        yaxis4=dict(domain=[0.6, 0.75]),
        yaxis5=dict(domain=[0.8, 0.95]),
    )

    return fig

# %%
