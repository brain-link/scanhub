// Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
// SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

// Custom hook for health check

import { useState, useEffect } from 'react'

function useHealthCheck(url: string, interval: number = 5000) {
  const [isReady, setIsReady] = useState(false)

  useEffect(() => {
    const intervalId = setInterval(() => {
      fetch(`${url}/health/readiness`)
        .then((response) => {
          response.status === 200 ? setIsReady(true) : setIsReady(false)
        })
        .catch(() => setIsReady(false))
    }, interval)

    return () => clearInterval(intervalId)
  }, [url, interval])

  return isReady
}

export default useHealthCheck
