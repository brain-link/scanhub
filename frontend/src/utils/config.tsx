const config = {
    baseURL: "http://localhost:8000",
    tools: {
        configuration: 'config',
        dataview: 'view'
    },
    // dicomSample: "https://www.dicomlibrary.com?requestType=WADO&studyUID=1.2.826.0.1.3680043.8.1055.1.20111103111148288.98361414.79379639&manage=02ef8f31ea86a45cfce6eb297c274598&token=8f71f81452d6b32ccfbd30431299809c",
    dicomSample: "dicomweb://raw.githubusercontent.com/Anush-DP/gdcmdata/master/MR-SIEMENS-DICOM-WithOverlays.dcm",
};

export default config;