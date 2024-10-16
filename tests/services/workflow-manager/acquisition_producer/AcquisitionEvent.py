#from enum import Enum

# class AcquisitionCommands(Enum):
#     """A class which contains the commands for the acquisition control.

#     The commands are defined as an enum.
#     """
#     # MEASURMENT
#     MEAS_START = 1000
#     MEAS_STOP = 1001
#     MEAS_PAUSE = 1002

class AcquisitionEvent:
    def __init__(self, instruction : str):
        self.instruction = instruction