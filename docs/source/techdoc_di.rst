Design Input (DI)
#################

!!This Section is Work in Progress.!!


User Needs
==========

Operational Needs
-----------------
+------------+--------------------------------------+---------------------------------------------+---------------------+------------------------------------------+--------------+
| ID         | User Need [User]                     | Design Input                                | Acceptance Criteria | Intended claim                           | Priority     |
+============+======================================+=============================================+=====================+==========================================+==============+
| PRS_0010   | Real-time Monitoring (Radiologist)   | - Continuously monitor and display MRI scan | 99% uptime          | Ensure real-time monitoring for accurate | Must Have    |
|            |                                      | data in real-time.                          |                     | diagnosis.                               |              |
|            |                                      | - Provide real-time feedback on scan quality|                     |                                          |              |
|            |                                      | and progress.                               |                     |                                          |              |
|            |                                      | - Instant notification for scan completion. |                     |                                          |              |
+------------+--------------------------------------+---------------------------------------------+---------------------+------------------------------------------+--------------+
| PRS_0020   | Alerting (MTA)                       | Real-time alerts for scan anomalies or      | <5 minutes          | Rapid response to scan anomalies or      | Should Have  |
|            |                                      | issues.                                     |                     | issues.                                  |              |
+------------+--------------------------------------+---------------------------------------------+---------------------+------------------------------------------+--------------+
| PRS_0030   | On-Prem Setup (IT Specialist)        | Support for on-prem setups.                 | 100% Compatibility  | Provide flexibility in deployment        | Must Have    |
|            |                                      |                                             |                     | options to cater to different            |              |
|            |                                      |                                             |                     | organizational needs.                    |              |
+------------+--------------------------------------+---------------------------------------------+---------------------+------------------------------------------+--------------+
| PRS_0040   | Cloud Setup (IT Specialist)          | Support for cloud setups in environments    | 100% Compatibility  | Enable versatile deployment options      | Must Have    |
|            |                                      | with no local compute workstations.         |                     | to accommodate varying infrastructure.   |              |
+------------+--------------------------------------+---------------------------------------------+---------------------+------------------------------------------+--------------+

Regulatory Needs
----------------
+------------+--------------------------------------+--------------------------------------------+----------------------+------------------------------------------+--------------+
| ID         | User Need (Actor)                    | Design Input                               | Acceptance Criteria  | Intended claim                           | Priority     |
+============+======================================+============================================+======================+==========================================+==============+
| PRS_0110   | Compliance (Regulatory Affairs       | - Compliance with HIPAA, GDPR, and FDA     | 100% Compliance      | Ensure compliance with industry          | Must Have    |
|            | Specialist)                          | regulations.                               |                      | regulations for patient safety.          |              |
|            |                                      | - Regular updates to adhere to evolving    |                      |                                          |              |
|            |                                      | regulations.                               |                      |                                          |              |
|            |                                      | - Detailed logging and audit trails.       |                      |                                          |              |
+------------+--------------------------------------+--------------------------------------------+----------------------+------------------------------------------+--------------+
| PRS_0120   | Data Security (System Administrator) | Strong data encryption and role-based      | 100% Compliance      | Secure patient data and adhere to        | Nice to Have |
|            |                                      | access control.                            |                      | compliance requirements.                 |              |
+------------+--------------------------------------+--------------------------------------------+----------------------+------------------------------------------+--------------+
| PRS_0130   | Compliance with ISO 14971:2019       | Implementation of Risk Mitigation Measures | 100% Compliance      | Minimize risks associated with the       | Must Have    |
|            | (Regulatory Affairs Specialist)      | (RMM) in adherence to ISO 14971:2019.      |                      | system operation.                        |              |
+------------+--------------------------------------+--------------------------------------------+----------------------+------------------------------------------+--------------+

Reliability and Resilience Needs
--------------------------------
+------------+--------------------------------------+--------------------------------------------+---------------------+------------------------------------------+--------------+
| ID         | User Need (User)                     | Design Input                               | Acceptance Criteria | Intended claim                           | Priority     |
+============+======================================+============================================+=====================+==========================================+==============+
| PRS_0210   | Reliability (Site/Support Engineer)  | System stability with minimum downtime.    | 99.99% uptime       | Maintain a reliable and stable MRI       | Must Have    |
|            |                                      |                                            |                     | acquisition system.                      |              |
+------------+--------------------------------------+--------------------------------------------+---------------------+------------------------------------------+--------------+

Usability Needs
---------------
+------------+--------------------------------------+--------------------------------------------+---------------------+------------------------------------------+--------------+
| ID         | User Need (User)                     | Design Input                               | Acceptance Criteria | Intended claim                           | Priority     |
+============+======================================+============================================+=====================+==========================================+==============+
| PRS_0310   | User-Friendly (MTA)                  | - Intuitive UI for scan setup and patient  | <30 minutes         | Streamline user interaction for          | Should Have  |
|            |                                      | management.                                | onboarding          | increased productivity.                  |              |
|            |                                      | - Comprehensive user manuals and guides.   |                     |                                          |              |
|            |                                      | - Quick access to frequently used features.|                     |                                          |              |
+------------+--------------------------------------+--------------------------------------------+---------------------+------------------------------------------+--------------+
| PRS_0320   | Advanced Features (Scientist)        | Access to raw MRI data and experimental    | N/A                 | Facilitate sequence development and      | Nice to Have |
|            |                                      | sequence options.                          |                     | research.                                |              |
+------------+--------------------------------------+--------------------------------------------+---------------------+------------------------------------------+--------------+

Interoperability Needs
----------------------
+------------+--------------------------------------+---------------------------------------------+----------------------+------------------------------------------+--------------+
| ID         | User Need (Actor)                    | Design Input                                | Acceptance Criteria  | Intended claim                           | Priority     |
+============+======================================+=============================================+======================+==========================================+==============+
| PRS_0410   |Interoperability (Healthcare Provider)| Compatibility with various DICOM systems.   | N/A                  | Seamless integration with existing       | Should Have  |
|            |                                      |                                             |                      | healthcare systems.                      |              |
+------------+--------------------------------------+---------------------------------------------+----------------------+------------------------------------------+--------------+
| PRS_0420   | Data Storage (Radiologist)           | Support for XNAT storage.                   | N/A                  | Ensure compatibility with widely used    | Must Have    |
|            |                                      |                                             |                      | medical imaging data storage formats.    |              |
+------------+--------------------------------------+---------------------------------------------+----------------------+------------------------------------------+--------------+
| PRS_0430   | File Format (Radiologist)            | Support for NIFTI file format.              | N/A                  | Facilitate diverse data representation   | Must Have    |
|            |                                      |                                             |                      | and interoperability.                    |              |
+------------+--------------------------------------+---------------------------------------------+----------------------+------------------------------------------+--------------+
| PRS_0440   | File Format (Scientist)              | Support for ISMRMRD file format.            | N/A                  | Facilitate diverse data representation   | Must Have    |              |
|            |                                      |                                             |                      | and interoperability.                    |              |
+------------+--------------------------------------+---------------------------------------------+----------------------+------------------------------------------+--------------+
| PRS_0450   | File Format (Scientist)              | Support for RAW MR file format.             | N/A                  | Facilitate diverse data representation   | Must Have    |
|            |                                      |                                             |                      | and interoperability.                    |              |
+------------+--------------------------------------+---------------------------------------------+----------------------+------------------------------------------+--------------+

Maintainability Needs
---------------------
+------------+--------------------------------------+---------------------------------------------+----------------------+--------------------------------------------+--------------+
| ID         | User Need (Actor)                    | Design Input                                | Acceptance Criteria  | Intended claim                             | Priority     |
+============+======================================+=============================================+======================+============================================+==============+
| PRS_0510   | Scalability (System Administrator)   | - Scalable architecture to accommodate      | <10% degradation     | Ensure system performance as data and      | Should Have  |
|            |                                      | increasing data and users.                  | at 2x data           | users grow.                                |              |
|            |                                      | - Modular design for easy updates and       |                      |                                            |              |
|            |                                      | enhancements.                               |                      |                                            |              |
|            |                                      | - Efficient data management and storage     |                      |                                            |              |
|            |                                      | solutions.                                  |                      |                                            |              |
+------------+--------------------------------------+---------------------------------------------+----------------------+--------------------------------------------+--------------+

System Interfaces to Third Party Solution Needs
-----------------------------------------------
+------------+---------------------------------------+---------------------------------------------+----------------------+------------------------------------------+--------------+
| ID         | User Need (Actor)                     | Design Input                                | Acceptance Criteria  | Intended claim                           | Priority     |
+============+=======================================+=============================================+======================+==========================================+==============+
| PRS_0610   | Patient Monitoring Systems (Healthcare| Seamless interaction with patient           | Real-time data       | Ensure real-time data exchange and       | Must Have    |
|            | Provider)                             | monitoring systems.                         | exchange             | patient safety.                          |              |
+------------+---------------------------------------+---------------------------------------------+----------------------+------------------------------------------+--------------+
