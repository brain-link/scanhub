import { graphql, useLazyLoadQuery } from 'react-relay'
import { Counter } from './Counter'
import type { ClientQuery } from './__generated__/ClientQuery.graphql'
import Plot from 'react-plotly.js'
import { useMemo } from 'react'

const query = graphql`
  query ClientQuery {
    me {
      id
      name
      age
    }
    allPatients {
      id
      sex
      birthday
      concern
      admissionDate
      status
    }
    getPatient(id: 20) {
      id
      sex
      birthday
      concern
      admissionDate
      status
    }
  }
`

const layout = {}

function count<T>(list: readonly T[], what: (item: T) => string) {
  const counts = new Map<string, number>()
  list.forEach(item => {
    const key = what(item)
    counts.set(key, (counts.get(key) ?? 0) + 1)
  })
  return counts
}

export function Client() {
  const { me, allPatients, getPatient } = useLazyLoadQuery<ClientQuery>(query, {}, {})
  const bar: Plotly.Data[] = useMemo(
    () => [{
      x: allPatients.map((_, i) => i),
      y: allPatients.map(p => new Date(p.birthday).getTime() / 1000),
      type: 'bar',
    }],
    [allPatients]
  )
  const pie: Plotly.Data[] = useMemo(
    () => [{
      type: 'pie',
      ...((() => {
        const counts = count(allPatients, p => p.sex)
        return {
          labels: Array.from(counts.keys()),
          values: Array.from(counts.values()),
        }
      })()),
    }],
    [allPatients]
  )
  return (
    <div>
      {me ?
        <>
          <p>Hello {me.name} ({me.id})! Current age: {me.age}.</p>
          <p>Patient: { getPatient.sex } </p>
          <ul>
            {allPatients.map(patient => (
              <li key={patient.id}>{patient.id} {patient.sex} {patient.birthday} {patient.concern}</li>
            ))}
          </ul>
          <Counter />
          <Plot layout={layout} data={pie} />
          <Plot layout={layout} data={bar} />
        </>
        :
        <p>No user detected.</p>
      }
    </div>
  )
}
