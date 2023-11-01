Product Requirements (PRS)
##########################

!! This Section is Work in Progress. !!

This section gathers all product requirements which can also be interpreted as the design input for the ScanHub platform.

Steakholder and User Roles
==========================

+----------+--------------------------------------------+-----------------------------------------------------------------------------------+
|    ID    |              Stakeholder                   |                                    Description                                    |
+==========+============================================+===================================================================================+
| SH_010   | MRI Technician / MTRA                      | Operates the MRI machine, prepares patients for scans, and ensures optimal        |
|          |                                            | image quality. They provide feedback on the system's usability and functionality. |
+----------+--------------------------------------------+-----------------------------------------------------------------------------------+
| SH_020   | Radiologist                                | Medical professionals who interpret MRI scans to diagnose medical conditions.     |
|          |                                            | They require high-quality images and efficient workflow for accurate diagnosis.   |
+----------+--------------------------------------------+-----------------------------------------------------------------------------------+
| SH_030   | Developer                                  | Software engineers responsible for designing, coding, and maintaining the MRI     |
|          |                                            | system software. They ensure the system meets all technical requirements.         |
+----------+--------------------------------------------+-----------------------------------------------------------------------------------+
| SH_040   | Scientist                                  | Researchers who use MRI for advanced studies and might require access to raw      |
|          |                                            | data and experimental features for research purposes.                             |
+----------+--------------------------------------------+-----------------------------------------------------------------------------------+
| SH_050   | System Administrator                       | IT professionals responsible for the system's setup, maintenance, and security.   |
|          |                                            | They ensure the system's reliability and data integrity.                          |
+----------+--------------------------------------------+-----------------------------------------------------------------------------------+
| SH_060   | Site Engineer                              | Technical experts responsible for the installation, maintenance, and repair of    |
|          |                                            | the MRI hardware. They ensure the system's physical components are functioning.   |
+----------+--------------------------------------------+-----------------------------------------------------------------------------------+
| SH_070   | Regulatory Affairs (RA) Specialist         | Professionals ensuring that the MRI system complies with all relevant regulatory  |
|          |                                            | standards and guidelines, such as FDA, HIPAA, and GDPR.                           |
+----------+--------------------------------------------+-----------------------------------------------------------------------------------+
| SH_080   | Medical Device Manufacturer                | Companies that produce and distribute the MRI system. They are concerned with     |
|          |                                            | the system's marketability, quality, and regulatory compliance.                   |
+----------+--------------------------------------------+-----------------------------------------------------------------------------------+
| SH_090   | Patient                                    | Individuals undergoing MRI scans. They are concerned with the comfort, safety,    |
|          |                                            | and privacy aspects of the MRI experience.                                        |
+----------+--------------------------------------------+-----------------------------------------------------------------------------------+
| SH_100   | Healthcare Facility / Clinic / Hospital /  | Organizations that provide healthcare services and use the MRI system for         |
|          | Customer                                   | patient diagnosis. They are concerned with the system's reliability, efficiency,  |
|          |                                            | and integration with other healthcare systems.                                    |
+----------+--------------------------------------------+-----------------------------------------------------------------------------------+


User Needs
==========

General
-------

User needs in the following table needs to be sharpened.

+----------+---------------------------------------------------------------------+-----------------------------------------------------------------------------------+---------------------+----------------+----------+
|    ID    |                 Product Requirements [Steakholder]                  |                                   Design Input                                    | Acceptance Criteria | Intended claim | Priority |
+==========+=====================================================================+===================================================================================+=====================+================+==========+
| PRS_0010 | Execution of an MRI acquisition/job/experiment                      | Upload pulseq sequence, execution MRI job with withflows                          |                     |                |          |
|          | (Radiologist, MRI Technician, Scientist)                            |                                                                                   |                     |                |          |
+----------+---------------------------------------------------------------------+-----------------------------------------------------------------------------------+---------------------+----------------+----------+
| PRS_0020 | Planning of an MRI examination                                      | Exam-Tree, workflows, processing modality worklist                                |                     |                |          |
|          | (Radiologist, MRI Technician, Scientist)                            |                                                                                   |                     |                |          |
+----------+---------------------------------------------------------------------+-----------------------------------------------------------------------------------+---------------------+----------------+----------+
| PRS_0030 | DICOM viewer                                                        | View DICOM image of a selected record, compare DICOM images,                      |                     |                |          |
|          | (Radiologist, MRI Technician, Scientist)                            | annotate DICOM image.                                                             |                     |                |          |
+----------+---------------------------------------------------------------------+-----------------------------------------------------------------------------------+---------------------+----------------+----------+
| PRS_0040 | User management                                                     | Assign different user roles, support of multi-tendency cloud environment          |                     |                |          |
|          | (System Administrator)                                              |                                                                                   |                     |                |          |
+----------+---------------------------------------------------------------------+-----------------------------------------------------------------------------------+---------------------+----------------+----------+
| PRS_0050 | Monitor device status                                               | Current execution progress, detectable device malfunctiuons,                      |                     |                |          |
|          | (Radiologist, MRI Technician, Scientist)                            | device connection                                                                 |                     |                |          |
+----------+---------------------------------------------------------------------+-----------------------------------------------------------------------------------+---------------------+----------------+----------+
| PRS_0060 | Monitor Patient safety                                              | Specific absorption rate (SAR), temparatur, total scan time duration,             |                     |                |          |
|          | (MRI Technician)                                                    | Optional: Video stream, patient communication system                              |                     |                |          |
+----------+---------------------------------------------------------------------+-----------------------------------------------------------------------------------+---------------------+----------------+----------+
| PRS_0070 | Integration of processing workflows                                 | Assambling of workflow steps to be executed on MRI raw data or images.            |                     |                |          |
|          | (Scientist, Developer)                                              | Includes system calibration, image reconstruction and analysis.                   |                     |                |          |
|          |                                                                     |                                                                                   |                     |                |          |
+----------+---------------------------------------------------------------------+-----------------------------------------------------------------------------------+---------------------+----------------+----------+
| PRS_0080 | System calibration                                                  | Adjust larmorfrequency, adjust gradients, adjust system flip angle,               |                     |                |          |
|          | (MRI Technician, Scientist, Site Engineer, Radiologist)             | B0-field shimming                                                                 |                     |                |          |
+----------+---------------------------------------------------------------------+-----------------------------------------------------------------------------------+---------------------+----------------+----------+
| PRS_0090 | Clinical report                                                     | Structured form to create a clinical report which allows to fomulate a diagnosis, |                     |                |          |
|          | (Radiologist)                                                       | viewer for clinical reports                                                       |                     |                |          |
+----------+---------------------------------------------------------------------+-----------------------------------------------------------------------------------+---------------------+----------------+----------+
| PRS_0100 | Device management                                                   | Organisation of different devices, device authentification, device selection,     |                     |                |          |
|          | (System Administrator, MRI Technician, Medical Device Manufacturer) | device access management (who is trained on which device?)                        |                     |                |          |
+----------+---------------------------------------------------------------------+-----------------------------------------------------------------------------------+---------------------+----------------+----------+


Operational Needs
-----------------
+----------+----------------------------------------+----------------------------------------------+---------------------+------------------------------------------+-------------+
|    ID    |   Product Requirements [Steakholder]   |                 Design Input                 | Acceptance Criteria |              Intended claim              |  Priority   |
+==========+========================================+==============================================+=====================+==========================================+=============+
| PRS_0010 | Real-time Monitoring (Radiologist)     | - Continuously monitor and display MRI scan  | 99% uptime          | Ensure real-time monitoring for accurate | Must Have   |
|          |                                        | data in real-time.                           |                     | diagnosis.                               |             |
|          |                                        | - Provide real-time feedback on scan quality |                     |                                          |             |
|          |                                        | and progress.                                |                     |                                          |             |
|          |                                        | - Instant notification for scan completion.  |                     |                                          |             |
+----------+----------------------------------------+----------------------------------------------+---------------------+------------------------------------------+-------------+
| PRS_0020 | Alerting (MRI Technician, Radiologist) | Real-time alerts for scan anomalies or       | <5 minutes          | Rapid response to scan anomalies or      | Should Have |
|          |                                        | issues.                                      |                     | issues.                                  |             |
+----------+----------------------------------------+----------------------------------------------+---------------------+------------------------------------------+-------------+
| PRS_0030 | On-Prem Setup (System Administrator)   | Support for on-prem setups.                  | 100% Compatibility  | Provide flexibility in deployment        | Must Have   |
|          |                                        |                                              |                     | options to cater to different            |             |
|          |                                        |                                              |                     | organizational needs.                    |             |
+----------+----------------------------------------+----------------------------------------------+---------------------+------------------------------------------+-------------+
| PRS_0040 | Cloud Setup (System Administrator)     | Support for cloud setups in environments     | 100% Compatibility  | Enable versatile deployment options      | Must Have   |
|          |                                        | with no local compute workstations.          |                     | to accommodate varying infrastructure.   |             |
+----------+----------------------------------------+----------------------------------------------+---------------------+------------------------------------------+-------------+

Regulatory Needs
----------------
+----------+--------------------------------------+--------------------------------------------+---------------------+------------------------------------+--------------+
|    ID    |          User Need (Actor)           |                Design Input                | Acceptance Criteria |           Intended claim           |   Priority   |
+==========+======================================+============================================+=====================+====================================+==============+
| PRS_0110 | Compliance (RA                       | - Compliance with HIPAA, GDPR, and FDA     | 100% Compliance     | Ensure compliance with industry    | Must Have    |
|          | Specialist)                          | regulations.                               |                     | regulations for patient safety.    |              |
|          |                                      | - Regular updates to adhere to evolving    |                     |                                    |              |
|          |                                      | regulations.                               |                     |                                    |              |
|          |                                      | - Detailed logging and audit trails.       |                     |                                    |              |
+----------+--------------------------------------+--------------------------------------------+---------------------+------------------------------------+--------------+
| PRS_0120 | Data Security (System Administrator) | Strong data encryption and role-based      | 100% Compliance     | Secure patient data and adhere to  | Nice to Have |
|          |                                      | access control.                            |                     | compliance requirements.           |              |
+----------+--------------------------------------+--------------------------------------------+---------------------+------------------------------------+--------------+
| PRS_0130 | Compliance with ISO 14971:2019       | Implementation of Risk Mitigation Measures | 100% Compliance     | Minimize risks associated with the | Must Have    |
|          | (RA Specialist)                      | (RMM) in adherence to ISO 14971:2019.      |                     | system operation.                  |              |
+----------+--------------------------------------+--------------------------------------------+---------------------+------------------------------------+--------------+

Reliability and Resilience Needs
--------------------------------
+----------+-----------------------------+-----------------------------------------+---------------------+------------------------------------+-----------+
|    ID    |      User Need (User)       |              Design Input               | Acceptance Criteria |           Intended claim           | Priority  |
+==========+=============================+=========================================+=====================+====================================+===========+
| PRS_0210 | Reliability (Site Engineer) | System stability with minimum downtime. | 99.99% uptime       | Maintain a reliable and stable MRI | Must Have |
|          |                             |                                         |                     | acquisition system.                |           |
+----------+-----------------------------+-----------------------------------------+---------------------+------------------------------------+-----------+

Usability Needs
---------------
+----------+--------------------------------+---------------------------------------------+---------------------+-------------------------------------+--------------+
|    ID    |        User Need (User)        |                Design Input                 | Acceptance Criteria |           Intended claim            |   Priority   |
+==========+================================+=============================================+=====================+=====================================+==============+
| PRS_0310 | User-Friendly (MRI Technician) | - Intuitive UI for scan setup and patient   | <30 minutes         | Streamline user interaction for     | Should Have  |
|          |                                | management.                                 | onboarding          | increased productivity.             |              |
|          |                                | - Comprehensive user manuals and guides.    |                     |                                     |              |
|          |                                | - Quick access to frequently used features. |                     |                                     |              |
+----------+--------------------------------+---------------------------------------------+---------------------+-------------------------------------+--------------+
| PRS_0320 | Advanced Features (Scientist)  | Access to raw MRI data and experimental     | N/A                 | Facilitate sequence development and | Nice to Have |
|          |                                | sequence options.                           |                     | research.                           |              |
+----------+--------------------------------+---------------------------------------------+---------------------+-------------------------------------+--------------+

Interoperability Needs
----------------------
+----------+-------------------------------+-------------------------------------------+---------------------+----------------------------------------+-------------+-----+
|    ID    |       User Need (Actor)       |               Design Input                | Acceptance Criteria |             Intended claim             |  Priority   |     |
+==========+===============================+===========================================+=====================+========================================+=============+=====+
| PRS_0410 | Interoperability              | Compatibility with various DICOM systems. | N/A                 | Seamless integration with existing     | Should Have |     |
|          | (Medical Device Manufacturer) |                                           |                     | healthcare systems.                    |             |     |
+----------+-------------------------------+-------------------------------------------+---------------------+----------------------------------------+-------------+-----+
| PRS_0420 | Data Storage (Radiologist)    | Support for XNAT storage.                 | N/A                 | Ensure compatibility with widely used  | Must Have   |     |
|          |                               |                                           |                     | medical imaging data storage formats.  |             |     |
+----------+-------------------------------+-------------------------------------------+---------------------+----------------------------------------+-------------+-----+
| PRS_0430 | File Format (Radiologist)     | Support for NIFTI file format.            | N/A                 | Facilitate diverse data representation | Must Have   |     |
|          |                               |                                           |                     | and interoperability.                  |             |     |
+----------+-------------------------------+-------------------------------------------+---------------------+----------------------------------------+-------------+-----+
| PRS_0440 | File Format (Scientist)       | Support for ISMRMRD file format.          | N/A                 | Facilitate diverse data representation | Must Have   |     |
|          |                               |                                           |                     | and interoperability.                  |             |     |
+----------+-------------------------------+-------------------------------------------+---------------------+----------------------------------------+-------------+-----+
| PRS_0450 | File Format (Scientist)       | Support for RAW MR file format.           | N/A                 | Facilitate diverse data representation | Must Have   |     |
|          |                               |                                           |                     | and interoperability.                  |             |     |
+----------+-------------------------------+-------------------------------------------+---------------------+----------------------------------------+-------------+-----+

Maintainability Needs
---------------------
+----------+------------------------------------+-----------------------------------------+---------------------+---------------------------------------+-------------+
|    ID    |         User Need (Actor)          |              Design Input               | Acceptance Criteria |            Intended claim             |  Priority   |
+==========+====================================+=========================================+=====================+=======================================+=============+
| PRS_0510 | Scalability (System Administrator) | - Scalable architecture to accommodate  | <10% degradation    | Ensure system performance as data and | Should Have |
|          |                                    | increasing data and users.              | at 2x data          | users grow.                           |             |
|          |                                    | - Modular design for easy updates and   |                     |                                       |             |
|          |                                    | enhancements.                           |                     |                                       |             |
|          |                                    | - Efficient data management and storage |                     |                                       |             |
|          |                                    | solutions.                              |                     |                                       |             |
+----------+------------------------------------+-----------------------------------------+---------------------+---------------------------------------+-------------+

System Interfaces to Third Party Solution Needs
-----------------------------------------------
+----------+-------------------------------+-----------------------------------+---------------------+------------------------------------+-----------+
|    ID    |       User Need (Actor)       |           Design Input            | Acceptance Criteria |           Intended claim           | Priority  |
+==========+===============================+===================================+=====================+====================================+===========+
| PRS_0610 | Patient Monitoring Systems    | Seamless interaction with patient | Real-time data      | Ensure real-time data exchange and | Must Have |
|          | (Medical Device Manufacturer) | monitoring systems.               | exchange            | patient safety.                    |           |
+----------+-------------------------------+-----------------------------------+---------------------+------------------------------------+-----------+
