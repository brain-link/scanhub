.. _deployment-scenarios:

=====================
Deployment Scenarios
=====================

The container architecture described in :doc:`architecture` does not change from
one installation to the next. What changes is *where* those containers run, and
which of the arrows between them become network hops that leave a machine, a
building or an organisation.

Three scenarios are relevant to ScanHub. They differ in how much is distributed,
not in what is deployed:

* **All-in-one on a single device** — everything on the scanner workstation.
  This is what runs today.
* **Distributed in a clinic** — the backend moves to a hospital server; the UI
  and the scanner become network clients.
* **Fully distributed** — the backend moves to a Kubernetes cloud platform and
  integrates with hospital IT systems. This is the target vision.

Read them as a progression: each step takes a boundary that was internal and
turns it into a network boundary that has to be secured.

.. list-table::
   :header-rows: 1
   :widths: 20 27 27 26

   * -
     - All-in-one *(today)*
     - Clinic
     - Fully distributed *(vision)*
   * - Backend runs on
     - The scanner-embedded workstation
     - One on-prem Docker host or cluster
     - Kubernetes cloud platform
   * - Brought up with
     - ``docker compose up``
     - ``docker compose`` on the server
     - Node pools, CPU and GPU
   * - UI reached at
     - ``localhost:8443``
     - Hospital network, over HTTPS
     - Internet, over HTTPS
   * - Device link
     - WebSocket over localhost
     - WebSocket over the hospital network
     - WebSocket from the imaging site
   * - Data lake
     - Bind-mounted host directory
     - Shared volume on the server
     - Shared object storage (PVC)
   * - Image archive
     - Local XNAT
     - XNAT on the same server
     - Hospital PACS
   * - Local IT needed
     - None
     - Hospital IT operates the server
     - None at the imaging site


All-in-one on a single device (today)
=====================================

.. mermaid::

   %%{init: {"flowchart": {"curve": "basis", "nodeSpacing": 40, "rankSpacing": 60}} }%%
   flowchart LR

       subgraph HOST[" Single scanner-embedded workstation · e.g. Nexus console "]
           direction LR

           subgraph BROWSER[" Browser "]
               ui["ScanHub UI<br/>localhost:8443"]
           end

           subgraph BACKEND[" Docker containers · docker compose up "]
               direction TB
               gw{{"nginx api-gateway<br/>TLS · reverse proxy"}}
               svc(["4 microservices<br/>user · patient · device · protocol"])
               dag["Dagster engine<br/>webserver + daemon"]
               db[("Databases<br/>Postgres x2 · MongoDB")]
               lake[["Data lake + XNAT<br/>shared volume · DICOM store"]]

               gw --> svc
               svc --> db
               svc -->|"orchestration"| dag
               svc -.-> lake
               dag -.-> lake
           end

           subgraph SCANNER[" Attached scanner "]
               dc["Device client<br/>localhost"]
           end
       end

       ui <-->|"HTTPS · TLS<br/>localhost"| gw
       dc <-.->|"WebSocket · device certificate<br/>localhost"| gw

       classDef client   fill:#e8f1fb,stroke:#4a7fb5,color:#1b3a5c
       classDef gateway  fill:#12354f,stroke:#0d2537,color:#ffffff
       classDef service  fill:#e5f4f1,stroke:#3f9e8c,color:#12433a
       classDef store    fill:#e7eff7,stroke:#4a7fb5,color:#1b3a5c
       classDef orch     fill:#efe7fb,stroke:#7a5cb5,color:#33215c
       classDef external fill:#fdf0e2,stroke:#c8752e,stroke-dasharray:4 3,color:#7a4212

       class ui client
       class gw gateway
       class svc service
       class db,lake store
       class dag orch
       class dc external

       style HOST    fill:none,stroke:#12354f
       style BROWSER fill:none,stroke:#c8cdd3,stroke-dasharray:5 4
       style BACKEND fill:none,stroke:#c8cdd3,stroke-dasharray:5 4
       style SCANNER fill:none,stroke:#c8752e,stroke-dasharray:5 4

This is the deployment used today, and the one :file:`docker-compose.yml`
describes directly. A single workstation embedded in the scanner — a Nexus
console, for example — runs the browser, every backend container and the device
client. ``docker compose up`` brings up the whole system, and every arrow in the
diagram stays on ``localhost``.

**The UI** is opened in the local browser at ``https://localhost:8443``. Because
the gateway publishes its ports on the host, other machines on the same network
can reach the same UI through port forwarding — convenient for a demo, and the
reason the ``8080``/``8443`` mappings are labelled *for development* in the
compose file.

**The device client** runs on the same host and connects to the ``device-manager``
over the local WebSocket. The attached scanner is served locally: no network in
between, no certificates crossing a boundary that matters.

**XNAT and the data lake** live on this machine too — the data lake as a
bind-mounted directory, XNAT as a locally reachable DICOM store.

The appeal of this setup is that it has no infrastructure requirements at all. A
scanner and a workstation are enough, which is precisely what makes a portable
low-field system usable outside a hospital — or outside the lab entirely. The
trade-off is equally clear: nothing is shared, nothing is backed up by
institutional IT, and the machine's CPU is the only compute the reconstruction
will ever get.


Distributed deployment in a clinic
==================================

.. mermaid::

   %%{init: {"flowchart": {"curve": "basis", "nodeSpacing": 40, "rankSpacing": 70}} }%%
   flowchart LR

       subgraph USER[" User device · nothing installed "]
           ui["Web browser<br/>ScanHub UI (React)"]
       end

       subgraph HOSPITAL[" Hospital IT · on-prem server "]
           direction TB
           gw{{"nginx api-gateway<br/>TLS · reverse proxy"}}
           svc(["4 microservices<br/>user · patient · device · protocol"])
           dag["Dagster engine<br/>webserver + daemon"]
           db[("Databases<br/>Postgres x2 · MongoDB")]
           lake[["Data lake + XNAT<br/>shared volume · DICOM store"]]

           gw --> svc
           svc --> db
           svc -->|"orchestration"| dag
           svc -.-> lake
           dag -.-> lake
       end

       subgraph MRI[" MRI device "]
           dc["Device client<br/>agent on / near the scanner"]
       end

       ui <-->|"HTTPS · TLS"| gw
       dc <-.->|"WebSocket · device certificate"| gw

       classDef client   fill:#e8f1fb,stroke:#4a7fb5,color:#1b3a5c
       classDef gateway  fill:#12354f,stroke:#0d2537,color:#ffffff
       classDef service  fill:#e5f4f1,stroke:#3f9e8c,color:#12433a
       classDef store    fill:#e7eff7,stroke:#4a7fb5,color:#1b3a5c
       classDef orch     fill:#efe7fb,stroke:#7a5cb5,color:#33215c
       classDef external fill:#fdf0e2,stroke:#c8752e,stroke-dasharray:4 3,color:#7a4212

       class ui client
       class gw gateway
       class svc service
       class db,lake store
       class dag orch
       class dc external

       style USER     fill:none,stroke:#c8cdd3
       style HOSPITAL fill:none,stroke:#12354f
       style MRI      fill:none,stroke:#c8752e

The same containers, moved off the scanner and onto a server that hospital IT
operates. One Docker host — or a small cluster — runs the entire backend: every
container from :file:`docker-compose.yml`, unchanged.

**Nothing is installed on the user side.** Any clinician workstation, laptop or
tablet on the hospital network opens the app in a browser and talks to the
gateway over HTTPS. This is the practical payoff of keeping the UI a pure client:
rolling out ScanHub to a department is a URL, not a software deployment.

**The scanner keeps only the device client** — a lightweight agent on or near the
machine that holds a WebSocket connection to the ``device-manager``, receives
scan commands and streams raw data back. It is the only ScanHub software running
at the machine, and the only component that has to be certified with the device.

Two things change compared to the all-in-one setup. Data now lives on hospital
infrastructure, with the backup, access control and physical security that
implies. And the two links leaving the server — browser to gateway, device client
to gateway — cross a real network, so TLS and device certificates stop being a
formality.


Fully distributed setup (vision)
================================

.. mermaid::

   %%{init: {"flowchart": {"curve": "basis", "nodeSpacing": 35, "rankSpacing": 65}} }%%
   flowchart LR

       subgraph EDGE[" Edge · imaging sites "]
           direction TB
           tablet["Portable device<br/>ScanHub UI"]
           mri["MRI device<br/>+ device client"]
       end

       subgraph CLOUD[" Cloud platform · Kubernetes "]
           direction TB
           gw{{"nginx api-gateway<br/>TLS · reverse proxy"}}

           subgraph CPU[" CPU node pool "]
               direction TB
               svc(["4 microservices<br/>user · patient · device · protocol"])
               db[("Databases<br/>Postgres x2 · MongoDB")]
           end

           subgraph GPU[" GPU node pool "]
               dag["Dagster engine<br/>webserver + daemon"]
           end

           lake[["Data lake<br/>shared object storage (PVC)"]]

           gw --> svc
           svc --> db
           svc -->|"orchestration"| dag
           svc -.-> lake
           dag -.-> lake
       end

       subgraph HOSP[" Hospital IT "]
           direction TB
           hl7["HL7 / FHIR engine<br/>interface · integration"]
           mwl["Modality Worklist<br/>DICOM worklist"]
           ris["RIS<br/>orders · worklist · reports"]
           pacs["PACS<br/>patient data + image archive"]
       end

       tablet <-->|"HTTPS · TLS"| gw
       mri <-.->|"WebSocket"| gw

       svc <-.->|"patient · study · worklist"| hl7
       hl7 --- ris
       hl7 --- mwl
       svc -.->|"archive DICOM"| pacs

       classDef client   fill:#e8f1fb,stroke:#4a7fb5,color:#1b3a5c
       classDef gateway  fill:#12354f,stroke:#0d2537,color:#ffffff
       classDef service  fill:#e5f4f1,stroke:#3f9e8c,color:#12433a
       classDef store    fill:#e7eff7,stroke:#4a7fb5,color:#1b3a5c
       classDef orch     fill:#efe7fb,stroke:#7a5cb5,color:#33215c
       classDef external fill:#fdf0e2,stroke:#c8752e,stroke-dasharray:4 3,color:#7a4212
       classDef hospital fill:#fbeaee,stroke:#a8324a,color:#5c1425

       class tablet client
       class gw gateway
       class svc service
       class db,lake store
       class dag orch
       class mri external
       class hl7,mwl,ris,pacs hospital

       style EDGE  fill:none,stroke:#c8cdd3
       style CLOUD fill:none,stroke:#1a6fc4
       style CPU   fill:none,stroke:#1a6fc4,stroke-dasharray:5 4
       style GPU   fill:none,stroke:#7a5cb5,stroke-dasharray:5 4
       style HOSP  fill:none,stroke:#a8324a

The target architecture, in which the backend leaves the hospital entirely and
the imaging site keeps almost nothing.

**At the edge**, an imaging site has no local IT: only the scanner, running the
device client, and a tablet or PC that opens the ScanHub UI. Sites become cheap
to add, which is the point — a low-field scanner in a clinic, in a van or in a
remote location is just another WebSocket connection.

**In the cloud**, the same containers run on Kubernetes, but the deployment can
finally exploit the fact that they were always separable. The microservices and
databases sit in a CPU node pool and scale horizontally; the Dagster engine sits
in a GPU node pool, where reconstruction and AI processing actually belong. The
data lake becomes shared object storage backed by a persistent volume claim
rather than a bind-mounted directory.

**Hospital IT** is integrated rather than replaced. ScanHub reads patient, study
and worklist data from PACS and RIS through the HL7/FHIR interface engine and the
DICOM Modality Worklist, and archives reconstructed DICOM images back into the
hospital PACS. The clinical record stays where clinicians and existing systems
expect it; ScanHub holds the working data.

**Both boundaries are trust boundaries.** Edge to cloud and cloud to hospital
each cross an organisational border, and each carries patient data. Everything
that is a local convenience in the all-in-one setup — self-signed certificates,
localhost WebSockets, an open ``5432`` — becomes a requirement here.


What stays the same
===================

Across all three scenarios:

* **The compose stack is the unit of deployment.** The same images and the same
  inter-container contracts are used whether the target is a scanner console or
  a node pool.
* **The gateway is the only ingress.** Every client reaches the backend through
  nginx, so relocating the backend changes a hostname, not the application.
* **The device client is the only software at the machine.** Everything else the
  scanner needs is on the other end of a WebSocket.
* **The UI is a browser away.** Nothing is installed on a user device in any
  scenario.
* **The data lake is a mount point, not a service.** A bind mount, a shared
  volume or a PVC — the containers see ``/data`` either way.

What changes is the length of the arrows, and how much of what runs on them has
to be secured, replicated and operated.