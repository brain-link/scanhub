from typing import List
from pydantic import BaseModel, Field
from enum import Enum


class MatrixSize(BaseModel):
    x: int = Field(1, description="Matrix size in the x dimension")
    y: int = Field(1, description="Matrix size in the y dimension")
    z: int = Field(1, description="Matrix size in the z dimension")


class FieldOfView(BaseModel):
    x: float = Field(..., description="Field of view in the x dimension in mm")
    y: float = Field(..., description="Field of view in the y dimension in mm")
    z: float = Field(..., description="Field of view in the z dimension in mm")


class EncodingSpace(BaseModel):
    matrixSize: MatrixSize = Field(..., description="Matrix size of the encoding space")
    fieldOfView_mm: FieldOfView = Field(..., description="Field of view of the encoding space")


class LimitType(BaseModel):
    minimum: int = Field(0, description="Minimum value")
    maximum: int = Field(0, description="Maximum value")
    center: int = Field(0, description="Center value")


class EncodingLimits(BaseModel):
    kspace_encoding_step_0: LimitType = Field(..., description="Encoding limits for k-space encoding step 0")
    kspace_encoding_step_1: LimitType = Field(..., description="Encoding limits for k-space encoding step 1")
    kspace_encoding_step_2: LimitType = Field(..., description="Encoding limits for k-space encoding step 2")


class Trajectories(str, Enum):
    """Pydantic definition of Trajectories"""
    CARTESIAN = "cartesian"
    EPI = "epi"
    RADIAL = "radial"
    GOLDENANGLE = "goldenangle"
    SPIRAL = "spiral"
    OTHER = "other"


class DiffusionDimensions(str, Enum):
    """Pydantic definition of diffusion dimensions"""
    AVERAGE = "average"
    CONTRAST = "contrast"
    PHASE = "phase"
    REPETITION = "repetition"
    SET = "set"
    SEGMENT = "segment"
    USER_0 = "user_0"
    USER_1 = "user_1"
    USER_2 = "user_2"
    USER_3 = "user_3"
    USER_4 = "user_4"
    USER_5 = "user_5"
    USER_6 = "user_6"
    USER_7 = "user_7"


class Encoding(BaseModel):
    encodedSpace: EncodingSpace = Field(..., description="Encoded space")
    reconSpace: EncodingSpace = Field(..., description="Reconstruction space")
    encodingLimits: EncodingLimits = Field(..., description="Encoding limits")
    trajectory: Trajectories = Field(..., description="Trajectories")


class ExperimentalConditions(BaseModel):
    H1resonanceFrequency_Hz: int = Field(..., description="H1 resonance frequency in Hz")


class GradientDirection(BaseModel):
    rl: float = Field(..., description="Gradient direction in the right-left dimension")
    ap: float = Field(..., description="Gradient direction in the anterior-posterior dimension")
    fh: float = Field(..., description="Gradient direction in the foot-head dimension")


class DiffusionType(BaseModel):
    gradientDirection: GradientDirection = Field(..., description="Gradient direction")
    bvalue: float = Field(..., description="b-value")


class SequenceParameters(BaseModel):
    TR: List[float] = Field(..., description="Repetition time in seconds")
    TE: List[float] = Field(..., description="Echo time in seconds")
    TI: List[float] = Field(..., description="Inversion time in seconds")
    flipAngle_deg: List[float] = Field(..., description="Flip angle in degrees")
    sequence_type: str = Field(..., description="sequence type")
    echo_spacing: List[float] = Field(..., description="Echo spacing in seconds")
    diffusionDimension: DiffusionDimensions = Field(..., description="Diffusion Dimensions")
    diffusion: List[DiffusionType] = Field(..., description="Diffusion information")
    diffusionScheme: str = Field(..., description="Diffusion scheme")


class PatientPositions(str, Enum):
    """Pydantic definition of patient postions."""
    HFP = "HFP"
    HFS = "HFS"
    HFDR = "HFDR"
    HFDL = "HFDL"
    FFP = "FFP"
    FFS = "FFS"
    FFDR = "FFDR"
    FFDL = "FFDL"


class MeasurementInformation(BaseModel):
    measurementID: str = Field(..., description="Measurement ID")
    patientPosition: PatientPositions = Field(..., description="Patient position")
    sequenceName: str = Field(..., description="Sequence ID")


class AcquisitionSystemInformation(BaseModel):
    deviceID: str = Field(..., description="device ID")


class UserParametersLong(BaseModel):
    name: str
    value: int

class UserParametersDouble(BaseModel):
    name: str
    value: float

class UserParametersString(BaseModel):
    name: str
    value: str

class UserParameters(BaseModel):
    userParameterLong: List[UserParametersLong] = Field(..., description="user parameter long")
    userParameterDouble: List[UserParametersDouble] = Field(..., description="user parameter double")
    userParameterString: List[UserParametersString] = Field(..., description="user parameter string")


class ISMRMRDHeader(BaseModel):
    measurementInformation: MeasurementInformation = Field(..., description="Measurement information")
    acquisitionSystemInformation: AcquisitionSystemInformation = Field(None, description="Acquisition system information")
    experimentalConditions: ExperimentalConditions = Field(..., description="Experimental conditions")
    encoding: List[Encoding] = Field(..., description="Encoding information")
    sequenceParameters: SequenceParameters = Field(..., description="Sequence parameters")
    userParameters: UserParameters = Field(..., description="User Parameters")

class NewCommands(str, Enum):
    """Pydantic definition of a commands."""

    START = "START"
    STOP = "STOP"
    PAUSE = "PAUSE"


class NewDeviceTask(BaseModel):
    ismrmrd_header: str
    command: NewCommands
    sequence: str

# Example data
# example_data = ISMRMRDHeader(
#     version=2,
#     measurementInformation=MeasurementInformation(
#         measurementID="12345",
#         seriesDate="2024-04-15",
#         seriesTime="12:00:00",
#         patientPosition="HFP",
#         protocolName="TSE",
#         seriesDescription="Head T2",
#         seriesInstanceUIDRoot="urn:uuid:12345678-abcd-1234-efgh-0123456789ab",
#         sequenceParameters=SequenceParameters(
#             TR=[1.0, 2.0, 3.0],
#             TE=[1.0, 2.0, 3.0],
#             TI=[1.0, 2.0, 3.0],
#             flipAngle_deg=[90.0, 90.0, 90.0],
#             echo_spacing=[0.001, 0.001, 0.001],
#             diffusionDimension="average",
#             diffusion=[
#                 DiffusionType(
#                     gradientDirection=GradientDirection(rl=1.0, ap=0.0, fh=0.0),
#                     bvalue=1000.0
#                 )
#             ],
#             diffusionScheme="DTI"
#         )
#     ),
#     experimentalConditions=ExperimentalConditions(H1resonanceFrequency_Hz=123),
#     encoding=[
#         Encoding(
#             encodedSpace=EncodingSpace(
#                 matrixSize=MatrixSize(x=128, y=128, z=1),
#                 fieldOfView_mm=FieldOfView(x=200, y=200, z=100)
#             ),
#             reconSpace=EncodingSpace(
#                 matrixSize=MatrixSize(x=128, y=128, z=1),
#                 fieldOfView_mm=FieldOfView(x=200, y=200, z=100)
#             ),
#             encodingLimits=EncodingLimits(
#                 kspace_encoding_step_0=LimitType(minimum=0, maximum=127, center=63),
#                 kspace_encoding_step_1=LimitType(minimum=0, maximum=127, center=63),
#                 kspace_encoding_step_2=LimitType(minimum=0, maximum=127, center=63)
#             ),
#             trajectory=TrajectoryType(trajectory="cartesian")
#         )
#     ]
# )
