<p align="center">
    <img src="scanhub-ui/public/logo.png" width="100" alt="ScanHub">
    <h1 align="center">ScanHub</h3>
</p>

<p align="center">
<a href="https://github.com/brain-link/scanhub/actions/workflows/build.yml" target="_blank">
    <img src="https://github.com/brain-link/scanhub/actions/workflows/build.yml/badge.svg" alt="Build"/>
</a>
<a href="https://github.com/brain-link/scanhub/actions/workflows/static-tests-backend.yml" target="_blank">
    <img src="https://github.com/brain-link/scanhub/actions/workflows/static-tests-backend.yml/badge.svg" alt="Static Tests Backend"/>
</a>

<a href="https://scanhub.brain-link.de/" target="_blank">
    <img src="https://img.shields.io/badge/Documentation-online-brightgreen" alt="Documentation"/>
</a>
</p>



# About

ScanHub is intended to be a multi modal acquisition software, which allows individualizable, modular and cloud-based processing of functional and anatomical medical images. 
It seamlessly merges the acquisition with the processing of complex data on a single platform.
ScanHub is open-source and freely availably to anyone :earth_africa:.

The greatest novalty of ScanHub is the cross-manufacturer and multi-modality aspect, allowing accessible cloud-based data processing in one framework :rocket:

Currently we are focussing on the development of an acquisition solution for the open-source MRI [OSI2One](https://www.opensourceimaging.org/2023/01/09/first-open-source-mri-scanner-presented-the-osii-one/).

ScanHub is designed as a client-server application. It consists of several services that form the backbone of the acquisition platform and a web-based frontend called scanhub-ui. (The [scanhub-ui](https://github.com/brain-link/scanhub-ui) repository was incorporated into the subfolder scanhub-ui of this repository to facilitate the joint development).

We welcome anyone who would like to join our mission, just [get in touch](mailto:info@brain-link.de) :email:.


## Demo :clapper:

The following video shows a short demonstration of the ScanHub UI (September 2023). You will see how to navigate through the acquisition planner, inspect an MRI sequence and start an MRI simulation on a virtual MRI scanner. In the end we are demonstrating how to view the DICOM image, reconstructed by our workflow engine subsequently to the acquisition.

https://github.com/user-attachments/assets/da900b3b-e9b3-45bf-a6bb-85f69f3d5f73


## About

The advent of cloud computing has enabled a new era of innovation, and ScanHub is at the forefront of leveraging this technology for the benefit of the MRI community. By shifting image reconstruction, processing, and storage from on-site infrastructure to the cloud, ScanHub offers a myriad of advantages over traditional MRI consoles:
1.	Open-source transparency: ScanHub's open-source nature fosters transparency and collaboration within the MRI community, encouraging the development of a unified standard and preventing the fragmentation caused by proprietary black-box solutions. This approach enables researchers and developers to build upon each other's work, accelerating innovation and improving the overall quality of MRI solutions.
2.	Cost-efficiency: ScanHub eliminates the need for expensive on-site hardware and software, reducing both upfront investments and ongoing maintenance costs. This allows institutions of all sizes to access advanced MRI processing capabilities without breaking the budget.
3.	Scalability and flexibility: The cloud-based nature of ScanHub enables seamless scaling of resources as needed, allowing users to easily accommodate fluctuations in demand or expand their capabilities. Furthermore, ScanHub's platform-agnostic design allows for the integration of custom processing algorithms and third-party solutions, promoting innovation and avoiding vendor lock-in.
4.	Efficient resource utilization: ScanHub's centralized resource management ensures optimal allocation and utilization of resources across multiple projects and users, preventing bottlenecks and maximizing efficiency.
5.	Enhanced collaboration and data sharing: ScanHub's cloud-based infrastructure facilitates easy data sharing and collaboration among teams and institutions, enabling researchers to pool resources and insights to accelerate the development of new diagnostic techniques and treatments.
6.	Security and compliance: ScanHub's cloud platform adheres to stringent data security protocols and compliance requirements, ensuring that sensitive patient data remains protected and confidential.


## Setting up the ScanHub Demo

<!-- start demo-setup -->

Scanhub is deployed using Docker and Docker Compose. Make sure they are installed. The following instructions will guide you through the process of an all-in-one deployment of scanhub, i.e. all the services and the device connector will run on the same device.

### 1. Building Scanhub:

The microservices within ScanHub are all build on the same base image, to ensure that critical dependencies match and identical data models are used.

Note, that the `.github/workflows/deploy-containers.yml` workflow deploys the latest scanhub-base image from the main branch to the github container registry (GHCR). Per default, this image is used when building scanhub with docker compose.

By the following steps, the scanhub-base image is build from the local code repository.


```
docker build -t scanhub-base -f services/base/Dockerfile .
```

To build scanhub with the base image which was just created, use the following command.

Note: You don't need to run `docker compose build` separately, if you want to use the default setup. `docker compose up --d` creates all the required images, if not already available.

```
docker compose build --build-arg SCANHUB_BASE_IMAGE=scanhub-base:latest
```
Alternatively, you can use the default image `ghcr.io/brain-link/scanhub/scanhub-base:latest` by running

```
docker compose build
```

Note: The repository contains an `.env` file which allows to modify the default image.

### 2. Starting Scanhub

To start all the containers, run the docker compose command.

```
docker compose up --d
```

To access the user interface, open your browser and navigate to [localhost](https://localhost:8443). By default Scanhub uses a self-signed https certificate that will cause a security warning by the browser. You may ignore this warning for localhost during development.
If you run ScanHub for the first time, you are asked to create the first user, when visiting [localhost](https://localhost:8443).


### 3. Register the Demo Device

Devices which are communicating with ScanHub need authenticate, which is done by a token-based approach. 
1. Login in and navigate to the library
2. Create a new device: Enter a device name and description
3. After clicking 'Create', you can download a credentials file which belongs to the new device.
4. Save the credentials file next to the example device in `scanhub/tools/examples`

### 4. Install and Run the Demo Device

The demo device is build on the ScanHub device sdk which needs to be installed as a dependency. You may want to install your dependencies in a virtual environment, e.g. by using conda.
```
conda create -n scanhub-device python=3.13
```
This creates a virtual environment named "scanhub-device" with python version 3.13). To active the virtual environment:
```
conda activate scanhub-device
```
Navigate to `scanhub/tools/device-sdk` and install the device-sdk package with the optional `example` dependencies.
```
pip install -e ".[example]"
```
Last but not least, go to `scanhub/tools/examples` and run
```
python example_usage.py
```

The following terminal output is expected:

    Device ID: d5b8bacd-1f52-4aaf-a3af-c8ee4e5352ee
    INFO:WebSockerHandler:WebSocket connection established.
    INFO:DeviceStateMachine:[STATE] Transitioned to ONLINE
    INFO:DeviceClient:Device registration sent.
    Client started and waiting for commands from the server.
    Server Feedback: Device ONLINE acknowledged.
    Server Feedback: Device registered successfully

### 5. Setup a Demo Protocol

To perfom an acquisition with the demo device, first a protocol needs to be setup in ScanHub. In the user interface, navigate to *Library* and click on *Create Sequence* to upload the provided test sequence available in the example folder. After setting name, description and type, you need to upload `scanhub/tools/examples/test-sequence.seq` as the sequence and `scanhub/tools/examples/header_test-sequence.xml` as the ISMRMRD header file. 

Once the sequence is uploaded, click on *Create Protocol* and fill in the form to create a demo protocol. Once the protocol is created, select it and click on *Create Task*. Thereby, a new acquisition task is created and assigned to the previously created protocol. Within the task creation form, you need to select the demo device created and the sequence created in the previous step. Calibration and field of view settings can be ignored for this demo.

### 6. Trigger the Demo Device

In the ScanHub UI, navigate to *Patients*, click on the "+" button and fill the form to create a new patient for the demo.
Open the patient, by clicking the button on the left of the new patient created.

Now, you should see the acquisition view for a patient within the ScanHub UI. Click the "+" button in the protocols section to create an instance from the protocol template we created in the previous step. 

Before starting the demo acquisition, make sure the demo device is online. This is indicated by a green circle in the right section of the navigation bar. 

Open the protocol, select the acquisition and click the play button to start the demo acquisition. You should see how the progress bar fills up. Once the acquisition is done, the ISMRMRD raw data file is uploaded and should appear in the drop down menu underneath the acquisition task. As soon as the raw data is uploaded, the workflow orchestration engine gets notified and automatically performs the image reconstruction using [MRpro](https://mrpro.rocks/). The reconstruction result is uploaded in DICOM format and can be selected from the file drop down menu underneath the task, as soon as it is available. 

<!-- end demo-setup -->


## Docker Controls

Run:

    docker compose down


During development you may start scanhub and the tools for development using the development-launcher.sh script.
All scripts are located in the `tools/scripts/` folder.
It has an option --full-rebuild. For details, have a look in the script.

    tools/scripts/development-launcher.sh --full-rebuild


## Documentation

See our dedicated [Documentation](https://scanhub.brain-link.de/) web page to get insights into the structure of ScanHub, microservice APIs and more.


## State of development

This software is not yet ready for clinical use!


## Contributor Guide

We appreciate every contribution to ScanHub, if you would like to contribute to the project, please contact us.
Based on a stable main-branch, we are implementing features based on issues.

Feel free to open a new issues for any feature that you are missing in the current main branch.
Each issue should have a detailed description including a description of the problem, bug or feature and a potential solution approach.
We appreciate it if the issue is updated with the actual solution approach during development.
This documentation step might be helpful when working on similar or related issues.

When you start working on an issue, please create a new branch according to the following naming convention.

    Branch name: <ID>-short-name

The `<ID>` refers to the ID of the related issue and `short-name` is a short expression for the title of the issue.
Please link the branch to the issue, as soon as you start working on it.

