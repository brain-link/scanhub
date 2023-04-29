from pydantic import BaseModel, parse_obj_as
from typing import List
from pypulseq.opts import Opts
from pypulseq.Sequence.sequence import Sequence
import numpy as np


class SequencePlot:
    def __init__(self, sequence_path: str) -> None:

        system = Opts(max_grad=32, grad_unit='mT/m', max_slew=130, slew_unit='mT/m/ms')
        
        self.seq_obj = Sequence(system=system)
        self.seq_obj.read(sequence_path)

        self.data = self.pulseq_to_dict(self.seq_obj)


    # Define the pydantic model for passing data to frontend
    class PlotData(BaseModel):
        x: list
        y: list
        type: str
        mode: str
        name: str
        yaxis: str
        hoverinfo: str = "name+x+text"

        
    def get_plot_data(self, duration: float = None) -> PlotData:

        if duration is None:
            duration = self.seq_obj.duration()[0]

        # time_idx = np.argmin(np.array(self.data["tx"]["time"]) - duration)
        time_idx = -1

        traces = []

        for idx, key in enumerate(self.data.keys()):
            traces.append(
                self.PlotData(
                    x=list(self.data[key]["time"][:time_idx]),
                    y=list(self.data[key]["values"][:time_idx]),
                    type="scatter",
                    mode="lines",
                    name=self.data[key]["name"],
                    yaxis=f"y{len(self.data.keys())-idx}"
                    # marker=dict( color=clr.plot[idx] )
                )
            )

        return parse_obj_as(List[self.PlotData], traces)


    # Parse the pulseq sequence object
    @staticmethod
    def pulseq_to_dict(seq, time_range=(0, np.inf), time_factor=1e3) -> dict:
        """Computes a sequence dictionary from pulseq sequence object
        Arguments:
            seq {Sequence} -- pypulseq sequence object
        Keyword Arguments:
            time_range {tuple} -- total time of the plotted sequence (default: {(0, np.inf)})
            time_factor {float} -- time prefix, e.g. s, ms, us, ... (default: {1e3})
        Raises:
            ValueError: If given timerange is not int/float or its number of elements is unequal to 2
        Returns:
            dict -- sequence dictionary, defining all channels
        """
        if not all([isinstance(x, (int, float)) for x in time_range]) or len(time_range) != 2:
            raise ValueError('Invalid time range')

        # Empty lists for RX and TX channel: [Time, Magnitude, Phase]
        rx, tx = [np.array([]), np.array([]), np.array([])], [np.array([]), np.array([]), np.array([])]
        # Empty gradient channel dictionary: {channel: [Time, Magnitude]}
        gradients = {channel: [np.array([]), np.array([])] for channel in ['gx', 'gy', 'gz']}

        t0 = 0

        for block_idx, block in enumerate(seq.dict_block_events):
            block = seq.get_block(block)
            is_valid = time_range[0] <= t0 <= time_range[1]
            if is_valid:
                # ADC event
                if hasattr(block, 'adc'):
                    adc = block.adc
                    # From Pulseq: According to the information from Klaus Scheffler and indirectly from Siemens this
                    # is the present convention - the samples are shifted by 0.5 dwell
                    t = adc.delay + (np.arange(int(adc.num_samples)) + 0.5) * adc.dwell
                    rx[0] = np.append(rx[0], time_factor * (t0 + t))
                    rx[1] = np.append(rx[1], np.ones(len(t)))
                    rx[2] = np.append(rx[2], np.angle(np.exp(1j * adc.phase_offset) *
                                                    np.exp(1j * 2 * np.pi * t * adc.freq_offset)))
                # RF event
                if hasattr(block, 'rf'):
                    rf = block.rf
                    t = rf.t + rf.delay
                    tx[0] = np.append(tx[0], time_factor * (t0 + t))
                    tx[1] = np.append(tx[1], np.abs(rf.signal))
                    tx[2] = np.append(tx[2], np.angle(rf.signal * np.exp(1j * rf.phase_offset) *
                                                    np.exp(1j * 2 * np.pi * rf.t * rf.freq_offset)))
                # Gradient event
                for idx, ch in enumerate(gradients.keys()):
                    if hasattr(block, ch):
                        grad = getattr(block, ch)

                        if grad.type == 'grad':
                            # In place unpacking of grad.t with the starred expression
                            t = grad.delay + [0, *(grad.t + (grad.t[1] - grad.t[0]) / 2),
                                            grad.t[-1] + grad.t[1] - grad.t[0]]
                            waveform = 1e-3 * np.array((grad.first, *grad.waveform, grad.last))
                        else:
                            t = np.cumsum([0, grad.delay, grad.rise_time, grad.flat_time, grad.fall_time])
                            waveform = 1e-3 * grad.amplitude * np.array([0, 0, 1, 1, 0])

                        gradients[ch][0] = np.append(gradients[ch][0], time_factor * (t0 + t))
                        gradients[ch][1] = np.append(gradients[ch][1], waveform)
            # Update current time offset
            t0 += seq.arr_block_durations[block_idx]

        return dict(
            tx=dict(name="Tx", time=tx[0], values=tx[1], unit="RF"),
            rx=dict(name="Rx", time=rx[0], values=rx[1], unit="ADC"),
            gr=dict(name="GR", time=gradients["gx"][0], values=gradients["gx"][1], unit="mT/m"),
            gp=dict(name="GP", time=gradients["gy"][0], values=gradients["gy"][1], unit="mT/m"),
            gs=dict(name="GS", time=gradients["gz"][0], values=gradients["gz"][1], unit="mT/m")
        )
