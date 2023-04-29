from enum import IntEnum


class PatientStatus(IntEnum):
    NEW = 0
    RECORDING = 1
    DIAGNOSIS = 2


class PatientSex(IntEnum):
    NONE = 0
    MALE = 1
    FEMALE = 2
    DIVERSE = 3


class Modality(IntEnum):
    NONE = 0
    MRI = 1
    ECG = 2
    EEG = 3
    CT = 4
