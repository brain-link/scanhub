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
│   ├── ops/
│   ├── ressources/
│   └── repository.py
├── poetry.lock
└── pyproject.toml
```

- dagster.yaml — Dagster instance configuration (run launcher, run coordinator, telemetry, etc.)
- Dockerfile — Container build definition for this service
- orchestrator/ — Python package with orchestration logic
    - jobs/ — Dagster jobs (pipelines/graphs) such as frequency calibration and image reconstruction
    - ops/ — Reusable Dagster ops (atomic computation steps)
    - repository.py — Dagster repository definition that registers jobs, ops, and resources
    - ressources/ — Dagster resources (interfaces to external systems like device manager, storage, etc.)


## 🚀 Getting Started

Install dependencies:

```bash
poetry install
```

Features:
* Task orchestration with Dagster
* Jobs for MR frequency calibration and image reconstruction
* Separation of reusable ops, jobs, and external resources
* Packaged for containerized deployment


---

📄 Licensed under the terms of the root [LICENSE](../../LICENSE).
