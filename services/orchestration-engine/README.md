# Orchestration Engine

The **Orchestration Engine** is a service built on [Dagster](https://dagster.io/) that manages computational task execution within the Brain-Link platform.  

It coordinates and executes directed acyclic graph (DAG)–based jobs (e.g. calibration, image reconstruction, image processing, etc.). In ScanHub these DAG-based jobs are defined by `DAGTask` which integrate with the `AcquisitionTasks` that are executed by the device-manager and provide the data for the `DAGTask`.

## 📂 Project Structure

```text
orchestration-engine
├── dagster.yaml
├── Dockerfile
├── LICENSE
├── orchestrator/
│   ├── jobs/
│   ├── assets/
│   ├── io/
│   ├── hooks.py
│   └── repository.py
├── uv.lock
└── pyproject.toml
```

- dagster.yaml — Dagster instance configuration (run launcher, run coordinator, telemetry, etc.)
- Dockerfile — Container build definition for this service
- orchestrator/ — Python package with orchestration logic
    - jobs/ — Dagster jobs (pipelines/graphs) such as frequency calibration and image reconstruction
    - assets/ — Reusable Dagster ops (atomic computation steps)
    - io/ — Assets, ops and io managers related to input and output
    - hooks.py - Hooks are used to notify the backend upon success of job execution
    - repository.py - Configuration/definition of the dagster repo components


## 🚀 Getting Started

Install dependencies:

```bash
uv sync
```

Features:
* Task orchestration with Dagster
* Jobs for MR frequency calibration and image reconstruction
* Separation of reusable ops, jobs, and external resources
* Packaged for containerized deployment


---

📄 Licensed under the terms of the root [LICENSE](../../LICENSE).
