Software Architecture Design Description (SWAD)
###############################################

!!This Section is Work in Progress.!!

Introduction
============
Purpose
-------
This document delineates the comprehensive architectural design and technical realization of the ScanHub software system for MRI data acquisition and processing.
It aims to provide a coherent high-level perspective of the system's context, its static, and dynamic structures, serving as a pivotal reference for developers, programmers, regulatory affairs, and quality assurance teams.
The document is intended to facilitate the technical realization of the system, enabling developers to comprehend and develop it ideally without necessitating further inquiries or making adhoc design decisions.
It also offers future project members an expedited overview of the software system's structure and provides the test team with ample information on the assembly and testing of the software components during the integration tests. Where details surpass the scope of this document, readers are directed to lower-level architecture and design documents.

Scope
-----
The ScanHub system is a cloud-based, open-source data acquisition & processing platform specifically designed for transforming the way MRI data is processed, stored, and shared.
This document focuses on the architecture of the ScanHub Platform, detailing its integration with advanced simulation devices, efficient resource utilization, enhanced data sharing capabilities, and rigorous security measures, all leveraged through the power of cloud computing.
It translates the requirements provided by the Design Input [DI] and the Software Requirements Specification [SWRS] into the system architecture, serving as a comprehensive guide for the realization of the software components.
For additional details and specifications, refer to the design input documentation [DI, SWRS].

References
----------
- [DI] ScanHub Design Input
- [DD] ScanHub Device Description
- [SWRS] ScanHub Software Requirements Specification
- [SWDD] ScanHub Software Design Description
  
Definitions, Acronyms, and Abbreviations
----------------------------------------

Tables
------


Figures
-------


System Context
==============


Key Scenarios 
-------------

The following keyn scenarios focus on the basic functionality of the device from both the user's and system's perspectives. This includes user interactions, as well as essential system procedures like startup, shutdown, and service functionalities. These scenarios are crucial for ensuring the software architecture supports seamless operation and maintenance of the MRI system.


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


System Decomposition
====================

.. figure:: _static/images/swad/ScanHub_Development_View.drawio.png
  :width: 800
  :alt: ScanHub Development View

  Figure 1: ScanHub Development View


+---------------+---------------------+-----------------------------------------------------------+--------------+ 
| ID            | Component           | Description                                               | Safety Class | 
+===============+=====================+===========================================================+==============+ 
| SWAD_CMP_0001 | Device Manager      | Manages connected devices, before and during acquisition. | A            | 
+---------------+---------------------+-----------------------------------------------------------+--------------+ 
| SWAD_CMP_0002 | Acquisition Control |                                                           |              | 
+---------------+---------------------+-----------------------------------------------------------+--------------+ 
| SWAD_CMP_0003 | Workflow Engine     |                                                           |              |
+---------------+---------------------+-----------------------------------------------------------+--------------+


.. figure:: _static/images/swad/ScanHub_Component_Connected_Device.drawio.png
    :width: 800
    :alt: ScanHub Connected Device

    Figure 2: ScanHub Connected Device Component



.. figure:: _static/images/swad/ScanHub_Component_Workflow.drawio.png
    :width: 800
    :alt: ScanHub Workflow

    Figure 3: ScanHub Workflow Component
