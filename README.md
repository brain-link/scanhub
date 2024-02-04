<p align="center">
  <a href="https://brain-link.de/wp-content/uploads/2022/03/ScanHub.svg"><img src="https://brain-link.de/wp-content/uploads/2022/03/ScanHub.svg" width="300" height="150" alt="ScanHub"></a>
</p>

<p align="center">
<a href="https://github.com/brain-link/scanhub/actions/workflows/build.yml" target="_blank">
    <img src="https://github.com/brain-link/scanhub/actions/workflows/build.yml/badge.svg" alt="Build"/>
</a>
<a href="https://github.com/brain-link/scanhub/actions/workflows/static-tests.yml" target="_blank">
    <img src="https://github.com/brain-link/scanhub/actions/workflows/static-tests.yml/badge.svg" alt="Static Tests"/>
</a>
<a href="https://codecov.io/gh/brain-link/scanhub" target="_blank">
    <img src="https://codecov.io/gh/brain-link/scanhub/graph/badge.svg?token=L1T3LA3EBX" alt="Coverage"/>
</a>
<a href="https://scanhub.brain-link.de/" target="_blank">
    <img src="https://img.shields.io/badge/Documentation-online-brightgreen" alt="Documentation"/>
</a>
</p>

-----------------
  
ScanHub is intended to be a multi modal acquisition software, which allows individualizable, modular and cloud-based processing of functional and anatomical medical images. 
It seamlessly merges the acquisition with the processing of complex data on a single platform.
ScanHub is open-source and freely availably to anyone :earth_africa:.

The greatest novalty of ScanHub is the cross-manufacturer and multi-modality aspect, allowing accessible cloud-based data processing in one framework :rocket:

Currently we are focussing on the development of an acquisition solution for the open-source MRI [OSI2One](https://www.opensourceimaging.org/2023/01/09/first-open-source-mri-scanner-presented-the-osii-one/).

ScanHub represents the backbone of our acquisition platform. In parallel we are working on a web-based frontend :arrow_right: [scanhub-ui](https://github.com/brain-link/scanhub-ui).

We welcome anyone who would like to join our mission, just [get in touch](mailto:info@brain-link.de) :email:.

Installation
------------

To install the package, you need install [Docker](https://docs.docker.com/engine/install/) first. 
The installation of ScanHub-UI is as simple as using the following command.

    docker-compose up -d --build


Documentation
-----------

See our dedicated [Documentation](https://scanhub.brain-link.de/) web page to get insights into the structure of ScanHub, microservice APIs and more.


About
-----------

The advent of cloud computing has enabled a new era of innovation, and ScanHub is at the forefront of leveraging this technology for the benefit of the MRI community. By shifting image reconstruction, processing, and storage from on-site infrastructure to the cloud, ScanHub offers a myriad of advantages over traditional MRI consoles:
1.	Open-source transparency: ScanHub's open-source nature fosters transparency and collaboration within the MRI community, encouraging the development of a unified standard and preventing the fragmentation caused by proprietary black-box solutions. This approach enables researchers and developers to build upon each other's work, accelerating innovation and improving the overall quality of MRI solutions.
2.	Cost-efficiency: ScanHub eliminates the need for expensive on-site hardware and software, reducing both upfront investments and ongoing maintenance costs. This allows institutions of all sizes to access advanced MRI processing capabilities without breaking the budget.
3.	Scalability and flexibility: The cloud-based nature of ScanHub enables seamless scaling of resources as needed, allowing users to easily accommodate fluctuations in demand or expand their capabilities. Furthermore, ScanHub's platform-agnostic design allows for the integration of custom processing algorithms and third-party solutions, promoting innovation and avoiding vendor lock-in.
4.	Efficient resource utilization: ScanHub's centralized resource management ensures optimal allocation and utilization of resources across multiple projects and users, preventing bottlenecks and maximizing efficiency.
5.	Enhanced collaboration and data sharing: ScanHub's cloud-based infrastructure facilitates easy data sharing and collaboration among teams and institutions, enabling researchers to pool resources and insights to accelerate the development of new diagnostic techniques and treatments.
6.	Security and compliance: ScanHub's cloud platform adheres to stringent data security protocols and compliance requirements, ensuring that sensitive patient data remains protected and confidential.
