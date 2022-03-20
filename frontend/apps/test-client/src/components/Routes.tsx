import { Link, Route, Routes, useParams } from 'react-router-dom'
import { PatientTable } from './PatientTable'
import { Navigation } from './NavBar'
import { Procedure, ProcedureMainContent, ProcedureMainContentSwitcher } from './Procedure'
import { version } from '../version'


function Patients() {
  return (
    <section className='grow flex-col gap-3'>
      <h1>Patients:</h1>
      <PatientTable />
    </section>
  )
}

function Patient() {
  const { patientId } = useParams()
  return (
    <section>
      <h1>{patientId}</h1>
      <p>
        <Link to='procedure-1'>Procedure 1</Link>
      </p>
    </section>
  )
}

function Docs() {
  return (
    <section>
      <h1>ScanHub Documentation v{version}</h1>
      <p>
        Under construction ...
      </p>
    </section>
  )
}

function Devices() {
  return (
    <section>
      <h1>My Devices</h1>
      <p>
        <ul>
          <li>register new devices</li>
          <li>configure existing devices</li>
          <li>remove existing devices</li>
        </ul>
      </p>
    </section>
  )
}

function NotFound() {
  return (
    <section>
      <h1>Resource Not Found</h1>
      <p>Please check the url path.</p>
    </section>
  )
}

export function RouteConfig() {
  return (
    <Routes>
      <Route path='/' element={<Navigation />}>
        <Route path='docs' element={<Docs />} />
        <Route path='devices' element={<Devices />} />
        <Route path='patients'>
          <Route index element={<Patients />} />
          <Route path=':patientId'>
            <Route index element={<Patient />} />
            <Route path=':procedureId' element={<Procedure />}>
              <Route path=':recordingId' element={<ProcedureMainContentSwitcher />}>
                <Route index element={<ProcedureMainContent />} />
                <Route path=':modality' element={<ProcedureMainContent />} />
              </Route>
            </Route>
          </Route>
        </Route>
        <Route path='*' element={<NotFound />} />
      </Route>
    </Routes>
  )
}
