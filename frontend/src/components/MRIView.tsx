import React, { Component } from 'react'

import CornerstoneViewport from "react-cornerstone-viewport"
import * as cornerstone from "cornerstone-core";
import * as cornerstoneMath from "cornerstone-math";
import * as cornerstoneTools from "cornerstone-tools";
import Hammer from "hammerjs";

import dicomParser from "dicom-parser";
import cornerstoneWADOImageLoader from "cornerstone-wado-image-loader";
// import * as cornerstoneWebImageLoader from "cornerstone-web-image-loader";


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

// export function MRIView() {
export class MRIView extends Component {
    render() {
        return (
            <CornerstoneViewport
                imageIds={[
                    // "wadouri:http://localhost:8043/wado?objectUID=1.2.826.0.1.3680043.2.1125.1.43099495893956056717571214082434568&requestType=WADO&contentType=application%2Fdicom"
                    "dicomweb://raw.githubusercontent.com/Anush-DP/gdcmdata/master/MR-SIEMENS-DICOM-WithOverlays.dcm"
                    // "https://rawgit.com/cornerstonejs/cornerstoneWebImageLoader/master/examples/Renal_Cell_Carcinoma.jpg"
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
                style={{ minWidth: "100%", height: "512px", flex: "1" }}
            />
        )
    }
}
