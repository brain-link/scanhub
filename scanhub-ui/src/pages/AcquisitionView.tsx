/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * AcquisitionView.tsx is responsible for rendering the acquisition view.
 */
import AddSharpIcon from '@mui/icons-material/AddSharp'
import FileDownloadIcon from '@mui/icons-material/FileDownload'
import OpenInNewIcon from '@mui/icons-material/OpenInNew'
import SaveIcon from '@mui/icons-material/Save'
import Badge from '@mui/joy/Badge'
import Box from '@mui/joy/Box'
import Divider from '@mui/joy/Divider'
import Dropdown from '@mui/joy/Dropdown'
import IconButton from '@mui/joy/IconButton'
import Menu from '@mui/joy/Menu'
import MenuButton from '@mui/joy/MenuButton'
import MenuItem from '@mui/joy/MenuItem'
import Option from '@mui/joy/Option'
import Select from '@mui/joy/Select'
import Sheet from '@mui/joy/Sheet'
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
import { ProtocolOut, AcquisitionTaskOut, ResultOut, ResultType } from '../openapi/generated-client/protocol'
import ExamFromTemplateModal from '../components/ExamFromTemplateModal'
import AccordionWithMenu from '../components/AccordionWithMenu'
import ExamItem, { ExamMenu } from '../components/ExamItem'
import TaskItem from '../components/TaskItem'
import { ITEM_UNSELECTED, ItemSelection } from '../interfaces/components.interface'
import Container from '@mui/joy/Container'
import AlertItem from '../components/AlertItem'
import { Alerts } from '../interfaces/components.interface'
import ExamInfo from '../components/ExamInfo'


function AcquisitionView() {
  const params = useParams()

  const [examFromTemplateModalOpen, setExamFromTemplateModalOpen] = React.useState(false)
  const [confirmAcquisitionLimitsModalOpen, setConfirmAcquisitionLimitsModalOpen] = React.useState(false)
  const [itemSelection, setItemSelection] = React.useState<ItemSelection>(ITEM_UNSELECTED)
  const [onAcquisitionLimitsConfirm, setOnAcquisitionLimitsConfirm] = React.useState<() => void>(() => () => { })
  const [selectedResultId, setSelectedResultId] = React.useState<string | undefined>(undefined)

  // Reset result selection when task changes
  React.useEffect(() => {
    setSelectedResultId(undefined)
  }, [itemSelection.itemId])

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
              setItemSelection({ type: 'ACQUISITION', name: task.name, itemId: task.id, status: task.status, progress: task.progress })
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
          <IconButton size='sm' variant='plain' color='neutral' onClick={() => setExamFromTemplateModalOpen(true)}>
            <AddSharpIcon />
          </IconButton>
        </Box>
        <Divider />

        <Box sx={{ minHeight: 0, overflow: 'hidden auto', flexGrow: 1, display: 'flex', flexDirection: 'column' }}>
          {protocols?.map((protocol: ProtocolOut) => (
            <AccordionWithMenu
              key={`protocol-${protocol.id}`}
              accordionSummary={
                <ExamItem
                  item={protocol}
                  onClick={() => setItemSelection({ type: 'protocol', name: protocol.name, itemId: protocol.id, status: protocol.status, progress: 0 })}
                  selection={itemSelection}
                />
              }
              accordionMenu={<ExamMenu item={protocol} refetchParentData={refetchProtocols} />}
              toolTipContent={<ExamInfo protocol={protocol} />}
            >
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
                    onClick={() => setItemSelection({ type: 'ACQUISITION', name: task.name, itemId: task.id, status: task.status, progress: task.progress })}
                    selection={itemSelection}
                  />
                </Box>
              ))}
            </AccordionWithMenu>
          ))}
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

      <ExamFromTemplateModal
        isOpen={examFromTemplateModalOpen}
        setOpen={setExamFromTemplateModalOpen}
        parentId={String(params.patientId)}
        onSubmit={refetchProtocols}
        createTemplate={false}
        modalType={'create'}
      />

      {/* Right panel: Row 1 (file selector + actions) + Row 2 (viewer toolbar) + canvas */}
      <Box sx={{ display: 'flex', flexDirection: 'column', flex: 1, overflow: 'hidden' }}>

        {/* Row 1: file selector + download/export */}
        {isTaskSelected && (
          <Box sx={{
            px: 1.5, py: 0.75,
            display: 'flex', alignItems: 'center', gap: 1,
            borderBottom: '1px solid', borderColor: 'divider',
            flexShrink: 0,
          }}>
            <Select
              size='sm'
              placeholder='No results yet'
              value={selectedResultId ?? null}
              onChange={(_, v) => v && setSelectedResultId(v)}
              sx={{ minWidth: 240 }}
            >
              {taskResults.map(result => {
                const dt = new Date(result.datetime_created)
                const label = (result.files?.[0] ? result.files[0] + ' | ' : '') +
                  dt.toLocaleDateString() + ', ' + dt.toLocaleTimeString()
                return (
                  <Option key={result.id} value={result.id}>{label}</Option>
                )
              })}
            </Select>

            {viewerType === 'MRD' && (
              <IconButton size='sm' variant='outlined' color='neutral' title='Download MRD' onClick={handleDownloadMrd}>
                <FileDownloadIcon sx={{ fontSize: 'var(--IconFontSize)' }} />
              </IconButton>
            )}

            {viewerType === 'DICOM' && (
              <Dropdown>
                <MenuButton
                  slots={{ root: IconButton }}
                  slotProps={{ root: { size: 'sm', variant: 'outlined', color: 'neutral', title: 'Share / Export' } }}
                >
                  <SaveIcon sx={{ fontSize: 'var(--IconFontSize)' }} />
                </MenuButton>
                <Menu size='sm' placement='bottom-end'>
                  <MenuItem onClick={handleDownloadDicom}>
                    <FileDownloadIcon sx={{ fontSize: 'var(--IconFontSize)' }} />
                    Download DICOM
                  </MenuItem>
                  <MenuItem onClick={handleExportToXnat}>
                    <OpenInNewIcon sx={{ fontSize: 'var(--IconFontSize)' }} />
                    Export to XNAT
                  </MenuItem>
                </Menu>
              </Dropdown>
            )}
          </Box>
        )}

        {/* Row 2 + canvas: rendered by each viewer */}
        {isTaskSelected && viewerType === 'MRD' && protocolId && taskId && selectedResultId ? (
          <RawDataViewer
            selectedResultId={selectedResultId}
            protocolId={protocolId}
            taskId={taskId}
          />
        ) : isTaskSelected && viewerType === 'DICOM' ? (
          <DicomViewer3D item={itemSelection} selectedResultId={selectedResultId} />
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
