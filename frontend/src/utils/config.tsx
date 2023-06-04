// Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
// SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

// Configuration file for the frontend

const config = {
    baseURL: "http://localhost:8000",
    tools: {
        configuration: 'config',
        dataview: 'view'
    },
    // dicomSample: "dicomweb://raw.githubusercontent.com/Anush-DP/gdcmdata/master/MR-SIEMENS-DICOM-WithOverlays.dcm",
    // dicomSample1: "dicomweb:https://marketing.webassets.siemens-healthineers.com/1800000000016144/8de2b3a4af48/IMA08_1800000000016144.IMA",
    // dicomSample2: "dicomweb:https://marketing.webassets.siemens-healthineers.com/1800000000034108/3320b98db24a/IMA01_1800000000034108.IMA",
    // dicomSample: "wadouri:http://localhost:8043/wado?objectUID=1.2.826.0.1.3680043.2.1125.1.43099495893956056717571214082434568&requestType=WADO&contentType=application%2Fdicom",
    dicomSample: "dicomweb:http://localhost:8042/wado?objectUID=1.3.12.2.1107.5.2.30.10003.30000008070707384689000000409&requestType=WADO&contentType=application%2Fdicom",
};

export default config;

