// import CenterFocusWeakSharpIcon from '@mui/icons-material/CenterFocusWeakSharp'
// import DescriptionSharpIcon from '@mui/icons-material/DescriptionSharp'
import SnippetFolderSharpIcon from '@mui/icons-material/SnippetFolderSharp'
import { Typography } from '@mui/joy'
import Accordion from '@mui/joy/Accordion'
import AccordionDetails from '@mui/joy/AccordionDetails'
import AccordionGroup from '@mui/joy/AccordionGroup'
import AccordionSummary from '@mui/joy/AccordionSummary'
import Card from '@mui/joy/Card'
import CircularProgress from '@mui/joy/CircularProgress'
// import ListItem from '@mui/joy/ListItem'
// import ListItemButton from '@mui/joy/ListItemButton'
import ListItemContent from '@mui/joy/ListItemContent'
// import ListItemDecorator from '@mui/joy/ListItemDecorator'
import Stack from '@mui/joy/Stack'
import * as React from 'react'
import { useQuery } from 'react-query'
import { useParams } from 'react-router-dom'

import client from '../client/exam-tree-queries'
import { Alerts } from '../interfaces/components.interface'
// import { ExamTreeProps } from '../interfaces/components.interface'
import { Exam } from '../interfaces/data.interface'
import AlertItem from './AlertItem'

// function ExamTree({ setDataPath }: ExamTreeProps) {
function ExamTree() {
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
        <AlertItem title='Error loading exams' type={Alerts.Error} />
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

                  {/* <AccordionGroup variant='outlined' sx={{ maxWidth: 400, borderRadius: 'md' }}>
                    {exam.jobs?.map((job) => (
                      <Accordion key={`procedure-${job.id}`}>
                        <AccordionSummary>
                          <DescriptionSharpIcon />
                          <ListItemContent>
                            <Typography level='title-sm'>{job.type}</Typography>
                            <Typography level='body-xs'>{`Created: ${new Date(
                              job.datetime_created,
                            ).toDateString()}`}</Typography>
                            <Typography level='body-xs'>{`Updated: ${
                              job.datetime_updated ? new Date(job.datetime_updated).toDateString() : '-'
                            }`}</Typography>
                          </ListItemContent>
                        </AccordionSummary>

                        <AccordionDetails>
                          <Typography level='title-md'> Records </Typography>

                          {job.records?.map(
                            (record) =>
                              // Check if job has records
                              // Only display the last record for each job
                              record.records &&
                              record.records.length > 0 && (
                                <ListItem key={`record-${record.records[record.records.length - 1].id}`}>
                                  <ListItemButton
                                    id='record-entry'
                                    onClick={() => {
                                      const datapath = record.records[record.records.length - 1].data_path
                                      setDataPath(datapath)
                                    }}
                                  >
                                    <ListItemDecorator sx={{ align: 'center', justify: 'center' }}>
                                      <CenterFocusWeakSharpIcon />
                                    </ListItemDecorator>

                                    <ListItemContent>
                                      <Typography level='title-sm'>{record.type}</Typography>
                                      <Typography level='title-sm'>
                                        {record.records[record.records.length - 1]
                                          ? record.records[record.records.length - 1].comment
                                          : '-'}
                                      </Typography>
                                      <Typography level='body-xs'>
                                        {`Created: ${new Date(
                                          record.records[record.records.length - 1].datetime_created,
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
                  </AccordionGroup> */}
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
