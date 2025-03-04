/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * SequenceUpload.tsx is responsible for rendering an interface to upload a new sequence.
 */
import * as React from 'react'
import { useMutation } from 'react-query'
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
import { MRISequence } from '../generated-client/sequence/api'


function SequenceUploadForm(props: ModalProps) {

  const [, showNotification] = useContext(NotificationContext)

  const [sequence, setSequence] = React.useState<MRISequence>({
    _id: '',
    name: '',
    description: '',
    sequence_type: '',  // eslint-disable-line camelcase
    tags: [],
    file: null,
    file_extension: '.seq',   // eslint-disable-line camelcase
  })

  const uploadSequence = useMutation(async (sequence: MRISequence) => {
    if (sequence.file == undefined || sequence.file == null) {
      showNotification({message: 'No file selected for upload.', type: 'warning'})
    }
    else {
      await sequenceApi.uploadMriSequenceFileApiV1MriSequencesUploadPost(sequence.file, sequence.name, sequence.description, sequence.sequence_type)
      .then(() => {
        showNotification({message: 'Sequence uploaded.', type: 'success'})
        props.onSubmit()
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

      <Stack spacing={1.5} justifyContent='flex-start'>
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
          defaultValue={sequence.sequence_type ? sequence.sequence_type : ''}
          required
        />

        <FormLabel> File Selection </FormLabel>
        <Stack direction={'row'} gap={'5px'} >
          <Typography>
            {'Selected file: '}
          </Typography>
          <Typography sx={{fontStyle: 'italic'}}>
            {sequence.file ? sequence.file?.name : '---'}
          </Typography>
        </Stack>
        <Button color='primary' aria-label='upload picture' component='label'>
          <input
            hidden
            accept='.seq'
            type='file'
            onChange={(e) => {
              e.preventDefault()
              setSequence({ ...sequence, file: e.target.files ? e.target.files[0] : null })
            }}
          />
          Upload sequence
        </Button>

        <Button
          size='sm'
          sx={{ maxWidth: 120 }}
          onClick={(event) => {
            event.preventDefault()
            if (sequence.file == undefined || sequence.file == null) {
              showNotification({message: 'No file selected for upload.', type: 'warning'})
            }
            else if (sequence.name == '') {
              showNotification({message: 'No sequence name given.', type: 'warning'})
            }
            else if (sequence.description == '') {
              showNotification({message: 'No sequence description given.', type: 'warning'})
            }
            // else if (sequence.type == '') {
            //   showNotification({message: 'No sequence type given.', type: 'warning'})
            // }
            else {
              uploadSequence.mutate(sequence)
              props.setOpen(false)
            }
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
