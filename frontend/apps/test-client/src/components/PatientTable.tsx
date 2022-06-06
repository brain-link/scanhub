import { NavLink } from 'react-router-dom'
import { graphql, useLazyLoadQuery } from 'react-relay'
import type { PatientTableQuery } from './__generated__/PatientTableQuery.graphql'

import { Link, useParams } from 'react-router-dom'
import React from 'react'

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

// const query = graphql`
//   query PatientTableQuery {
//     allPatients {
//       id
//       sex
//       birthday
//       concern
//       admissionDate
//       status
//     }
//   }
// `

// export function PatientTable() {
//   const { allPatients } = useLazyLoadQuery<PatientTableQuery>(query, {}, {})
//   return (
//     <>
//       <label>
//         <input type='search' />
//       </label>
//       <table className='grow col-4'>
//         <thead>
//           <tr>
//             <th><input type='checkbox' /></th>
//             <th>ID</th>
//             <th>Sex <span className='fa fa-arrow-down' /></th>
//             <th>Birthday</th>
//           </tr>
//         </thead>
//         <tbody>
//           {allPatients.map(patient => (
//             <tr key={patient.id}>
//               <td><input type='checkbox' /></td>
//               <td><Link to={patient.id}>{patient.id}</Link></td>
//               <td>{patient.sex}</td>
//               <td>{patient.birthday}</td>
//             </tr>
//           ))}
//         </tbody>
//       </table>
//     </>
//   )
// }

export interface Patient {
  id: number;
  sex: string;
  birthday: number;
  concern: string;
  admission_date: number;
  status: string;
}

export function PatientTable() {
  // const { allPatients } = useLazyLoadQuery<PatientTableQuery>(query, {}, {})

  export function User() {
    let params = useParams();
  
    let [loading, setLoading] = React.useState(true);
    let [patient, setPatient] = React.useState<Patient | null>(null);
  
    React.useEffect(() => {
      setLoading(true);
      const fetchData = async () => {
        const response = await fetch(`http://localhost:8000/patients/${params.id}`);
        const newData = await response.json();
        setPatient(newData);
        setLoading(false);
      };
  
      fetchData();
    }, []);

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
          {allPatients.map(patient => (
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
