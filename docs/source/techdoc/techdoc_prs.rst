Product Requirement Specification (PRS)
########################################

!! This Section is Work in Progress. !!

This section gathers all product requirements which can also be interpreted as the design input for the ScanHub platform.

Steakholder and User Roles
==========================

+----------+--------------------------------------------+-----------------------------------------------------------------------------------+
|    ID    |              Stakeholder                   |                                    Description                                    |
+==========+============================================+===================================================================================+
| SH_010   | Medical Professional                       | Medical professionals who operate or interpret the MRI scans. Operators prepare   |
|          | (MTRA, Radiologist)                        | patients, ensure optimal image quality, and provide feedback on the system's      |
|          |                                            | usability and functionality. Radiologists interpret the MRI scans to diagnose     |
|          |                                            | medical conditions.                                                               |
+----------+--------------------------------------------+-----------------------------------------------------------------------------------+
| SH_020   | Scientist                                  | Researchers who use MRI for advanced studies require access to experimental       |
|          |                                            | features, customized sequences (upload) and retrieval of raw data at distinct     |
|          |                                            | stages.                                                                           |   
+----------+--------------------------------------------+-----------------------------------------------------------------------------------+
| SH_030   | System Administrator                       | IT professionals responsible for the setup, maintenance, and security of the      |
|          |                                            | system. They ensure the reliability and data integrity of the system.             |
+----------+--------------------------------------------+-----------------------------------------------------------------------------------+
| SH_040   | (Field/Service) Engineer                   | Technical experts responsible for the installation, maintenance, and repair of    |
|          |                                            | the system. They ensure that the hardware as well as software components          |
|          |                                            | are functioning.                                                                  |
+----------+--------------------------------------------+-----------------------------------------------------------------------------------+
| SH_050   | Patient                                    | Individuals undergoing MRI scans. They are concerned with the comfort, safety,    |
|          |                                            | and privacy aspects of the MRI experience.                                        |
+----------+--------------------------------------------+-----------------------------------------------------------------------------------+
| SH_060   | Medical Device Manufacturer                | Company that produces and distribute the MRI system. It is concerned with the     |
|          | (Regulatory Affairs)                       | system’s marketability, quality, and regulatory compliance.                       |
+----------+--------------------------------------------+-----------------------------------------------------------------------------------+
| SH_070   | Healthcare Facility / Clinic / Hospital /  | Organizations that provide healthcare services and use the MRI system for         |
|          | Research Institution / Customer            | patient diagnosis. They are concerned with the system's reliability, efficiency,  |
|          | (Interoperability Manager)                 | and integration with other healthcare systems IT and healthcare workflows.        |
+----------+--------------------------------------------+-----------------------------------------------------------------------------------+


User Needs
==========

General
-------

.. list-table::
   :header-rows: 1
   :widths: 10 30 35 15 15 10

   * - ID
     - Product Requirements (Stakeholder)
     - Design Input
     - Acceptance Criteria
     - Intended claim
     - Priority
   * - PRS_0010
     - Execution of an MRI acquisition/job/experiment (Medical Professional, Scientist)
     - Upload pulseq sequence, execution MRI job with withflows
     -
     -
     -
   * - PRS_0020
     - Planning of an MRI examination (Medical Professional, Scientist)
     - Protocol-Tree, workflows, processing modality worklist
     -
     -
     -
   * - PRS_0030
     - DICOM viewer (Medical Professional, Scientist)
     - View DICOM image of a selected record, compare DICOM images, annotate DICOM image.
     -
     -
     -
   * - PRS_0040
     - User management (System Administrator)
     - Assign different user roles, support of multi-tendency cloud environment
     -
     -
     -
   * - PRS_0050
     - Monitor device status (Medical Professional, Scientist)
     - Current execution progress, detectable device malfunctiuons, device connection
     -
     -
     -
   * - PRS_0060
     - Monitor Patient safety (Medical Professional)
     - Specific absorption rate (SAR), temparatur, total scan time duration, Optional: Video stream, patient communication system
     -
     -
     -
   * - PRS_0070
     - Integration of processing workflows (Scientist)
     - Assambling of workflow steps to be executed on MRI raw data or images. Includes system calibration, image reconstruction and analysis.
     -
     -
     -
   * - PRS_0080
     - System calibration (Medical Professional, Scientist, Site Engineer)
     - Adjust larmorfrequency, adjust gradients, adjust system flip angle, B0-field shimming
     -
     -
     -
   * - PRS_0090
     - Clinical report (Medical Professional)
     - Structured form to create a clinical report which allows to fomulate a diagnosis, viewer for clinical reports
     -
     -
     -
   * - PRS_0100
     - Device management (System Administrator, Medical Professional, Medical Device Manufacturer)
     - Organisation of different devices, device authentification, device selection, device access management (who is trained on which device?)
     -
     -
     -


Operational Needs
-----------------
.. list-table::
   :header-rows: 1
   :widths: 10 25 35 15 20 10

   * - ID
     - Product Requirements (Stakeholder)
     - Design Input
     - Acceptance Criteria
     - Intended claim
     - Priority
   * - PRS_0010
     - Real-time Monitoring (Medical Professional)
     - * Continuously monitor and display MRI scan data in real-time.
       * Provide real-time feedback on scan quality and progress.
       * Instant notification for scan completion.
     - 99% uptime
     - Ensure real-time monitoring for accurate diagnosis.
     - Must Have
   * - PRS_0020
     - Alerting (Medical Professional)
     - Real-time alerts for scan anomalies or issues.
     - <5 minutes
     - Rapid response to scan anomalies or issues.
     - Should Have
   * - PRS_0030
     - On-Prem Setup (System Administrator)
     - Support for on-prem setups.
     - 100% Compatibility
     - Provide flexibility in deployment options to cater to different organizational needs.
     - Must Have
   * - PRS_0040
     - Cloud Setup (System Administrator)
     - Support for cloud setups in environments with no local compute workstations.
     - 100% Compatibility
     - Enable versatile deployment options to accommodate varying infrastructure.
     - Must Have

Regulatory Needs
----------------
.. list-table::
   :header-rows: 1
   :widths: 10 25 35 15 20 10

   * - ID
     - User Need (Stakeholder)
     - Design Input
     - Acceptance Criteria
     - Intended claim
     - Priority
   * - PRS_0110
     - Compliance (Regulatory Affairs)
     - * Compliance with HIPAA, GDPR, and FDA regulations.
       * Regular updates to adhere to evolving regulations.
       * Detailed logging and audit trails.
     - 100% Compliance
     - Ensure compliance with industry regulations for patient safety.
     - Must Have
   * - PRS_0120
     - Data Security (System Administrator)
     - Strong data encryption and role-based access control.
     - 100% Compliance
     - Secure patient data and adhere to compliance requirements.
     - Nice to Have
   * - PRS_0130
     - Compliance with ISO 14971:2019 (Regulatory Affairs)
     - Implementation of Risk Mitigation Measures (RMM) in adherence to ISO 14971:2019.
     - 100% Compliance
     - Minimize risks associated with the system operation.
     - Must Have

Reliability and Resilience Needs
--------------------------------
+----------+-----------------------------+-----------------------------------------+---------------------+------------------------------------+-----------+
|    ID    |   User Need (Stakeholder)   |              Design Input               | Acceptance Criteria |           Intended claim           | Priority  |
+==========+=============================+=========================================+=====================+====================================+===========+
| PRS_0210 | Reliability (Field Engineer)| System stability with minimum downtime. | 99.99% uptime       | Maintain a reliable and stable MRI | Must Have |
|          |                             |                                         |                     | acquisition system.                |           |
+----------+-----------------------------+-----------------------------------------+---------------------+------------------------------------+-----------+

Usability Needs
---------------
.. list-table::
   :header-rows: 1
   :widths: 10 25 35 15 20 10

   * - ID
     - User Need (Stakeholder)
     - Design Input
     - Acceptance Criteria
     - Intended claim
     - Priority
   * - PRS_0310
     - User-Friendly (Medical Professional)
     - * Intuitive UI for scan setup and patient management.
       * Comprehensive user manuals and guides.
       * Quick access to frequently used features.
     - <30 minutes onboarding
     - Streamline user interaction for increased productivity.
     - Should Have
   * - PRS_0320
     - Advanced Features (Scientist)
     - Access to raw MRI data and experimental sequence options.
     - N/A
     - Facilitate sequence development and research.
     - Nice to Have

Interoperability Needs
----------------------
+----------+--------------------------------------+-------------------------------------------+---------------------+----------------------------------------+-------------+-----+
|    ID    |      User Need (Stakeholder)         |               Design Input                | Acceptance Criteria |             Intended claim             |  Priority   |     |
+==========+======================================+===========================================+=====================+========================================+=============+=====+
| PRS_0410 | Interoperability                     | Compatibility with various DICOM systems. | N/A                 | Seamless integration with existing     | Should Have |     |
|          | (Medical Device Manufacturer)        |                                           |                     | healthcare systems.                    |             |     |
+----------+--------------------------------------+-------------------------------------------+---------------------+----------------------------------------+-------------+-----+
| PRS_0420 | Data Storage (Medical Professional)  | Support for XNAT storage.                 | N/A                 | Ensure compatibility with widely used  | Must Have   |     |
|          |                                      |                                           |                     | medical imaging data storage formats.  |             |     |
+----------+--------------------------------------+-------------------------------------------+---------------------+----------------------------------------+-------------+-----+
| PRS_0430 | File Format (Medical Professional)   | Support for NIFTI file format.            | N/A                 | Facilitate diverse data representation | Must Have   |     |
|          |                                      |                                           |                     | and interoperability.                  |             |     |
+----------+--------------------------------------+-------------------------------------------+---------------------+----------------------------------------+-------------+-----+
| PRS_0440 | File Format (Scientist)              | Support for ISMRMRD file format.          | N/A                 | Facilitate diverse data representation | Must Have   |     |
|          |                                      |                                           |                     | and interoperability.                  |             |     |
+----------+--------------------------------------+-------------------------------------------+---------------------+----------------------------------------+-------------+-----+
| PRS_0450 | File Format (Scientist)              | Support for RAW MR file format.           | N/A                 | Facilitate diverse data representation | Must Have   |     |
|          |                                      |                                           |                     | and interoperability.                  |             |     |
+----------+--------------------------------------+-------------------------------------------+---------------------+----------------------------------------+-------------+-----+

Maintainability Needs
---------------------
.. list-table::
   :header-rows: 1
   :widths: 10 25 35 15 20 10

   * - ID
     - User Need (Stakeholder)
     - Design Input
     - Acceptance Criteria
     - Intended claim
     - Priority
   * - PRS_0510
     - Scalability (System Administrator)
     - * Scalable architecture to accommodate increasing data and users.
       * Modular design for easy updates and enhancements.
       * Efficient data management and storage solutions.
     - <10% degradation at 2x data
     - Ensure system performance as data and users grow.
     - Should Have

System Interfaces to Third Party Solution Needs
-----------------------------------------------
+----------+-------------------------------+-----------------------------------+---------------------+------------------------------------+-----------+
|    ID    |    User Need (Stakeholder)    |           Design Input            | Acceptance Criteria |           Intended claim           | Priority  |
+==========+===============================+===================================+=====================+====================================+===========+
| PRS_0610 | Patient Monitoring Systems    | Seamless interaction with patient | Real-time data      | Ensure real-time data exchange and | Must Have |
|          | (Medical Device Manufacturer) | monitoring systems.               | exchange            | patient safety.                    |           |
+----------+-------------------------------+-----------------------------------+---------------------+------------------------------------+-----------+
