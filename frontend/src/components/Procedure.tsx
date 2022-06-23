import { Outlet, Link, useParams } from 'react-router-dom'
// import { getModalityComponent } from './modalities'
import { w3cwebsocket as W3CWebSocket } from 'websocket';
import { useQuery } from 'react-query';
import { Record } from './Interfaces';
import { format_date } from '../utils/formatter';

import * as cornerstone from "cornerstone-core";
import * as cornerstoneMath from "cornerstone-math";
import * as cornerstoneTools from "cornerstone-tools";
import Hammer from "hammerjs";
import * as cornerstoneWebImageLoader from "cornerstone-web-image-loader";
import CVport from "react-cornerstone-viewport";

const client = new W3CWebSocket('ws://localhost:8000/ws/1234');

client.onopen = () => {
  console.log('WebSocket Client Connected');
};
client.onmessage = (message) => {
  console.log(message);
};

import {
  CCard,
  CCol,
  CListGroup,
  CListGroupItem,
  CRow,
  CCardBody,
  CCardImage,
  CCardText,
  CCardTitle,
  CNav,
  CNavItem,
  CContainer,
  CWidgetStatsB,
  CLink,
  CButton,
  CCardHeader,
} from '@coreui/react'

// async function startRecording() {
//   await fetch(
//     'http://localhost:81/api/TriggerAcquisition?cmd=MEAS_START',
//     {
//       mode: 'no-cors',
//     }
//   )
// }


async function startRecording() {
  await fetch(
    'http://localhost:81/api/TriggerAcquisition?cmd=MEAS_START',
    {
      mode: 'no-cors',
    }
  )
}

export function range(startStop: number, stop?: number, step?: number) {
  const start = stop !== undefined ? startStop : 0
  const stop_ = stop ?? startStop
  const step_ = step ?? 1
  const length = Math.floor((stop_ - start) / step_)
  return new Array(length).fill(0).map((_, i) => start + i * step_)
}

export function ProcedureSidebar() {

  let params = useParams()

  const { data: records, isSuccess } = useQuery<Record[]>(`patients/${params.patientId}/${params.procedureId}/records`)

  if (!isSuccess) {
    return <div>Loading ...</div>
  }

  return (
    // <div className='grow flex-col scroll-y'>
    <>
    <CCard className='grow flex-col scroll-y'>
      <CCardHeader className="h5">Records</CCardHeader>
      <CCardBody>
        <CListGroup>
          {
            records?.map(record => (
              // <CListGroupItem component='a' to={`record-${record.id}`}>
              <CListGroupItem component={Link} to={`record-${record.id}`}>
                <div className="d-flex w-100 justify-content-between">
                  <h5 className="mb-1">Recording {record.id}</h5>
                  <small> 
                    {/* <Date> {format_date(record.date)} </Date>  */}
                    { format_date(record.date) }
                  </small>
                </div>
                <p className="mb-1">
                  {record.comment}
                </p>
                <small>Device ID: {record.device_id}</small>
              </CListGroupItem>
            ))
          }
        </CListGroup>
        <CButton 
          color="info" 
          size="lg"
          variant = "outline"
          onClick={() => {
            // var input = "Testmessage"
            // client.send(input)
            startRecording()
          }}
          >
            Rec
        </CButton>
      </CCardBody>
    </CCard>
    </>
    // </div>
  )
}


export function ProcedureMainContentSwitcher() {
  return (
    <>
    <CNav variant='pills'>
      <CNavItem>
        {/* <CNavLink to='configure-mri' component={NavLink}>Config</CNavLink> */}
        {/* <CNavLink to='' component={NavLink}>Config</CNavLink> */}
      </CNavItem>
      <CNavItem>
        {/* <CNavLink to='dicom' component={NavLink}>View</CNavLink> */}
        {/* <CNavLink to='' component={NavLink}>View</CNavLink> */}
      </CNavItem>
    </CNav>
    <Outlet />
    </>
  )
}

// let imageIds = [
//   "dicomweb://raw.githubusercontent.com/Anush-DP/gdcmdata/master/MR-SIEMENS-DICOM-WithOverlays.dcm",
//   "dicomweb://s3.amazonaws.com/lury/PTCTStudy/1.3.6.1.4.1.25403.52237031786.3872.20100510032220.11.dcm",
//   "dicomweb://s3.amazonaws.com/lury/PTCTStudy/1.3.6.1.4.1.25403.52237031786.3872.20100510032220.12.dcm"
// ];

cornerstoneWebImageLoader.external.cornerstone = cornerstone;
cornerstoneTools.external.cornerstone = cornerstone;
cornerstoneTools.external.cornerstoneMath = cornerstoneMath;
cornerstoneTools.external.Hammer = Hammer;
cornerstoneTools.init();

export function ProcedureMainContent() {
  let params = useParams()

  // const Modality = getModalityComponent(modality ?? 'configure-mri')
  // if (recordingId === undefined) {
  //   throw new Error(`Error in routing, recordingId is undefined.`)
  // }
  // return (
  //   <Modality recordingId={recordingId} />
  // )
  return (
    <>
    <CCard>
      <CCardHeader className="h5"> Record { params.recordingId }</CCardHeader>
      <CCardBody>

        {/* MRI Viewer goes here */}
        {/* <CVport
          imageIds={imageIds}
          // tools={tools}
          style={{ minWidth: "100%", height: "512px", flex: "1" }}
        /> */}

        <CVport
              imageIds={[
                "https://rawgit.com/cornerstonejs/cornerstoneWebImageLoader/master/examples/Renal_Cell_Carcinoma.jpg"
              ]}
              style={{ minWidth: "100%", height: "512px", flex: "1" }}
            />

      </CCardBody>
    </CCard>
    </>
  )
}

export function Procedure() {
  let params = useParams()
  return (
    <>
    <CRow className="m-2">
      <CCol xs="auto" className="me-3 align-self-end">
        <h2> Patient { params.patientId } </h2> 
      </CCol>
      <CCol xs="auto" className="align-self-end">
        <h4> Procedure { params.procedureId } </h4>
      </CCol>
    </CRow>

    <CRow className='m-2'>
      <CCol md={3}>
        <ProcedureSidebar />
      </CCol>
      <CCol md={9}>
        <Outlet />
      </CCol>
    </CRow>
  </>
  )
}
