import dicomParser from "dicom-parser";
import cornerstone from "cornerstone-core";
import cornerstoneWADOImageLoader from "cornerstone-wado-image-loader";
import cornerstoneMath from "cornerstone-math";
import cornerstoneTools from "cornerstone-tools";
import Hammer from "hammerjs";
//import MyCustomTool from "./custom_tool";

export default function initCornerstone() {
  // Cornertone Tools
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
  const fontFamily =
    "Work Sans, Roboto, OpenSans, HelveticaNeue-Light, Helvetica Neue Light, Helvetica Neue, Helvetica, Arial, Lucida Grande, sans-serif";
  cornerstoneTools.textStyle.setFont(`16px ${fontFamily}`);
  cornerstoneTools.toolStyle.setToolWidth(2);
  cornerstoneTools.toolColors.setToolColor("rgb(255, 255, 0)");
  cornerstoneTools.toolColors.setActiveColor("rgb(0, 255, 0)");

  cornerstoneTools.store.state.touchProximity = 40;

//  cornerstoneTools.addTool(MyCustomTool);
  cornerstoneTools.setToolActive("MyCustom", { mouseButtonMask: 1 });

  const OverlayTool = cornerstoneTools.OverlayTool;
  cornerstoneTools.addTool(OverlayTool);
  cornerstoneTools.setToolEnabled("Overlay", {});

  // IMAGE LOADER
  cornerstoneWADOImageLoader.external.cornerstone = cornerstone;
  cornerstoneWADOImageLoader.external.dicomParser = dicomParser;
  cornerstoneWADOImageLoader.webWorkerManager.initialize({
    maxWebWorkers: navigator.hardwareConcurrency || 1,
    startWebWorkersOnDemand: true,
    taskConfiguration: {
      decodeTask: {
        initializeCodecsOnStartup: false,
        usePDFJS: false,
        strict: false
      }
    }
  });

  // Debug
  window.cornerstone = cornerstone;
  window.cornerstoneTools = cornerstoneTools;
}
