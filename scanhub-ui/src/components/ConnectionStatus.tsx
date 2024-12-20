
/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * ConnectionStatus.tsx checks the connection to the backend services and displays either a small button that indicates the status or a full overview page.
 */
import React, { useContext } from 'react'
import { useQuery } from 'react-query'
import { useNavigate } from 'react-router-dom';

import IconButton from '@mui/joy/IconButton'
import LanIcon from '@mui/icons-material/Lan';
import Typography from '@mui/joy/Typography'
import Box from '@mui/joy/Box';

import {
  patientManagerHealthApi,
  examManagerHealthApi,
  workflowManagerHealthApi,
  userLoginManagerHealthApi,
  deviceManagerHealthApi,
  sequenceManagerHealthApi } from '../api'
import NotificationContext from '../NotificationContext'
import useHealthCheck from '../utils/Healthcheck'


export default function ConnectionStatus({buttonOrPage}: {buttonOrPage: 'button' | 'page'}) {
    const [, showNotification] = useContext(NotificationContext)
    const navigate = useNavigate()
  
    const {
      // data,
      isError: patientManagerHealthIsError
    } = useQuery<{}>({
      queryKey: ['patientManagerHealth'],
      refetchInterval: 5000,
      retry: 0,
      queryFn: async () => {
        return await patientManagerHealthApi
        .readinessApiV1PatientHealthReadinessGet({timeout: 1000})
        .then((result) => {
          if (patientManagerHealthIsError && result.data.status == 'ok') {
            showNotification({message: 'Reconnected to patient-manager after connection loss.', type: 'success'})
          }
          // return result.data
        })
        .catch((error) => {
            return Promise.reject('Error at health check of patient-manager.')
        })
      },
    })

    const {
      // data,
      isError: examManagerHealthIsError
    } = useQuery<{}>({
      queryKey: ['examManagerHealth'],
      refetchInterval: 5000,
      retry: 0,
      queryFn: async () => {
        return await examManagerHealthApi
        .readinessApiV1ExamHealthReadinessGet({timeout: 1000})
        .then((result) => {
          if (examManagerHealthIsError && result.data.status == 'ok') {
            showNotification({message: 'Reconnected to exam-manager after connection loss.', type: 'success'})
          }
          // return result.data
        })
        .catch((error) => {
            return Promise.reject('Error at health check of exam-manager.')
        })
      },
    })

    const {
      // data,
      isError: workflowManagerHealthIsError
    } = useQuery<{}>({
      queryKey: ['workflowManagerHealth'],
      refetchInterval: 5000,
      retry: 0,
      queryFn: async () => {
        return await workflowManagerHealthApi
        .readinessApiV1WorkflowmanagerHealthReadinessGet({timeout: 1000})
        .then((result) => {
          if (workflowManagerHealthIsError && result.data.status == 'ok') {
            showNotification({message: 'Reconnected to workflow-manager after connection loss.', type: 'success'})
          }
          // return result.data
        })
        .catch((error) => {
            return Promise.reject('Error at health check of workflow-manager.')
        })
      },
    })

    const {
      // data,
      isError: userLoginHealthIsError
    } = useQuery<{}>({
      queryKey: ['userLoginHealth'],
      refetchInterval: 5000,
      retry: 0,
      queryFn: async () => {
        return await userLoginManagerHealthApi
        .readinessApiV1UserloginHealthReadinessGet({timeout: 1000})
        .then((result) => {
          if (userLoginHealthIsError && result.data.status == 'ok') {
            showNotification({message: 'Reconnected to user-login-manager after connection loss.', type: 'success'})
          }
          // return result.data
        })
        .catch((error) => {
          return Promise.reject('Error at health check of user-login-manager.')
        })
      },
    })

    const {
      // data,
      isError: deviceManagerHealthIsError
    } = useQuery<{}>({
      queryKey: ['deviceManagerHealth'],
      refetchInterval: 5000,
      retry: 0,
      queryFn: async () => {
        return await deviceManagerHealthApi
        .readinessApiV1DeviceHealthReadinessGet({timeout: 1000})
        .then((result) => {
          if (deviceManagerHealthIsError && result.data.status == 'ok') {
            showNotification({message: 'Reconnected to device-manager after connection loss.', type: 'success'})
          }
          // return result.data
        })
        .catch((error) => {
          return Promise.reject('Error at health check of device-manager.')
        })
      },
    })

    const {
      // data,
      isError: sequenceManagerHealthIsError
    } = useQuery<{}>({
      queryKey: ['sequenceManagerHealth'],
      refetchInterval: 5000,
      retry: 0,
      queryFn: async () => {
        return await sequenceManagerHealthApi
        .healthCheckApiV1MriSequencesHealthGet({timeout: 1000})
        .then((result) => {
          if (sequenceManagerHealthIsError && result.data.status == 'ok') {
            showNotification({message: 'Reconnected to sequence-manager after connection loss.', type: 'success'})
          }
          // return result.data
        })
        .catch((error) => {
          return Promise.reject('Error at health check of sequence-manager.')
        })
      },
    })

    const nginxProxyIsError = useHealthCheck('http://localhost:8080')
  
    let statusColor: 'primary' | 'warning' | 'danger';
    statusColor = 'primary';
    if (patientManagerHealthIsError
        || examManagerHealthIsError
        || workflowManagerHealthIsError
        || userLoginHealthIsError
        || deviceManagerHealthIsError
        || nginxProxyIsError) {
      statusColor = 'warning';
    }
    // statusColor = 'danger';
    if (buttonOrPage == 'button') {
      return (
        <IconButton
          variant='outlined'
          color={statusColor}
          size='sm'
          onClick={() => {
            navigate('/connections')
          }}
        >
          {<LanIcon />}
        </IconButton>
      )
    }
    else {
      return (
        <Box sx={{display: 'flex', alignItems: 'stretch', width: '20%', margin: 'auto'}}>
          <Box
            sx={{
              rowGap: 0.4,
              columnGap: 4,
              p: 2,
              display: 'grid',
              gridTemplateColumns: 'auto 1fr',
              '& > *:nth-of-type(odd)': {
                color: 'text.secondary',
              },
            }}
          >
            <Typography fontSize='sm'>Patient Manager</Typography>
            <Typography level='body-sm' textColor='text.primary'>
              {patientManagerHealthIsError ? 'NOT REACHABLE' : 'OK'}
            </Typography>

            <Typography fontSize='sm'>Exam Manager</Typography>
            <Typography level='body-sm' textColor='text.primary'>
              {examManagerHealthIsError ? 'NOT REACHABLE' : 'OK'}
            </Typography>

            <Typography fontSize='sm'>Workflow Manager</Typography>
            <Typography level='body-sm' textColor='text.primary'>
              {workflowManagerHealthIsError ? 'NOT REACHABLE' : 'OK'}
            </Typography>

            <Typography fontSize='sm'>User/Login Manager</Typography>
            <Typography level='body-sm' textColor='text.primary'>
              {userLoginHealthIsError ? 'NOT REACHABLE' : 'OK'}
            </Typography>

            <Typography fontSize='sm'>Device Manager</Typography>
            <Typography level='body-sm' textColor='text.primary'>
              {deviceManagerHealthIsError ? 'NOT REACHABLE' : 'OK'}
            </Typography>

            <Typography fontSize='sm'>Sequence Manager</Typography>
            <Typography level='body-sm' textColor='text.primary'>
              {sequenceManagerHealthIsError ? 'NOT REACHABLE' : 'OK'}
            </Typography>

            <Typography fontSize='sm'>Microservice Proxy</Typography>
            <Typography level='body-sm' textColor='text.primary'>
              {nginxProxyIsError ? 'NOT REACHABLE' : 'OK'}
            </Typography>
          </Box>
        </Box>
      )
    }
  }