.. _tech-doc:

Technical Documentation
========================

.. note::
   This section is a work in progress. Content, requirement IDs, and diagrams
   will keep evolving alongside the ScanHub / A4IM development.

Purpose
-------
This chapter collects the technical and regulatory documentation for the ScanHub
platform and the A4IM MRI scanner it powers. The documents follow a standard
medical-device software documentation trail that translates stakeholder needs
into product requirements, software requirements, and finally the software
architecture that implements them.

Document Overview
------------------
.. list-table::
   :header-rows: 1
   :widths: 12 15 43 30

   * - Document
     - Abbreviation
     - Purpose
     - Primary Audience
   * - :doc:`Product Requirement Specification <techdoc_prs>`
     - PRS
     - Captures stakeholder and user needs and turns them into prioritized
       product-level requirements. Serves as the design input for the SWRS.
     - Product management, regulatory affairs
   * - :doc:`Software Requirements Specification <techdoc_swrs>`
     - SWRS
     - Derives concrete, verifiable functional and non-functional software
       requirements from the PRS, together with representative usage
       scenarios and device-communication data models.
     - Software engineers, test engineers, quality assurance
   * - :doc:`Software Architecture Design Description <techdoc_swad>`
     - SWAD
     - Describes how the software is structured — its components, layers,
       and deployment context — to satisfy the requirements defined in the
       SWRS.
     - Developers, architects, integration and test teams

Traceability
------------
Each need in the PRS is assigned a unique ``PRS_xxxx`` ID. Every functional
requirement in the SWRS references the ``PRS_xxxx`` ID it originates from in
its *Reference/Traceability* column, and each functional requirement carries
its own ``A4IM_FR_xxx`` ID. This creates an auditable chain from a stakeholder
need, through a product requirement, to a verifiable software requirement.
The SWAD in turn maps requirements onto the software components responsible
for implementing them.

Scope
-----
Together, the documents in this chapter define and describe:

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
----------
- Product Requirement Specification (PRS) for the A4IM scanner, detailing the
  expectations and needs from a product standpoint.
- System Requirements Specification (SRS) for the A4IM scanner, outlining the
  system-level requirements the software must meet to ensure compatibility
  and performance within the MRI system.
- Risk Assessment Worksheet, identifying potential risks associated with the
  software and the necessary mitigations to ensure patient and operator
  safety.

.. note::
   Document numbers and versions for the SRS and Risk Assessment Worksheet
   will be added once those documents are finalized.

Content
-------
.. toctree::
   :maxdepth: 1

   techdoc_prs
   techdoc_swrs
   techdoc_swad
