/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 * 
 * ExamTemplateItem.tsx is responsible for rendering an exam template item.
 */

import * as React from 'react'
import { useMutation } from 'react-query'

import Typography from '@mui/joy/Typography'
import Card from '@mui/joy/Card'
import CardContent from '@mui/joy/CardContent'
import Dropdown from '@mui/joy/Dropdown';
import MenuButton from '@mui/joy/MenuButton';
import IconButton from '@mui/joy/IconButton'
import MenuItem from '@mui/joy/MenuItem';
import Menu from '@mui/joy/Menu'
import MoreHorizIcon from '@mui/icons-material/MoreHoriz'

import LoginContext from '../LoginContext'
import { ExamOut } from '../generated-client/exam';
import { TemplateItemInterface } from '../interfaces/components.interface'
import { examApi } from '../api';


export default function ExamTemplateItem(prop: TemplateItemInterface<ExamOut>) {

  const [user, ] = React.useContext(LoginContext)

  const deleteExamTemplate = useMutation(async () => {
    await examApi.examDeleteApiV1ExamExamIdDelete(
      prop.item.id, {headers: {Authorization: 'Bearer ' + user?.access_token}}
    ).then(() => {
      prop.onDeleted()
    })
  })

  return (
    <Card variant="outlined" sx={{ width: '100%' }}>
        <CardContent>

          <Dropdown>
            <MenuButton variant='plain' sx={{zIndex: 'snackbar', '--IconButton-size': '25px', position: 'absolute', top: '0.5rem', right: '0.5rem'}} slots={{root: IconButton}}>
              <MoreHorizIcon />
            </MenuButton>
            <Menu
              id='context-menu'
              variant='plain'
              sx={{ zIndex: 'snackbar' }}
            >
              <MenuItem key='delete' onClick={() => {deleteExamTemplate.mutate()}}>
                Delete
              </MenuItem>
            </Menu>
          </Dropdown>

          <Typography level="title-md">Exam: { prop.item.name }</Typography>
          
          <Typography level='body-sm' textColor='text.tertiary'>ID: { prop.item.id }</Typography>
          <Typography level='body-sm' textColor='text.tertiary'>Site: { prop.item.site }</Typography>
          <Typography level='body-sm' textColor='text.tertiary'>Address: { prop.item.address }</Typography>
          <Typography level='body-sm' textColor='text.tertiary'>Creator: { prop.item.creator }</Typography>
          <Typography level='body-sm' textColor='text.tertiary'>Created: { new Date(prop.item.datetime_created).toDateString() }</Typography>
          <Typography level='body-sm' textColor='text.tertiary'>Updated: { prop.item.datetime_updated ? new Date(prop.item.datetime_updated).toDateString() : '-'}</Typography>

        </CardContent>
    </Card>
  )
}
