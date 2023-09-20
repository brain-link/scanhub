ScanHub - Product Requirement Specifications (PRS)
=================================================

Add requireemnts to the table below.:
- Current setups often don't allow running in the cloud - on prem setups need to be supported


+--------------+-----------+-------------------------------------------+------------------------------------------+---------------------+------------------------------------+
| ID           | Priority* | Customer Need (Customer)                  | Product Requirement                      | Targeted Performance| Intended claim**                   |
+==============+===========+===========================================+==========================================+=====================+====================================+
| SH_PRS_010   | 3         | Real-time Monitoring (Radiologist)        | Continuously monitor and display MRI scan| 99% uptime          | Ensure real-time monitoring for    |
|              |           |                                           | data in real-time.                       |                     | accurate diagnosis.                |
+--------------+-----------+-------------------------------------------+------------------------------------------+---------------------+------------------------------------+
| SH_PRS_020   | 2         | Interoperability (Healthcare Provider)    | Compatibility with various DICOM systems.| N/A                 | Seamless integration with existing |
|              |           |                                           |                                          |                     | healthcare systems.                |
+--------------+-----------+-------------------------------------------+------------------------------------------+---------------------+------------------------------------+
| SH_PRS_030   | 1         | Remote Access (Radiologist)               | Enable secure remote access to MRI data. | N/A                 | Facilitate remote diagnosis and    |
|              |           |                                           |                                          |                     | consultations.                     |
+--------------+-----------+-------------------------------------------+------------------------------------------+---------------------+------------------------------------+
| SH_PRS_040   | 2         | Alerting (MTA)                            | Real-time alerts for scan anomalies or   | <5 minutes          | Rapid response to scan anomalies   |
|              |           |                                           | issues.                                  |                     | or issues.                         |
+--------------+-----------+-------------------------------------------+------------------------------------------+---------------------+------------------------------------+
| SH_PRS_050   | 3         | Compliance (Regulatory Affairs Specialist)| Compliance with HIPAA, GDPR, and FDA     | 100% Compliance     | Ensure compliance with industry    |
|              |           |                                           | regulations.                             |                     | regulations for patient safety.    |
+--------------+-----------+-------------------------------------------+------------------------------------------+---------------------+------------------------------------+
| SH_PRS_060   | 2         | User-Friendly (MTA)                       | Intuitive UI for scan setup and patient  | <30 minutes         | Streamline user interaction for    |
|              |           |                                           | management.                              | onboarding          | increased productivity.            |
+--------------+-----------+-------------------------------------------+------------------------------------------+---------------------+------------------------------------+
| SH_PRS_070   | 2         | Reliability (Site/Support Engineer)       | System stability with minimum downtime.  | 99.99% uptime       | Maintain a reliable and stable     |
|              |           |                                           |                                          |                     | MRI acquisition system.            |
+--------------+-----------+-------------------------------------------+------------------------------------------+---------------------+------------------------------------+
| SH_PRS_080   | 1         | Advanced Features (Scientist)             | Access to raw MRI data and experimental  | N/A                 | Facilitate sequence development    |
|              |           |                                           | sequence options.                        |                     | and research.                      |
+--------------+-----------+-------------------------------------------+------------------------------------------+---------------------+------------------------------------+
| SH_PRS_090   | 1         | Data Security (System Administrator)      | Strong data encryption and role-based    | 100% Compliance     | Secure patient data and adhere to  |
|              |           |                                           | access control.                          |                     | compliance requirements.           |
+--------------+-----------+-------------------------------------------+------------------------------------------+---------------------+------------------------------------+
| SH_PRS_100   | 2         | Scalability (System Administrator)        | Scalable architecture to accommodate     | <10% degradation    | Ensure system performance as data  |
|              |           |                                           | increasing data and users.               | at 2x data          | and users grow.                    |
+--------------+-----------+-------------------------------------------+------------------------------------------+---------------------+------------------------------------+

