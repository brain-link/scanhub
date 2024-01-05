# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

from cartesian_reco_operator import CartesianRecoOperator
from dicom_operator import DICOMOperator

from monai.deploy.core import Application, env, resource


@resource(cpu=1)
# pip_packages can be a string that is a path(str) to requirements.txt file or a list of packages.
@env(pip_packages=["scikit-image >= 0.17.2", "numpy >= 1.24.3"])
class App(Application):
    """This is an MRI cartesian reco application.

    This showcases how the MONAI application framework is used in the ScanHub platform.
    """

    # App's name. <class name>('App') if not specified.
    name = "mri_cartesian_reco_map"
    # App's description. <class docstring> if not specified.
    description = "This is an MRI cartesian reco application."
    # App's version. <git version tag> or '0.0.0' if not specified.
    version = "0.0.1"

    def compose(self):
        """This application has three operators.

        Each operator has a single input and a single output port.
        Each operator performs some kind of image processing function.
        """
        cartesian_op = CartesianRecoOperator()
        dicom_op = DICOMOperator()

        self.add_flow(cartesian_op, dicom_op)
        # self.add_flow(sobel_op, median_op, {"image": "image"})
        # self.add_flow(sobel_op, median_op, {"image": {"image"}})


if __name__ == "__main__":
    App(do_run=True)
