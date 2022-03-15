import { useEffect, useState } from 'react'

function useTime(updateFrequencyMs: number) {
  const [time, setTime] = useState(new Date())
  useEffect(
    () => {
      const intervalId = setInterval(() => setTime(new Date()), updateFrequencyMs)
      return () => clearInterval(intervalId)
    },
    [updateFrequencyMs]
  )
  return time
}

export function Clock() {
  // even though we only show minutes, update is happening more often
  // so the minute switch happens timely
  const time = useTime(2000)
  const hours = time.getHours().toFixed(0).padStart(2, '0')
  const minutes = time.getMinutes().toFixed(0).padStart(2, '0')
  return (
    <time dateTime={time.toISOString()}>
      {hours}:{minutes}
    </time>
  )
}
