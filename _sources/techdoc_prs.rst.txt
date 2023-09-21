Product Requirement Specifications (PRS)
========================================

!!This Section is Work in Progress.!!

Add requireemnts to the table below.:
- Current setups often don't allow running in the cloud - on prem setups need to be supported
- XNAT support
- NIFTI support
- ISMRMRD support
- RAW MR support


MRI Acquisition Device Software: Product Requirement Specification (PRS)
========================================================================

.. table:: 
   :widths: 10 10 40 30 10 20

   +--------------+-----------------+--------------------------------------+-------------------------------------------+---------------------+-----------------------------------------+
   | ID           | Priority        | User Need (User)                     | Product Requirement                       | Targeted Performance| Intended claim                          |
   +==============+=================+======================================+===========================================+=====================+=========================================+
   | SH_PRS_010   | Must Have       | Real-time Monitoring (Radiologist)   | Continuously monitor and display MRI scan | 99% uptime          | Ensure real-time monitoring for accurate|
   |              |                 |                                      | data in real-time.                        |                     | diagnosis.                              |
   +--------------+-----------------+--------------------------------------+-------------------------------------------+---------------------+-----------------------------------------+
   | SH_PRS_050   | Must Have       | Compliance (Regulatory Affairs       | Compliance with HIPAA, GDPR, and FDA      | 100% Compliance     | Ensure compliance with industry         |
   |              |                 | Specialist)                          | regulations.                              |                     | regulations for patient safety.         |
   +--------------+-----------------+--------------------------------------+-------------------------------------------+---------------------+-----------------------------------------+
   | SH_PRS_070   | Must Have       | Reliability (Site/Support Engineer)  | System stability with minimum downtime.   | 99.99% uptime       | Maintain a reliable and stable MRI      |
   |              |                 |                                      |                                           |                     | acquisition system.                     |
   +--------------+-----------------+--------------------------------------+-------------------------------------------+---------------------+-----------------------------------------+
   | SH_PRS_020   | Should Have     | Interoperability (Legal Manufacturer)| Compatibility with various DICOM systems. | N/A                 | Seamless integration with existing      |
   |              |                 |                                      |                                           |                     | healthcare systems.                     |
   +--------------+-----------------+--------------------------------------+-------------------------------------------+---------------------+-----------------------------------------+
   | SH_PRS_040   | Should Have     | Alerting (MTA)                       | Real-time alerts for scan anomalies or    | <5 minutes          | Rapid response to scan anomalies or     |
   |              |                 |                                      | issues.                                   |                     | issues.                                 |
   +--------------+-----------------+--------------------------------------+-------------------------------------------+---------------------+-----------------------------------------+
   | SH_PRS_060   | Should Have     | User-Friendly (MTA)                  | Intuitive UI for scan setup and patient   | <30 minutes         | Streamline user interaction for         |
   |              |                 |                                      | management.                               | onboarding          | increased productivity.                 |
   +--------------+-----------------+--------------------------------------+-------------------------------------------+---------------------+-----------------------------------------+
   | SH_PRS_100   | Should Have     | Scalability (System Administrator)   | Scalable architecture to accommodate      | <10% degradation    | Ensure system performance as data and   |
   |              |                 |                                      | increasing data and users.                | at 2x data          | users grow.                             |
   +--------------+-----------------+--------------------------------------+-------------------------------------------+---------------------+-----------------------------------------+
   | SH_PRS_030   | Nice to Have    | Remote Access (Radiologist)          | Enable secure remote access to MRI data.  | N/A                 | Facilitate remote diagnosis and         |
   |              |                 |                                      |                                           |                     | consultations.                          |
   +--------------+-----------------+--------------------------------------+-------------------------------------------+---------------------+-----------------------------------------+
   | SH_PRS_080   | Nice to Have    | Advanced Features (Scientist)        | Access to raw MRI data and experimental   | N/A                 | Facilitate sequence development and     |
   |              |                 |                                      | sequence options.                         |                     | research.                               |
   +--------------+-----------------+--------------------------------------+-------------------------------------------+---------------------+-----------------------------------------+
   | SH_PRS_090   | Nice to Have    | Data Security (System Administrator) | Strong data encryption and role-based     | 100% Compliance     | Secure patient data and adhere to       |
   |              |                 |                                      | access control.                           |                     | compliance requirements.                |
   +--------------+-----------------+--------------------------------------+-------------------------------------------+---------------------+-----------------------------------------+

