Software Requirement Specification (SWRS)
#########################################

!! This Section is Work in Progress. !!


General
=======
Purpose
-------
This document encompasses all relevant software requirements, both functional and non-functional, for the MRI acquisition software of the A4IM scanner system. At the software system level, it integrates inputs from various foundational documents to provide a comprehensive outline of the required software functionalities and attributes. Specifically, this SW Requirements Specification (SWRS) draws from the following sources:

- Product Requirement Specification (PRS) for the A4IM scanner, detailing the expectations and needs from a product standpoint.
- System Requirements Specification (SRS) for the A4IM scanner, outlining the system-level requirements that the software must meet to ensure compatibility and performance within the MRI system.
- Risk Assessment Worksheet, identifying potential risks associated with the software and the necessary mitigations to ensure patient and operator safety.

This SWRS aims to detail the complete software solution for the A4IM MRI system, ensuring that all aspects of software functionality, safety, and performance are thoroughly addressed.

Scope
-----
The scope of this document is to define the functional and non-functional requirements for the MRI acquisition software for the A4IM scanner. This includes, but is not limited to, the following aspects:

- Acquisition and processing of MRI data.
- User interface and interaction mechanisms for medical professionals.
- Integration with healthcare facility systems, including patient management and data storage solutions.
- Compliance with healthcare regulations and standards for data protection, privacy, and security.
- System performance, reliability, and maintenance requirements.
- Safety measures and risk mitigation strategies relevant to software operation.

By covering these areas, the SWRS aims to ensure that the software meets all necessary criteria for successful deployment and operation within medical and research settings.

References
----------
Product Requirement Specification (PRS) for the A4IM Scanner, Document No. [To Be Added], Version [To Be Added].
System Requirements Specification (SRS) for the A4IM Scanner, Document No. [To Be Added], Version [To Be Added].
Risk Assessment Worksheet for the A4IM Scanner Software, Document No. [To Be Added], Version [To Be Added].
Note: The document numbers and versions will be finalized and added to this section upon completion of the respective documents.

This section sets the foundation for the development and evaluation of the MRI acquisition software, ensuring alignment with the overall objectives and requirements of the A4IM scanner system.

Software Requirements (Software System)
======================================
Overview SW Description
-----------------------
This document pertains to the MRI acquisition software for the A4IM scanner, aimed at providing a comprehensive solution for the acquisition, processing, and management of MRI data. The software is designed to ensure high-quality imaging of the human head and extremities, with a focus on maximizing the efficiency and effectiveness of diagnostic processes within healthcare facilities.

The MRI acquisition software integrates seamlessly with the A4IM scanner's hardware components, including the permanent magnets, radiofrequency (RF) coils, and gradient coils, to facilitate the capture of detailed images. It also includes functionalities for patient data management, real-time scan monitoring, image reconstruction, and storage, all within a user-friendly interface that supports healthcare professionals in their daily operations.

For detailed information on the system's intended use, components, and operational context, please refer to the Device Description document provided earlier.

Scenarios and Use Cases
-----------------------
To outline the main usage scenarios and inform the definition of system requirements, we identify the stakeholders of the MRI acquisition as defined in the PRS. The following scenarios and use cases are derived from the PRS and SRS and serve as a basis for the functional requirements of the software system. Each scenario is associated with the relevant stakeholders and provides a high-level description of the expected system behavior. The scenarios are as follows:

System Startup and Initialization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- Scenario: Booting up the MRI system, initializing all software components, and conducting self-checks.
- Procedure: Automated system checks for hardware and software integrity, loading of necessary drivers and applications, and verification of system readiness for operation.
- Stakeholder: SH_010, SH_020, SH_030, SH_040

User Authentication and Access Control
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- Scenario: Ensuring only authorized personnel can operate or access different levels of the system.
- Procedure: Secure login processes, role-based access control, and user authentication protocols.
- Stakeholder: SH_030

Patient Data Input and Retrieval
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- Scenario: Entering new patient data or retrieving existing patient records before starting a scan.
- Procedure: Integration with hospital information systems for seamless data exchange, ensuring data accuracy and privacy compliance.
- Stakeholder: SH_010, SH_020

Scan Parameter Selection and Customization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- Scenario: Selection and customization of MRI scan parameters based on the specific clinical requirements.
- Procedure: User interfaces that allow for easy selection and adjustment of scan parameters, including sequence, FOV dimensions and offsets, information on the hardware setup (e.g. coil code, etc.)
- Stakeholder: SH_010, SH_020

Real-Time Scan Monitoring
~~~~~~~~~~~~~~~~~~~~~~~~~
- Scenario: Monitoring the MRI scan in real-time and making necessary adjustments.
- Procedure: Dynamic display of scanning progress
- Stakeholder: SH_010, SH_020

Image Reconstruction and Storage
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- Scenario: Reconstruction of the raw scan data to produce images and storing them appropriately.
- Procedure: Automated image reconstruction algorithms, along with efficient data storage solutions both on-premises and in cloud environments.
- Stakeholder: SH_010, SH_020, SH_030

System Shutdown and Secure Data Handling
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- Scenario: Properly shutting down the system while ensuring all patient data is securely saved and protected.
- Procedure: Step-by-step shutdown process that includes data backup, closing of all active sessions, and hardware cooling procedures.
- Stakeholder: SH_010, SH_020, SH_030

Routine Maintenance and Calibration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- Scenario: Regular system maintenance and calibration to ensure ongoing accuracy and efficiency.
- Procedure: Scheduled maintenance tasks, automated calibration routines, and alerts for maintenance requirements.
- Stakeholder: SH_010, SH_020, SH_040

Error Detection and Alerting
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- Scenario: Detecting system errors or malfunctions and alerting the appropriate personnel.
- Procedure: Continuous system monitoring with automated error detection algorithms and alert notifications with detailed information to system administrators or technicians. Simplified alert with instructions in any other case.
- Stakeholder: SH_010 – SH_040

Software Updates and Upgrades
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- Scenario: Updating the system software to enhance functionality or address security issues.
- Procedure: Secure and efficient software update processes, with minimal system downtime and comprehensive post-update checks.
- Stakeholder: SH_020, SH_030, SH_040

Emergency Protocols and System Recovery
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- Scenario: Handling system emergencies or failures, including emergency shutdown, data recovery and system restoration.
- Procedure: Defined emergency protocols, rapid system recovery procedures, and data backup solutions for ensuring data integrity.
- Stakeholder: SH_030, SH_040System Administrator (SH_050), Site Engineer (SH_060)

Data Security and Compliance
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- Scenario: Ensuring the system adheres to relevant data security and privacy regulations.
- Procedure: Implementing strong encryption, audit trails, and compliance with standards like HIPAA and GDPR.
- Stakeholder: SH_030

Patient Safety Monitoring
~~~~~~~~~~~~~~~~~~~~~~~~~
- Scenario: Continuously monitoring patient safety parameter.
- Procedure: Monitoring of SAR level and implementation of safety cutoffs or alerts.
- Stakeholder: SH_010, SH_020

Sequence Upload
~~~~~~~~~~~~~~~
- Scenario:Testing of sequences or new procedures under development.
- Procedure:Enable import of custom sequences.
- Stakeholder:SH_020

Data Export
~~~~~~~~~~~
- Scenario:Development/evaluation of new/customized reconstruction methods or the comparison of reconstruction methods.
- Procedure:Implementation of export functions on different stages, i.e. raw k-space data export, DICOM export, etc.
- Stakeholder:SH_020

Support
~~~~~~~
- Scenario:The system does not behave as expected or reports an error.
- Procedure:System administrator reads our error message and notifies the manufacturer for support or troubleshooting to restore operability of the system. The manufacturer provides remote support and schedules an appointment with a field/service engineer as soon as possible.
- Stakeholder:SH_030, SH_060, SH_040


System Startup and Initialization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Scenario: Booting up the MRI system, initializing all software components, and conducting self-checks.
* Procedure: Automated system checks for hardware and software integrity, loading of necessary drivers and applications, and verification of system readiness for operation.
* Stakeholder: System Administrator (SH_050), Site Engineer (SH_060)

User Authentication and Access Control
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Scenario: Ensuring only authorized personnel can operate or access different levels of the system.
* Procedure: Secure login processes, role-based access control, and user authentication protocols.
* Stakeholder: System Administrator (SH_050)

Patient Data Input and Retrieval
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Scenario: Entering new patient data or retrieving existing patient records before starting a scan.
* Procedure: Integration with hospital information systems for seamless data exchange, ensuring data accuracy and privacy compliance.
* Stakeholder: MRI Technician/MTRA (SH_010), Radiologist (SH_020)

Scan Parameter Selection and Customization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Scenario: Selection and customization of MRI scan parameters based on the specific clinical requirements.
* Procedure: User interfaces that allow for easy selection and adjustment of scan parameters, including sequence types, intensity, and duration.
* Stakeholder: MRI Technician/MTRA (SH_010), Radiologist (SH_020), Scientist (SH_040)

Real-Time Scan Monitoring and Adjustment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Scenario: Monitoring the MRI scan in real-time and making necessary adjustments.
* Procedure: Dynamic display of scanning progress, with capabilities to adjust parameters on-the-fly for optimal image quality.
* Stakeholder: MRI Technician/MTRA (SH_010), Radiologist (SH_020)

Image Processing and Storage
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Scenario: Processing the raw scan data to produce images and storing them appropriately.
* Procedure: Automated image reconstruction algorithms, along with efficient data storage solutions both on-premises and in cloud environments.
* Stakeholder: Radiologist (SH_020), Scientist (SH_040), System Administrator (SH_050)

System Shutdown and Secure Data Handling
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Scenario: Properly shutting down the system while ensuring all patient data is securely saved and protected.
* Procedure: Step-by-step shutdown process that includes data backup, closing of all active sessions, and hardware cooling procedures.
* Stakeholder: System Administrator (SH_050)

Routine Maintenance and Calibration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Scenario: Regular system maintenance and calibration to ensure ongoing accuracy and efficiency.
* Procedure: Scheduled maintenance tasks, automated calibration routines, and alerts for maintenance requirements.
* Stakeholder: Site Engineer (SH_060), MRI Technician/MTRA (SH_010)

Error Detection and Alerting
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Scenario: Detecting system errors or malfunctions and alerting the appropriate personnel.
* Procedure: Continuous system monitoring with automated error detection algorithms and alert notifications to system administrators or technicians.
* Stakeholder: System Administrator (SH_050), Site Engineer (SH_060)

Software Updates and Upgrades
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Scenario: Updating the system software to enhance functionality or address security issues.
* Procedure: Secure and efficient software update processes, with minimal system downtime and comprehensive post-update checks.
* Stakeholder: System Administrator (SH_050), Developer (SH_030)

Emergency Protocols and System Recovery
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Scenario: Handling system emergencies or failures, including data recovery and system restoration.
* Procedure: Defined emergency protocols, rapid system recovery procedures, and data backup solutions for ensuring data integrity.
* Stakeholder: System Administrator (SH_050), Site Engineer (SH_060)

Interoperability with Other Healthcare Systems
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Scenario: Seamless interaction and data exchange with other healthcare systems like EHRs, PACS, and RIS.
* Procedure: Implementing standard protocols and APIs for data exchange, ensuring compatibility with various healthcare IT infrastructures.
* Stakeholder: System Administrator (SH_050), Radiologist (SH_020), Healthcare Facility (SH_100)

Remote System Diagnostics and Support
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Scenario: Providing remote assistance and diagnostics for technical issues or user queries.
* Procedure: Remote access capabilities for technical support staff, diagnostic tools for system analysis, and secure communication channels.
* Stakeholder: System Administrator (SH_050), Site Engineer (SH_060)

Data Security and Compliance
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Scenario: Ensuring the system adheres to relevant data security and privacy regulations.
* Procedure: Implementing strong encryption, audit trails, and compliance with standards like HIPAA and GDPR.
* Stakeholder: System Administrator (SH_050), Regulatory Affairs Specialist (SH_070)

Power Management and Efficiency
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Scenario: Efficient management of system power consumption and operational efficiency.
* Procedure: Power-saving modes during periods of inactivity, efficient power usage during scans, and monitoring of overall system power consumption.
* Stakeholder: System Administrator (SH_050), Site Engineer (SH_060)

Customization and Configuration Management
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Scenario: Customizing system settings and configurations to meet specific site or user requirements.
* Procedure: Flexible configuration options with user-friendly interfaces, along with configuration profiles for different user roles or scanning requirements.
* Stakeholder: System Administrator (SH_050), MRI Technician/MTRA (SH_010)

Patient Safety Monitoring
~~~~~~~~~~~~~~~~~~~~~~~~~

* Scenario: Continuously monitoring patient safety parameters during scans.
* Procedure: Automated systems for tracking patient vitals, SAR levels, and implementing safety cutoffs or alerts.
* Stakeholder: MRI Technician/MTRA (SH_010), Radiologist (SH_020)




Functional Requirements
=======================

The functional requirements of the MRI acquisition software are derived from the scenarios and use cases outlined in the previous section. These requirements define the specific capabilities and behaviors that the software must exhibit to fulfill the needs of the stakeholders and ensure the successful operation of the MRI system. The functional requirements are organized into categories based on the primary functionalities they address, including acquisition, processing, user interaction, system management, and safety monitoring.

General Requirements
--------------------

.. csv-table::
    :header: "ID", "Description of Requirement", "Verification Idea", "Reference/Traceability", "A4IM Version"
    :widths: 10, 60, 80, 30, 10

    "A4IM_FR_010", "The software shall enable the execution of MRI acquisition jobs, including the upload and execution of pulseq sequences with workflows.", "Conduct an MRI acquisition job using a pulseq sequence and verify workflow integration and execution.", "PRS_0010", "1.0"
    "A4IM_FR_020", "The software shall offer planning tools for MRI examinations, integrating exam trees, workflows, and processing modality worklists.", "Plan an MRI examination using the software tools and verify the integration with exam trees and workflows.", "PRS_0020", "1.0"
    "A4IM_FR_030", "The software shall provide a DICOM viewer to view, compare, and annotate DICOM images of selected records.", "Load a DICOM image in the viewer, perform comparisons and annotations, and verify the functionality.", "PRS_0030", "1.0"
    "A4IM_FR_040", "The software must support user management, allowing assignment of different user roles and supporting a multi-tenancy cloud environment.", "Simulate different user roles to verify role-based access and check for multi-tenancy functionality.", "PRS_0040", "1.0"
    "A4IM_FR_050", "The software shall monitor and display the MRI device's status, including current execution progress, malfunctions, and device connection status.", "During an MRI scan, verify the software displays the current execution progress and detects any malfunctions.", "PRS_0050", "1.0"
    "A4IM_FR_060", "The software must monitor patient safety parameters such as SAR, temperature, total scan time duration, and optionally provide a video stream and patient communication system.", "Simulate an MRI scan and verify monitoring of all specified patient safety parameters.", "PRS_0060", "1.0"
    "A4IM_FR_070", "The software shall enable the integration of processing workflows for MRI raw data or images, including system calibration, image reconstruction, and analysis.", "Test a processing workflow on MRI raw data and verify the execution of system calibration, image reconstruction, and analysis.", "PRS_0070", "1.0"
    "A4IM_FR_080", "The software shall support system calibration activities such as adjustment of Larmor frequency, gradients, system flip angle, and B0-field shimming.", "Perform system calibration using the software and verify the adjustments.", "PRS_0080", "1.0"
    "A4IM_FR_090", "The software must provide a structured form for creating clinical reports, allowing medical professionals to formulate diagnoses.", "Create a clinical report using the software and verify the functionality supports diagnosis formulation.", "PRS_0090", "1.0"
    "A4IM_FR_100", "The software shall manage devices, including organization of different devices, authentication, device selection, and access management based on training.", "Verify the software can organize and manage access to multiple devices with device-specific training requirements.", "PRS_0100", "1.0"


Operational Requirements
------------------------
.. csv-table::
    :header: "ID", "Description of Requirement", "Verification Idea", "Reference/Traceability", "A4IM Version"
    :widths: 10, 60, 80, 30, 10

    "A4IM_FR_110", "The software must continuously monitor and display MRI scan data in real-time, providing feedback on scan quality and progress with instant notification upon scan completion.", "Verify real-time monitoring during an MRI scan, including feedback on scan quality and instant notification at completion.", "PRS_0010", "1.0"
    "A4IM_FR_120", "The software shall provide real-time alerts for scan anomalies or issues, with a response time of less than 5 minutes.", "Simulate a scan anomaly and verify that the software provides an alert within 5 minutes.", "PRS_0020", "1.0"
    "A4IM_FR_130", "The software shall support on-prem setups with 100% compatibility.", "Set up the software in an on-prem environment and verify full functionality and compatibility.", "PRS_0030", "1.0"
    "A4IM_FR_140", "The software shall support cloud setups, accommodating environments without local compute workstations.", "Deploy the software in a cloud environment and verify functionality without local compute dependencies.", "PRS_0040", "1.0"


Regulatory Needs
----------------

.. csv-table::
    :header: "ID", "Description of Requirement", "Verification Idea", "Reference/Traceability", "A4IM Version"
    :widths: 10, 60, 80, 30, 10

    "A4IM_FR_210", "The software must comply with HIPAA, GDPR, FDA regulations, and undergo regular updates for ongoing compliance.", "Review documentation and change logs to verify compliance and regular updates for regulations.", "PRS_0110", "1.0"
    "A4IM_FR_220", "The software shall ensure strong data encryption and role-based access control for securing patient data.", "Test the encryption and access control features to verify compliance with security standards.", "PRS_0120", "1.0"
    "A4IM_FR_230", "The software shall implement Risk Mitigation Measures (RMM) in adherence to ISO 14971:2019.", "Evaluate the implementation of RMM and verify adherence to ISO 14971:2019.", "PRS_0130", "1.0"


Reliability and Resilience Needs
--------------------------------

.. csv-table::
    :header: "ID", "Description of Requirement", "Verification Idea", "Reference/Traceability", "A4IM Version"
    :widths: 10, 60, 80, 30, 10

    "A4IM_FR_210", "The software shall ensure system stability with minimum downtime, aiming for 99.99% uptime.", "Monitor the system over a defined period to verify that the uptime meets or exceeds 99.99%.", "PRS_0210", "1.0"


Performance Requirements
========================

.. csv-table::
    :header: "ID", "Description of Requirement", "Verification Idea", "Reference/Traceability", "A4IM Version"
    :widths: 10, 60, 80, 30, 10

    "A4IM_FR_810", "The software shall initialize and be ready for use within 60 seconds of system startup, ensuring quick readiness for medical operations.", "Measure the time from system startup to when the software is fully operational and ready for use, verifying it does not exceed 60 seconds.", "Startup Performance", "1.0"
    "A4IM_FR_820", "The software shall shut down properly within 30 seconds, ensuring data integrity and system safety.", "Verify the shutdown process from initiation to completion, ensuring it occurs within 30 seconds without data loss or system issues.", "Shutdown Performance", "1.0"
    "A4IM_FR_830", "The software must respond to user inputs within 2 seconds under normal operating conditions, providing a responsive user experience.", "Conduct user interaction tests to verify response times for various commands under normal operating conditions.", "User Input Response", "1.0"
    "A4IM_FR_840", "The software shall provide real-time monitoring with a reaction time not exceeding 1 second, ensuring timely feedback during MRI scans.", "Test the real-time monitoring feature by simulating MRI scans and measuring the reaction time to changes in scan parameters.", "Real-Time Monitoring Performance", "1.0"
    "A4IM_FR_850", "The software must recover from common errors or crashes and restore operation within 60 seconds, minimizing downtime during critical operations.", "Simulate common software errors or crashes and measure the time taken for the software to recover and become operational again.", "Error Recovery Performance", "1.0"


System Interfaces
=================

Interoperability Needs
----------------------

.. csv-table::
    :header: "ID", "Description of Requirement", "Verification Idea", "Reference/Traceability", "A4IM Version"
    :widths: 10, 60, 80, 30, 10

    "A4IM_FR_410", "The software shall ensure compatibility with various DICOM systems for seamless integration with existing healthcare systems.", "Test interoperability with multiple DICOM systems to validate compatibility and seamless integration.", "PRS_0410", "1.0"
    "A4IM_FR_420", "The software shall support data storage using the XNAT platform, ensuring compatibility with widely used medical imaging data storage formats.", "Demonstrate the software's ability to store and retrieve data using the XNAT platform, verifying compatibility.", "PRS_0420", "1.0"
    "A4IM_FR_430", "The software shall support the NIFTI file format for facilitating diverse data representation and interoperability.", "Validate the software's capability to process and manage NIFTI file format data through testing and user feedback.", "PRS_0430", "1.0"
    "A4IM_FR_440", "The software shall support the ISMRMRD file format, aiding in diverse data representation and interoperability for research purposes.", "Ensure the software can handle ISMRMRD file format data seamlessly, facilitating research and development activities.", "PRS_0440", "1.0"
    "A4IM_FR_450", "The software shall support the RAW MR file format, enabling researchers to work with unprocessed MRI data.", "Confirm the software's ability to import, export, and utilize RAW MR file format data for advanced research applications.", "PRS_0450", "1.0"


External Interfaces
===================

.. csv-table::
    :header: "ID", "Description of Requirement", "Verification Idea", "Reference/Traceability", "A4IM Version"
    :widths: 10, 60, 80, 30, 10

    "A4IM_FR_610", "The software shall ensure seamless interaction with patient monitoring systems to enable real-time data exchange, thereby ensuring patient safety.", "Demonstrate real-time data exchange with a patient monitoring system and verify seamless interaction without delays or errors.", "PRS_0610", "1.0"


Warnings, Messages, and Alerts
==============================

.. csv-table::
    :header: "ID", "Description of Requirement", "Verification Idea", "Reference/Traceability", "A4IM Version"
    :widths: 10, 60, 80, 30, 10

    "A4IM_FR_710", "The software shall implement a system for warnings, messages, and alerts in compliance with IEC 60601-1-8, ensuring clear and effective communication of critical information to users.", "Conduct testing to ensure that all warnings, messages, and alerts comply with the specifications of IEC 60601-1-8, including the clarity of communication and the effectiveness of alerting users to critical issues.", "IEC 60601-1-8", "1.0"


Usability
=========

Usability Requirements
----------------------
.. csv-table::
    :header: "ID", "Description of Requirement", "Verification Idea", "Reference/Traceability", "A4IM Version"
    :widths: 10, 60, 80, 30, 10

    "A4IM_FR_310", "The software shall provide an intuitive UI for scan setup and patient management, including comprehensive user manuals and guides, with quick access to frequently used features.", "Conduct usability testing with medical professionals to ensure they can effectively use the system for scan setup and patient management within 30 minutes of initial training.", "PRS_0310", "1.0"
    "A4IM_FR_320", "The software shall provide access to raw MRI data and experimental sequence options for scientists.", "Verify through user feedback and testing that scientists can access and utilize raw MRI data and experimental sequences for their research.", "PRS_0320", "1.0"

Maintenance and Service
=======================

Maintainability Requirements
----------------------------

.. csv-table::
    :header: "ID", "Description of Requirement", "Verification Idea", "Reference/Traceability", "A4IM Version"
    :widths: 10, 60, 80, 30, 10

    "A4IM_FR_510", "The software shall have a scalable architecture to accommodate increasing data and users, featuring a modular design for easy updates and enhancements, and efficient data management and storage solutions.", "Test the system's performance under doubled data and user load to ensure less than 10% degradation.", "PRS_0510", "1.0"














+--------------+-------------+------------+--------------+
|      ID      | Requirement | Acceptance | Traceability |
+==============+=============+============+==============+
| SWRS_FR_0001 | TBD         | TBD        | TBD          |
+--------------+-------------+------------+--------------+
| SWRS_FR_0002 | TBD         | TBD        | TBD          |
+--------------+-------------+------------+--------------+
| SWRS_FR_0003 | TBD         | TBD        | TBD          |
+--------------+-------------+------------+--------------+

Device Communication
====================

Acquisition Request
-------------------

The following information shall be communicated with an acquisition request to specify modality specific instructions/commands.
Authentification and authorization topics are left out for now.

Request:

- **device-id:** Double check if request was communicated to the right device
- **command:** Start, stop, pause, ...
- **parameters:** Key-value pairs, can be simple values, instruction files or a combination of both, device limits
- **record-id:** ID which is assigned per initial request and traced from record creation to the last workflow step, gives access to job-id (may be extended by additional trace ID)
- **device-authentication-key:** TBD

Response: HTTPS_RESPONSE


**Communication Flow**

(Replace by better formatting)

    UI 
    
    -> Acquisition Control

        -> Request acquisition command/parameters (sequence manager)

        -> create record (exam manager) 

        -> get device (device manager)

    -> Device (acquisition request) 
    
    -> Workflow Manager 
    
    -> Workflows


**MR-Domain Model**

(To be moved to SWAD)
JSON payload which is communicated from acquisition control to device (MRI acquisition request).
The following example is


.. code-block:: javascript
    :linenos:

    device_id: str,
    command: enum, // start, stop, pause
    parameters: {
        context: str, // content of a sequence file (can be pulseq)
        format: enum, // pulseq, ocra, ...
        acqusition_limits: {
            // parameters used to calculate SAR, double check for completeness
            patient_height: float,
            patient_weight: float,
            patient_gender: enum,
            patient_age: int,
        },
        sequence_parameters: {
            // User input for MRI console to execute the sequence properly, for now only fov.
            // Note: The following section is specific to the format (here pulseq). 
            // It may vary for different sequence formats and thus should be 
            // implemented as a generic dictionary inside a pydantic MR domain model.
            fov: [
                float, 
                float, 
                float
            ],
            fov_offset: [
                float, 
                float, 
                float
            ]
        }
    }


Device Monitor
--------------

Monitoring of device status through direct connection between device and device manager.
Get the current device status: connected, disconnected, scanning, etc.
    
    TODO: What are possible device status?

The device status is to be implemented as an enum with defined situations (see above).


Device Configuration
--------------------

This set of parameters is specific to one device. Read and/or write requests are performed through the device manager.
Some parameters are fixed limits and cannot be modified by the device manager (`system_limits`).
Another set of parameters may vary over time and may be set from a workflow/workflow-step result (`current_device_configuration`).

.. code-block:: javascript
    :linenos:

    
    system_limits: {
    // hard system limits (read only)
        max_gradients: [
            float, 
            float, 
            float
        ],
        max_rf_duration: float,
        adc_deadtime: float,
        rf_dead_time: float,
        // ...
    },
    current_device_configuration: {
    // temporary system values (read and write)
        larmor_frequency: float,
        flip_angle_calibration: float,
        gradient_calibration: [
            float, 
            float, 
            float
        ],
        gradient_offset: [
            float, 
            float, 
            float
        ],
        // ...
    }




