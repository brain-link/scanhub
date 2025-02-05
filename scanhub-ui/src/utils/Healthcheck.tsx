/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * Healthcheck.tsx contains a custom hook for health check
 */
import { useEffect, useState } from 'react'

function useHealthCheck(url: string, interval: number = 5000) {
  const [isError, setIsError] = useState(false)

  useEffect(() => {
    const intervalId = setInterval(() => {
      fetch(`${url}/health/readiness`)
        .then((response) => {
          response.status === 200 ? setIsError(false) : setIsError(true)
        })
        .catch(() => setIsError(true))
    }, interval)

    return () => clearInterval(intervalId)
  }, [url, interval])

  return isError
}

export default useHealthCheck
