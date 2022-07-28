import { useParams, Link } from 'react-router-dom';
import {
  CListGroup,
  CListGroupItem,
  CBadge,
  CCol, 
  CRow, 
  CCard, 
  CCardHeader, 
  CModalBody,
  CModal,
  CModalTitle,
  CButton,
  CModalHeader,
  CForm,
  CFormInput,
  CModalFooter,
  CCardBody,
  CLink} from '@coreui/react';

import { useMutation } from 'react-query';
import { Procedure, Patient } from './Interfaces';
import { useState } from 'react';
import { DeleteWarning } from './DeleteContext';
import React from 'react';
import axios from 'axios';

const baseURL = "http://localhost:8000/";


export function PatientIndex() {

  let params = useParams()
  
  const [patient, setPatient] = React.useState<Patient | undefined>(undefined);
  // Is this single procedure variable necessary?
  const [procedure, setProcedure] = useState<Procedure>({ id: 0, patient_id: 0, reason: "", date: "" });
  const [procedures, setProcedures] = React.useState<Procedure[] | undefined>(undefined);
  const [visible, setVisible] = useState(false);

  // fetch procedures
  React.useEffect(() => {
    axios.get(`${baseURL}patients/${params.patientId}/procedures/`)
      .then((response) => {setProcedures(response.data)})
  }, []);

  // fetch patient
  React.useEffect(() => {
    axios.get(`${baseURL}patients/${params.patientId}/`)
      .then((response) => {setPatient(response.data)})
  }, []);

  const mutation = useMutation(async(e) => {
    // await axios.post(`http://localhost:8000/patients/${params.patientId}/procedures/new/`, procedure)
    await axios.post(`http://localhost:8000/patients/${params.patientId}/procedures/new/`, procedure)
    .then((response) => {
      
      setProcedure(response.data) // required?

      // Refetch all procedures and update state variable
      axios.get(`${baseURL}patients/${params.patientId}/procedures/`)
      .then((response) => { setProcedures(response.data) })

    })
    .catch((err) => {
      console.log(err)
    })
  })

  if (!procedures || !patient) {
    return <div> Loading ... </div>
  }

  return (
    <>
      <CRow className="m-2">
        <CCol xs={4}>

          {/* Patient information */}

          <CCard>
            <CCardHeader className="h5">Patient</CCardHeader>
            <CCardBody>
              <CListGroup>
                <CListGroupItem className="d-flex justify-content-between align-items-center">
                  <div>
                    <h6>ID</h6>
                    {patient?.id}
                  </div>
                </CListGroupItem>
                <CListGroupItem className="d-flex justify-content-between align-items-center">
                  <div>
                    <h6>Birthday</h6>
                    {patient?.birthday}
                  </div>
                </CListGroupItem>
                <CListGroupItem className="d-flex justify-content-between align-items-center">
                  <div>
                    <h6>Sex</h6>
                    {patient?.sex}
                  </div>
                </CListGroupItem>
                <CListGroupItem className="d-flex justify-content-between align-items-center">
                  <div>
                    <h6>Number of Procedures</h6>
                    <CBadge color="primary" shape="rounded-pill">
                      {procedures.length}
                    </CBadge>
                  </div>
                </CListGroupItem>
                <CListGroupItem className="d-flex justify-content-between align-items-center">
                  <div>
                    <h6>Concern</h6>
                    {patient?.concern}
                  </div>
                </CListGroupItem>
              </CListGroup>
            </CCardBody>
          </CCard>

        </CCol>

        <CCol xs={8}>

          {/* Procedure table */}

          <CCard>
            <CCardHeader className="h5">Procedures</CCardHeader>
            <CCardBody>
              <div className="mb-2 d-flex w-100 justify-content-start">

                {/* Model to create a new procedure */}

                <CButton 
                  color="primary" 
                  onClick={() => setVisible(!visible)}
                  variant="outline"
                >
                  New Procedure
                </CButton>
                <CModal visible={visible} onClose={() => setVisible(false)}>
                  <CModalHeader>
                    <CModalTitle>Create New Record</CModalTitle>
                  </CModalHeader>
                  <CModalBody>
                    <CForm>
                      <CFormInput
                        id="floatingInputValue"
                        name="reason"
                        label="Reason" 
                        placeholder={ procedure.reason }
                        text="Please indicate the reason for the procedure."
                        onChange={ (e) => setProcedure({...procedure, [e.target.name]: e.target.value}) }
                        />
                    </CForm>
                  </CModalBody>
                  <CModalFooter>
                    <CButton color="primary" onClick={ () => { mutation.mutate(); setVisible(false) }}>Save</CButton>
                  </CModalFooter>
                </CModal>

              </div>

              {/* List of procedures */}

              <CListGroup>
                {
                  procedures?.map(procedure => (
                    // TODO: Fix this Link-Component issue
                    <CListGroupItem component={Link} to={`${patient.id}/${procedure.id}`}>
                      <div className="d-flex justify-content-between">
                        <h5 className="mb-1">Procedure {procedure.id}</h5>
                        {/* TODO: Procedures cannot be deleted */}
                        <DeleteWarning contextURL={`http://localhost:8000/patients/${params.patientId}/${procedure.id}/`} />
                      </div>
                      <small>{procedure.date}</small>
                      <p className="mb-1">{procedure.reason}</p>
                    </CListGroupItem>
                  ))
                }
              </CListGroup>

            </CCardBody>
          </CCard>
        </CCol>
      </CRow>
    </>
  )
}
