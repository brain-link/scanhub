import { useParams } from 'react-router-dom';
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
  CLink,
  CFormInput,
  CModalFooter,
  CCloseButton, 
  CCardBody} from '@coreui/react';

import { useQuery, useMutation } from 'react-query';
import { Procedure, Patient } from './Interfaces';
import { useState } from 'react';
import React from 'react';
import axios from 'axios';


export function PatientIndex() {

  let params = useParams()

  const { data: procedures, isSuccess: procedureSuccess } = useQuery<Procedure[]>(`patients/${params.patientId}/procedures/`);
  const { data: patient, isSuccess: patientSuccess } = useQuery<Patient>(`patients/${params.patientId}/`);
  
  if (!procedureSuccess || !patientSuccess) {
    return <div> Loading ... </div>
  }

  return (
    <>
      <CRow className="m-2">
        <CCol xs={4}>
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
          <CCard>
            <CCardHeader className="h5">Procedures</CCardHeader>
            <CCardBody>
              <div className="mb-2 d-flex w-100 justify-content-start">
                <NewProcedure />
              </div>
              <CListGroup>
                {
                  procedures?.map(procedure => (
                    <CListGroupItem component={CLink} to={`${patient.id}/${procedure.id}`}>
                      <div className="d-flex w-100 justify-content-between">
                        <h5 className="mb-1">Procedure {procedure.id}</h5>
                        <DeleteWarning procedure_id={procedure.id} />
                      </div>
                      <small>{procedure.date}</small>
                      <p className="mb-1">
                        Description of the procedure, that contains information about the modalities, number of records, etc.
                      </p>
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

function DeleteWarning({procedure_id}) {
  let params = useParams()
  const [visible, setVisible] = useState(false)
  const deletePost = async () => {
    return await axios.delete(`http://localhost:8000/patients/${params.patientId}/${procedure_id}/`);
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
            You are about to delete procedure { procedure_id }, are you sure that you want to proceed?
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


function NewProcedure() {

  let params = useParams()
  let patient = parseInt(params.patientId ? params.patientId : "0");
  const [data, setData] = useState<Procedure>({ id: 0, patient_id: patient, reason: "", date: "" })
  const [visible, setVisible] = useState(false)

  const handleChange = (event) => {
    setData({
      ...data,
      [event.target.name]: event.target.value
    })
  }
  
  const mutation = useMutation(async() => {
    return await axios.post(`http://localhost:8000/patients/${params.patientId}/procedures/new/`, data)
    .catch( (error) => { console.log(error) });
  })

  return (
    <>
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
              placeholder={ data.reason }
              text="Please indicate the reason for the procedure."
              onChange={ handleChange }/>
          </CForm>
        </CModalBody>
        <CModalFooter>
          <CButton color="primary" onClick={ () => { mutation.mutate(); setVisible(false) }}>Save</CButton>
        </CModalFooter>
      </CModal>
    </>
  )
}