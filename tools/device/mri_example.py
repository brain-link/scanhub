# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Test MRI-Device."""
from fastapi import FastAPI
from device import Device

app = FastAPI()

class Mri(Device):
    """implementation of connector between mri device and acqcontrol"""
    @staticmethod
    def simulate_scan():
        """simulates a scan"""
        # TODO: This is just for debug purposes
        return

    @staticmethod
    def start_scan(scan_request, records_path):
        """do something to start the scan"""
        Mri.simulate_scan()

    @staticmethod
    def pre_scan(scan_request):
        """steps to do before the scan is executed"""
        return

    @staticmethod
    def post_scan(scan_request):
        """steps to do after the scan was executed"""
        return

## TBD: This shall be replaced with the workflow-manager's API
mri = Mri("127.0.0.1:8080/api/v1/mri/acquisitioncontrol", "./records/", app)
