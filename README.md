<p align="center">
  <a href="https://brain-link.de/wp-content/uploads/2022/03/ScanHub.svg"><img src="https://brain-link.de/wp-content/uploads/2022/03/ScanHub.svg" width="300" height="150" alt="ScanHub"></a>
</p>

<p align="center">
<a href="https://github.com/brain-link/scanhub/actions/workflows/build.yml" target="_blank">
    <img src="https://github.com/brain-link/scanhub/actions/workflows/build.yml/badge.svg" alt="Github Actions">
</a>
<a href="https://github.com/brain-link/scanhub/actions/workflows/test.yml" target="_blank">
    <img src="https://github.com/brain-link/scanhub/actions/workflows/test.yml/badge.svg" alt="Github Actions">
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

See our [Wiki](https://github.com/brain-link/scanhub/wiki) to get insight into the structure of ScanHub, documentation of microservices and more.


About
-----------

The advent of cloud computing has enabled a new era of innovation, and ScanHub is at the forefront of leveraging this technology for the benefit of the MRI community. By shifting image reconstruction, processing, and storage from on-site infrastructure to the cloud, ScanHub offers a myriad of advantages over traditional MRI consoles:
1.	Open-source transparency: ScanHub's open-source nature fosters transparency and collaboration within the MRI community, encouraging the development of a unified standard and preventing the fragmentation caused by proprietary black-box solutions. This approach enables researchers and developers to build upon each other's work, accelerating innovation and improving the overall quality of MRI solutions.
2.	Cost-efficiency: ScanHub eliminates the need for expensive on-site hardware and software, reducing both upfront investments and ongoing maintenance costs. This allows institutions of all sizes to access advanced MRI processing capabilities without breaking the budget.
3.	Scalability and flexibility: The cloud-based nature of ScanHub enables seamless scaling of resources as needed, allowing users to easily accommodate fluctuations in demand or expand their capabilities. Furthermore, ScanHub's platform-agnostic design allows for the integration of custom processing algorithms and third-party solutions, promoting innovation and avoiding vendor lock-in.
4.	Efficient resource utilization: ScanHub's centralized resource management ensures optimal allocation and utilization of resources across multiple projects and users, preventing bottlenecks and maximizing efficiency.
5.	Enhanced collaboration and data sharing: ScanHub's cloud-based infrastructure facilitates easy data sharing and collaboration among teams and institutions, enabling researchers to pool resources and insights to accelerate the development of new diagnostic techniques and treatments.
6.	Security and compliance: ScanHub's cloud platform adheres to stringent data security protocols and compliance requirements, ensuring that sensitive patient data remains protected and confidential.


License
-------

ScanHub, including all its source code and associated documentation (collectively, the "Software"), is dual-licensed under the GNU General Public License version 3 (GPLv3) and the ScanHub commercial license.

### Open Source License

If you want to use the Software under the terms of the GPLv3, you may do so for free. Under the GPLv3, you are allowed to modify and distribute the Software, but any derivative works that you distribute must also be licensed under the GPLv3. For the precise terms and conditions, please refer to the text of the GPLv3, which is included with the Software and can also be found at: http://www.gnu.org/licenses/gpl-3.0.html

### Commercial License

If you wish to use the Software without the restrictions of the GPLv3, such as for the purpose of developing proprietary software that includes the Software without the obligation to disclose your source code, you may purchase a commercial license from BRAIN-LINK UG (haftungsbeschränkt).

The commercial license grants you, the licensee, the rights to use, modify, and distribute the Software without the requirement of providing the source code of your proprietary software to the end users. The commercial license also includes access to premium support and services.

For more information on the commercial license, including pricing, please contact us at info@brain-link.de.

### Choice of License

You may choose to use the Software under either the GPLv3 or the commercial license. If you choose to use the Software under the GPLv3, you must comply with all of the terms of the GPLv3. If you choose to use the Software under the commercial license, you must comply with all of the terms of the commercial license.

### Disclaimer

This is not a legal document. The exact terms of the GPLv3 and the commercial license are specified in their respective legal texts. This document is merely intended to provide a general overview of the dual licensing scheme.

