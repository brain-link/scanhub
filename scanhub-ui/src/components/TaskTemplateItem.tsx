/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 * 
 * TaskTemplateItem.tsx is responsible for rendering a task template item.
 */

import * as React from 'react'
import { useMutation } from 'react-query'

import Typography from '@mui/joy/Typography'
import Card from '@mui/joy/Card'
import CardContent from '@mui/joy/CardContent'
import Accordion from '@mui/joy/Accordion'
import AccordionSummary from '@mui/joy/AccordionSummary'
import AccordionDetails from '@mui/joy/AccordionDetails'
import Dropdown from '@mui/joy/Dropdown';
import MenuButton from '@mui/joy/MenuButton';
import IconButton from '@mui/joy/IconButton'
import MenuItem from '@mui/joy/MenuItem';
import Menu from '@mui/joy/Menu'
import MoreHorizIcon from '@mui/icons-material/MoreHoriz'

import LoginContext from '../LoginContext'
import { TaskOut } from '../generated-client/exam';
import { TemplateItemInterface } from '../interfaces/components.interface'
import { taskApi } from '../api'


export default function TaskTemplateItem(prop: TemplateItemInterface<TaskOut>) {

  const [user, ] = React.useContext(LoginContext)

  const deleteTaskTemplate = useMutation(async () => {
    await taskApi.deleteTaskApiV1ExamTaskTaskIdDelete(
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
              <MenuItem key='delete' onClick={() => {deleteTaskTemplate.mutate()}}>
                Delete
              </MenuItem>
            </Menu>
          </Dropdown>
          <Typography level="title-md">Task</Typography>

          <Typography level='body-sm' textColor='text.tertiary'>ID: { prop.item.id }</Typography>
          <Typography level='body-sm' textColor='text.tertiary'>Workflow ID: { prop.item.workflow_id }</Typography>
          <Typography level='body-sm' textColor='text.tertiary'>Type: { prop.item.type }</Typography>
          <Typography level='body-sm' textColor='text.tertiary'>Description: { prop.item.description }</Typography>
          <Typography level='body-sm' textColor='text.tertiary'>Created: { new Date(prop.item.datetime_created).toDateString() }</Typography>

          {/* TODO: Add updated datetime to tasks? */}
          {/* <Typography level='body-sm' textColor='text.tertiary'>Updated: { prop.item.datetime_updated ? new Date(prop.item.datetime_updated).toDateString() : '-'}</Typography> */}

          {/* Arguments: dict[str, str] */}
          <Accordion>
            <AccordionSummary>
              <Typography level='body-sm' textColor='text.tertiary'>Arguments</Typography>
            </AccordionSummary>
            <AccordionDetails>
              {
                prop.item.args && Object.entries(prop.item.args).map((arg, index) => (
                  <Typography key={index} level='body-sm' textColor='text.tertiary'>{arg[0]}: {arg[1]}</Typography>
                ))
              }
            </AccordionDetails>
          </Accordion>
          
          {/* Artifacts: dict[str, list[dict[str, str]]] */}
          <Accordion>
            <AccordionSummary>
              <Typography level='body-sm' textColor='text.tertiary'>Artifacts</Typography>
            </AccordionSummary>
            <AccordionDetails>
              {
                prop.item.artifacts && Object.entries(prop.item.artifacts).map((artifact, index) => (
                  <Typography key={index} level='body-sm' textColor='text.tertiary'>{artifact[0]}: {artifact[1]}</Typography>
                ))
              }
            </AccordionDetails>
            {/* <AccordionDetails>
              <AccordionGroup>
                {
                  // Iterate outer dict
                  prop.item.artifacts && Object.entries(prop.item.artifacts).map((artifact, index) => (
                  
                    <Accordion key={index}>
                      <AccordionSummary>
                        <Typography level='body-sm' textColor='text.tertiary'>{artifact[0]}</Typography>
                      </AccordionSummary>
                      
                      <AccordionDetails>
                        {
                          // Iterate through list of outer dict
                          artifact[1].map((artifact_entry, index) => (
                            <Accordion key={index}>
                              <AccordionSummary>
                                <Typography level='body-sm' textColor='text.tertiary'>{artifact[0]} {index+1}</Typography>
                              </AccordionSummary>
                              <AccordionDetails>
                                {
                                  // Iterate inner dict
                                  artifact_entry && Object.entries(artifact_entry).map((desc, index2) => (
                                    <Typography key={index2} level='body-sm' textColor='text.tertiary'>{desc[0]}: {desc[1]}</Typography>
                                  ))
                                }
                              </AccordionDetails>
                            </Accordion>
                          ))
                        }
                      </AccordionDetails>
                    </Accordion>
                  ))
                }
              </AccordionGroup>
            </AccordionDetails> */}
          </Accordion>
          
          {/* Destinations: list[dict[str, str]] */}
          <Accordion>
            <AccordionSummary>
              <Typography level='body-sm' textColor='text.tertiary'>Destinations</Typography>
            </AccordionSummary>
            <AccordionDetails>
              {
                prop.item.destinations && Object.entries(prop.item.destinations).map((destination, index) => (
                  <Typography key={index} level='body-sm' textColor='text.tertiary'>{destination[0]}: {destination[1]}</Typography>
                ))
              }
            </AccordionDetails>
            {/* <AccordionDetails>
              <AccordionGroup>
                {
                  prop.item.task_destinations.map((destination, index) => (
                    <Accordion key={index}>
                      <AccordionSummary>
                        <Typography level='body-sm' textColor='text.tertiary'>Destination {index+1}</Typography>
                      </AccordionSummary>
                      <AccordionDetails>
                        {
                          destination && Object.entries(destination).map((values, index2) => (
                            <Typography key={index2} level='body-sm' textColor='text.tertiary'>{values[0]}: {values[1]}</Typography>
                          ))
                        }
                      </AccordionDetails>
                    </Accordion>
                  ))
                }
              </AccordionGroup>
            </AccordionDetails> */}
          </Accordion>

      </CardContent>
    </Card>
  )
}

