/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * SequenceView.tsx is responsible for rendering the sequence table and for adding, modifying and removing sequences.
 */
import * as React from 'react'
import { useMutation, useQuery } from 'react-query'

import IconButton from '@mui/joy/IconButton'
import AddSharpIcon from '@mui/icons-material/AddSharp'
import DeleteIcon from '@mui/icons-material/DeleteOutlined'
import FileOpenOutlinedIcon from '@mui/icons-material/FileOpen'
import Box from '@mui/joy/Box'
import LinearProgress from '@mui/joy/LinearProgress'
import Modal from '@mui/joy/Modal'
import Sheet from '@mui/joy/Sheet'
import ModalClose from '@mui/joy/ModalClose'
import Stack from '@mui/joy/Stack'
import Typography from '@mui/joy/Typography'
import Container from '@mui/system/Container'
import { DataGrid, GridColDef, GridCellParams, GridActionsCellItem } from '@mui/x-data-grid'

import NotificationContext from '../NotificationContext'
import { sequenceApi } from '../api'
import { MRISequenceOut, BaseMRISequence } from '../generated-client/exam'
import { Alerts } from '../interfaces/components.interface'
import AlertItem from '../components/AlertItem'
import SequenceUpload from '../components/SequenceUpload'
import ConfirmDeleteModal from '../components/ConfirmDelteModal'


export default function SequenceView() {
  const [, showNotification] = React.useContext(NotificationContext)
  const [dialogOpen, setDialogOpen] = React.useState<boolean>(false)
  const [sequenceToDelete, setSequenceToDelete] = React.useState<MRISequenceOut | undefined>(undefined)
  const [isUpdating, setIsUpdating] = React.useState<boolean>(false)
  const [sequenceOpen, setSequenceOpen] = React.useState<MRISequenceOut | undefined>(undefined)

  const {
    data: sequences,
    isLoading,
    isError,
    refetch,
  } = useQuery<MRISequenceOut[]>({
    queryKey: ['sequences'],
    queryFn: async () => {
      return await sequenceApi
        .getAllMriSequencesApiV1ExamSequencesAllGet()
        .then((result) => {
          return result.data
        })
    },
  })

  const delteMutation = useMutation<unknown, unknown, MRISequenceOut>(async (sequence) => {
    await sequenceApi.deleteMriSequenceEndpointApiV1ExamSequenceSequenceIdDelete(sequence._id)
      .then(() => {
        showNotification({message: 'Deleted sequence ' + sequence.name, type: 'success'})
        refetch()
      })
      .catch((err) => {
        let errorMessage = null
        if (err?.response?.data?.detail) {
          errorMessage = 'Could not delete sequence. Detail: ' + err.response.data.detail
        } else {
          errorMessage = 'Could not delete sequence.'
        }
        showNotification({message: errorMessage, type: 'warning'})
      })
  })

  const updateMutation = useMutation<unknown, unknown, MRISequenceOut>(async (sequence) => {
    await sequenceApi.updateMriSequenceEndpointApiV1ExamSequenceSequenceIdPut(sequence._id, sequence as BaseMRISequence)
      .then(() => {
        showNotification({message: 'Modified sequence ' + sequence.name, type: 'success'})
        setIsUpdating(false)
        refetch()
      })
      .catch((err) => {
        let errorMessage = null
        if (err?.response?.data?.detail) {
          errorMessage = 'Could not update sequence. Detail: ' + err.response.data.detail
        } else {
          errorMessage = 'Could not update sequence.'
        }
        setIsUpdating(false)
        refetch()
        showNotification({message: errorMessage, type: 'warning'})
      })
  })

  if (isLoading) {
    return (
      <Container maxWidth={false} sx={{ width: '50%', mt: 5, justifyContent: 'center' }}>
        <Typography>Loading sequences...</Typography>
        <LinearProgress variant='plain' />
      </Container>
    )
  }

  if (isError) {
    return (
      <Container maxWidth={false} sx={{ width: '50%', mt: 5, justifyContent: 'center' }}>
        <AlertItem title='Error Loading Sequences' type={Alerts.Error} />
      </Container>
    )
  }

  const columns: GridColDef<MRISequenceOut>[] = [
    { field: '_id', headerName: 'ID', width: 200, editable: false },
    { field: 'name', headerName: 'Name', width: 200, editable: true },
    { field: 'description', headerName: 'Description', width: 500, editable: true },
    { field: 'sequence_type', headerName: 'Type', width: 200, editable: true },
    {
      field: 'created_at', headerName: 'Added', width: 150, editable: false,
      valueFormatter: (value) => (value ? new Date(value).toLocaleString() : '')
    },
    {
      field: 'updated_at', headerName: 'Last updated', width: 150, editable: false,
      valueFormatter: (value) => (value ? new Date(value).toLocaleString() : '')
    },
    {
      field: 'actions', type: 'actions', headerName: '', width: 150, cellClassName: 'actions', filterable: false,
      getActions: (row) => [
        <GridActionsCellItem
          key='1'
          icon={<DeleteIcon />}
          label='Delete'
          color='inherit'
          onClick={() => { setSequenceToDelete(row.row) }}
        />,
        <GridActionsCellItem
          key='2'
          icon={<FileOpenOutlinedIcon />}
          label='Open'
          color='inherit'
          onClick={() => {
            setSequenceOpen(row.row as MRISequenceOut)
          }}
        />,
      ]
    },
  ]

  return (
    <Box sx={{ p: 3, width: '100%'}}>
      <SequenceUpload
        isOpen={dialogOpen}
        setOpen={setDialogOpen}
        onSubmit={() => {
          refetch()
        }}
      />

      <Stack direction='row' sx={{ justifyContent: 'space-between', mb: 2 }}> 
        <Typography level='title-md'>List of Sequences</Typography>
        <IconButton size='sm' variant='outlined'>
          <AddSharpIcon onClick={() => setDialogOpen(true)} />
        </IconButton>
      </Stack>

      <div style={{ height:'80vh', width: '100%'}}>
        <DataGrid
          rows={sequences}
          columns={columns}
          getRowId={(sequence) => sequence._id ? sequence._id : ''}
          hideFooterSelectedRowCount 
          editMode={'row'}
          rowHeight={45}  // MUI default is 52
          autoPageSize= {true}
          loading={isUpdating}
          processRowUpdate={(updatedSequence) => {
            setIsUpdating(true)
            updateMutation.mutate(updatedSequence)
            return updatedSequence
          }}
          onCellClick={(params: GridCellParams) => {
            if (params.field == '_id') {
              setSequenceOpen(params.row as MRISequenceOut)
            }
          }}
          sx={{
            "&.MuiDataGrid-root .MuiDataGrid-cell:focus-within": {
              outline: "none !important",
            },
          }}
        />
      </div>


      <ConfirmDeleteModal 
        onSubmit={() => sequenceToDelete ? delteMutation.mutate(sequenceToDelete) : () => {}}
        isOpen={sequenceToDelete ? true : false} 
        setOpen={(status) => {
          if (status == false) setSequenceToDelete(undefined)
        }}
        modalType={'modify'}
        item={'sequence ' + sequenceToDelete?.name}
      />


      <Modal
        aria-labelledby="modal-title"
        aria-describedby="modal-desc"
        open={sequenceOpen != undefined}
        onClose={() => setSequenceOpen(undefined)}
        sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}
      >
        <Sheet
          variant="outlined"
          sx={{
            width: '50vw',
            borderRadius: 'md',
            p: 3,
            boxShadow: 'lg',
            maxHeight: '70vh',
            display: 'flex',
            flexDirection: 'column',
          }}
        >
          <ModalClose variant="plain" sx={{ m: 1 }} />
          <Typography component="h2" id="modal-title" level="h4" sx={{ fontWeight: 'lg', mb: 1 }}>
            {sequenceOpen?.name}
          </Typography>
          <Box
            sx={{
              bgcolor: 'background.level1',
              borderRadius: 'sm',
              p: 2,
              width: '100%',
              flex: 1,
              minHeight: 0,
              overflow: 'auto',
              mt: 2,
            }}
          >
            <Typography id="modal-desc" textColor="text.tertiary" component="pre" sx={{ m: 0, whiteSpace: 'pre-wrap' }}>
              {sequenceOpen?.file}
            </Typography>
          </Box>
        </Sheet>
      </Modal>

    </Box>
  )
}
