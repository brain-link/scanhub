/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * AcquisitionControl.tsx is responsible for rendering the acquisition trigger and process.
 */
import PlayCircleIcon from '@mui/icons-material/PlayCircle'
import StopCircleIcon from '@mui/icons-material/StopCircle';
import Box from '@mui/joy/Box'
import IconButton from '@mui/joy/IconButton'
import LinearProgress from '@mui/joy/LinearProgress'
import Stack from '@mui/joy/Stack'
import Typography from '@mui/joy/Typography'
import axios from 'axios'
import React from 'react'
import { useMutation } from '@tanstack/react-query'

import { ItemStatus } from '../openapi/generated-client/protocol'
import { ItemSelection } from '../interfaces/components.interface'
import LoginContext from '../LoginContext'
import NotificationContext from '../NotificationContext'
import baseUrls from '../utils/Urls'


const STATUS_LABEL: Record<string, string> = {
  // device states
  NEW: 'Ready',
  UPDATED: 'Ready',
  STARTED: 'Starting...',
  INPROGRESS: 'Scanning...',
  ACQUIRED: 'Scan acquired',
  FINISHED: 'Scan complete',
  ERROR: 'Device error',
  TRANSFERRING: 'Transferring data...',
  // pipeline states
  RECONSTRUCTING: 'Reconstructing...',
  SUCCEEDED: 'Reconstruction complete',
  FAILED: 'Reconstruction failed',
  CANCELLED: 'Cancelled',
}

const FAILURE_STATUSES = new Set(['ERROR', 'FAILED', 'CANCELLED'])
const ALWAYS_INDETERMINATE_STATUSES = new Set(['STARTED', 'TRANSFERRING', 'RECONSTRUCTING'])

function AcquisitionControl({ itemSelection, openConfirmModal }: {
  itemSelection: ItemSelection, openConfirmModal: (onConfirmed: () => void) => void
}){
  const [, showNotification] = React.useContext(NotificationContext)
  const [user] = React.useContext(LoginContext)
  const hasTriggeredRef = React.useRef(false)
  const [liveProgress, setLiveProgress] = React.useState<number | undefined>(undefined)
  const [liveStatusLabel, setLiveStatusLabel] = React.useState<string | undefined>(undefined)
  const [rawTaskStatus, setRawTaskStatus] = React.useState<string | undefined>(undefined)

  React.useEffect(() => {
    if (!itemSelection.itemId || itemSelection.type !== 'ACQUISITION' || !user?.access_token) {
      setLiveProgress(undefined)
      setLiveStatusLabel(undefined)
      setRawTaskStatus(undefined)
      return
    }

    const url = `${baseUrls.deviceService}/api/v1/device/task-stream/${itemSelection.itemId}?token=${user.access_token}`
    const es = new EventSource(url)

    es.onmessage = (event: MessageEvent<string>) => {
      const data: { task_status: string; progress: number } = JSON.parse(event.data)
      setRawTaskStatus(data.task_status)
      setLiveProgress(data.progress)
      setLiveStatusLabel(STATUS_LABEL[data.task_status] ?? data.task_status)
      if (FAILURE_STATUSES.has(data.task_status) || data.task_status === 'SUCCEEDED') {
        es.close()
      }
    }

    return () => es.close()
  }, [itemSelection.itemId, itemSelection.type, user?.access_token])

  const processTaskMutation = useMutation({
    mutationKey: ['triggerAcquisition'],
    mutationFn: async () => {
      if (hasTriggeredRef.current) return
      hasTriggeredRef.current = true
      try {
        await axios.post(
          `${baseUrls.deviceService}/api/v1/device/trigger_acquisition/${itemSelection.itemId}`
        )
        showNotification({message: 'Started task', type: 'success'})
      } catch {
        showNotification({message: 'Error at starting task.', type: 'warning'})
      } finally {
        hasTriggeredRef.current = false
      }
    },
  })

  return (
    <Box sx={{ display: 'flex', gap: 1, alignItems: 'center' }}>
      <IconButton
        size='sm'
        variant='plain'
        color={'neutral'}
        disabled={processTaskMutation.isPending || itemSelection.type !== 'ACQUISITION'}
        onClick={() => {
          openConfirmModal(() => {
            if (itemSelection.itemId == undefined) {
              showNotification({message: 'No item selected!', type: 'warning'})
            } else if (itemSelection.type == 'ACQUISITION') {
              if (!processTaskMutation.isPending){
                processTaskMutation.mutate()
              }
            } else {
              showNotification({message: 'Acquisition trigger not implemented for this item type!', type: 'warning'})
            }
          })
        }}
      >
        { itemSelection.status == ItemStatus.Started ? <StopCircleIcon /> : <PlayCircleIcon /> }
      </IconButton>

      <Stack direction='column' sx={{ flex: 1 }}>
        <Typography level='title-sm'>
          {itemSelection.type ?
            'Execute ' + itemSelection.type + ' "' + itemSelection.name + '"'
          :
            'Select item to start...'}
        </Typography>
        {(() => {
          const progressValue = liveProgress ?? itemSelection.progress ?? 0
          const label = liveStatusLabel ?? STATUS_LABEL[itemSelection.status]
          const showPct = progressValue > 0 && progressValue < 100
          const isFailure = rawTaskStatus
            ? FAILURE_STATUSES.has(rawTaskStatus)
            : itemSelection.status === ItemStatus.Error
          const currentStatus = rawTaskStatus ?? itemSelection.status
          const isIndeterminate =
            ALWAYS_INDETERMINATE_STATUSES.has(currentStatus)
            || (currentStatus === ItemStatus.Inprogress && progressValue === 0)
          return (
            <>
              <LinearProgress
                determinate={!isIndeterminate}
                value={isIndeterminate ? undefined : progressValue}
                color={isFailure ? 'danger' : 'primary'}
                sx={{ marginTop: 1 }}
              />
              {label && (
                <Typography
                  level='body-xs'
                  sx={{ marginTop: 0.5, color: isFailure ? 'danger.500' : 'neutral.500' }}
                >
                  {label}{showPct ? ` — ${progressValue}%` : ''}
                </Typography>
              )}
            </>
          )
        })()}
      </Stack>
    </Box>
  )
}

export default AcquisitionControl
