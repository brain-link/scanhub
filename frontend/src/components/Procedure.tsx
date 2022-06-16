import { Link, NavLink, Outlet, useParams } from 'react-router-dom'
// import { getModalityComponent } from './modalities'
import { w3cwebsocket as W3CWebSocket } from "websocket";

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
} from '@coreui/react'

// async function startRecording() {
//   await fetch(
//     'http://localhost:81/api/TriggerAcquisition?cmd=MEAS_START',
//     {
//       mode: 'no-cors',
//     }
//   )
// }

export function range(startStop: number, stop?: number, step?: number) {
  const start = stop !== undefined ? startStop : 0
  const stop_ = stop ?? startStop
  const step_ = step ?? 1
  const length = Math.floor((stop_ - start) / step_)
  return new Array(length).fill(0).map((_, i) => start + i * step_)
}

export function ProcedureSidebar() {
  let params = useParams()
  return (
    // <div className='grow flex-col scroll-y'>
    <>
      { range(50).map(i => (

          // <Link key={i} to={`mri-recording-${i}`}>
          //   <section className='flex'>
          //     <CCard className='mb-2' style={{ maxWidth: '500px' }}>
          //       <CRow className="g-0">
          //         <CCol md={4}>
          //         <CCardImage component="svg" orientation="top" width="100%" height="100" role="img" aria-label="Placeholder">
          //           <title>Placeholder</title><rect width="100%" height="100%" fill="#868e96"></rect>
          //         </CCardImage>
          //         </CCol>
          //         <CCol md={8}>
          //           <CCardBody>
          //             <CCardTitle>MRI Exam {i+1}</CCardTitle>
          //             <CCardText>Exam description</CCardText>
          //           </CCardBody>
          //         </CCol>
          //       </CRow>
          //     </CCard>
          //   </section>
          // </Link>

        <CWidgetStatsB
          className="mb-3"
          progress={{ color: 'success', value: 100/(i+1) }}
          title="MRI Examination"
          text="Some description of the recording."
          value={
            <CLink to={`record-${i}`} component={ Link }> Record {i} </CLink>
          }
        /> )) 
      } 
    </>
    // </div>
  )
}


export function ProcedureMainContentSwitcher() {
  return (
    <>
      <CNav variant='pills' className='mb-2'>
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
    <CContainer>
      <h1> Recording: { params.recordingId } </h1>
      <CButton 
        color="primary" 
        size="lg"
        onClick={() => {
          var input = "Testmessage"
          client.send(input)
        }}
        >
          START SCAN
      </CButton>
    </CContainer>
  )
}

export function Procedure() {
  let params = useParams()
  return (
    <>
      <CRow CRow className='m-2'>
        <h1> Patient { params.patientId } </h1> 
        <h2> Procedure { params.procedureId } </h2>
      </CRow>
      <CRow className='m-2'>
        <CCol md={3}>
          <ProcedureSidebar />
        </CCol>
        <CCol md={9}>
          <CCard className='grow'>
            <Outlet />
          </CCard> 
        </CCol>
      </CRow>
    </>
  )
}
