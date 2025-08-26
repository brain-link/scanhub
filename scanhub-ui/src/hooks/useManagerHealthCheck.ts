/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * useManagerHealthcheck.tsx contains a generalized hook for manager health checks
 */
import React from 'react'
import { useQuery } from '@tanstack/react-query';
import { useRef } from 'react';
import NotificationContext from '../NotificationContext'

type HealthFn<T> = () => Promise<T>;


export function useManagerHealthCheck<T>(
	key: string,
  apiFn: HealthFn<T>,
  serviceName: string
) {

	const [, showNotification] = React.useContext(NotificationContext)
  const prevError = useRef(false);

  const query = useQuery({
    queryKey: [key],
    queryFn: apiFn,
    refetchInterval: 5000,
    retry: 0,
  });

  React.useEffect(() => {
		// Connection lost
		if (query.isError && !prevError.current) {
      showNotification({
        message: `Connection lost to ${serviceName}.`,
        type: 'warning',
      });
    }
		// Reconnected
    if (query.isSuccess && (query.data as any)?.status === 'ok' && prevError.current) {
      showNotification({
        message: `Reconnected to ${serviceName} after connection loss.`,
        type: 'success',
      });
    }

    prevError.current = query.isError;
  }, [query.isSuccess, query.isError, query.data]);

  return {
    ...query,
    isHealthy: query.isSuccess && (query.data as any)?.status === 'ok',
  };
}
