import CenterFocusWeakSharpIcon from '@mui/icons-material/CenterFocusWeakSharp'
import DescriptionSharpIcon from '@mui/icons-material/DescriptionSharp'
import SnippetFolderSharpIcon from '@mui/icons-material/SnippetFolderSharp'
import { Typography } from '@mui/joy'
import Accordion from '@mui/joy/Accordion'
import AccordionDetails from '@mui/joy/AccordionDetails'
import AccordionGroup from '@mui/joy/AccordionGroup'
import AccordionSummary from '@mui/joy/AccordionSummary'
import Card from '@mui/joy/Card'
import CircularProgress from '@mui/joy/CircularProgress'
import ListItem from '@mui/joy/ListItem'
import ListItemButton from '@mui/joy/ListItemButton'
import ListItemContent from '@mui/joy/ListItemContent'
import ListItemDecorator from '@mui/joy/ListItemDecorator'
import Stack from '@mui/joy/Stack'
import * as React from 'react'
import { useQuery } from 'react-query'
import { useParams } from 'react-router-dom'

import client from '../client/exam-tree-queries'
import { Alerts } from '../interfaces/components.interface'
import { ExamTreeProps } from '../interfaces/components.interface'
import { Exam } from '../interfaces/data.interface'
import AlertItem from './AlertItem'

function ExamTree({ setDataPath }: ExamTreeProps) {
  const params = useParams()

  const {
    data: exams,
    // refetch,
    isLoading,
    isError,
  } = useQuery<Exam[], Error>({
    queryKey: ['exam', params.patientId],
    queryFn: () => client.examService.getAll(Number(params.patientId)),
  })

  return (
    <Stack sx={{ minWidth: '300px' }}>
      <Stack sx={{ mb: 2 }}>
        <Typography level='title-lg'> Exam Tree </Typography>
        <Typography level='body-md'> Patient ID: {params.patientId} </Typography>
      </Stack>

      {isLoading ? (
        <CircularProgress />
      ) : isError ? (
        <AlertItem title='Error loading exams' type={Alerts.Danger} />
      ) : (
        <Card sx={{ p: 0 }}>
          <AccordionGroup>
            {exams?.map((exam) => (
              <Accordion key={`exam-${exam.id}`}>
                <AccordionSummary>
                  <SnippetFolderSharpIcon />
                  <ListItemContent>
                    <Typography level='title-sm'>{exam.name}</Typography>
                    <Typography level='body-sm'>{exam.status}</Typography>
                    <Typography level='body-xs'>{`Created: ${new Date(
                      exam.datetime_created,
                    ).toDateString()}`}</Typography>
                    <Typography level='body-xs'>{`Updated: ${
                      exam.datetime_updated ? new Date(exam.datetime_updated).toDateString() : '-'
                    }`}</Typography>
                  </ListItemContent>
                </AccordionSummary>

                <AccordionDetails>
                  <Typography level='title-md'> Procedures </Typography>

                  <AccordionGroup variant='outlined' sx={{ maxWidth: 400, borderRadius: 'md' }}>
                    {exam.procedures?.map((procedure) => (
                      <Accordion key={`procedure-${procedure.id}`}>
                        <AccordionSummary>
                          <DescriptionSharpIcon />
                          <ListItemContent>
                            <Typography level='title-sm'>{procedure.name}</Typography>
                            <Typography level='body-xs'>{`Created: ${new Date(
                              procedure.datetime_created,
                            ).toDateString()}`}</Typography>
                            <Typography level='body-xs'>{`Updated: ${
                              procedure.datetime_updated ? new Date(procedure.datetime_updated).toDateString() : '-'
                            }`}</Typography>
                          </ListItemContent>
                        </AccordionSummary>

                        <AccordionDetails>
                          <Typography level='title-md'> Records </Typography>

                          {procedure.jobs?.map(
                            (job) =>
                              // Check if job has records
                              // Only display the last record for each job
                              job.records &&
                              job.records.length > 0 && (
                                <ListItem key={`record-${job.records[job.records.length - 1].id}`}>
                                  <ListItemButton
                                    id='record-entry'
                                    onClick={() => {
                                      const datapath = job.records[job.records.length - 1].data_path
                                      setDataPath(datapath)
                                    }}
                                  >
                                    <ListItemDecorator sx={{ align: 'center', justify: 'center' }}>
                                      <CenterFocusWeakSharpIcon />
                                    </ListItemDecorator>

                                    <ListItemContent>
                                      <Typography level='title-sm'>{job.type}</Typography>
                                      <Typography level='title-sm'>
                                        {job.records[job.records.length - 1]
                                          ? job.records[job.records.length - 1].comment
                                          : '-'}
                                      </Typography>
                                      <Typography level='body-xs'>
                                        {`Created: ${new Date(
                                          job.records[job.records.length - 1].datetime_created,
                                        ).toDateString()}`}
                                      </Typography>
                                    </ListItemContent>
                                  </ListItemButton>
                                </ListItem>
                              ),
                          )}
                        </AccordionDetails>
                      </Accordion>
                    ))}
                  </AccordionGroup>
                </AccordionDetails>
              </Accordion>
            ))}
          </AccordionGroup>
        </Card>
      )}
    </Stack>
  )
}

export default ExamTree
