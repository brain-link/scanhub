Product Requirement Specification (PRS)
########################################

.. note::
   This section is a work in progress.

This section gathers the product requirements for the ScanHub platform,
derived from stakeholder and user needs. It forms the design input from
which the :doc:`Software Requirements Specification <techdoc_swrs>` and,
ultimately, the :doc:`Software Architecture Design Description <techdoc_swad>`
are derived.

Stakeholders and User Roles
=============================

The table below lists the stakeholder groups considered when deriving the
product requirements. Each stakeholder ID is referenced from the requirement
tables below to indicate who a given need originates from.

.. list-table::
   :header-rows: 1
   :widths: 10 25 65

   * - ID
     - Stakeholder
     - Description
   * - SH_010
     - Medical Professional (MTRA, Radiologist)
     - Medical professionals who operate or interpret the MRI scans. Operators
       prepare patients, ensure optimal image quality, and provide feedback on
       the system's usability and functionality. Radiologists interpret the
       MRI scans to diagnose medical conditions.
   * - SH_020
     - Scientist
     - Researchers who use MRI for advanced studies and require access to
       experimental features, customized sequences (upload), and retrieval of
       raw data at distinct stages.
   * - SH_030
     - System Administrator
     - IT professionals responsible for the setup, maintenance, and security
       of the system. They ensure the reliability and data integrity of the
       system.
   * - SH_040
     - (Field/Service) Engineer
     - Technical experts responsible for the installation, maintenance, and
       repair of the system. They ensure that the hardware and software
       components are functioning correctly.
   * - SH_050
     - Patient
     - Individuals undergoing MRI scans. They are concerned with the comfort,
       safety, and privacy aspects of the MRI experience.
   * - SH_060
     - Medical Device Manufacturer (Regulatory Affairs)
     - Company that produces and distributes the MRI system. It is concerned
       with the system's marketability, quality, and regulatory compliance.
   * - SH_070
     - Healthcare Facility / Clinic / Hospital / Research Institution /
       Customer (Interoperability Manager)
     - Organizations that provide healthcare services and use the MRI system
       for patient diagnosis. They are concerned with the system's
       reliability, efficiency, and integration with other healthcare IT
       systems and workflows.


User Needs
==========

The following tables translate the stakeholder concerns above into concrete,
prioritized product needs. Each need is assigned a unique ``PRS_xxxx`` ID that
is referenced from the corresponding software requirement in the
:doc:`SWRS <techdoc_swrs>`.

General
-------

Needs that apply broadly to everyday use of the platform, covering the core
acquisition, planning, viewing, and administrative capabilities.

.. list-table::
   :header-rows: 1
   :widths: 10 30 35 15 15 10

   * - ID
     - Product Requirement (Stakeholder)
     - Design Input
     - Acceptance Criteria
     - Intended Claim
     - Priority
   * - PRS_0010
     - Execution of an MRI acquisition/job/experiment (Medical Professional,
       Scientist)
     - Upload Pulseq sequence, execute MRI job with workflows
     -
     -
     -
   * - PRS_0020
     - Planning of an MRI examination (Medical Professional, Scientist)
     - Protocol tree, workflows, processing modality worklist
     -
     -
     -
   * - PRS_0030
     - DICOM viewer (Medical Professional, Scientist)
     - View DICOM image of a selected record, compare DICOM images, annotate
       DICOM image
     -
     -
     -
   * - PRS_0040
     - User management (System Administrator)
     - Assign different user roles, support multi-tenancy cloud environment
     -
     -
     -
   * - PRS_0050
     - Monitor device status (Medical Professional, Scientist)
     - Current execution progress, detectable device malfunctions, device
       connection
     -
     -
     -
   * - PRS_0060
     - Monitor patient safety (Medical Professional)
     - Specific absorption rate (SAR), temperature, total scan time duration;
       optional video stream and patient communication system
     -
     -
     -
   * - PRS_0070
     - Integration of processing workflows (Scientist)
     - Assembling of workflow steps to be executed on MRI raw data or images,
       including system calibration, image reconstruction, and analysis
     -
     -
     -
   * - PRS_0080
     - System calibration (Medical Professional, Scientist, Site Engineer)
     - Adjust Larmor frequency, adjust gradients, adjust system flip angle,
       B0-field shimming
     -
     -
     -
   * - PRS_0090
     - Clinical report (Medical Professional)
     - Structured form to create a clinical report allowing formulation of a
       diagnosis, viewer for clinical reports
     -
     -
     -
   * - PRS_0100
     - Device management (System Administrator, Medical Professional, Medical
       Device Manufacturer)
     - Organization of different devices, device authentication, device
       selection, device access management (who is trained on which device?)
     -
     -
     -


Operational Needs
------------------

Needs related to how reliably and flexibly the system runs once deployed,
independent of a specific clinical workflow.

.. list-table::
   :header-rows: 1
   :widths: 10 25 35 15 20 10

   * - ID
     - Product Requirement (Stakeholder)
     - Design Input
     - Acceptance Criteria
     - Intended Claim
     - Priority
   * - PRS_0710
     - Real-time monitoring (Medical Professional)
     - * Continuously monitor and display MRI scan data in real time.
       * Provide real-time feedback on scan quality and progress.
       * Instant notification for scan completion.
     - 99% uptime
     - Ensure real-time monitoring for accurate diagnosis.
     - Must Have
   * - PRS_0720
     - Alerting (Medical Professional)
     - Real-time alerts for scan anomalies or issues.
     - < 5 minutes
     - Rapid response to scan anomalies or issues.
     - Should Have
   * - PRS_0730
     - On-prem setup (System Administrator)
     - Support for on-prem setups.
     - 100% compatibility
     - Provide flexibility in deployment options to cater to different
       organizational needs.
     - Must Have
   * - PRS_0740
     - Cloud setup (System Administrator)
     - Support for cloud setups in environments with no local compute
       workstations.
     - 100% compatibility
     - Enable versatile deployment options to accommodate varying
       infrastructure.
     - Must Have

Regulatory Needs
------------------

Needs driven by applicable healthcare, data-protection, and medical-device
regulations that the platform must comply with.

.. list-table::
   :header-rows: 1
   :widths: 10 25 35 15 20 10

   * - ID
     - Product Requirement (Stakeholder)
     - Design Input
     - Acceptance Criteria
     - Intended Claim
     - Priority
   * - PRS_0110
     - Compliance (Regulatory Affairs)
     - * Compliance with HIPAA, GDPR, and FDA regulations.
       * Regular updates to adhere to evolving regulations.
       * Detailed logging and audit trails.
     - 100% compliance
     - Ensure compliance with industry regulations for patient safety.
     - Must Have
   * - PRS_0120
     - Data security (System Administrator)
     - Strong data encryption and role-based access control.
     - 100% compliance
     - Secure patient data and adhere to compliance requirements.
     - Nice to Have
   * - PRS_0130
     - Compliance with ISO 14971:2019 (Regulatory Affairs)
     - Implementation of Risk Mitigation Measures (RMM) in adherence to
       ISO 14971:2019.
     - 100% compliance
     - Minimize risks associated with system operation.
     - Must Have

Reliability and Resilience Needs
-----------------------------------

Needs concerning system uptime and the ability to keep operating dependably
over time.

.. list-table::
   :header-rows: 1
   :widths: 10 25 35 15 20 10

   * - ID
     - Product Requirement (Stakeholder)
     - Design Input
     - Acceptance Criteria
     - Intended Claim
     - Priority
   * - PRS_0210
     - Reliability (Field Engineer)
     - System stability with minimum downtime.
     - 99.99% uptime
     - Maintain a reliable and stable MRI acquisition system.
     - Must Have

Usability Needs
-------------------

Needs concerning ease of learning and day-to-day efficiency for platform
users.

.. list-table::
   :header-rows: 1
   :widths: 10 25 35 15 20 10

   * - ID
     - Product Requirement (Stakeholder)
     - Design Input
     - Acceptance Criteria
     - Intended Claim
     - Priority
   * - PRS_0310
     - User-friendly (Medical Professional)
     - * Intuitive UI for scan setup and patient management.
       * Comprehensive user manuals and guides.
       * Quick access to frequently used features.
     - < 30 minutes onboarding
     - Streamline user interaction for increased productivity.
     - Should Have
   * - PRS_0320
     - Advanced features (Scientist)
     - Access to raw MRI data and experimental sequence options.
     - N/A
     - Facilitate sequence development and research.
     - Nice to Have

Interoperability Needs
--------------------------

Needs concerning the exchange of data with third-party systems and standard
medical imaging formats.

.. list-table::
   :header-rows: 1
   :widths: 10 25 35 15 20 10

   * - ID
     - Product Requirement (Stakeholder)
     - Design Input
     - Acceptance Criteria
     - Intended Claim
     - Priority
   * - PRS_0410
     - Interoperability (Medical Device Manufacturer)
     - Compatibility with various DICOM systems.
     - N/A
     - Seamless integration with existing healthcare systems.
     - Should Have
   * - PRS_0420
     - Data storage (Medical Professional)
     - Support for XNAT storage.
     - N/A
     - Ensure compatibility with widely used medical imaging data storage
       formats.
     - Must Have
   * - PRS_0430
     - File format (Medical Professional)
     - Support for NIfTI file format.
     - N/A
     - Facilitate diverse data representation and interoperability.
     - Must Have
   * - PRS_0440
     - File format (Scientist)
     - Support for ISMRMRD file format.
     - N/A
     - Facilitate diverse data representation and interoperability.
     - Must Have
   * - PRS_0450
     - File format (Scientist)
     - Support for raw MR file format.
     - N/A
     - Facilitate diverse data representation and interoperability.
     - Must Have

Maintainability Needs
-------------------------

Needs concerning the ability to evolve, scale, and update the platform over
its lifetime without degrading performance.

.. list-table::
   :header-rows: 1
   :widths: 10 25 35 15 20 10

   * - ID
     - Product Requirement (Stakeholder)
     - Design Input
     - Acceptance Criteria
     - Intended Claim
     - Priority
   * - PRS_0510
     - Scalability (System Administrator)
     - * Scalable architecture to accommodate increasing data and users.
       * Modular design for easy updates and enhancements.
       * Efficient data management and storage solutions.
     - < 10% degradation at 2x data
     - Ensure system performance as data and users grow.
     - Should Have

System Interfaces to Third-Party Solution Needs
----------------------------------------------------

Needs concerning integration with external systems that are not part of
ScanHub itself, such as patient monitoring equipment.

.. list-table::
   :header-rows: 1
   :widths: 10 25 35 15 20 10

   * - ID
     - Product Requirement (Stakeholder)
     - Design Input
     - Acceptance Criteria
     - Intended Claim
     - Priority
   * - PRS_0610
     - Patient monitoring systems (Medical Device Manufacturer)
     - Seamless interaction with patient monitoring systems.
     - Real-time data exchange
     - Ensure real-time data exchange and patient safety.
     - Must Have
