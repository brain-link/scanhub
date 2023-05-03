"""Test MRI-Device."""
import logging
import pathlib
from fastapi import FastAPI
from device import Device

import julia  # pylint: disable=wrong-import-order
julia.install()
from julia import KomaMRI  # pylint: disable=no-name-in-module,wrong-import-position,wrong-import-order


app = FastAPI()

class Mri(Device):
    """implementation of connector between mri device and acqcontrol"""

    @staticmethod
    def start_scan(scan_request, records_path):
        scan_request.record_id = 1 # TODO: remove, test purposes

        seq_file = f"{records_path}{scan_request.record_id}\\sequence"
        sequence = ""
        with open(seq_file, "r", encoding='UTF-8') as sequence_file:
            sequence = sequence_file.read()
        logging.debug("Loaded sequence: %s", sequence)
        logging.debug(seq_file)
        #seq = KomaMRI.read_seq("C:/Users/johan/git/scanhub/tools/device/records/1/sequence")
        seq = KomaMRI.read_seq(seq_file)
        sys = KomaMRI.Scanner()
        obj = KomaMRI.brain_phantom2D()

        raw = KomaMRI.simulate(obj, seq, sys)
        KomaMRI.plot_signal(raw)
        return

    @staticmethod
    def pre_scan(scan_request):
        """steps to do before the scan is executed"""
        return

    @staticmethod
    def post_scan(scan_request):
        """steps to do after the scan was executed"""
        return

cur_path = pathlib.Path(__file__).parent.resolve()
mri = Mri("127.0.0.1:8080/api/v1/mri/acquisitioncontrol", f"{cur_path}\\records\\", app)
