// Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
// SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
// PatientTable.tsx is responsible for rendering the patient table view.
import * as React from 'react'

import Typography from '@mui/joy/Typography'
import Card from '@mui/joy/Card'
import CardContent from '@mui/joy/CardContent'
import Accordion from '@mui/joy/Accordion'
import AccordionSummary from '@mui/joy/AccordionSummary'
import AccordionDetails from '@mui/joy/AccordionDetails'

import { TaskOut } from "../generated-client/exam";
import { TemplateItemInterface } from '../interfaces/components.interface'


export default function TaskTemplateItem(prop: TemplateItemInterface<TaskOut>) {

  return (
    <Card variant="outlined">
        <CardContent>
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
              prop.item.args && Object.entries(prop.item.args).map((arg) => (
                <Typography level='body-sm' textColor='text.tertiary'>{arg[0]}: {arg[1]}</Typography>
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
              // Iterate outer dict
              prop.item.artifacts && Object.entries(prop.item.artifacts).map((artifact) => (
                <Accordion>
                  <AccordionSummary>
                    <Typography level='body-sm' textColor='text.tertiary'>{artifact[0]}</Typography>
                  </AccordionSummary>
                  <AccordionDetails>
                    {
                      // Iterate through list of outer dict
                      artifact[1].map((artifact_entry, index) => (
                        <Accordion>
                          <AccordionSummary>
                            <Typography level='body-sm' textColor='text.tertiary'>{index}</Typography>
                          </AccordionSummary>
                          <AccordionDetails>
                            {
                              // Iterate inner dict
                              artifact_entry && Object.entries(artifact_entry).map((desc) => (
                                <Typography level='body-sm' textColor='text.tertiary'>{desc[0]}: {desc[1]}</Typography>
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
          </AccordionDetails>
        </Accordion>
        
        {/* Destinations: list[dict[str, str]] */}
        <Accordion>
          <AccordionSummary>
            <Typography level='body-sm' textColor='text.tertiary'>Destinations</Typography>
          </AccordionSummary>
          <AccordionDetails>
            {
              prop.item.task_destinations.map((destination, index) => (
                <Accordion>
                  <AccordionSummary>
                    <Typography level='body-sm' textColor='text.tertiary'>{index}</Typography>
                  </AccordionSummary>
                  <AccordionDetails>
                    {
                      destination && Object.entries(destination).map((values) => (
                        <Typography level='body-sm' textColor='text.tertiary'>{values[0]}: {values[1]}</Typography>
                      ))
                    }
                  </AccordionDetails>
                </Accordion>
              ))
            }
          </AccordionDetails>
        </Accordion>

      </CardContent>
    </Card>
  )
}

