<p align="center">
  <a href="https://brain-link.de/wp-content/uploads/2022/03/ScanHub.svg"><img src="https://brain-link.de/wp-content/uploads/2022/03/ScanHub.svg" width="300" height="150" alt="ScanHub"></a>
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

-----------------
  
ScanHub is intended to be a multi modal acquisition platform, which allows individualizable, modular and cloud-based processing of functional and anatomical medical images. 
It seamlessly merges the acquisition with the processing of complex data on a single platform.
ScanHub is open-source and freely availably to anyone :earth_africa:.

The greatest novalty of ScanHub is the cross-manufacturer and multi-modality aspect, allowing accessible cloud-based data processing in one framework :rocket:

Currently we are focussing on the development of an acquisition solution for the open-source MRI [OSI2One](https://www.opensourceimaging.org/2023/01/09/first-open-source-mri-scanner-presented-the-osii-one/).

ScanHub is designed as a client-server application. It consists of several services that form the backbone of the acquisition platform and a web-based frontend called scanhub-ui. (The [scanhub-ui](https://github.com/brain-link/scanhub-ui) repository was incorporated into the subfolder scanhub-ui of this repository to facilitate the joint development).

We welcome anyone who would like to join our mission, just [get in touch](mailto:info@brain-link.de) :email:.


Demo :clapper:
--------------

The following video shows a short demonstration of the ScanHub UI (September 2023). You will see how to navigate through the acquisition planner, inspect an MRI sequence and start an MRI simulation on a virtual MRI scanner. In the end we are demonstrating how to view the DICOM image, reconstructed by our workflow engine subsequently to the acquisition.

https://github.com/brain-link/scanhub-ui/assets/42237900/beb8edc9-04c4-4f96-83d7-d8134bd2840e

Installation
------------

Scanhub is deployed using docker and docker-compose. Make sure they are installed first. To build scanhub, make sure that there is an internet connection.

Building and running scanhub can be achieved using the following docker-compose command inside the scanhub repository:

    docker-compose up --detach --build


By default this builds the services with a base docker image from ghcr.io/brain-link/scanhub/scanhub-base:latest. To incorporate the latest changes, as during development, rebuild the scanhub-base image and use the build-arg BASE_IMG=scanhub-base:latest. To do this, build and start the project with the following commands:

    cd services/base
    docker build -t scanhub-base .
    cd ../..
    docker-compose build --build-arg BASE_IMG=scanhub-base:latest
    docker-compose up --detach


During development you may start scanhub and the tools for development using the development-launcher.sh script. It has an option --full-rebuild. For details, have a look in the script.

    development-launcher.sh --full-rebuild


Default Username and Password
-----------------------------

For now a default user needs to be created manually in the user database. The database entry of an example user with username "Max" and password "letmein" is shown in defaultuser.txt and defaultuser.csv


Documentation
-----------

See our dedicated [Documentation](https://scanhub.brain-link.de/) web page to get insights into the structure of ScanHub, microservice APIs and more.

Contributor Guide
-----------

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

About
-----------

The advent of cloud computing has enabled a new era of innovation, and ScanHub is at the forefront of leveraging this technology for the benefit of the MRI community. By shifting image reconstruction, processing, and storage from on-site infrastructure to the cloud, ScanHub offers a myriad of advantages over traditional MRI consoles:
1.	Open-source transparency: ScanHub's open-source nature fosters transparency and collaboration within the MRI community, encouraging the development of a unified standard and preventing the fragmentation caused by proprietary black-box solutions. This approach enables researchers and developers to build upon each other's work, accelerating innovation and improving the overall quality of MRI solutions.
2.	Cost-efficiency: ScanHub eliminates the need for expensive on-site hardware and software, reducing both upfront investments and ongoing maintenance costs. This allows institutions of all sizes to access advanced MRI processing capabilities without breaking the budget.
3.	Scalability and flexibility: The cloud-based nature of ScanHub enables seamless scaling of resources as needed, allowing users to easily accommodate fluctuations in demand or expand their capabilities. Furthermore, ScanHub's platform-agnostic design allows for the integration of custom processing algorithms and third-party solutions, promoting innovation and avoiding vendor lock-in.
4.	Efficient resource utilization: ScanHub's centralized resource management ensures optimal allocation and utilization of resources across multiple projects and users, preventing bottlenecks and maximizing efficiency.
5.	Enhanced collaboration and data sharing: ScanHub's cloud-based infrastructure facilitates easy data sharing and collaboration among teams and institutions, enabling researchers to pool resources and insights to accelerate the development of new diagnostic techniques and treatments.
6.	Security and compliance: ScanHub's cloud platform adheres to stringent data security protocols and compliance requirements, ensuring that sensitive patient data remains protected and confidential.
