/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * SequenceUpload.tsx is responsible for rendering an interface to upload a new sequence.
 */
import React from 'react'
import { useMutation } from '@tanstack/react-query'
import { useContext } from 'react'

import Button from '@mui/joy/Button'
import FormLabel from '@mui/joy/FormLabel'
import Input from '@mui/joy/Input'
import Modal from '@mui/joy/Modal'
import ModalClose from '@mui/joy/ModalClose'
import ModalDialog from '@mui/joy/ModalDialog'
import Stack from '@mui/joy/Stack'
import Typography from '@mui/joy/Typography'

import NotificationContext from '../NotificationContext'
import { sequenceApi } from '../api'
import { ModalProps } from '../interfaces/components.interface'
import { BaseMRISequence } from '../openapi/generated-client/exam/api'



function SequenceUploadForm(props: ModalProps) {

  const [, showNotification] = useContext(NotificationContext)

  const [sequence, setSequence] = React.useState<BaseMRISequence>({
    name: '',
    description: '',
    sequence_type: '',  // eslint-disable-line camelcase
    tags: []
  })
  const [seqFile, setSeqFile] = React.useState<File | undefined>(undefined)
  const [xmlFile, setXmlFile] = React.useState<File | undefined>(undefined)

  const uploadSequence = useMutation<void, Error, BaseMRISequence>({
    mutationFn: async (sequence: BaseMRISequence) => {
      if (seqFile === undefined) {
        showNotification({message: 'No sequence file selected', type: 'warning'})
        return
      }
      await sequenceApi.createMriSequenceApiV1ExamSequencePost(
        seqFile,
        xmlFile ?? new File([], 'null'), 
        sequence.name,
        sequence.description ?? '',
        sequence.sequence_type as string,
        sequence.tags
      )
      .then(() => {
        showNotification({message: 'Sequence uploaded.', type: 'success'})
        props.onSubmit()
        props.setOpen(false)
      })
      .catch(() => {
        showNotification({message: 'Error on sequence upload.', type: 'warning'})
      })
    }
  })

  return (
    <>
      <Typography id='basic-modal-dialog-title' component='h2' level='inherit' fontSize='1.25em' mb={3}>
        Upload sequence
      </Typography>

      <Stack spacing={1.5} justifyContent='flex-start' sx={{width: '100%'}}>
        <FormLabel> Name </FormLabel>
        <Input
          name='name'
          onChange={(e) => setSequence({ ...sequence, [e.target.name]: e.target.value })}
          placeholder='Sequence name'
          defaultValue={sequence.name}
          required
        />

        <FormLabel> Description </FormLabel>
        <Input
          name='description'
          onChange={(e) => setSequence({ ...sequence, [e.target.name]: e.target.value })}
          placeholder='Sequence description'
          defaultValue={sequence.name}
          required
        />

        <FormLabel> Type </FormLabel>
        <Input
          name='sequence_type'
          onChange={(e) => setSequence({ ...sequence, [e.target.name]: e.target.value })}
          placeholder='Sequence type'
          defaultValue={sequence.sequence_type ? String(sequence.sequence_type) : ''}
          required
        />

        <FormLabel> File Selection </FormLabel>
        <Stack direction={'row'} gap={2} sx={{alignItems: 'center'}}>
          <Button component='label' color='primary' size='sm' sx={{width: 150}}>
            <input
              hidden
              accept='.seq'
              type='file'
              onChange={(e) => {
                const file = e.target.files?.[0]
                setSeqFile(file ?? undefined)
              }}
            />
            Upload sequence
          </Button>
          <Typography noWrap level='title-sm'>{'Selected file: '}</Typography>
            <Typography
              textColor="text.tertiary"
              sx={{ flex: 1, minWidth: 0, overflowWrap: 'anywhere' }}
            >
              {seqFile ? seqFile.name : '-'}
            </Typography>
        </Stack>

        <Stack direction={'row'} gap={2} sx={{alignItems: 'center'}}>
          <Button component='label' color='primary' size='sm' sx={{width: 150}}>
            <input
              hidden
              accept='.xml'
              type='file'
              onChange={(e) => {
                const file = e.target.files?.[0]
                setXmlFile(file ?? undefined)
              }}
            />
            Upload header
          </Button>
          <Typography level='title-sm'>{'Selected file: '}</Typography>
          <Typography
              textColor="text.tertiary"
              sx={{ flex: 1, minWidth: 0, overflowWrap: 'anywhere' }}
            >
              {xmlFile ? xmlFile?.name : '-'}
            </Typography>
        </Stack>
        

        <Button
          size='sm'
          sx={{ alignSelf: 'flex-end' }}
          onClick={(event) => {
            event.preventDefault()
            uploadSequence.mutate(sequence)
          }}
        >
          Save
        </Button>
      </Stack>
    </>
  )
}


function SequenceUpload(props: ModalProps) {
  return (
    <React.Fragment>
      <Modal
        open={props.isOpen}
        color='neutral'
        onClose={() => props.setOpen(false)}
        sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}
      >
        <ModalDialog
          aria-labelledby='basic-modal-dialog-title'
          aria-describedby='basic-modal-dialog-description'
          sx={{ width: '50vw', borderRadius: 'md', p: 5 }}
        >
          <ModalClose
            sx={{
              top: '10px',
              right: '10px',
              borderRadius: '50%',
              bgcolor: 'background.body',
            }}
          />
          <SequenceUploadForm {...props} />
        </ModalDialog>
      </Modal>
    </React.Fragment>
  )
}

export default SequenceUpload
