// Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
// SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

// MRIView.tsx is responsible for rendering the MRI view of the patient view.

import * as React from 'react';

import CornerstoneViewport from "react-cornerstone-viewport"
import * as cornerstone from "cornerstone-core";
import * as cornerstoneMath from "cornerstone-math";
import * as cornerstoneTools from "cornerstone-tools";
import Hammer from "hammerjs";
import axios from 'axios';

import dicomParser from "dicom-parser";
import cornerstoneWADOImageLoader from "cornerstone-wado-image-loader";
// import * as cornerstoneWebImageLoader from "cornerstone-web-image-loader";
import Container from '@mui/joy/Container';
import CircularProgress from '@mui/joy/CircularProgress';
import config from '../../../utils/config';
import { useParams } from 'react-router-dom';

cornerstoneTools.external.cornerstone = cornerstone;
cornerstoneTools.external.Hammer = Hammer;
cornerstoneTools.external.cornerstoneMath = cornerstoneMath;

//
cornerstoneTools.init({
  mouseEnabled: true,
  touchEnabled: true,
  globalToolSyncEnabled: true,
  showSVGCursors: true
});
localStorage.setItem("debug", "cornerstoneTools");

// Preferences
// const fontFamily =
//   "Work Sans, Roboto, OpenSans, HelveticaNeue-Light, Helvetica Neue Light, Helvetica Neue, Helvetica, Arial, Lucida Grande, sans-serif";
// cornerstoneTools.textStyle.setFont(`16px ${fontFamily}`);

cornerstoneTools.toolStyle.setToolWidth(2);
cornerstoneTools.toolColors.setToolColor("rgb(255, 255, 255)");
cornerstoneTools.toolColors.setActiveColor("rgb(255, 255, 255)");

cornerstoneTools.store.state.touchProximity = 40;

//  cornerstoneTools.addTool(MyCustomTool);
cornerstoneTools.setToolActive("MyCustom", { mouseButtonMask: 1 });

const OverlayTool = cornerstoneTools.OverlayTool;
cornerstoneTools.addTool(OverlayTool);
cornerstoneTools.setToolEnabled("Overlay", {});


// IMAGE LOADER
// cornerstoneWebImageLoader.external.cornerstone = cornerstone;

cornerstoneWADOImageLoader.external.cornerstone = cornerstone;
cornerstoneWADOImageLoader.external.dicomParser = dicomParser;
cornerstoneWADOImageLoader.webWorkerManager.initialize({
  maxWebWorkers: navigator.hardwareConcurrency || 1,
  startWebWorkersOnDemand: true,
  taskConfiguration: {
    decodeTask: {
      initializeCodecsOnStartup: true,
      usePDFJS: true,
      strict: true
    }
  }
});

export function MRIView() {

    const params = useParams();
    const [dataUrl, setDataUrl] = React.useState<String | null>(null);

    async function get_record_data() {
        await axios.get(`${config.baseURL}/records/${params.procedureId}`)
        .then((response) => {
            console.log("Response from record fetch in MRIView: ", response.data.data.toString())
            setDataUrl(response.data.data ? response.data.data.toString() : null)
        })
        .catch((err) => {console.log(err)})
    }
    
    React.useEffect(() => {
        get_record_data();
        console.log(dataUrl);
    }, [])

    if (!dataUrl) {
        <Container maxWidth={false} sx={{ width: '50%', mt: 5, justifyContent: 'center' }}>
            {/* <Typography>Loading patients...</Typography> */}
            {/* <LinearProgress /> */}
            <CircularProgress />
        </Container>
    }
    
        
    return (
        <CornerstoneViewport
            imageIds={[
                // config.dicomSample1,
                // config.dicomSample2
                `dicomweb:${dataUrl}`
            ]}
            tools={[
                // Mouse
                {
                    name: 'Wwwc',
                    mode: 'active',
                    modeOptions: { mouseButtonMask: 1 },
                },
                {
                    name: 'Zoom',
                    mode: 'active',
                    modeOptions: { mouseButtonMask: 2 },
                },
                {
                    name: 'Pan',
                    mode: 'active',
                    modeOptions: { mouseButtonMask: 4 },
                },
                // Scroll
                { name: 'StackScrollMouseWheel', mode: 'active' },
                // Touch
                { name: 'PanMultiTouch', mode: 'active' },
                { name: 'ZoomTouchPinch', mode: 'active' },
                { name: 'StackScrollMultiTouch', mode: 'active' },
            ]}
            style={{ minWidth: "100%", height: "100%", flex: "1" }}
        />
    )
}

export default MRIView;