/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * AcquisitionView.tsx is responsible for rendering the acquisition view.
 */
import AddSharpIcon from '@mui/icons-material/AddSharp'
import FolderIcon from '@mui/icons-material/Folder'
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import CircularProgress from '@mui/joy/CircularProgress';
import HighlightOffIcon from '@mui/icons-material/HighlightOff';
import RadioButtonUncheckedIcon from '@mui/icons-material/RadioButtonUnchecked';
import FolderOpenIcon from '@mui/icons-material/FolderOpen'
import Badge from '@mui/joy/Badge'
import Box from '@mui/joy/Box'
import Container from '@mui/joy/Container'
import Divider from '@mui/joy/Divider'
import IconButton from '@mui/joy/IconButton'
import Sheet from '@mui/joy/Sheet'
import Stack from '@mui/joy/Stack'
import Typography from '@mui/joy/Typography'
import React from 'react'
import { useQuery } from '@tanstack/react-query'
import { useParams } from 'react-router-dom'

import { dataApi, protocolApi, patientApi, resultApi, taskApi } from '../api'
import AcquisitionControl from '../components/AcquisitionControl'
import ConfirmAcquisitionLimitsModal from '../components/AcquisitionLimitsModal'
import DicomViewer3D from '../viewer/dicom/DicomViewer'
import RawDataViewer from '../viewer/mrd/RawDataViewer'
import PatientInfo from '../components/PatientInfo'
import { PatientOut } from '../openapi/generated-client/patient'
import { ProtocolOut, AcquisitionTaskOut, ResultOut, ResultType, ItemStatus } from '../openapi/generated-client/protocol'
import ProtocolFromTemplateModal from '../components/ProtocolFromTemplateModal'
import ProtocolItem from '../components/ProtocolItem'
import TaskItem from '../components/TaskItem'
import { ITEM_UNSELECTED, ItemSelection, Alerts } from '../interfaces/components.interface'
import AlertItem from '../components/AlertItem'


function AcquisitionView() {
  const params = useParams()

  const [protocolFromTemplateModalOpen, setProtocolFromTemplateModalOpen] = React.useState(false)
  const [confirmAcquisitionLimitsModalOpen, setConfirmAcquisitionLimitsModalOpen] = React.useState(false)
  const [itemSelection, setItemSelection] = React.useState<ItemSelection>(ITEM_UNSELECTED)
  const [onAcquisitionLimitsConfirm, setOnAcquisitionLimitsConfirm] = React.useState<() => void>(() => () => { })
  const [selectedResultId, setSelectedResultId] = React.useState<string | undefined>(undefined)

  // Reset result selection when task changes
  React.useEffect(() => {
    setSelectedResultId(undefined)
  }, [itemSelection.itemId])

  const [expandedProtocols, setExpandedProtocols] = React.useState<Set<string>>(new Set())

  const toggleProtocol = (id: string) => {
    setExpandedProtocols(prev => {
      const next = new Set(prev)
      next.has(id) ? next.delete(id) : next.add(id)
      return next
    })
  }

  const [draggingTaskIndex, setDraggingTaskIndex] = React.useState<number | undefined>(undefined)
  const [draggingProtocolId, setDraggingProtocolId] = React.useState<string | undefined>(undefined)

  const handleDragStart = (index: number, protocolId: string) => {
    setDraggingTaskIndex(index)
    setDraggingProtocolId(protocolId)
  }

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault()
  }

  const handleDrop = async (index: number, protocol: ProtocolOut) => {
    if (draggingTaskIndex === undefined || draggingProtocolId !== protocol.id || draggingTaskIndex === index) return
    const tasks = [...protocol.tasks]
    const [draggedTask] = tasks.splice(draggingTaskIndex, 1)
    tasks.splice(index, 0, draggedTask)
    await taskApi.reorderTasks({ task_ids: tasks.map(t => t.id) })
    refetchProtocols()
    setDraggingTaskIndex(undefined)
    setDraggingProtocolId(undefined)
  }

  // Patient query
  const {
    data: patient,
    refetch: refetchPatient,
    isLoading: patientLoading,
    isError: patientError,
  } = useQuery<PatientOut>({
    queryKey: ['patient', params.patientId],
    queryFn: async () => (await patientApi.getPatient(params.patientId!)).data,
    refetchInterval: 1000,
  })

  // Protocols query
  const { data: protocols, refetch: refetchProtocols } = useQuery<ProtocolOut[], Error>({
    queryKey: ['allProtocols', params.patientId],
    queryFn: async () => {
      const result = await protocolApi.getAllPatientProtocols(params.patientId!)
      if (itemSelection.itemId != undefined) {
        result.data.forEach((protocol) => {
          if (protocol.id === itemSelection.itemId)
            setItemSelection({ type: 'protocol', name: protocol.name, itemId: protocol.id, status: protocol.status, progress: 0 })
          protocol.tasks.forEach((task) => {
            if (task.id === itemSelection.itemId)
              setItemSelection({ type: 'ACQUISITION', name: task.name, itemId: task.id, status: task.status, progress: task.progress, deviceId: task.device_id ? String(task.device_id) : undefined })
          })
        })
      }
      return result.data
    },
    refetchInterval: 1000,
  })

  // Task data query for the selected task
  const { data: taskData } = useQuery({
    queryKey: ['task-data', itemSelection.itemId, itemSelection.status],
    enabled: !!itemSelection.itemId && itemSelection.type === 'ACQUISITION',
    queryFn: async () => {
      const { data } = await taskApi.getTask(itemSelection.itemId!)
      return data
    },
    refetchInterval: 2000,
  })

  const protocolId: string | undefined = taskData ? String(taskData.protocol_id) : undefined
  const taskId: string | undefined = itemSelection.itemId

  const taskResults: ResultOut[] = React.useMemo(() => {
    const raw = Array.isArray(taskData?.results) ? taskData!.results as ResultOut[] : []
    return raw
      .filter(r => r.type === ResultType.Mrd || r.type === ResultType.Dicom)
      .sort((a, b) => new Date(b.datetime_created).getTime() - new Date(a.datetime_created).getTime())
  }, [taskData?.results])

  // Auto-select the newest result when list updates
  React.useEffect(() => {
    if (taskResults.length === 0) return
    if (!selectedResultId || !taskResults.find(r => r.id === selectedResultId)) {
      setSelectedResultId(taskResults[0].id)
    }
  }, [taskResults])

  const selectedResult = taskResults.find(r => r.id === selectedResultId)
  const viewerType: 'MRD' | 'DICOM' | undefined =
    selectedResult?.type === ResultType.Mrd ? 'MRD' :
    selectedResult?.type === ResultType.Dicom ? 'DICOM' :
    undefined

  // Download / export handlers
  async function handleDownloadMrd() {
    if (!protocolId || !taskId || !selectedResultId) return
    try {
      const response = await dataApi.downloadMRD(protocolId, taskId, selectedResultId, { responseType: 'blob' })
      const filename = selectedResult?.files?.[0] ?? 'data.mrd'
      const blobUrl = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = blobUrl
      link.setAttribute('download', filename)
      document.body.appendChild(link)
      link.click()
      link.parentNode?.removeChild(link)
      window.URL.revokeObjectURL(blobUrl)
    } catch (e) {
      console.error('Failed to download MRD', e)
    }
  }

  async function handleDownloadDicom() {
    if (!protocolId || !taskId || !selectedResultId || !selectedResult?.files?.length) return
    try {
      for (const filename of selectedResult.files.filter(f => f.toLowerCase().endsWith('.dcm'))) {
        const response = await dataApi.getDicom(protocolId, taskId, selectedResultId, filename, { responseType: 'blob' })
        const blobUrl = window.URL.createObjectURL(new Blob([response.data]))
        const link = document.createElement('a')
        link.href = blobUrl
        link.setAttribute('download', filename)
        document.body.appendChild(link)
        link.click()
        link.parentNode?.removeChild(link)
        window.URL.revokeObjectURL(blobUrl)
      }
    } catch (e) {
      console.error('Failed to download DICOM', e)
    }
  }

  async function handleExportToXnat() {
    if (!protocolId || !taskId || !selectedResultId || !selectedResult?.files?.length) return
    try {
      const filename = selectedResult.files.find(f => f.toLowerCase().endsWith('.dcm')) ?? selectedResult.files[0]
      await resultApi.uploadToXnat(protocolId, taskId, selectedResultId, filename)
      alert(`Successfully exported ${filename} to XNAT`)
    } catch (e) {
      console.error('Failed to export to XNAT', e)
      alert('Failed to export to XNAT')
    }
  }

  if (patientError || patient == undefined) {
    return (
      <Container maxWidth={false} sx={{ width: '50%', mt: 5, justifyContent: 'center' }}>
        <AlertItem title='Error getting patient information / patient undefined.' type={Alerts.Error} />
      </Container>
    )
  }

  const isTaskSelected = !!itemSelection.itemId && itemSelection.type === 'ACQUISITION'

  return (
    <Box sx={{ flex: 1, display: 'flex', flexDirection: 'row', width: '100%', minHeight: 0, overflow: 'hidden' }}>
      <Sheet
        className='Sidebar'
        sx={{
          height: '100%',
          width: 'var(--Sidebar-width)',
          p: 2,
          flexShrink: 0,
          display: 'flex',
          flexDirection: 'column',
          gap: 1.5,
          borderRight: '1px solid',
          borderColor: 'divider',
        }}
      >
        <Box sx={{ display: 'flex', gap: 1, alignItems: 'center' }}>
          <Typography level='title-md'>Patient Info</Typography>
        </Box>
        <Divider />
        <PatientInfo patient={patient} isLoading={patientLoading} isError={patientError} />
        <Divider />

        <Box sx={{ display: 'flex', gap: 1, alignItems: 'center', justifyContent: 'space-between' }}>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 3 }}>
            <Typography level='title-md'>Protocols</Typography>
            <Badge badgeContent={protocols?.length} color='primary' />
          </Box>
          <IconButton size='sm' variant='plain' color='neutral' onClick={() => setProtocolFromTemplateModalOpen(true)}>
            <AddSharpIcon />
          </IconButton>
        </Box>
        <Divider />

        <Box sx={{
          minHeight: 0,
          overflow: 'hidden auto',
          flexGrow: 1,
          display: 'flex',
          flexDirection: 'column',
          scrollbarWidth: 'thin',
          scrollbarColor: 'rgba(255,255,255,0.22) rgba(255,255,255,0.05)',
          '&::-webkit-scrollbar': { width: '6px' },
          '&::-webkit-scrollbar-track': { background: 'rgba(255,255,255,0.05)', borderRadius: '3px' },
          '&::-webkit-scrollbar-thumb': { background: 'rgba(255,255,255,0.22)', borderRadius: '3px' },
          '&::-webkit-scrollbar-thumb:hover': { background: 'rgba(255,255,255,0.40)' },
        }}>
          {protocols?.map((protocol: ProtocolOut) => {
            const isExpanded = expandedProtocols.has(protocol.id)
            return (
              <Stack key={`protocol-${protocol.id}`} direction='column' width='100%'>
                <ProtocolItem
                  item={protocol}
                  refetchParentData={refetchProtocols}
                  onClick={() => toggleProtocol(protocol.id)}
                  selection={itemSelection}
                  icon={isExpanded ? <FolderOpenIcon fontSize='small' /> : <FolderIcon fontSize='small' />}
                  hoverIcon={<FolderOpenIcon fontSize='small' />}
                />
                {isExpanded && (
                  <Stack direction='column' sx={{ pl: 2 }}>
                    {protocol.tasks?.map((task: AcquisitionTaskOut, index: number) => (
                      <Box
                        key={`task-${task.id}`}
                        draggable
                        onDragStart={() => handleDragStart(index, protocol.id)}
                        onDragOver={handleDragOver}
                        onDrop={() => handleDrop(index, protocol)}
                        sx={{
                          cursor: 'grab',
                          '&:active': { cursor: 'grabbing' },
                          opacity: (draggingTaskIndex === index && draggingProtocolId === protocol.id) ? 0.5 : 1,
                        }}
                      >
                        <TaskItem
                          item={task}
                          refetchParentData={refetchProtocols}
                          onClick={() => setItemSelection({ type: 'ACQUISITION', name: task.name, itemId: task.id, status: task.status, progress: task.progress, deviceId: task.device_id ? String(task.device_id) : undefined })}
                          selection={itemSelection}
                          icon={
                            task.status === ItemStatus.Finished ? <CheckCircleIcon fontSize='small' /> : (
                              task.status === ItemStatus.Inprogress ? <CircularProgress variant='plain' size="sm" /> : (
                                task.status === ItemStatus.Error ? <HighlightOffIcon fontSize='small' /> : <RadioButtonUncheckedIcon fontSize='small' />
                              )
                            )
                          }
                          results={itemSelection.itemId === task.id ? taskResults : undefined}
                          selectedResultId={itemSelection.itemId === task.id ? selectedResultId : undefined}
                          onResultSelect={itemSelection.itemId === task.id ? setSelectedResultId : undefined}
                        />
                      </Box>
                    ))}
                  </Stack>
                )}
              </Stack>
            )
          })}
        </Box>

        <Divider />

        <ConfirmAcquisitionLimitsModal
          item={patient}
          isOpen={confirmAcquisitionLimitsModalOpen}
          setOpen={setConfirmAcquisitionLimitsModalOpen}
          onSubmit={() => { refetchPatient(); onAcquisitionLimitsConfirm() }}
        />

        <AcquisitionControl
          itemSelection={itemSelection}
          openConfirmModal={(callback: () => void) => {
            if (itemSelection.type === 'ACQUISITION') {
              setOnAcquisitionLimitsConfirm(() => callback)
              setConfirmAcquisitionLimitsModalOpen(true)
            } else {
              callback()
            }
          }}
        />
      </Sheet>

      <ProtocolFromTemplateModal
        isOpen={protocolFromTemplateModalOpen}
        setOpen={setProtocolFromTemplateModalOpen}
        parentId={String(params.patientId)}
        onSubmit={refetchProtocols}
        createTemplate={false}
        modalType={'create'}
      />

      {/* Right panel: viewer toolbar + canvas */}
      <Box sx={{ display: 'flex', flexDirection: 'column', flex: 1, overflow: 'hidden' }}>
        {isTaskSelected && viewerType === 'MRD' && protocolId && taskId && selectedResultId ? (
          <RawDataViewer
            selectedResultId={selectedResultId}
            protocolId={protocolId}
            taskId={taskId}
            onDownload={handleDownloadMrd}
            taskName={taskData?.name}
          />
        ) : isTaskSelected && viewerType === 'DICOM' ? (
          <DicomViewer3D
            item={itemSelection}
            selectedResultId={selectedResultId}
            onDownloadDicom={handleDownloadDicom}
            onExportToXnat={handleExportToXnat}
          />
        ) : isTaskSelected && taskResults.length === 0 ? (
          <Container maxWidth={false} sx={{ width: '50%', mt: 5 }}>
            <AlertItem title='No results available for this task yet.' type={Alerts.Info} />
          </Container>
        ) : (
          <DicomViewer3D item={itemSelection} />
        )}
      </Box>
    </Box>
  )
}

export default AcquisitionView
