Software Architecture Design Description (SWAD)
##################################################

.. note::
   This section is a work in progress. The diagrams below are placeholders
   pending conversion of the existing draw.io figures to Mermaid.

Introduction
============
Purpose
-------
This document delineates the comprehensive architectural design and technical
realization of the ScanHub software system for MRI data acquisition and
processing. It aims to provide a coherent, high-level perspective of the
system's context and its static and dynamic structures, serving as a pivotal
reference for developers, programmers, regulatory affairs, and quality
assurance teams. The document is intended to facilitate the technical
realization of the system, enabling developers to understand and build it
without necessitating further inquiries or ad hoc design decisions. It also
offers future project members an expedited overview of the software system's
structure and provides the test team with sufficient information on the
assembly and testing of the software components during integration testing.
Where details surpass the scope of this document, readers are directed to
lower-level architecture and design documents.

Scope
-----
The ScanHub system is a cloud-based, open-source data acquisition and
processing platform specifically designed for transforming the way MRI data
is processed, stored, and shared. This document focuses on the architecture
of the ScanHub platform, detailing its integration with advanced simulation
devices, efficient resource utilization, enhanced data-sharing capabilities,
and rigorous security measures, all leveraged through the power of cloud
computing. It translates the requirements provided by the Design Input [DI]
and the Software Requirements Specification [SWRS] into the system
architecture, serving as a comprehensive guide for the realization of the
software components. For additional details and specifications, refer to the
design input documentation [DI, SWRS].

References
----------
- [DI] ScanHub Design Input
- [DD] ScanHub Device Description
- [SWRS] :doc:`ScanHub Software Requirements Specification <techdoc_swrs>`
- [SWDD] ScanHub Software Design Description

Definitions, Acronyms, and Abbreviations
------------------------------------------

.. note::
   No terms have been defined yet. This subsection will list project-specific
   terms, acronyms, and abbreviations used throughout the document.

Tables
------

.. note::
   No additional tables beyond those embedded in the sections below are
   currently defined.

Figures
-------

.. note::
   All figures are embedded in the sections below; there is no separate
   figure index at this stage.


System Context
==============

Key Scenarios
-------------

The following key scenarios focus on the basic functionality of the device
from both the user's and system's perspectives. This includes user
interactions, as well as essential system procedures like startup, shutdown,
and service functionality. These scenarios are crucial for ensuring the
software architecture supports seamless operation and maintenance of the MRI
system. They complement the detailed, stakeholder-tagged scenarios already
defined in the :doc:`SWRS <techdoc_swrs>`.

.. note::
   Key scenarios specific to the architecture (e.g. startup sequence, failover
   behavior) are still to be added.

System Decomposition
=====================

The following development view shows how the ScanHub UI, the ScanHub Core
domain (with its Acquisition, Study Management, Workflow, Persistence, and
Governance layers), connected devices, and external systems (workflow
runners, PACS, and other storage) relate to one another.

.. mermaid::

   %% Placeholder for the "ScanHub Development View" diagram
   %% (previously ScanHub_Development_View.drawio.png).
   %% TODO: recreate the full development view here.
   flowchart TB
       TODO["TODO: ScanHub Development View"]

.. list-table::
   :header-rows: 1
   :widths: 15 20 50 15

   * - ID
     - Component
     - Description
     - Safety Class
   * - SWAD_CMP_0001
     - Device Manager
     - Manages connected devices, before and during acquisition.
     - A
   * - SWAD_CMP_0002
     - Acquisition Control
     -
     -
   * - SWAD_CMP_0003
     - Workflow Engine
     -
     -

The two component diagrams below zoom into the *Acquisition* layer's
interaction with a connected device, and into the *Workflow* layer's
interaction with external workflow runners, respectively.

.. mermaid::

   %% Placeholder for the "ScanHub Connected Device Component" diagram
   %% (previously ScanHub_Component_Connected_Device.drawio.png).
   %% TODO: recreate the connected-device component diagram here.
   flowchart TB
       TODO2["TODO: ScanHub Connected Device Component"]

.. mermaid::

   %% Placeholder for the "ScanHub Workflow Component" diagram
   %% (previously ScanHub_Component_Workflow.drawio.png).
   %% TODO: recreate the workflow component diagram here.
   flowchart TB
       TODO3["TODO: ScanHub Workflow Component"]
