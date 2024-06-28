/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * ExamInstanceInfo.tsx is responsible for rendering additional information#
 * of an exam instance item.
 */
import Box from '@mui/joy/Box'
import Chip from '@mui/joy/Chip'
import Stack from '@mui/joy/Stack'
import Typography from '@mui/joy/Typography'
import * as React from 'react'
// import IconButton from '@mui/joy/IconButton'
// import MoreHorizIcon from '@mui/icons-material/MoreHoriz'
// import Dropdown from '@mui/joy/Dropdown'
// import Menu from '@mui/joy/Menu'
// import MenuButton from '@mui/joy/MenuButton'
// import MenuItem from '@mui/joy/MenuItem'
import { useMutation } from 'react-query'

import { ExamOut } from '../generated-client/exam'
// import ExamModal from './ExamModal'
import LoginContext from '../LoginContext'
import { examApi } from '../api'
import { InstanceInterface } from '../interfaces/components.interface'
import { Button } from '@mui/joy'

function ExamInstanceInfo({ data: exam, refetchParentData }: InstanceInterface<ExamOut>) {
  const [user] = React.useContext(LoginContext)
  // const [examModalOpen, setExamModalOpen] = React.useState(false)

  const deleteExam = useMutation(async () => {
    await examApi
      .examDeleteApiV1ExamExamIdDelete(exam.id, { headers: { Authorization: 'Bearer ' + user?.access_token } })
      .then(() => {
        refetchParentData()
      })
  })

  // const updateExam = useMutation(async (data: Exam) => {
  //   await client.examService
  //     .update(data.id, data)
  //     .then(() => {
  //       refetchParentData()
  //     })
  //     .catch((err) => {
  //       console.log('Error on exam update: ', err)
  //     })
  // })

  return (
    <Box sx={{display: 'flex', alignItems: 'stretch'}}>
      <Box sx={{display: 'flex', flexDirection: 'column', justifyContent: 'center'}}>
        <Button key='edit' onClick={() => {}} variant='outlined'>
          Edit
        </Button>
        <Button
          key='delete'
          onClick={() => {
            deleteExam.mutate()
          }}
          variant='outlined'
        >
          Delete
        </Button>
      </Box>
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
        <Typography fontSize='sm'>Name</Typography>
        <Typography level='body-sm' textColor='text.primary'>
          {exam.name}
        </Typography>

        <Typography fontSize='sm'>ID</Typography>
        <Typography level='body-sm' textColor='text.primary'>
          {exam.id}
        </Typography>

        <Typography fontSize='sm'>Note</Typography>
        <Typography level='body-sm' textColor='text.primary'>
          {exam.status}
        </Typography>

        <Typography fontSize='sm'>Issuer</Typography>
        <Typography level='body-sm' textColor='text.primary'>
          {exam.creator}
        </Typography>

        <Typography fontSize='sm'>Site</Typography>
        <Typography level='body-sm' textColor='text.primary'>
          {exam.site}
        </Typography>

        <Typography fontSize='sm'>Created</Typography>
        <Typography level='body-sm' textColor='text.primary'>
          {new Date(exam.datetime_created).toDateString()}
        </Typography>

        <Typography fontSize='sm'>Updated</Typography>
        <Typography level='body-sm' textColor='text.primary'>
          {exam.datetime_updated ? new Date(exam.datetime_updated).toDateString() : '-'}
        </Typography>

        <Typography fontSize='sm'>Status</Typography>
        <Stack direction='row' spacing={0.5}>
          <Chip size='sm' color={exam.is_template ? 'success' : 'danger'} sx={{ fontWeight: 'lg' }}>
            Template
          </Chip>
          <Chip size='sm' color={exam.is_frozen ? 'success' : 'danger'} sx={{ fontWeight: 'lg' }}>
            Frozen
          </Chip>
        </Stack>
      </Box>

      {/* <ExamModal
        data={exam}
        dialogOpen={examModalOpen}
        setDialogOpen={setExamModalOpen}
        handleModalSubmit={(data: Exam) => {
          updateExam.mutate(data)
        }}
      /> */}
    </Box>
  )
}

export default ExamInstanceInfo
