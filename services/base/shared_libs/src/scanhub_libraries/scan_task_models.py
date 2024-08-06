# Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
"""
This module contains a set of Pydantic models designed to facilitate 
the creation of an MRI scan job,including a minimal ISMRMRD header.
These models help structure and validate the data necessary for 
defining MRI scans, sequences, and associated parameters.
"""

from enum import Enum
from typing import List

from pydantic import BaseModel, Field


class MatrixSize(BaseModel):
    """Represents the dimensions of the matrix size in the encoding space."""

    x: int = Field(1, description="Matrix size in the x dimension")
    y: int = Field(1, description="Matrix size in the y dimension")
    z: int = Field(1, description="Matrix size in the z dimension")


class FieldOfView(BaseModel):
    """Represents the field of view in millimeters in each dimension."""

    x: float = Field(..., description="Field of view in the x dimension in mm")
    y: float = Field(..., description="Field of view in the y dimension in mm")
    z: float = Field(..., description="Field of view in the z dimension in mm")


class EncodingSpace(BaseModel):
    """Represents the encoding space parameters, including matrix size and field of view."""

    matrixSize: MatrixSize = Field(..., description="Matrix size of the encoding space")
    fieldOfView_mm: FieldOfView = Field(..., description="Field of view of the encoding space")


class LimitType(BaseModel):
    """Defines the encoding limits."""

    minimum: int = Field(0, description="Minimum value")
    maximum: int = Field(0, description="Maximum value")
    center: int = Field(0, description="Center value")


class EncodingLimits(BaseModel):
    """Defines the encoding limits for k-space encoding steps."""

    kspace_encoding_step_0: LimitType = \
        Field(..., description="Encoding limits for k-space encoding step 0")
    kspace_encoding_step_1: LimitType = \
        Field(..., description="Encoding limits for k-space encoding step 1")
    kspace_encoding_step_2: LimitType = \
        Field(..., description="Encoding limits for k-space encoding step 2")


class Trajectories(str, Enum):
    """Enumeration of possible trajectory types."""

    CARTESIAN = "cartesian"
    EPI = "epi"
    RADIAL = "radial"
    GOLDENANGLE = "goldenangle"
    SPIRAL = "spiral"
    OTHER = "other"


class DiffusionDimensions(str, Enum):
    """Enumeration of possible diffusion dimensions."""

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
    """Defines the encoding parameters for the scan."""

    encodedSpace: EncodingSpace = Field(..., description="Encoded space")
    reconSpace: EncodingSpace = Field(..., description="Reconstruction space")
    encodingLimits: EncodingLimits = Field(..., description="Encoding limits")
    trajectory: Trajectories = Field(..., description="Trajectories")


class ExperimentalConditions(BaseModel):
    """Defines the experimental conditions."""

    H1resonanceFrequency_Hz: int = Field(..., description="H1 resonance frequency in Hz")


class GradientDirection(BaseModel):
    """Defines the gradient direction in each dimension."""

    rl: float = Field(..., description="Gradient direction in the right-left dimension")
    ap: float = Field(..., description="Gradient direction in the anterior-posterior dimension")
    fh: float = Field(..., description="Gradient direction in the foot-head dimension")


class DiffusionType(BaseModel):
    """Defines the diffusion parameters."""

    gradientDirection: GradientDirection = Field(..., description="Gradient direction")
    bvalue: float = Field(..., description="b-value")


class SequenceParameters(BaseModel):
    """Defines the sequence parameters for the scan."""

    TR: List[float] = Field(..., description="Repetition time in seconds")
    TE: List[float] = Field(..., description="Echo time in seconds")
    TI: List[float] = Field(..., description="Inversion time in seconds")
    flipAngle_deg: List[float] = Field(..., description="Flip angle in degrees")
    sequence_type: str = Field(..., description="Sequence type")
    echo_spacing: List[float] = Field(..., description="Echo spacing in seconds")
    diffusionDimension: DiffusionDimensions = Field(..., description="Diffusion Dimensions")
    diffusion: List[DiffusionType] = Field(..., description="Diffusion information")
    diffusionScheme: str = Field(..., description="Diffusion scheme")


class PatientPositions(str, Enum):
    """Enumeration of possible patient positions."""

    HFP = "HFP"
    HFS = "HFS"
    HFDR = "HFDR"
    HFDL = "HFDL"
    FFP = "FFP"
    FFS = "FFS"
    FFDR = "FFDR"
    FFDL = "FFDL"


class MeasurementInformation(BaseModel):
    """Defines the measurement information."""

    measurementID: str = Field(..., description="Measurement ID")
    patientPosition: PatientPositions = Field(..., description="Patient position")
    sequenceName: str = Field(..., description="Sequence ID")


class AcquisitionSystemInformation(BaseModel):
    """Defines the acquisition system information."""

    deviceID: str = Field(..., description="Device ID")


class UserParametersLong(BaseModel):
    """Defines a user parameter with a long value."""

    name: str = Field(..., description="Parameter name")
    value: int = Field(..., description="Parameter value")


class UserParametersDouble(BaseModel):
    """Defines a user parameter with a double value."""

    name: str = Field(..., description="Parameter name")
    value: float = Field(..., description="Parameter value")


class UserParametersString(BaseModel):
    """Defines a user parameter with a string value."""

    name: str = Field(..., description="Parameter name")
    value: str = Field(..., description="Parameter value")


class UserParameters(BaseModel):
    """Defines a collection of user parameters."""

    userParameterLong: List[UserParametersLong] = \
        Field(..., description="User parameters with long values")
    userParameterDouble: List[UserParametersDouble] = \
        Field(..., description="User parameters with double values")
    userParameterString: List[UserParametersString] = \
        Field(..., description="User parameters with string values")


class ISMRMRDHeader(BaseModel):
    """Defines the ISMRMRD header for the MRI scan job."""

    measurementInformation: MeasurementInformation = \
        Field(..., description="Measurement information")
    acquisitionSystemInformation: AcquisitionSystemInformation = \
        Field(None, description="Acquisition system information")
    experimentalConditions: ExperimentalConditions = \
        Field(..., description="Experimental conditions")
    encoding: List[Encoding] = Field(..., description="Encoding information")
    sequenceParameters: SequenceParameters = Field(..., description="Sequence parameters")
    userParameters: UserParameters = Field(..., description="User Parameters")


class Commands(str, Enum):
    """Enumeration of possible commands."""

    START = "START"
    STOP = "STOP"
    PAUSE = "PAUSE"


class DeviceTask(BaseModel):
    """Defines a new device task with an ISMRMRD header and a command."""

    ismrmrd_header: str = Field(..., description="ISMRMRD header in JSON format")
    command: Commands = Field(..., description="Command")
    sequence: str = Field(..., description="Sequence")
