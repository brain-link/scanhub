""" Code to fill mrd-template from raw data (based on patrick_05). """

import os
import datetime
import time

import ismrmrd
import h5py
import ctypes
import numpy as np


def headerGradientScale(header_xml, gradient_scaling_factors, idx=0):
    for space in ['encodedSpace', 'reconSpace']:
        field_of_view = getattr(header_xml.encoding[idx], space).fieldOfView_mm
        field_of_view.x /= gradient_scaling_factors[0]
        field_of_view.y /= gradient_scaling_factors[1]
        field_of_view.z /= gradient_scaling_factors[2]
    return header_xml


def headerFill(header_xml, **kwargs):
    if header_xml is None:
        raise ValueError("header_xml is None. Cannot set attributes.")
        
    """
    Setzt Werte in header_xml anhand einer vordefinierten Zuordnung und gibt das aktualisierte Objekt zurück.
    
    Beispiel:
    header_xml = headerFill(header_xml, systemVendor="Siemens", studyDate="2025-03-18")
    """
    # Stelle sicher, dass die Haupt-Objekte existieren
    #if header_xml.studyInformation is None:
    #    header_xml.studyInformation = ismrmrd.xsd.StudyInformation()
    #if header_xml.measurementInformation is None:
    #    header_xml.measurementInformation = ismrmrd.xsd.MeasurementInformation()
    #if header_xml.acquisitionSystemInformation is None:
    #    header_xml.acquisitionSystemInformation = ismrmrd.xsd.AcquisitionSystemInformation()
    #if header_xml.experimentalConditions is None:
    #    header_xml.experimentalConditions = ismrmrd.xsd.ExperimentalConditions()
        
    # Switch-Case-ähnliche Struktur für erlaubte Ziel-Felder
    field_mapping = {
        # subjectInformation
        "patientName": (header_xml.subjectInformation, str),
        "patientWeight_kg": (header_xml.subjectInformation, float),
        "patientHeight_m": (header_xml.subjectInformation, float),
        "patientID": (header_xml.subjectInformation, str),
        "patientBirthdate": (header_xml.subjectInformation, "date"),
        "patientGender": (header_xml.subjectInformation, "gender"),
        
        # studyInformation
        "studyDate": (header_xml.studyInformation, "date"),
        "studyTime": (header_xml.studyInformation, "time"),
        "studyID": (header_xml.studyInformation, str),
        "accessionNumber": (header_xml.studyInformation, "long"),
        "referringPhysicianName": (header_xml.studyInformation, str),
        "studyDescription": (header_xml.studyInformation, str),
        "studyInstanceUID": (header_xml.studyInformation, str),
        "bodyPartExamined": (header_xml.studyInformation, str),
        
        # measurementInformation
        "measurementID": (header_xml.measurementInformation, str),
        "seriesDate": (header_xml.studyInformation, "date"),
        "seriesTime": (header_xml.studyInformation, "time"),
        "patientPosition": (header_xml.measurementInformation, "patientPositionType"),
        "relativeTablePosition": (header_xml.measurementInformation, "threeDimensionalFloat"),
        "initialSeriesNumber": (header_xml.measurementInformation, "long"),
        "protocolName": (header_xml.measurementInformation, str),
        "sequenceName": (header_xml.measurementInformation, str),
        "seriesDescription": (header_xml.measurementInformation, str),
           # measurementDependency << complex dataset -> use add_measurementDependency() method
        "seriesInstanceUIDRoot": (header_xml.measurementInformation, str),
        "frameOfReferenceUID": (header_xml.measurementInformation, str),
        "referencedImageSequence": (header_xml.measurementInformation, str),
        
        # acquisition system
        "systemVendor": (header_xml.acquisitionSystemInformation, str),
        "systemModel": (header_xml.acquisitionSystemInformation, str),
        "systemFieldStrength_T": (header_xml.measurementInformation, float),
        "relativeReceiverNoiseBandwidth": (header_xml.measurementInformation, float),
        "receiverChannels": (header_xml.acquisitionSystemInformation, "uint16"),
            # coilLabel  << complex dataset -> use add_coilLabel() method
        "institutionName": (header_xml.measurementInformation, str),
        "stationName": (header_xml.measurementInformation, str),
        "deviceID": (header_xml.measurementInformation, str),
        "deviceSerialNumber": (header_xml.measurementInformation, str),
        
        # experimentalConditions
        "H1resonanceFrequency_Hz": (header_xml.experimentalConditions, "long")
    }

    for field, value in kwargs.items():
        if field not in field_mapping:
            print(f"Warnung: Unbekanntes Feld '{field}', wird übersprungen.")
            continue

        target_obj, expected_type = field_mapping[field]
        
        #######################
        # Check the datatypes #
        #######################
        
        # "Standard" datatypes #
        if expected_type == "date":
            try:
                value = datetime.datetime.strptime(value, "%Y-%m-%d").date()  # Konvertieren zu Date-Objekt
            except ValueError:
                print(f"Fehler: '{field}' muss im Format YYYY-MM-DD sein.")
                return false
        elif expected_type == "time":
            try:
                value = datetime.datetime.strptime(value, "%H:%M:%S").time()  # Konvertieren zu Time-Objekt
            except ValueError:
                print(f"Fehler: '{field}' muss im Format HH:MM:SS sein.")
                return false
        elif expected_type == float:
            # Prüfen, ob es sich um eine gültige Fließkommazahl handelt
            if not isinstance(value, (float, np.floating)):
                print(f"Fehler: '{value}' ist keine gültige float-Zahl: {value}")
                return false
        elif expected_type == "long":
            if not (isinstance(value, (int, np.integer)) and -9223372036854775808 <= value <= 9223372036854775807):
                print(f"Fehler: '{field}' muss eine ganze Zahl sein.")
                return false
        elif expected_type == "uint16":
            # Prüfen, ob der Wert eine Ganzzahl im Bereich von uint16 ist
            if not (isinstance(value, (int, np.integer)) and 0 <= value <= 65535):
                print(f"Fehler: '{field}' muss eine ganze Zahl im Bereich von 0 bis 65535 sein.")
                return false
                
        # "Special" datatypes #
        elif expected_type == "threeDimensionalFloat":
            if isinstance(value, (list, tuple, np.ndarray)) and len(value) == 3 and all(isinstance(v, (int, float)) for v in value):
                target_obj.x, target_obj.y, target_obj.z = map(float, value)
                continue  # Kein `setattr` nötig, da die Werte direkt zugewiesen wurden
            else:
                print(f"Fehler: '{field}' muss eine Liste oder ein Array mit genau 3 Zahlen sein.")
                return false
        elif expected_type == "gender":
            value = value.upper()  # Kleinschreibung erlauben
            if value not in ('M', 'F', 'O'):
                print(f"Fehler: '{field}' muss 'M', 'F' oder 'O' (Other) sein.")
                return false
        elif expected_type == "patientPositionType":
            value = value.upper()  # Kleinschreibung erlauben
            if value not in ("HFP", "HFS", "HFDR", "HFDL", "FFP", "FFS", "FFDR", "FFDL"):
                print(f"Fehler: '{field}' muss 'HFP', 'HFS', 'HFDR', 'HFDL', 'FFP', 'FFS', 'FFDR' oder 'FFDL' sein.")
                return false
        elif not isinstance(value, expected_type):
            print(f"Fehler: '{field}' erwartet {expected_type.__name__}, aber {type(value).__name__} erhalten.")
            return false

        # Setze das Feld im XML-Header
        try:
            setattr(target_obj, field, value)
        except AttributeError as e:
            print(f"Fehler beim Setzen von {target_obj} {field}: {e}")

    return header_xml  # Falls weitere Verarbeitung nötig ist


def fill_mrd_template(output_filepath,
                      mrd_template_filepath,
                      raw_data_filepath,
                      measurement_id,
                      patient_position,
                      system_vendor,
                      system_model,
                      n_coil_available,
                      h1_resonance_frequency_hz,
                      gradient_scaling_factors,
                      n_coil_used,
                      slice_orientation_matrix,
                      position_shift,
                      patient_table_position):
                          
                          
    # read template
    mrd_template = ismrmrd.Dataset(mrd_template_filepath)
                          
    header_xml = ismrmrd.xsd.CreateFromDocument(mrd_template.read_xml_header())
        
    #print("DEBUG after Read: header_xml type:", type(header_xml))
    print("Template MRD header:", header_xml)
    print("")

    # Read Raw Data:
    h5py_rawdata = h5py.File(raw_data_filepath)
    acuired_data_real_part = h5py_rawdata['rawdata']['real'][0]
    acuired_data_real_part = h5py_rawdata['rawdata']['imag'][0]
    rawData = acuired_data_real_part + 1j * acuired_data_real_part

    # create new output file
    if os.path.isfile(output_filepath):
        os.remove(output_filepath)
    output_mrd_dataset = ismrmrd.Dataset(output_filepath)
    
    #################
    # Update header #
    #################
    # === studyInformation ===
    current_date = datetime.date.today().isoformat()  #<- with "import datetime"  YYYY-MM-DD <- "2025-03-18"
    #current_date = datetime.today().date().isoformat() #<- with "from datetime import datetime"  YYYY-MM-DD <- "2025-03-18"
    current_time = datetime.datetime.now().time().isoformat(timespec='seconds')  # HH:MM:SS <- "14:30:00"
    header_xml   = headerFill(header_xml, studyDate=current_date, studyTime=current_time)
    
    # === measurementInformation ===
    header_xml = headerFill(header_xml, measurementID=measurement_id, patientPosition=patient_position)
    
    # === acquisitionSystemInformation ===
    header_xml = headerFill(header_xml, systemVendor=system_vendor, systemModel=system_model, receiverChannels=n_coil_available)
    
    # === experimentalConditions ===
    header_xml = headerFill(header_xml, H1resonanceFrequency_Hz=h1_resonance_frequency_hz)
    
    # === encoding ===
    # All fields:  maxOccurs="1" minOccurs="1" -> Exactly 1 entry!
    # Rescale FOV
    headerGradientScale(header_xml, gradient_scaling_factors)
        
    # header_xml.encoding[0].encodedSpace.matrixSize
    # header_xml.encoding[0].encodedSpace.fieldOfView_mm
    # header_xml.reconSpace[0].encodedSpace.matrixSize
    # header_xml.reconSpace[0].encodedSpace.fieldOfView_mm
    # header_xml.reconSpace[0].encodingLimits.xxx << see type!
    # header_xml.reconSpace[0].trajectory.xxx << see type!
    # header_xml.reconSpace[0].trajectoryDescription.xxx << see type!
    # header_xml.reconSpace[0].parallelImaging.xxx << see type!
    # header_xml.reconSpace[0].echoTrainLength << long

    # === sequenceParameters ===
    # PURELY SEQ-DEV
    # TR / TE / TI / flipAngle_deg / sequence_type / echo_spacing / diffusionDimension / diffusion / diffusionScheme
    
    # === userParameters ===
    # PURELY SEQ-DEV for now
    #<userParameterString>
    #  <name>PulseqFile</name>
    #  <value>myFile.seq</value>
    #</userParameterString>
    #<userParameterString>
    #  <name>MyReconContainer</name>
    #  <value>Gadgetron</value>
    #</userParameterString>
    #<userParameterString>
    #  <name>MyReconConfig</name>
    #  <value>myFile.reco.gadegtron.xml</value>
    #</userParameterString>
    
    # === waveformInformation ===
    # PURELY HARDWARE (ECG,Pulsewave, ...) 

    print("Filled MRD header:", header_xml)
    print("")
    # Write updated header
    output_mrd_dataset.write_xml_header(header_xml.toXML())

    ################################    
    ### ===   ACQUISITIONS   === ###
    ################################
    # Process and update acquisitions
    start_idx = 0
    for i in range(mrd_template.number_of_acquisitions()):
        current_acq = mrd_template.read_acquisition(i)
        current_acq_head = current_acq.getHead()

        setattr(current_acq_head, 'active_channels', ctypes.c_uint16(n_coil_used))
        setattr(current_acq_head, 'available_channels', ctypes.c_uint16(n_coil_available))

        # Set encoding directions
        for fieldname in ['read_dir', 'phase_dir', 'slice_dir']:
            tmp_dir_result_np_array = np.dot(slice_orientation_matrix,   np.frombuffer(getattr(current_acq_head, fieldname), dtype=np.float32)  )
            tmp_dir_result_ctypes_array = (ctypes.c_float * 3)(*tmp_dir_result_np_array)
            setattr(current_acq_head, fieldname, tmp_dir_result_ctypes_array)

        # Set Slice position
        position_result_np_array = np.add(  np.frombuffer(getattr(current_acq_head, 'position'), dtype=np.float32)  , position_shift)
        position_result_ctypes_array = (ctypes.c_float * 3)(*position_result_np_array)
        setattr(current_acq_head, "position", position_result_ctypes_array)
        
        # Set patient_table_position
        table_position_result_ctypes_array = (ctypes.c_float * 3)(*patient_table_position)
        setattr(current_acq_head, "patient_table_position", table_position_result_ctypes_array)

        # Write Head to Acquisition
        current_acq.setHead(current_acq_head)
        
        # Write RawData to Acquisition
        try:
            # Get ADC sample count
            adc_samples = current_acq_head.number_of_samples
            # Extract corresponding raw data
            current_acq.data[:] = rawData[start_idx:start_idx + adc_samples]
            start_idx += adc_samples
        except IndexError:
            print(f"Error: Mismatch in rawData size at acquisition {i}. Skipping acquisition.")
            break
        
        # Append acquisition to output_mrd_dataset
        output_mrd_dataset.append_acquisition(current_acq)
        
    # Close Dataset
    output_mrd_dataset.close()


def main():
    # FILE PATHES
    # mrd_template_filepath = '/home/hucker/venv/a4im_ismrmrd/TestData/davids_t2_tse.si/3d-tse_t2.ismrmrd.h5'
    # output_filepath   = '/home/hucker/venv/a4im_ismrmrd/TestData/data_ismrmrd_t2__pyTEST05.h5'
    # rawdata_filepath   = '/home/hucker/venv/a4im_ismrmrd/TestData/RawDataOnly/RawData_hdf5_T2.h5'
    mrd_template_filepath = '/home/ben/Schreibtisch/Arbeit/ISMRMRD-handling/resources/davids_t2_tse.si/3d-tse_t2.ismrmrd.h5'
    output_filepath  = '/home/ben/Schreibtisch/Arbeit/ISMRMRD-handling/output/data_ismrmrd_t2__pyTEST05.h5'
    rawdata_filepath   = '/home/ben/Schreibtisch/Arbeit/ISMRMRD-handling/resources/RawDataOnly/RawData_hdf5_T2.h5'

    # GET DATA TO FILL IN
    n_coil_available = 1             # GET FROM BRAINLINKS
    system_vendor = 'COOL STUFF'     # GET FROM BRAINLINKS
    system_model = 'NICE MACHINE'    # GET FROM BRAINLINKS
    h1_resonance_frequency_hz = int(0.05 * 42 * 1000)
    measurement_id = '123_456_789_10'   # GET FROM BRAINLINKS <- 3 Underscores between numbers also e.g. 166008_353211551_361452753_28

    # FOV/UI DEFINITIONS
    n_coil_used = 1
    patient_position = 'HFS'  # GET FROM BRAINLINKS
    position_shift = np.array([10, 20, 30], dtype=np.float32)  # GET FROM BRAINLINKS
    slice_orientation_matrix = np.array([[1,  0,  0],
                                         [0,  0, -1],
                                         [0,  1,  0]], dtype=np.float32)
    gradient_scaling_factors = np.array([2, 2, 2], dtype=np.float32)  # GET FROM BRAINLINKS
    patient_table_position = np.zeros(3, dtype=np.float32)

    # Reset position and orientation
    #position_shift = np.array([0, 0, 0], dtype=np.float32)  # GET FROM BRAINLINKS
    #slice_orientation_matrix = np.array([[1, 0, 0],
    #                                     [0, 1, 0],
    #                                     [0, 0, 1]], dtype=np.float32)
    gradient_scaling_factors = [1, 1, 1]  # GET FROM BRAINLINKS

    # fill template
    startzeit = time.time()
    fill_mrd_template(output_filepath,
                      mrd_template_filepath,
                      rawdata_filepath,
                      measurement_id,
                      patient_position,
                      system_vendor,
                      system_model,
                      n_coil_available,
                      h1_resonance_frequency_hz,
                      gradient_scaling_factors,
                      n_coil_used,
                      slice_orientation_matrix,
                      position_shift,
                      patient_table_position)
    endzeit = time.time()
    laufzeit = endzeit - startzeit
    print(f"Laufzeit der Funktion: {laufzeit} Sekunden")
    

if __name__ == "__main__":
    main()

