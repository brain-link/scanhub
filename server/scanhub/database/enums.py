from enum import Enum, IntEnum


class ProductType(IntEnum):
    ARTICLE = 1
    PAGE = 2


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
    MRI = 0
    ECG = 1
    EEG = 2
    ABC = 3


class Action(str, Enum):
    CREATE = "create"
    DELETE = "delete"
    EDIT = "edit"
