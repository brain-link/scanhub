import { Outlet, Link, useParams } from 'react-router-dom';
import { useState } from 'react';
import { w3cwebsocket as W3CWebSocket } from 'websocket';
import { useMutation } from 'react-query';
import { Record } from './Interfaces';
import { format_date } from '../utils/formatter';
import { MRIView } from './MRIView';
import { SequenceForm } from './SequenceHandler';
import { DeleteWarning } from './DeleteContext';
import axios from 'axios';
import React from 'react';
import {
  CCard,
  CCol,
  CListGroup,
  CListGroupItem,
  CRow,
  CCardBody,
  CNav,
  CNavItem,
  CModal,
  CModalBody,
  CModalHeader,
  CModalFooter,
  CModalTitle,
  CNavLink,
  CButton,
  CCardHeader,
  CForm,
  CFormInput
} from '@coreui/react'

const baseURL = "http://localhost:8000/";


const client = new W3CWebSocket('ws://localhost:8000/ws/1234');

client.onopen = () => {
  console.log('WebSocket Client Connected');
};
client.onmessage = (message) => {
  console.log(message);
};


async function startRecording() {
  await fetch(
    'http://localhost:81/api/TriggerAcquisition?cmd=MEAS_START',
    {
      mode: 'no-cors',
    }
  )
}

export function RecordsTable() {

  let params = useParams()

  const [record, setRecord] = React.useState<Record>({ id: 0, procedure_id: 0, device_id: 0, date: "", thumbnail: "", data: "", comment: "" });
  const [records, setRecords] = React.useState<Record[] | undefined >(undefined);
  const [visible, setVisible] = React.useState(false);
  const [activeKey, setActiveKey] = React.useState<Number | undefined>(undefined);

  // Function to fetch all records
  async function fetchRecords() {
    await axios.get(`${baseURL}patients/${params.patientId}/${params.procedureId}/records/`)
    .then((response) => {setRecords(response.data)})
  }

  // Fetch records
  React.useEffect(() => {
    fetchRecords()
  }, []);

  // Post a new record and refetch records table
  const mutation = useMutation(async() => {
    await axios.post(`${baseURL}patients/${params.patientId}/${params.procedureId}/records/new/`, record)
    .then((response) => {
      setRecord(response.data) // required?
      fetchRecords()
    })
    .catch((err) => {
      console.log(err)
    })
  })

  if (!records) {
    return <div> Loading ... </div>
  }

  return (
    // <div className='grow flex-col scroll-y'>
    <>
    
    {/* Records table */}

    <CCard className='grow flex-col scroll-y'>
      <CCardHeader className="h5">Records</CCardHeader>
      <CCardBody>
        <CListGroup>
          {
            records?.map(record => (
              // <CListGroupItem component='a' to={`record-${record.id}`}>
              <CListGroupItem component={Link} to={`r-${record.id}`} 
                active={activeKey===record.id}
                onClick={() => setActiveKey(record.id)}>
                
                  <div className="d-flex w-100 justify-content-between">
                    <h5 className="mb-1">Recording {record.id}</h5>
                    <DeleteWarning 
                      contextURL={`http://localhost:8000/patients/${params.patientId}/${params.procedureId}/records/${record.id}/`}
                      onClose={ fetchRecords() }/>
                  </div>
                  <p className="mb-1"> {record.comment} </p>
                  <div className="d-flex w-100 justify-content-between">
                    <small>Device ID: {record.device_id}</small>
                    <small> { format_date(record.date) } </small>
                  </div>
              </CListGroupItem>
            ))
          }
        </CListGroup>
        
        <CRow className="mt-2">
          <CCol>

            {/* Modal to create a new record */}

            <CButton 
              color="primary" 
              onClick={() => setVisible(!visible)}
              variant="outline"
            >
              New Record
            </CButton>
            <CModal visible={visible} onClose={() => setVisible(false)}>
              <CModalHeader>
                <CModalTitle>Create New Record</CModalTitle>
              </CModalHeader>
              <CModalBody>
                <CForm>
                  <CFormInput
                    id="floatingInputValue"
                    name="comment"
                    label="Comment" 
                    placeholder={ record.comment }
                    text="This is a brief comment on the record."
                    onChange={ (e) => setRecord({...record, [e.target.name]: e.target.value}) }/>

                  {/* <CFormInput 
                    id="floatingInputValue" 
                    name="thumbnail"
                    label="Thumbnail"
                    placeholder={ data.thumbnail } 
                    onChange={ handleChange }/> */}

                </CForm>
              </CModalBody>
              <CModalFooter>
                <CButton color="primary" onClick={ () => { mutation.mutate(); setVisible(false) }}>Save</CButton>
              </CModalFooter>
            </CModal>

          </CCol>

          {/* Record button */}

          <CCol>
            <CButton 
              color="danger" 
              variant = "outline"
              onClick={() => { startRecording() }}
              >
                Record 
            </CButton>
          </CCol>
        </CRow>
    
      </CCardBody>
    </CCard>
    </>
    // </div>
  )
}

export function ProcedureMainContentSwitcher() {

  let params = useParams()

  const [activeKey, setActiveKey] = useState(1)

  return (
    <CCard>
      <CCardHeader className="h5"> Record { params.recordingId }</CCardHeader>
      <CCardBody>

        <CNav variant='pills' className='mb-2'>
          <CNavItem>
            <CNavLink 
              to='view-mri' 
              component={Link} 
              active={activeKey === 1} 
              onClick={() => setActiveKey(1)}>
                View
            </CNavLink>
          </CNavItem>
          <CNavItem>
            <CNavLink 
              to='sequence' 
              component={Link} 
              active={activeKey === 2} 
              onClick={() => setActiveKey(2)}>
                Sequence
            </CNavLink>
          </CNavItem>
        </CNav>

        <Outlet />

      </CCardBody>
    </CCard>
  )
}

export function ProcedureMainContent() {
  const {content} = useParams()

  console.log(content)

  switch(content) {
    case 'view-mri': return <MRIView />
    case 'sequence': return <SequenceForm />
    default: return <></>
  }
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
        <RecordsTable />
      </CCol>
      <CCol md={9}>
        <Outlet />
      </CCol>
    </CRow>
  </>
  )
}