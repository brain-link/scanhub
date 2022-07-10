import { Outlet, Link, useParams } from 'react-router-dom';
import { useState } from 'react';
import { w3cwebsocket as W3CWebSocket } from 'websocket';
import { useMutation, useQuery } from 'react-query';
import { Record } from './Interfaces';
import { format_date } from '../utils/formatter';
import { MRIView } from './MRIView';
import { SequenceForm } from './SequenceHandler';
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
  CLink,
  CFormInput,
  CCloseButton,
} from '@coreui/react'


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
              <CListGroupItem component={Link} to={`r-${record.id}`}>
                  <div className="d-flex w-100 justify-content-between">
                    <h5 className="mb-1">Recording {record.id}</h5>
                    <DeleteWarning record_id={record.id} />
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
            <NewRecord />
          </CCol>
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

function DeleteWarning({record_id}) {
  let params = useParams()
  const [visible, setVisible] = useState(false)
  const deletePost = async () => {
    return await axios.delete(`http://localhost:8000/patients/${params.patientId}/${params.procedureId}/records/${record_id}/`);
  }
  return (
    <>
      <CCloseButton onClick={ () => setVisible(!visible) }/>
      <CModal visible={visible} onClose={() => setVisible(false)}>
        <CModalHeader>
          <CModalTitle>Delete Record</CModalTitle>
        </CModalHeader>
        <CModalBody>
          <p>
            You are about to delete record { record_id }, are you sure that you want to proceed?
          </p>
          <CButton
            color='danger'
            variant='outline'
            onClick={ () => {deletePost(); setVisible(false)}  }
          > Confirm Delete </CButton>
        </CModalBody>

      </CModal>
    </>
  )
}

export function NewRecord() {

  let params = useParams()
  let procedure = parseInt(params.procedureId ? params.procedureId : "0");

  const [data, setData] = useState<Record>({ id: 0, procedure_id: procedure, device_id: 1, date: "", thumbnail: "", data: "", comment: "String value" })
  const [visible, setVisible] = useState(false)

  const handleChange = (event) => {
    setData({
      ...data,
      [event.target.name]: event.target.value
    })
  }
  
  const mutation = useMutation(async() => {
    return await axios.post(`http://localhost:8000/patients/${params.patientId}/${params.procedureId}/records/new/`, data)
    .catch( (error) => { console.log(error) });
  })

  return (
    <>
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
              placeholder={ data.comment }
              text="This is a brief comment on the record."
              onChange={ handleChange }/>
            {/* <CFormInput 
              id="floatingInputValue" 
              name="thumbnail"
              label="Thumbnail"
              placeholder={ data.thumbnail } 
              onChange={ handleChange }/> */}
          </CForm>
        </CModalBody>
        <CModalFooter>
          {/* <CButton color="secondary" onClick={ () => setVisible(false) }>Close</CButton> */}
          <CButton color="primary" onClick={ () => { mutation.mutate(); setVisible(false) }}>Save</CButton>
        </CModalFooter>
      </CModal>
    </>
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
        <ProcedureSidebar />
      </CCol>
      <CCol md={9}>
        <Outlet />
      </CCol>
    </CRow>
  </>
  )
}