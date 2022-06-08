import { NavLink } from 'react-router-dom'
import { graphql, useLazyLoadQuery } from 'react-relay'
import type { PatientTableQuery } from './__generated__/PatientTableQuery.graphql'

import { Link, useParams } from 'react-router-dom'
import React, { useEffect, useState } from 'react'

import {
  CTable,
  CTableBody,
  CTableDataCell,
  CTableHead,
  CTableRow,
  CTableHeaderCell,
  CBadge,
  CNavLink,
} from '@coreui/react'


export const getPatients = async () => {

  const response = await fetch("http://localhost:8000/patients/");

  const data = await response.json();

  if (data.patients) {
    return data.patients;
  }

  return Promise.reject('Failed to get patients from backend');
};


export function PatientTable() {

  const [patients, setPatients] = useState([])

  const get_patients = async () => {
    try {
      const request = await getPatients();
      setPatients(request)
    }
    catch(err) {
      console.log(err);
    }
  }

  useEffect(() => {
    get_patients()
  }, [])

  return (
    <>
      <CTable hover borderless>
        <CTableHead color='dark'>
          <CTableRow>
            <CTableHeaderCell scope="col">ID</CTableHeaderCell>
            <CTableHeaderCell scope="col">Sex <span className='fa fa-arrow-down' /></CTableHeaderCell>
            <CTableHeaderCell scope="col">Birthday</CTableHeaderCell>
            <CTableHeaderCell scope="col"><input type='checkbox' /></CTableHeaderCell>
          </CTableRow>
        </CTableHead>
        <CTableBody>
          {patients.map(patient => (
            <CTableRow key={patient.id}>
              <CTableHeaderCell scope="row">
              {/* <CBadge color="light" size='sm' className='w-25'>
                <CNavLink to={patient.id} component={NavLink}>{patient.id}</CNavLink>
              </CBadge> */}
              <CNavLink to={patient.id} component={NavLink}>{patient.id}</CNavLink>
              </CTableHeaderCell>
              <CTableDataCell>{patient.sex}</CTableDataCell>
              <CTableDataCell>{patient.birthday}</CTableDataCell>
              <CTableDataCell><input type='checkbox' /></CTableDataCell>
            </CTableRow>
          ))}
        </CTableBody>
      </CTable>
    </>
  )
}
