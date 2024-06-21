/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * ExamTemplateItem.tsx is responsible for rendering an exam template item.
 */
import MoreHorizIcon from '@mui/icons-material/MoreHoriz'
import Card from '@mui/joy/Card'
import CardContent from '@mui/joy/CardContent'
import Dropdown from '@mui/joy/Dropdown'
import IconButton from '@mui/joy/IconButton'
import Menu from '@mui/joy/Menu'
import MenuButton from '@mui/joy/MenuButton'
import MenuItem from '@mui/joy/MenuItem'
import Typography from '@mui/joy/Typography'
import * as React from 'react'
import { useMutation } from 'react-query'

import LoginContext from '../LoginContext'
import { examApi } from '../api'
import { ExamOut } from '../generated-client/exam'
import { TemplateInterface } from '../interfaces/components.interface'

export default function ExamTemplateItem(prop: TemplateInterface<ExamOut>) {
  const [user] = React.useContext(LoginContext)

  const deleteExamTemplate = useMutation(async () => {
    await examApi
      .examDeleteApiV1ExamExamIdDelete(prop.data.id, { headers: { Authorization: 'Bearer ' + user?.access_token } })
      .then(() => {
        prop.onDeleted()
      })
  })

  return (
    <Card variant='outlined' sx={{ width: '100%' }}>
      <CardContent>
        <Dropdown>
          <MenuButton
            variant='plain'
            sx={{
              zIndex: 'snackbar',
              '--IconButton-size': '25px',
              position: 'absolute',
              top: '0.5rem',
              right: '0.5rem',
            }}
            slots={{ root: IconButton }}
          >
            <MoreHorizIcon />
          </MenuButton>
          <Menu id='context-menu' variant='plain' sx={{ zIndex: 'snackbar' }}>
            <MenuItem
              key='delete'
              onClick={() => {
                deleteExamTemplate.mutate()
              }}
            >
              Delete
            </MenuItem>
          </Menu>
        </Dropdown>

        <Typography level='title-md'>Exam: {prop.data.name}</Typography>

        <Typography level='body-sm' textColor='text.tertiary'>
          ID: {prop.data.id}
        </Typography>
        <Typography level='body-sm' textColor='text.tertiary'>
          Site: {prop.data.site}
        </Typography>
        <Typography level='body-sm' textColor='text.tertiary'>
          Address: {prop.data.address}
        </Typography>
        <Typography level='body-sm' textColor='text.tertiary'>
          Creator: {prop.data.creator}
        </Typography>
        <Typography level='body-sm' textColor='text.tertiary'>
          Created: {new Date(prop.data.datetime_created).toDateString()}
        </Typography>
        <Typography level='body-sm' textColor='text.tertiary'>
          Updated: {prop.data.datetime_updated ? new Date(prop.data.datetime_updated).toDateString() : '-'}
        </Typography>
      </CardContent>
    </Card>
  )
}
