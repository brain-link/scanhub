.. _architecture-overview:

======================
Microservice Architecture
======================

ScanHub is not a single application but a set of small, independently
deployable containers wired together by ``docker compose``. Each container owns
one concern — authentication, patient records, device communication, protocol
handling, orchestration or persistence — and reaches the others only over HTTP
on the internal Docker network or through the shared data lake.

This page gives a bird's-eye view of that landscape. It is deliberately
simplified: build arguments, secrets, health checks and development-only port
mappings are mentioned only where they explain a design decision. For the
authoritative definition of every container see :file:`docker-compose.yml`, and
for the routing table :file:`infrastructure/nginx_config.conf`.

.. note::

   This page describes the ``integration`` branch. On ``main`` the
   ``protocol-manager`` does not yet exist; its responsibilities are still split
   across ``exam-manager`` and ``workflow-manager``. The container is named
   ``user-login-manager`` in :file:`docker-compose.yml`; it is sometimes
   referred to as *user-manager* for short.


The container landscape
=======================

.. mermaid::

   %%{init: {"flowchart": {"curve": "basis", "nodeSpacing": 40, "rankSpacing": 55}} }%%
   flowchart TB

       %% ---------------- Client ----------------
       subgraph CLIENT[" Client "]
           direction LR
           ui["scanhub-ui<br/>React · TypeScript · Vite"]
           mri["MRI device<br/>device client"]
       end

       %% ---------------- Gateway ----------------
       gw{{"nginx · api-gateway<br/>TLS :8443 · reverse proxy"}}

       %% ---------------- Microservices ----------------
       subgraph SERVICES[" Microservices · FastAPI "]
           direction LR
           user(["user-login-manager<br/>:8000"])
           patient(["patient-manager<br/>:8100"])
           device(["device-manager<br/>:8000 · WS"])
           protocol(["protocol-manager<br/>:8000"])
       end

       %% ---------------- Orchestration ----------------
       subgraph ORCH[" Orchestration engine "]
           direction LR
           dagit["dagster-webserver<br/>Dagit UI :3000"]
           daemon["dagster-daemon<br/>hooks · sensors"]
       end

       %% ---------------- Persistence ----------------
       subgraph STORAGE[" Persistence "]
           direction LR
           patientdb[("patient-db<br/>Postgres")]
           scanhubdb[("db-scanhub<br/>users · protocols<br/>devices · tasks")]
           seqdb[("db-sequence<br/>MongoDB · Pulseq")]
           lake[["data lake<br/>bind-mounted volume"]]
       end

       xnat["XNAT<br/>external DICOM store"]

       %% ---------------- Ingress ----------------
       ui -->|"HTTPS / REST"| gw
       mri -.->|"WebSocket"| gw

       gw -->|"routed via reverse proxy"| user & patient & device & protocol
       gw --> dagit

       %% ---------------- Service to store ----------------
       user --> scanhubdb
       patient --> patientdb
       device --> scanhubdb
       protocol --> scanhubdb
       protocol --> seqdb
       protocol -.->|"archive"| xnat

       %% ---------------- Orchestration ----------------
       protocol -->|"orchestration"| dagit
       dagit <--> daemon

       %% ---------------- Data lake ----------------
       device -.->|"read / write"| lake
       protocol -.->|"read / write"| lake
       daemon -.->|"read / write"| lake

       %% ---------------- Styling ----------------
       classDef client   fill:#e8f1fb,stroke:#4a7fb5,stroke-width:1px,color:#1b3a5c
       classDef gateway  fill:#12354f,stroke:#0d2537,stroke-width:1px,color:#ffffff
       classDef service  fill:#e5f4f1,stroke:#3f9e8c,stroke-width:1px,color:#12433a
       classDef store    fill:#e7eff7,stroke:#4a7fb5,stroke-width:1px,color:#1b3a5c
       classDef orch     fill:#efe7fb,stroke:#7a5cb5,stroke-width:1px,color:#33215c
       classDef external fill:#fdf0e2,stroke:#c8752e,stroke-width:1px,stroke-dasharray:4 3,color:#7a4212

       class ui client
       class gw gateway
       class user,patient,device,protocol service
       class patientdb,scanhubdb,seqdb,lake store
       class dagit,daemon orch
       class mri,xnat external

       style CLIENT   fill:none,stroke:#c8cdd3,stroke-dasharray:5 4
       style SERVICES fill:none,stroke:#c8cdd3,stroke-dasharray:5 4
       style ORCH     fill:none,stroke:#c8cdd3,stroke-dasharray:5 4
       style STORAGE  fill:none,stroke:#c8cdd3,stroke-dasharray:5 4

**How to read the diagram.** Solid arrows are synchronous HTTP calls, dashed
arrows are asynchronous or file-based interactions, and orange dashed outlines
mark components outside the compose stack. Rounded boxes are microservices,
cylinders are databases, and the hexagon is the single ingress point.


Client
======

The **scanhub-ui** is a React single-page application (TypeScript, Vite). It is
a pure client: it holds no state of its own and reaches every backend capability
through the gateway, never by addressing a service directly. This keeps CORS and
TLS handling in one place and means the UI does not need to know how the backend
is decomposed.

.. note::

   The gateway serves the UI at ``/`` as well. In the current
   :file:`docker-compose.yml` the containerised ``scanhub-ui`` service is
   commented out and nginx proxies ``/`` to ``host.docker.internal:3000``, i.e.
   the Vite dev server running on the host. Switching to the containerised
   frontend means enabling the service and pointing the ``location /`` block at
   ``http://scanhub-ui:3000/``.

The second kind of client is the **device client**, a small agent running on or
next to the scanner. Rather than polling, it holds a WebSocket connection through
the gateway to the ``device-manager``, so the backend can push scan commands to
the scanner and the scanner can stream raw data back.


API gateway
===========

A single **nginx** container (``api-gateway``) terminates TLS and reverse proxies
every inbound request to the matching upstream based on the URL prefix:

.. list-table::
   :header-rows: 1
   :widths: 34 66

   * - Route
     - Upstream
   * - ``/``
     - ScanHub UI (Vite dev server on the host, or the ``scanhub-ui`` container)
   * - ``/api/v1/userlogin``
     - ``user-login-manager:8000``
   * - ``/api/v1/patient``
     - ``patient-manager:8100``
   * - ``/api/v1/device``
     - ``device-manager:8000``
   * - ``/api/v1/device/ws``
     - ``device-manager:8000`` — WebSocket, with ``Upgrade``/``Connection`` headers
   * - ``/api/v1/protocol``
     - ``protocol-manager:8000``
   * - ``/dagster/``
     - ``dagster-webserver:3000`` — Dagit UI, also WebSocket-upgraded
   * - ``/api/v1/<service>/login``
     - ``user-login-manager:8000/api/v1/userlogin/login`` — every service exposes
       its own ``login`` path, all of which the gateway funnels to the single
       login service

The container listens on ``8080`` (plain HTTP) and ``8443`` (TLS); the
production ``80``/``443`` mappings are present but commented out. The TLS
certificate and private key are supplied as Docker secrets and read from
``/run/secrets/``. Because the gateway is the only entry point, the microservices
themselves publish no host ports and address each other by compose service name
on the internal network.


Microservices
=============

Each service is a small FastAPI application with its own image, built from
:file:`services/<name>/` on a shared ``SCANHUB_BASE_IMAGE``, and each exposes a
``/health/readiness`` endpoint that compose uses to sequence startup via
``depends_on: service_healthy``.

.. list-table::
   :header-rows: 1
   :widths: 22 8 42 28

   * - Container
     - Port
     - Responsibility
     - Persists to
   * - ``user-login-manager``
     - 8000
     - Login, tokens, users and access control.
     - ``db-scanhub``
   * - ``patient-manager``
     - 8100
     - Patient demographics and identifiers.
     - ``patient-db``
   * - ``device-manager``
     - 8000 (+ WS)
     - Device registration, connection state, command channel to the scanner.
     - ``db-scanhub``, data lake
   * - ``protocol-manager``
     - 8000
     - Protocols, tasks and acquisitions; owns the MRI sequences, hands work to
       the orchestration engine and archives results.
     - ``db-scanhub``, ``db-sequence``, data lake, XNAT

The dependency graph is deliberately shallow: only ``protocol-manager`` declares
a dependency on another service (``device-manager``), and everything else depends
solely on its database. The important boundary is **patient data** —
``patient-manager`` is the only container holding the ``patient-db`` credentials,
so every other service refers to a patient by identifier only. That separation is
what allows personal health information to be isolated or hosted separately
without touching the rest of the stack.


Persistence
===========

``db-scanhub``
   PostgreSQL 15.2, holding the operational tables: users, devices, protocols,
   tasks and acquisitions. Shared by ``user-login-manager``, ``device-manager``
   and ``protocol-manager``, which receive the same credential secrets. It
   publishes ``5432`` to the host — explicitly marked *for development only*.

``patient-db``
   A separate PostgreSQL 15.2 instance dedicated to patient records, reachable
   only from ``patient-manager`` and with no host port mapping.

``db-sequence``
   MongoDB, storing Pulseq sequence definitions, whose nested and evolving
   structure fits a document store better than a relational schema.

``data lake``
   The host directory ``${DATA_LAKE_DIR}``, bind-mounted at ``/data`` into
   exactly those containers that handle bulk data: ``device-manager``,
   ``protocol-manager`` and both Dagster containers. Raw k-space, reconstructed
   images and intermediate artefacts are written here as files; only metadata and
   file references travel through the databases, which keeps large binary
   payloads out of both the database and the HTTP layer.

All database credentials are injected as Docker secrets and read through the
``*_FILE`` environment variables rather than being passed in plaintext, and each
database keeps its data in a named volume so ``docker compose down`` does not
discard it.


Orchestration engine
====================

Everything that happens *after* an acquisition — reconstruction, processing,
export — is a Dagster job rather than inline service code. Two containers share
one image (``scanhub-orchestration-engine``) and one configuration anchor:

* **dagster-webserver** serves the Dagit UI on port 3000 under the
  ``/dagster`` path prefix, which is what allows the gateway to proxy it under
  the same origin as the rest of the app.
* **dagster-daemon** runs schedules and sensors and executes queued runs.

Both mount the ``dagster_storage`` volume (run logs, schedules, sensor state) and
the data lake. Splitting processing out this way means a long reconstruction
never blocks an HTTP request, failed runs can be retried and inspected in Dagit,
and new processing steps can be added without redeploying the services.


External systems
================

**XNAT** is an imaging archive outside the compose stack. Once a task completes,
``protocol-manager`` — the only service configured for it — exports the resulting
DICOM data. The connection is configured through ``XNAT_HOST``, ``XNAT_USER``,
``XNAT_PASSWORD`` and ``XNAT_PROJECT_ID``, defaulting to
``http://host.docker.internal:8081`` and project ``A4IM``.


A typical acquisition
=====================

A scan touches most of the stack:

#. The operator signs in through the UI; ``user-login-manager`` validates the
   credentials and issues a token.
#. The operator selects a patient (``patient-manager``) and a protocol
   (``protocol-manager``), which loads the matching sequence from ``db-sequence``.
#. Starting the acquisition creates a task in ``db-scanhub``; ``device-manager``
   pushes the command to the scanner over the WebSocket.
#. The scanner streams raw data back; ``device-manager`` writes it to the data
   lake and records only the file reference in the database.
#. ``protocol-manager`` triggers a Dagster job; ``dagster-daemon`` picks it up,
   reads the raw data from the lake and writes the reconstruction back.
#. The result is archived to XNAT and becomes visible in the UI.

Two rules hold throughout, and they are what keep the containers independently
replaceable: no service reads another service's database, and no bulk data is
passed through the HTTP layer.

.. seealso::

   :doc:`deployment` — how this same set of containers is deployed on a single
   scanner workstation, on a clinic server, or on a Kubernetes cluster.