Product Requirement Specifications (PRS)
========================================

!!This Section is Work in Progress.!!

Operational Requirements
------------------------
+------------+--------------+--------------------------------------+---------------------------------------------+---------------------+------------------------------------------+
| ID         | Priority     | User Need (User)                     | Product Requirement                         | Targeted Performance| Intended claim                           |
+============+==============+======================================+=============================================+=====================+==========================================+
| PRS_0010   | Must Have    | Real-time Monitoring (Radiologist)   | - Continuously monitor and display MRI scan | 99% uptime          | Ensure real-time monitoring for accurate |
|            |              |                                      | data in real-time.                          |                     | diagnosis.                               |
|            |              |                                      | - Provide real-time feedback on scan quality|                     |                                          |
|            |              |                                      | and progress.                               |                     |                                          |
|            |              |                                      | - Instant notification for scan completion. |                     |                                          |
+------------+--------------+--------------------------------------+---------------------------------------------+---------------------+------------------------------------------+
| PRS_0020   | Should Have  | Alerting (MTA)                       | Real-time alerts for scan anomalies or      | <5 minutes          | Rapid response to scan anomalies or      |
|            |              |                                      | issues.                                     |                     | issues.                                  |
+------------+--------------+--------------------------------------+---------------------------------------------+---------------------+------------------------------------------+
| PRS_0030   | Must Have    | On-Prem Setup (IT Specialist)        | Support for on-prem setups.                 | 100% Compatibility  | Provide flexibility in deployment        |
|            |              |                                      |                                             |                     | options to cater to different            |
|            |              |                                      |                                             |                     | organizational needs.                    |
+------------+--------------+--------------------------------------+---------------------------------------------+---------------------+------------------------------------------+
| PRS_0040   | Must Have    | Cloud Setup (IT Specialist)          | Support for cloud setups in environments    | 100% Compatibility  | Enable versatile deployment options      |
|            |              |                                      | with no local compute workstations.         |                     | to accommodate varying infrastructure.   |
+------------+--------------+--------------------------------------+---------------------------------------------+---------------------+------------------------------------------+

Regulatory Requirements
-----------------------
+------------+--------------+--------------------------------------+--------------------------------------------+----------------------+------------------------------------------+
| ID         | Priority     | User Need (Actor)                    | Product Requirement                        | Targeted Performance | Intended claim                           |
+============+==============+======================================+============================================+======================+==========================================+
| PRS_0110   | Must Have    | Compliance (Regulatory Affairs       | - Compliance with HIPAA, GDPR, and FDA     | 100% Compliance      | Ensure compliance with industry          |
|            |              | Specialist)                          | regulations.                               |                      | regulations for patient safety.          |
|            |              |                                      | - Regular updates to adhere to evolving    |                      |                                          |
|            |              |                                      | regulations.                               |                      |                                          |
|            |              |                                      | - Detailed logging and audit trails.       |                      |                                          |
+------------+--------------+--------------------------------------+--------------------------------------------+----------------------+------------------------------------------+
| PRS_0120   | Nice to Have | Data Security (System Administrator) | Strong data encryption and role-based      | 100% Compliance      | Secure patient data and adhere to        |
|            |              |                                      | access control.                            |                      | compliance requirements.                 |
+------------+--------------+--------------------------------------+--------------------------------------------+----------------------+------------------------------------------+
| PRS_0130   | Must Have    | Compliance with ISO 14971:2019       | Implementation of Risk Mitigation Measures | 100% Compliance      | Minimize risks associated with the       |
|            |              | (Regulatory Affairs Specialist)      | (RMM) in adherence to ISO 14971:2019.      |                      | system operation.                        |
+------------+--------------+--------------------------------------+--------------------------------------------+----------------------+------------------------------------------+

Reliability and Resilience Requirements
---------------------------------------
+------------+--------------+--------------------------------------+--------------------------------------------+---------------------+------------------------------------------+
| ID         | Priority     | User Need (User)                     | Product Requirement                        | Targeted Performance| Intended claim                           |
+============+==============+======================================+============================================+=====================+==========================================+
| PRS_0210   | Must Have    | Reliability (Site/Support Engineer)  | System stability with minimum downtime.    | 99.99% uptime       | Maintain a reliable and stable MRI       |
|            |              |                                      |                                            |                     | acquisition system.                      |
+------------+--------------+--------------------------------------+--------------------------------------------+---------------------+------------------------------------------+

Usability Requirements
----------------------
+------------+--------------+--------------------------------------+--------------------------------------------+---------------------+------------------------------------------+
| ID         | Priority     | User Need (User)                     | Product Requirement                        | Targeted Performance| Intended claim                           |
+============+==============+======================================+============================================+=====================+==========================================+
| PRS_0310   | Should Have  | User-Friendly (MTA)                  | - Intuitive UI for scan setup and patient  | <30 minutes         | Streamline user interaction for          |
|            |              |                                      | management.                                | onboarding          | increased productivity.                  |
|            |              |                                      | - Comprehensive user manuals and guides.   |                     |                                          |
|            |              |                                      | - Quick access to frequently used features.|                     |                                          |
+------------+--------------+--------------------------------------+--------------------------------------------+---------------------+------------------------------------------+
| PRS_0320   | Nice to Have | Advanced Features (Scientist)        | Access to raw MRI data and experimental    | N/A                 | Facilitate sequence development and      |
|            |              |                                      | sequence options.                          |                     | research.                                |
+------------+--------------+--------------------------------------+--------------------------------------------+---------------------+------------------------------------------+

Interoperability Requirements
-----------------------------
+------------+--------------+--------------------------------------+---------------------------------------------+----------------------+------------------------------------------+
| ID         | Priority     | User Need (Actor)                    | Product Requirement                         | Targeted Performance | Intended claim                           |
+============+==============+======================================+=============================================+======================+==========================================+
| PRS_0410   | Should Have  |Interoperability (Healthcare Provider)| Compatibility with various DICOM systems.   | N/A                  | Seamless integration with existing       |
|            |              |                                      |                                             |                      | healthcare systems.                      |
+------------+--------------+--------------------------------------+---------------------------------------------+----------------------+------------------------------------------+
| PRS_0420   | Must Have    | Data Storage (Radiologist)           | Support for XNAT storage.                   | N/A                  | Ensure compatibility with widely used    |
|            |              |                                      |                                             |                      | medical imaging data storage formats.    |
+------------+--------------+--------------------------------------+---------------------------------------------+----------------------+------------------------------------------+
| PRS_0430   | Must Have    | File Format (Radiologist)            | Support for NIFTI file format.              | N/A                  | Facilitate diverse data representation   |
|            |              |                                      |                                             |                      | and interoperability.                    |
+------------+--------------+--------------------------------------+---------------------------------------------+----------------------+------------------------------------------+
| PRS_0440   | Must Have    | File Format (Scientist)              | Support for ISMRMRD file format.            | N/A                  | Facilitate diverse data representation   |
|            |              |                                      |                                             |                      | and interoperability.                    |
+------------+--------------+--------------------------------------+---------------------------------------------+----------------------+------------------------------------------+
| PRS_0450   | Must Have    | File Format (Scientist)              | Support for RAW MR file format.             | N/A                  | Facilitate diverse data representation   |
|            |              |                                      |                                             |                      | and interoperability.                    |
+------------+--------------+--------------------------------------+---------------------------------------------+----------------------+------------------------------------------+

Maintainability Requirements
----------------------------
+------------+--------------+--------------------------------------+---------------------------------------------+----------------------+--------------------------------------------+
| ID         | Priority     | User Need (Actor)                    | Product Requirement                         | Targeted Performance | Intended claim                             |
+============+==============+======================================+=============================================+======================+============================================+
| PRS_0510   | Should Have  | Scalability (System Administrator)   | - Scalable architecture to accommodate      | <10% degradation     | Ensure system performance as data and      |
|            |              |                                      | increasing data and users.                  | at 2x data           | users grow.                                |
|            |              |                                      | - Modular design for easy updates and       |                      |                                            |
|            |              |                                      | enhancements.                               |                      |                                            |
|            |              |                                      | - Efficient data management and storage     |                      |                                            |
|            |              |                                      | solutions.                                  |                      |                                            |
+------------+--------------+--------------------------------------+---------------------------------------------+----------------------+--------------------------------------------+

System Interfaces to Third Party Solutions
------------------------------------------
+------------+--------------+---------------------------------------+---------------------------------------------+----------------------+------------------------------------------+
| ID         | Priority     | User Need (Actor)                     | Product Requirement                         | Targeted Performance | Intended claim                           |
+============+==============+=======================================+=============================================+======================+==========================================+
| PRS_0610   | Must Have    | Patient Monitoring Systems (Healthcare| Seamless interaction with patient           | Real-time data       | Ensure real-time data exchange and       |
|            |              | Provider)                             | monitoring systems.                         | exchange             | patient safety.                          |
+------------+--------------+---------------------------------------+---------------------------------------------+----------------------+------------------------------------------+
