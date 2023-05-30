<p align="center">
  <a href="https://brain-link.de/wp-content/uploads/2022/03/ScanHub.svg"><img src="https://brain-link.de/wp-content/uploads/2022/03/ScanHub.svg" width="300" height="150" alt="ScanHub"></a>
</p>


[![build](https://github.com/brain-link/scanhub-ui/actions/workflows/build.yml/badge.svg?branch=main)](https://github.com/brain-link/scanhub-ui/actions/workflows/build.yml)
[![static-tests](https://github.com/brain-link/scanhub-ui/actions/workflows/static-tests.yml/badge.svg?branch=main)](https://github.com/brain-link/scanhub-ui/actions/workflows/static-tests.yml)

-----------------
  

## Demo :clapper:

https://user-images.githubusercontent.com/42237900/193445329-93d344d1-2587-4d99-abe0-332d3c63e66d.mp4
  
ScanHub is intended to be a multi modal acquisition software, which allows individualizable, modular and cloud-based processing of functional and anatomical medical images. 
It seamlessly merges the acquisition with the processing of complex data on a single platform.
ScanHub is open-source and freely availably to anyone :earth_africa:.

The greatest novalty of ScanHub is the cross-manufacturer and multi-modality aspect, allowing accessible cloud-based data processing in one framework :rocket:

Currently we are focussing on the development of an acquisition solution for the open-source MRI [OSI2One](https://www.opensourceimaging.org/2023/01/09/first-open-source-mri-scanner-presented-the-osii-one/).

This project only provides the user interface to interact with ScanHub. 
Check out the backbone of our acquisition platform :arrow_right: [ScanHub](https://github.com/brain-link/scanhub).

We welcome anyone who would like to join our mission, just [get in touch](mailto:info@brain-link.de) :email:.

Installation
------------

To install the package, you need install [Docker](https://docs.docker.com/engine/install/) first. 
The installation of ScanHub-UI is as simple as using the following command.

    docker-compose up -d --build
    
Note that you need to install [ScanHub](https://github.com/brain-link/scanhub), which is the backbone of the user interface.
Documentation on the installation of scanhub can be found in the README file.

Structural Overview
-----------

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

ScanHub is **BSD-licenced** (3 clause):

    Copyright (c) 2021-2022, authors of ScanHub. All rights reserved.

    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions are met:

    1. Redistributions of source code must retain the above copyright notice, this
       list of conditions and the following disclaimer.

    2. Redistributions in binary form must reproduce the above copyright notice,
       this list of conditions and the following disclaimer in the documentation
       and/or other materials provided with the distribution.

    3. Neither the name of the copyright holder nor the names of its
       contributors may be used to endorse or promote products derived from
       this software without specific prior written permission.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
    AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
    IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
    DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
    FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
    DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
    SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
    CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
    OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
    OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
