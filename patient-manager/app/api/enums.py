"""Definition of patient enums."""
from enum import IntEnum


class PatientStatus(IntEnum):
    """Patient status enum."""

    NEW = 0
    RECORDING = 1
    DIAGNOSIS = 2


class PatientSex(IntEnum):
    """Patient sex enum."""

    NONE = 0
    MALE = 1
    FEMALE = 2
    DIVERSE = 3


class Modality(IntEnum):
    """Modalities enum."""

    NONE = 0
    MRI = 1
    ECG = 2
    EEG = 3
    CT = 4
