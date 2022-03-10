import { useMemo, useState } from 'react'
import { graphql, useSubscription } from 'react-relay'
import type { CounterSubscription } from './__generated__/CounterSubscription.graphql'

const subscription = graphql`
  subscription CounterSubscription($upto: Int!) {
    data(upto: $upto) {
      id
      sex
      birthday
      concern
      admissionDate
      status
    }
  }
`

export function Counter() {
  const [upto, setUpto] = useState(10)
  useSubscription<CounterSubscription>(
    useMemo(
      () => ({
        subscription,
        variables: { upto },
        onNext: (p) => console.log('Next.', p),
        onCompleted: () => console.log('Completed.'),
      }),
      [upto]
    )
  )
  return (
    <div>
      <input type='number' value={upto} onChange={ev => setUpto(ev.target.valueAsNumber)} />
    </div>
  )
}
