# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

import monai.deploy.core as md
from monai.deploy.core import DataPath, ExecutionContext, Image, InputContext, IOType, Operator, OutputContext

import numpy as np

fft2 = np.fft.fft2
ifft2 = np.fft.ifft2

fftshift = np.fft.fftshift
ifftshift = np.fft.ifftshift

@md.input("image", DataPath, IOType.DISK)
@md.output("image", Image, IOType.IN_MEMORY)
# If `pip_packages` is specified, the definition will be aggregated with the package dependency list of other
# operators and the application in packaging time.
@md.env(pip_packages=["numpy >= 1.24.3"])
class CartesianRecoOperator(Operator):
    """This Operator implements a Cartesian MRI reco.

    It has a single k-space input and single image output.
    """

    @staticmethod
    def np_ifft(kspace: np.ndarray, out: np.ndarray):
        """Perform inverse FFT function (kspace to [magnitude] image).

        Performs iFFT on the input data and updates the display variables for
        the image domain (magnitude) image and the kspace as well.

        Parameters
        ----------
            kspace (np.ndarray): Complex kspace ndarray
            out (np.ndarray): Array to store values
        """
        np.absolute(fftshift(ifft2(ifftshift(kspace))), out=out)


    def compute(self, op_input: InputContext, op_output: OutputContext, context: ExecutionContext):
        """Compute the cartesian reco.
        """
        input_path = op_input.get().path
        if input_path.is_dir():
            input_path = next(input_path.glob("*.*"))  # take the first file

        kspacedata = np.load(input_path)

        img = np.zeros_like(kspacedata, dtype=np.float32)

        CartesianRecoOperator.np_ifft(kspacedata, img)

        ################################################################
        # Store DICOM
        ################################################################

        img16 = img.astype(np.float16)
        
        op_output.set(Image(img16))

        # data_in = io.imread(input_path)[:, :, :3]  # discard alpha channel if exists
        # data_out = filters.sobel(data_in)

        # op_output.set(Image(data_out))
