.. Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
   SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

ScanHub Documentation
#####################

Welcome to the online documentation of ScanHub, an open-source multimodal acquisition platform dedicated to workflows of medical imaging. Focusing prominently on MRI technology, ScanHub addresses the nuanced challenges of image acquisition, processing, and sharing by seamlessly integrating cloud-based solutions.

Developed in response to the challenges in traditional MRI infrastructure, such as scalability, cost-efficiency, and collaborative limitations, ScanHub emerges as a solution, ensuring the management and utilization of MRI data. By relocating image reconstruction and storage to the cloud, it not only aims to reduce associated costs but also enhances scalability and collaboration across various spectrums of MRI research and clinical applications.

Getting started
---------------


.. grid:: 2
   :gutter: 3

   .. grid-item-card:: Demo Guide

      If you are interested in trying ScanHub, these are the instructions to guide you through setting up scanhub.

      .. button-ref:: demo-guide
         :expand:
         :color: primary
         :click-parent:

         Go to demo guide

   .. grid-item-card:: Technical Documentation

      Within the development of ScanHub, also the technical documentation for future MDR certification is addressed.
      The documentation is work in progress, yet it provides a good overview of the functional scope.

      .. button-ref:: tech-doc
         :expand:
         :color: primary
         :click-parent:

         Go to tech docs

   .. grid-item-card:: Web API

      ScanHub is a cloud-native, microservice-based acquisition platform. 
      All the microservices have a REST api to communicate with each other.
      A description and documentation of these endpoints, which can also be accessed via OpenAPI docs, can be found here.

      .. button-ref:: web-api
         :expand:
         :color: primary
         :click-parent:

         Go to web api

   .. grid-item-card:: Code Reference

      This part contains all the auto-generated code documentation which is collected from all the different microservices.

      .. button-ref:: source-code
         :expand:
         :color: primary
         :click-parent:

         Go to code documentation


.. toctree::
   :maxdepth: 1

   introduction/index
   demo
   techdoc/index
   api/index
   sourcecode/index


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
