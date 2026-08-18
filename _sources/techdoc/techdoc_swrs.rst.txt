Software Requirements Specification (SWRS)
############################################

.. note::
   This section is a work in progress.

Purpose
=======
This document defines the functional and non-functional software requirements
for the MRI acquisition software of the A4IM scanner system. It integrates
inputs from the foundational documents listed under *References* to provide a
complete outline of the required software functionalities and attributes, and
forms the basis from which the
:doc:`Software Architecture Design Description <techdoc_swad>` is derived.

Scope
=====
The scope of this document is to define the functional and non-functional
requirements for the MRI acquisition software of the A4IM scanner. This
includes, but is not limited to:

- Acquisition and processing of MRI data.
- User interface and interaction mechanisms for medical professionals.
- Integration with healthcare facility systems, including patient management
  and data storage solutions.
- Compliance with healthcare regulations and standards for data protection,
  privacy, and security.
- System performance, reliability, and maintenance requirements.
- Safety measures and risk mitigation strategies relevant to software
  operation.

References
==========
- Product Requirement Specification (PRS) for the A4IM scanner, detailing the
  expectations and needs from a product standpoint. See
  :doc:`techdoc_prs`.
- System Requirements Specification (SRS) for the A4IM scanner, outlining the
  system-level requirements the software must meet to ensure compatibility
  and performance within the MRI system.
- Risk Assessment Worksheet, identifying potential risks associated with the
  software and the necessary mitigations to ensure patient and operator
  safety.

.. note::
   Document numbers and versions for the SRS and Risk Assessment Worksheet
   will be added once those documents are finalized.

Software Overview
==================
This document pertains to the MRI acquisition software for the A4IM scanner,
providing a comprehensive solution for the acquisition, processing, and
management of MRI data. The software is designed to ensure high-quality
imaging of the human head and extremities, maximizing the efficiency and
effectiveness of diagnostic processes within healthcare facilities.

The MRI acquisition software integrates with the A4IM scanner's hardware
components, including the permanent magnets, radiofrequency (RF) coils, and
gradient coils, to facilitate the capture of detailed images. It also
includes functionality for patient data management, real-time scan
monitoring, image reconstruction, and storage, all within a user-friendly
interface that supports healthcare professionals in their daily operations.

For detailed information on the system's intended use, components, and
operational context, refer to the Device Description document.

Scenarios and Use Cases
========================
To outline the main usage scenarios and inform the definition of system
requirements, this section lists the stakeholders of the MRI acquisition
system as defined in the :doc:`techdoc_prs`. The following scenarios and use
cases serve as the basis for the functional requirements defined further
below. Each scenario is associated with the relevant stakeholders and
provides a high-level description of the expected system behavior.

System Startup and Initialization
------------------------------------

* Scenario: Booting up the MRI system, initializing all software components,
  and conducting self-checks.
* Procedure: Automated system checks for hardware and software integrity,
  loading of necessary drivers and applications, and verification of system
  readiness for operation.
* Stakeholder: System Administrator (SH_030), (Field/Service) Engineer
  (SH_040)

User Authentication and Access Control
------------------------------------------

* Scenario: Ensuring only authorized personnel can operate or access
  different levels of the system.
* Procedure: Secure login processes, role-based access control, and user
  authentication protocols.
* Stakeholder: System Administrator (SH_030)

Patient Data Input and Retrieval
------------------------------------

* Scenario: Entering new patient data or retrieving existing patient records
  before starting a scan.
* Procedure: Integration with hospital information systems for seamless data
  exchange, ensuring data accuracy and privacy compliance.
* Stakeholder: Medical Professional (SH_010)

Scan Parameter Selection and Customization
------------------------------------------------

* Scenario: Selection and customization of MRI scan parameters based on
  specific clinical requirements.
* Procedure: User interfaces that allow for easy selection and adjustment of
  scan parameters, including sequence type, intensity, and duration.
* Stakeholder: Medical Professional (SH_010), Scientist (SH_020)

Real-Time Scan Monitoring and Adjustment
------------------------------------------

* Scenario: Monitoring the MRI scan in real time and making necessary
  adjustments.
* Procedure: Dynamic display of scanning progress, with the ability to adjust
  parameters on the fly for optimal image quality.
* Stakeholder: Medical Professional (SH_010)

Image Processing and Storage
--------------------------------

* Scenario: Processing the raw scan data to produce images and storing them
  appropriately.
* Procedure: Automated image reconstruction algorithms, along with efficient
  data storage solutions both on-premises and in cloud environments.
* Stakeholder: Medical Professional (SH_010), Scientist (SH_020), System
  Administrator (SH_030)

System Shutdown and Secure Data Handling
------------------------------------------

* Scenario: Properly shutting down the system while ensuring all patient data
  is securely saved and protected.
* Procedure: A step-by-step shutdown process that includes data backup,
  closing of all active sessions, and hardware cooling procedures.
* Stakeholder: System Administrator (SH_030)

Routine Maintenance and Calibration
---------------------------------------

* Scenario: Regular system maintenance and calibration to ensure ongoing
  accuracy and efficiency.
* Procedure: Scheduled maintenance tasks, automated calibration routines, and
  alerts for maintenance requirements.
* Stakeholder: (Field/Service) Engineer (SH_040), Medical Professional
  (SH_010)

Error Detection and Alerting
--------------------------------

* Scenario: Detecting system errors or malfunctions and alerting the
  appropriate personnel.
* Procedure: Continuous system monitoring with automated error-detection
  algorithms and alert notifications to system administrators or
  technicians.
* Stakeholder: System Administrator (SH_030), (Field/Service) Engineer
  (SH_040)

Software Updates and Upgrades
---------------------------------

* Scenario: Updating the system software to enhance functionality or address
  security issues.
* Procedure: Secure and efficient software update processes, with minimal
  system downtime and comprehensive post-update checks.
* Stakeholder: System Administrator (SH_030), Medical Device Manufacturer
  (SH_060)

Emergency Protocols and System Recovery
------------------------------------------

* Scenario: Handling system emergencies or failures, including emergency
  shutdown, data recovery, and system restoration.
* Procedure: Defined emergency protocols, rapid system recovery procedures,
  and data backup solutions for ensuring data integrity.
* Stakeholder: System Administrator (SH_030), (Field/Service) Engineer
  (SH_040)

Interoperability with Other Healthcare Systems
--------------------------------------------------

* Scenario: Seamless interaction and data exchange with other healthcare
  systems such as EHRs, PACS, and RIS.
* Procedure: Implementing standard protocols and APIs for data exchange,
  ensuring compatibility with various healthcare IT infrastructures.
* Stakeholder: System Administrator (SH_030), Medical Professional (SH_010),
  Healthcare Facility (SH_070)

Remote System Diagnostics and Support
-----------------------------------------

* Scenario: Providing remote assistance and diagnostics for technical issues
  or user queries.
* Procedure: Remote access capabilities for technical support staff,
  diagnostic tools for system analysis, and secure communication channels.
* Stakeholder: System Administrator (SH_030), (Field/Service) Engineer
  (SH_040)

Data Security and Compliance
--------------------------------

* Scenario: Ensuring the system adheres to relevant data security and
  privacy regulations.
* Procedure: Implementing strong encryption, audit trails, and compliance
  with standards like HIPAA and GDPR.
* Stakeholder: System Administrator (SH_030), Medical Device Manufacturer
  (SH_060)

Power Management and Efficiency
-----------------------------------

* Scenario: Efficient management of system power consumption and operational
  efficiency.
* Procedure: Power-saving modes during periods of inactivity, efficient power
  usage during scans, and monitoring of overall system power consumption.
* Stakeholder: System Administrator (SH_030), (Field/Service) Engineer
  (SH_040)

Customization and Configuration Management
------------------------------------------------

* Scenario: Customizing system settings and configurations to meet specific
  site or user requirements.
* Procedure: Flexible configuration options with user-friendly interfaces,
  along with configuration profiles for different user roles or scanning
  requirements.
* Stakeholder: System Administrator (SH_030), Medical Professional (SH_010)

Patient Safety Monitoring
------------------------------

* Scenario: Continuously monitoring patient safety parameters during scans.
* Procedure: Automated systems for tracking patient vitals and SAR levels,
  and implementing safety cutoffs or alerts.
* Stakeholder: Medical Professional (SH_010)

Sequence Upload
--------------------

* Scenario: Testing of sequences or new procedures under development.
* Procedure: Enable import of custom sequences.
* Stakeholder: Scientist (SH_020)

Data Export
----------------

* Scenario: Development/evaluation of new or customized reconstruction
  methods, or comparison of reconstruction methods.
* Procedure: Implementation of export functions at different stages, e.g.
  raw k-space data export, DICOM export, etc.
* Stakeholder: Scientist (SH_020)

Support
-----------

* Scenario: The system does not behave as expected or reports an error.
* Procedure: The system administrator reads the error message and notifies
  the manufacturer for support or troubleshooting to restore operability of
  the system. The manufacturer provides remote support and schedules an
  appointment with a field/service engineer as soon as possible.
* Stakeholder: System Administrator (SH_030), Medical Device Manufacturer
  (SH_060), (Field/Service) Engineer (SH_040)


Functional Requirements
=========================

The functional requirements of the MRI acquisition software are derived from
the scenarios and use cases outlined above. They define the specific
capabilities and behaviors the software must exhibit to fulfill the needs of
the stakeholders and ensure the successful operation of the MRI system. The
functional requirements are organized into categories based on the primary
functionalities they address, including acquisition, processing, user
interaction, system management, and safety monitoring. The
*Reference/Traceability* column links each requirement back to the product
requirement it implements (see :doc:`techdoc_prs`).

General Requirements
------------------------

Core, everyday functional capabilities of the acquisition software.

.. csv-table::
    :header: "ID", "Description of Requirement", "Verification Idea", "Reference/Traceability", "A4IM Version"
    :widths: 10, 60, 80, 30, 10

    "A4IM_FR_010", "The software shall enable the execution of MRI acquisition jobs, including the upload and execution of Pulseq sequences with workflows.", "Conduct an MRI acquisition job using a Pulseq sequence and verify workflow integration and execution.", "PRS_0010", "1.0"
    "A4IM_FR_020", "The software shall offer planning tools for MRI examinations, integrating protocol trees, workflows, and processing modality worklists.", "Plan an MRI examination using the software tools and verify the integration with protocol trees and workflows.", "PRS_0020", "1.0"
    "A4IM_FR_030", "The software shall provide a DICOM viewer to view, compare, and annotate DICOM images of selected records.", "Load a DICOM image in the viewer, perform comparisons and annotations, and verify the functionality.", "PRS_0030", "1.0"
    "A4IM_FR_040", "The software must support user management, allowing assignment of different user roles and supporting a multi-tenancy cloud environment.", "Simulate different user roles to verify role-based access and check for multi-tenancy functionality.", "PRS_0040", "1.0"
    "A4IM_FR_050", "The software shall monitor and display the MRI device's status, including current execution progress, malfunctions, and device connection status.", "During an MRI scan, verify the software displays the current execution progress and detects any malfunctions.", "PRS_0050", "1.0"
    "A4IM_FR_060", "The software must monitor patient safety parameters such as SAR, temperature, and total scan time duration, and optionally provide a video stream and patient communication system.", "Simulate an MRI scan and verify monitoring of all specified patient safety parameters.", "PRS_0060", "1.0"
    "A4IM_FR_070", "The software shall enable the integration of processing workflows for MRI raw data or images, including system calibration, image reconstruction, and analysis.", "Test a processing workflow on MRI raw data and verify the execution of system calibration, image reconstruction, and analysis.", "PRS_0070", "1.0"
    "A4IM_FR_080", "The software shall support system calibration activities such as adjustment of Larmor frequency, gradients, system flip angle, and B0-field shimming.", "Perform system calibration using the software and verify the adjustments.", "PRS_0080", "1.0"
    "A4IM_FR_090", "The software must provide a structured form for creating clinical reports, allowing medical professionals to formulate diagnoses.", "Create a clinical report using the software and verify the functionality supports diagnosis formulation.", "PRS_0090", "1.0"
    "A4IM_FR_100", "The software shall manage devices, including organization of different devices, authentication, device selection, and access management based on training.", "Verify the software can organize and manage access to multiple devices with device-specific training requirements.", "PRS_0100", "1.0"


Operational Requirements
----------------------------

Requirements covering the day-to-day operation and deployment flexibility of
the platform once installed.

.. csv-table::
    :header: "ID", "Description of Requirement", "Verification Idea", "Reference/Traceability", "A4IM Version"
    :widths: 10, 60, 80, 30, 10

    "A4IM_FR_110", "The software must continuously monitor and display MRI scan data in real-time, providing feedback on scan quality and progress with instant notification upon scan completion.", "Verify real-time monitoring during an MRI scan, including feedback on scan quality and instant notification at completion.", "PRS_0710", "1.0"
    "A4IM_FR_120", "The software shall provide real-time alerts for scan anomalies or issues, with a response time of less than 5 minutes.", "Simulate a scan anomaly and verify that the software provides an alert within 5 minutes.", "PRS_0720", "1.0"
    "A4IM_FR_130", "The software shall support on-prem setups with 100% compatibility.", "Set up the software in an on-prem environment and verify full functionality and compatibility.", "PRS_0730", "1.0"
    "A4IM_FR_140", "The software shall support cloud setups, accommodating environments without local compute workstations.", "Deploy the software in a cloud environment and verify functionality without local compute dependencies.", "PRS_0740", "1.0"


Regulatory Needs
--------------------

Requirements ensuring compliance with applicable healthcare and
medical-device regulations.

.. csv-table::
    :header: "ID", "Description of Requirement", "Verification Idea", "Reference/Traceability", "A4IM Version"
    :widths: 10, 60, 80, 30, 10

    "A4IM_FR_210", "The software must comply with HIPAA, GDPR, FDA regulations, and undergo regular updates for ongoing compliance.", "Review documentation and change logs to verify compliance and regular updates for regulations.", "PRS_0110", "1.0"
    "A4IM_FR_220", "The software shall ensure strong data encryption and role-based access control for securing patient data.", "Test the encryption and access control features to verify compliance with security standards.", "PRS_0120", "1.0"
    "A4IM_FR_230", "The software shall implement Risk Mitigation Measures (RMM) in adherence to ISO 14971:2019.", "Evaluate the implementation of RMM and verify adherence to ISO 14971:2019.", "PRS_0130", "1.0"


Reliability and Resilience Needs
--------------------------------------

Requirements ensuring the system remains stable and available.

.. csv-table::
    :header: "ID", "Description of Requirement", "Verification Idea", "Reference/Traceability", "A4IM Version"
    :widths: 10, 60, 80, 30, 10

    "A4IM_FR_910", "The software shall ensure system stability with minimum downtime, aiming for 99.99% uptime.", "Monitor the system over a defined period to verify that the uptime meets or exceeds 99.99%.", "PRS_0210", "1.0"


Performance Requirements
==========================

Requirements defining the timing behavior the software must meet under
normal operating conditions, independent of any single functional feature.

.. csv-table::
    :header: "ID", "Description of Requirement", "Verification Idea", "Reference/Traceability", "A4IM Version"
    :widths: 10, 60, 80, 30, 10

    "A4IM_FR_810", "The software shall initialize and be ready for use within 60 seconds of system startup, ensuring quick readiness for medical operations.", "Measure the time from system startup to when the software is fully operational and ready for use, verifying it does not exceed 60 seconds.", "Startup Performance", "1.0"
    "A4IM_FR_820", "The software shall shut down properly within 30 seconds, ensuring data integrity and system safety.", "Verify the shutdown process from initiation to completion, ensuring it occurs within 30 seconds without data loss or system issues.", "Shutdown Performance", "1.0"
    "A4IM_FR_830", "The software must respond to user inputs within 2 seconds under normal operating conditions, providing a responsive user experience.", "Conduct user interaction tests to verify response times for various commands under normal operating conditions.", "User Input Response", "1.0"
    "A4IM_FR_840", "The software shall provide real-time monitoring with a reaction time not exceeding 1 second, ensuring timely feedback during MRI scans.", "Test the real-time monitoring feature by simulating MRI scans and measuring the reaction time to changes in scan parameters.", "Real-Time Monitoring Performance", "1.0"
    "A4IM_FR_850", "The software must recover from common errors or crashes and restore operation within 60 seconds, minimizing downtime during critical operations.", "Simulate common software errors or crashes and measure the time taken for the software to recover and become operational again.", "Error Recovery Performance", "1.0"


System Interfaces
===================

Requirements governing how the software exchanges data with other clinical
and research systems.

Interoperability Needs
--------------------------

.. csv-table::
    :header: "ID", "Description of Requirement", "Verification Idea", "Reference/Traceability", "A4IM Version"
    :widths: 10, 60, 80, 30, 10

    "A4IM_FR_410", "The software shall ensure compatibility with various DICOM systems for seamless integration with existing healthcare systems.", "Test interoperability with multiple DICOM systems to validate compatibility and seamless integration.", "PRS_0410", "1.0"
    "A4IM_FR_420", "The software shall support data storage using the XNAT platform, ensuring compatibility with widely used medical imaging data storage formats.", "Demonstrate the software's ability to store and retrieve data using the XNAT platform, verifying compatibility.", "PRS_0420", "1.0"
    "A4IM_FR_430", "The software shall support the NIfTI file format for facilitating diverse data representation and interoperability.", "Validate the software's capability to process and manage NIfTI file format data through testing and user feedback.", "PRS_0430", "1.0"
    "A4IM_FR_440", "The software shall support the ISMRMRD file format, aiding in diverse data representation and interoperability for research purposes.", "Ensure the software can handle ISMRMRD file format data seamlessly, facilitating research and development activities.", "PRS_0440", "1.0"
    "A4IM_FR_450", "The software shall support the raw MR file format, enabling researchers to work with unprocessed MRI data.", "Confirm the software's ability to import, export, and utilize raw MR file format data for advanced research applications.", "PRS_0450", "1.0"


External Interfaces
=====================

Requirements governing interfaces to devices and systems outside of
ScanHub's own software boundary, such as patient monitoring equipment.

.. csv-table::
    :header: "ID", "Description of Requirement", "Verification Idea", "Reference/Traceability", "A4IM Version"
    :widths: 10, 60, 80, 30, 10

    "A4IM_FR_610", "The software shall ensure seamless interaction with patient monitoring systems to enable real-time data exchange, thereby ensuring patient safety.", "Demonstrate real-time data exchange with a patient monitoring system and verify seamless interaction without delays or errors.", "PRS_0610", "1.0"


Warnings, Messages, and Alerts
=================================

Requirements for how the software communicates critical information,
warnings, and status messages to its users.

.. csv-table::
    :header: "ID", "Description of Requirement", "Verification Idea", "Reference/Traceability", "A4IM Version"
    :widths: 10, 60, 80, 30, 10

    "A4IM_FR_710", "The software shall implement a system for warnings, messages, and alerts in compliance with IEC 60601-1-8, ensuring clear and effective communication of critical information to users.", "Conduct testing to ensure that all warnings, messages, and alerts comply with the specifications of IEC 60601-1-8, including the clarity of communication and the effectiveness of alerting users to critical issues.", "IEC 60601-1-8", "1.0"


Usability
==========

Requirements ensuring the software is efficient and approachable for its
intended users.

Usability Requirements
---------------------------

.. csv-table::
    :header: "ID", "Description of Requirement", "Verification Idea", "Reference/Traceability", "A4IM Version"
    :widths: 10, 60, 80, 30, 10

    "A4IM_FR_310", "The software shall provide an intuitive UI for scan setup and patient management, including comprehensive user manuals and guides, with quick access to frequently used features.", "Conduct usability testing with medical professionals to ensure they can effectively use the system for scan setup and patient management within 30 minutes of initial training.", "PRS_0310", "1.0"
    "A4IM_FR_320", "The software shall provide access to raw MRI data and experimental sequence options for scientists.", "Verify through user feedback and testing that scientists can access and utilize raw MRI data and experimental sequences for their research.", "PRS_0320", "1.0"

Maintenance and Service
=========================

Requirements ensuring the software can be maintained, scaled, and updated
over its operational lifetime.

Maintainability Requirements
----------------------------------

.. csv-table::
    :header: "ID", "Description of Requirement", "Verification Idea", "Reference/Traceability", "A4IM Version"
    :widths: 10, 60, 80, 30, 10

    "A4IM_FR_510", "The software shall have a scalable architecture to accommodate increasing data and users, featuring a modular design for easy updates and enhancements, and efficient data management and storage solutions.", "Test the system's performance under doubled data and user load to ensure less than 10% degradation.", "PRS_0510", "1.0"


Device Communication
======================

This section specifies the data exchanged between ScanHub Core and a
connected acquisition device, complementing the functional requirements
above with the concrete message formats used at the device boundary.
Authentication and authorization aspects of this communication are
intentionally left out for now and are addressed elsewhere.

Acquisition Request
------------------------

The following information shall be communicated with an acquisition request
to specify modality-specific instructions and commands.

Request:

- **device-id:** Double-checked so the request is communicated to the right
  device.
- **command:** Start, stop, pause, ...
- **parameters:** Key-value pairs; can be simple values, instruction files,
  or a combination of both, subject to device limits.
- **record-id:** ID assigned per initial request and traced from record
  creation through the last workflow step; gives access to the job-id (may
  be extended by an additional trace ID).
- **device-authentication-key:** TBD

Response: ``HTTPS_RESPONSE``

**Communication Flow**

.. mermaid::

   sequenceDiagram
       participant UI
       participant AC as Acquisition Control
       participant SM as Sequence Manager
       participant PM as Protocol Manager
       participant DM as Device Manager
       participant DEV as Device
       participant WM as Workflow Manager

       UI->>AC: Request acquisition
       AC->>SM: Request acquisition command / parameters
       AC->>PM: Create record
       AC->>DM: Get device
       AC->>DEV: Send acquisition request
       AC->>WM: Trigger workflow
       WM->>WM: Execute workflows

**MR Domain Model**

.. note::
   This data model belongs conceptually to the device interface described in
   the :doc:`SWAD <techdoc_swad>` and may be moved there in a future
   revision.

The following example shows the JSON payload communicated from Acquisition
Control to a device as part of an MRI acquisition request.

.. code-block:: javascript
    :linenos:

    device_id: str,
    command: enum, // start, stop, pause
    parameters: {
        context: str, // content of a sequence file (can be pulseq)
        format: enum, // pulseq, ocra, ...
        acquisition_limits: {
            // parameters used to calculate SAR, double check for completeness
            patient_height: float,
            patient_weight: float,
            patient_gender: enum,
            patient_age: int,
        },
        sequence_parameters: {
            // User input for the MRI console to execute the sequence properly, for now only fov.
            // Note: the following section is specific to the format (here pulseq).
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
------------------

Monitoring of device status is done through a direct connection between the
device and the device manager, giving access to the current device status,
e.g. connected, disconnected, or scanning.

.. note::
   The full set of possible device statuses is still to be defined. Once
   defined, device status will be implemented as an enum with clearly
   specified states.


Device Configuration
-------------------------

This set of parameters is specific to a single device. Read and/or write
requests are performed through the device manager. Some parameters are fixed
limits and cannot be modified by the device manager (``system_limits``).
Another set of parameters may vary over time and may be set from a
workflow/workflow-step result (``current_device_configuration``).

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
