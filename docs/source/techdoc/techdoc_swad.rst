Software Architecture Design Description (SWAD)
##################################################

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


Definitions, Acronyms, and Abbreviations
------------------------------------------

- **UI** -- User Interface; the ScanHub UI, a React/TypeScript single-page
  application.
- **API Gateway** -- Reverse proxy (nginx) that terminates TLS and is the
  single entry point routing requests from the UI to the backend services.
- **WS** -- WebSocket; bidirectional connection used between the Device
  Manager and a connected MRI device.
- **SSE** -- Server-Sent Events; one-way HTTP stream used to push live task
  status updates from the Device Manager to the UI.
- **JWT / OAuth2** -- Token format and authorization framework used for
  authenticating users and services; access tokens are issued by the
  User-Login Manager.
- **Dagster** -- Data-orchestration framework used by the Orchestration
  Engine to define and execute the reconstruction pipeline as a graph of
  assets and ops.
- **MRpro** -- Open-source MR image reconstruction library used by the
  Orchestration Engine to reconstruct images from raw acquisition data.
- **MRD / ISMRMRD** -- (ISMRM) Raw Data format used to store raw MRI
  acquisition data.
- **Pulseq (.seq)** -- Open MR sequence description format; MRI sequences
  are stored and versioned by the Protocol Manager.
- **DICOM** -- Digital Imaging and Communications in Medicine; format used
  for reconstructed images and results.
- **PACS / XNAT** -- External systems for long-term image archiving and
  research data management; ScanHub can export data to such systems.
- **Data Lake** -- Shared filesystem volume mounted by the Device Manager
  and the Orchestration Engine, used to exchange raw and reconstructed data
  files between services without routing large binaries through the
  database layer.


Figures
-------
- :ref:`Figure 1: MRI Acquisition Workflow (key scenario) <fig-mri-acquisition-workflow>`
- :ref:`Figure 2: System Overview <fig-system-overview>`
- :ref:`Figure 3: System Decomposition (development view) <fig-system-decomposition>`
- :ref:`Figure 4: Connected Device Component <fig-connected-device-component>`
- :ref:`Figure 5: Workflow / Orchestration Component <fig-workflow-orchestration-component>`


System Context
==============

Key Scenarios
-------------

The following key scenario focuses on the basic functionality of the system
from both the user's and system's perspective. It illustrates how the
software components introduced in `System Decomposition`_ collaborate at
runtime and complements the detailed, stakeholder-tagged scenarios already
defined in the :doc:`SWRS <techdoc_swrs>`.

MRI Acquisition Workflow
~~~~~~~~~~~~~~~~~~~~~~~~~
An operator selects a patient, defines a protocol with one or more
acquisition tasks (device, sequence, and acquisition parameters), and starts
the acquisition. The Device Manager relays the start command to the
connected device over its open WebSocket connection, reports live progress
back to the UI, and, once the raw data has been transferred, hands the data
off to the Orchestration Engine for reconstruction. Completion, failure, or
cancellation of the reconstruction pipeline is reported back through the
Protocol Manager (persisted task/result state) and to the UI (live status).

.. _fig-mri-acquisition-workflow:

**Figure 1 -- MRI Acquisition Workflow**

.. mermaid::

   sequenceDiagram
       actor Operator
       participant UI as ScanHub UI
       participant PROT as Protocol Manager
       participant DM as Device Manager
       participant DEV as MRI Device
       participant OE as Orchestration Engine

       Operator->>UI: Select patient, define protocol & task
       UI->>PROT: Create protocol / task (device, sequence)
       Operator->>UI: Start acquisition
       UI->>DM: trigger_acquisition(task_id)
       DM->>PROT: Fetch task & sequence
       DM->>DEV: WS start(sequence, parameters)
       DEV-->>DM: WS status(BUSY, progress)
       DM->>PROT: Update task status
       DM-->>UI: SSE task status
       DEV-->>DM: WS raw data file (MRD)
       DM->>DM: Store file in data lake
       DM->>PROT: Create blank result
       DM->>OE: Submit reconstruction job
       OE->>OE: Reconstruct (MRpro), convert to DICOM, AI post-processing
       OE->>PROT: Register DICOM result, set task FINISHED
       OE->>DM: Push completion event
       DM-->>UI: SSE task FINISHED
       UI->>PROT: Fetch DICOM result
       UI-->>Operator: Display reconstructed image

If the device reports an error, or the reconstruction job fails or is
cancelled, the same channels are used to propagate the corresponding
``ERROR`` / ``FAILED`` / ``CANCELLED`` status to the task and to the UI
instead of ``FINISHED``.


System Decomposition
=====================

ScanHub is a cloud-native platform built from independently deployable
services: a browser-based UI, an API gateway, four FastAPI microservices
covering authentication, patient management, protocol/task/result
management and device connectivity, and a Dagster-based orchestration
engine that performs image reconstruction. Services communicate over the
internal Docker network via REST, WebSocket, SSE, and the Dagster GraphQL
API; each stateful service owns its own database, and large binary data is
exchanged through a shared data lake volume rather than through the
databases.

.. _fig-system-overview:

**Figure 2 -- System Overview**

.. mermaid::

   flowchart LR
       operator(["Operator"])
       device[["MRI Device / Simulator"]]
       archive[("PACS / XNAT")]

       subgraph scanhub["ScanHub Platform"]
           direction LR
           ui["ScanHub UI"]
       end

       operator -- HTTPS --> ui
       device <-- WebSocket --> scanhub
       scanhub -. optional export .-> archive

The platform is reached by operators through a browser over HTTPS, and by
MRI devices (real or simulated) through a persistent WebSocket connection.
Reconstructed results can optionally be exported to an external archive
such as PACS or XNAT.

.. _fig-system-decomposition:

**Figure 3 -- System Decomposition (development view)**

.. mermaid::

   flowchart TB
       ui["ScanHub UI<br/>(React / TypeScript)"]
       gw["API Gateway<br/>(nginx)"]

       ui --> gw

       subgraph core["Core Services"]
           direction TB
           auth["User-Login Manager<br/>Governance: auth, users"]
           pat["Patient Manager<br/>Study Management: patients"]
           prot["Protocol Manager<br/>Workflow: protocols, tasks, results, sequences"]
           devm["Device Manager<br/>Acquisition: devices, WS gateway, SSE"]
       end

       gw --> auth
       gw --> pat
       gw --> prot
       gw --> devm

       subgraph data["Persistence"]
           direction TB
           sdb[("scanhub-database<br/>PostgreSQL")]
           pdb[("patient-database<br/>PostgreSQL")]
           seqdb[("sequence-database<br/>MongoDB")]
           lake[("Data Lake<br/>shared volume")]
       end

       auth --> sdb
       devm --> sdb
       prot --> sdb
       prot --> seqdb
       pat --> pdb
       devm --> lake

       devm <--> device[["Connected MRI Device"]]

       devm --> oe["Orchestration Engine<br/>(Dagster)"]
       oe --> lake
       oe --> prot
       oe --> devm

The development view groups the backend into the conceptual layers used
throughout this document, each realized by one microservice: *Governance*
(User-Login Manager -- OAuth2/JWT authentication and user management),
*Study Management* (Patient Manager -- patient records), *Workflow*
(Protocol Manager -- protocols, acquisition tasks, results, and MRI
sequences), and *Acquisition* (Device Manager -- device registry and the
WebSocket/SSE gateway to connected devices). The *Persistence* layer is
split by data shape: relational state in two PostgreSQL databases, sequence
files in MongoDB, and large binary acquisition/reconstruction files in a
shared data lake volume. The Orchestration Engine consumes the data lake and
reports results and status back to the Workflow and Acquisition layers. All
UI traffic passes through the nginx API Gateway, which also terminates TLS
and proxies the Dagster web UI for pipeline observability.

The two component diagrams below zoom into the *Acquisition* layer's
interaction with a connected device, and into the *Workflow* layer's
reconstruction pipeline, respectively.

.. _fig-connected-device-component:

**Figure 4 -- Connected Device Component**

.. mermaid::

   flowchart LR
       device[["MRI Device / Simulator SDK"]]
       ui["ScanHub UI"]
       prot["Protocol Manager"]
       oe["Orchestration Engine"]
       lake[("Data Lake")]

       subgraph devm["Device Manager"]
           direction TB
           ws["WebSocket endpoint /ws<br/>register, ping, status, file-transfer"]
           mon["Heartbeat monitor<br/>marks device OFFLINE on timeout"]
           http["REST endpoints<br/>devices, trigger_acquisition"]
           sse["SSE endpoint /task-stream"]
       end

       device <--> ws
       ws --> mon
       ui --> http
       http -- start command --> ws
       http <--> prot
       ws -- raw data file --> lake
       ws -- submit reconstruction job --> oe
       oe -- push-event --> sse
       sse -- task status --> ui

A device authenticates on ``/ws`` with a device id/token pair, then sends
periodic ``ping`` heartbeats; a missed-heartbeat timeout marks it
``OFFLINE`` even on an ungraceful disconnect. Acquisitions are started via a
REST call from the UI, which the Device Manager forwards as a ``start``
command over the device's WebSocket. Device status and progress updates are
persisted to the Protocol Manager and re-broadcast to the UI over SSE. Once
the raw data file has been streamed to the Device Manager, it is written to
the data lake, a result record is created, and a Dagster reconstruction job
is submitted; the ``/task/{id}/push-event`` endpoint lets the Orchestration
Engine report pipeline completion back through the same SSE stream.

.. _fig-workflow-orchestration-component:

**Figure 5 -- Workflow / Orchestration Component**

.. mermaid::

   flowchart LR
       lake[("Data Lake")]
       prot["Protocol Manager"]
       devm["Device Manager (SSE)"]

       subgraph oe["Orchestration Engine (Dagster)"]
           direction LR
           acq["acquisition_data_asset<br/>load MRD + device parameters"]
           recon["mrpro_direct_reconstruction<br/>MRpro image reconstruction"]
           dcm["DICOM conversion"]
           smooth["image_smoothing<br/>AI post-processing"]
           sensors["Run-status sensors<br/>on success / failure / canceled"]

           acq --> recon --> dcm --> smooth --> sensors
       end

       lake --> acq
       sensors -- register result, set task status --> prot
       sensors -- push-event --> devm

The Orchestration Engine runs the reconstruction pipeline as a Dagster job
composed of assets: raw MRD and device parameters are loaded from the data
lake, reconstructed into images with MRpro, converted to DICOM, and passed
through an AI-based smoothing/post-processing step. Dagster run-status
sensors observe the job's outcome and, on success, register the resulting
DICOM files as a result and mark the task ``FINISHED``; on failure or
cancellation they mark the task ``FAILED`` / ``CANCELLED`` instead. In both
cases the sensors also push a completion event to the Device Manager so the
UI is updated in real time.
