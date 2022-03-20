import { Link } from 'react-router-dom'
import { graphql, useLazyLoadQuery } from 'react-relay'
import type { PatientTableQuery } from './__generated__/PatientTableQuery.graphql'

const query = graphql`
  query PatientTableQuery {
    allPatients {
      id
      sex
      birthday
      concern
      admissionDate
      status
    }
  }
`

export function PatientTable() {
  const { allPatients } = useLazyLoadQuery<PatientTableQuery>(query, {}, {})
  return (
    <>
      <label>
        <input type='search' />
      </label>
      <table className='grow' style={{ ['--columns' as string]: 4 }}>
        <thead>
          <tr>
            <th><input type='checkbox' /></th>
            <th>ID</th>
            <th>Sex <span className='fa fa-arrow-down' /></th>
            <th>Birthday</th>
          </tr>
        </thead>
        <tbody>
          {allPatients.map(patient => (
            <tr key={patient.id}>
              <td><input type='checkbox' /></td>
              <td><Link to={patient.id}>{patient.id}</Link></td>
              <td>{patient.sex}</td>
              <td>{patient.birthday}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </>
  )
}
