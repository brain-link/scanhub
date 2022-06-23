import { Outlet, Link, useParams } from 'react-router-dom'
import { w3cwebsocket as W3CWebSocket } from 'websocket';
import { useQuery } from 'react-query';
import { Record } from './Interfaces';
import { format_date } from '../utils/formatter';

import { MRIView } from './MRIView';

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
          color="danger" 
          className="mt-2"
          size="lg"
          variant = "outline"
          onClick={() => {
            startRecording()
          }}
          >
            Record 
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

export function ProcedureMainContent() {
  let params = useParams()

  return (
    <>
    <CCard>
      <CCardHeader className="h5"> Record { params.recordingId }</CCardHeader>
      <CCardBody>

        < MRIView />

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