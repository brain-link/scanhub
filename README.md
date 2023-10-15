<p align="center">
  <a href="https://brain-link.de/wp-content/uploads/2022/03/ScanHub.svg"><img src="https://brain-link.de/wp-content/uploads/2022/03/ScanHub.svg" width="300" height="150" alt="ScanHub"></a>
</p>

<p align="center">
  <a href="https://github.com/brain-link/scanhub-ui/actions/workflows/build.yml" target="_blank">
      <img src="https://github.com/brain-link/scanhub-ui/actions/workflows/build.yml/badge.svg" alt="Github Actions">
  </a>
  <a href="https://github.com/brain-link/scanhub-ui/actions/workflows/static-tests-backend.yml" target="_blank">
      <img src="https://github.com/brain-link/scanhub-ui/actions/workflows/static-tests-backend.yml/badge.svg" alt="Github Actions">
  </a>
  <a href="https://github.com/brain-link/scanhub-ui/actions/workflows/static-tests-frontend.yml" target="_blank">
      <img src="https://github.com/brain-link/scanhub-ui/actions/workflows/static-tests-frontend.yml/badge.svg" alt="Github Actions">
  </a>  
</p>

-----------------

About
-----

ScanHub is intended to be a multi modal acquisition software, which allows individualizable, modular and cloud-based processing of functional and anatomical medical images. 
It seamlessly merges the acquisition with the processing of complex data on a single platform.
ScanHub is open-source and freely availably to anyone :earth_africa:.

The greatest novalty of ScanHub is the cross-manufacturer and multi-modality aspect, allowing accessible cloud-based data processing in one framework :rocket:

Currently we are focussing on the development of an acquisition solution for the open-source MRI [OSI2One](https://www.opensourceimaging.org/2023/01/09/first-open-source-mri-scanner-presented-the-osii-one/).

This project only provides the user interface to interact with ScanHub. 
Check out the backbone of our acquisition platform :arrow_right: [ScanHub](https://github.com/brain-link/scanhub).

We welcome anyone who would like to join our mission, just [get in touch](mailto:info@brain-link.de) :email:.


Demo :clapper:
--------------

The following video shows a short demonstration of the ScanHub UI (September 2023). You will see how to navigate through the acquisition planner, inspect an MRI sequence and start an MRI simulation on a virtual MRI scanner. In the end we are demonstrating how to view the DICOM image, reconstructed by our workflow engine subsequently to the acquisition.

https://github.com/brain-link/scanhub-ui/assets/42237900/beb8edc9-04c4-4f96-83d7-d8134bd2840e



Installation
------------

To install the package, you need install [Docker](https://docs.docker.com/engine/install/) first. 
The installation of ScanHub-UI is as simple as using the following command.

    docker-compose up -d --build
    
Note that you need to install [ScanHub](https://github.com/brain-link/scanhub), which is the backbone of the user interface.
Documentation on the installation of scanhub can be found in the README file.

Structural Overview
-------------------

The repository structures in two major components: the patient manager and the user interface. The patient-manager is suppose to emulate a simplified clinical patient management system. This part of the software might be replaced during setup in a (clinical) research facility. To provide a clean separation between data and patient, the patient manager is location here and is not part of the ScanHub backbone.

The frontend contains a `src/` directory which is structured as follows.

* views: All "main" views filling the whole browser window. This components are only included in the router file.
  * dashboard
  * patient-list/patient-table
  * device-list/device-table
  * patient-index
* components: Sub-components for views, if a view is more complex, sub-components might be gathered in a sub-folder. Components can be accessed from different views or also from other components.
* interfaces: Interface files contain ".interface" in front of the file ending ".tsx"
  * data.interface: Interfaces of all data objects like patient, device, workflow, etc.
  * component.interface: Component property interfaces
* client: (Global) Definition of the query client.
  * abstract-query-client: Template
  * urls: Base urls for data queries
  * queries: Constructions of all data query services
  * healthcheck: Queries to health endpoints
* utils: Contains general helper functions and global variables which can be shared between components/views.


The frontend application is written in react-typescript. The UI/UX is designed with MUI. We aim to build the application solely based on [MUI Joy-UI](https://mui.com/joy-ui/getting-started/overview/) and limit ourselves to using material ui in exceptions where there is not yet a solution with joy ui.

ScanHub-UI implements the following routes using the react-router-dom package (see `Routes.tsx`):

* patients
  * /patient-id/exam-id/procedure-id
* devices
* _workflows_
* dashboard/home

Database queries are performed using axios and an abstract-query-client implementation. The query clients can be found in the client directory.


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
