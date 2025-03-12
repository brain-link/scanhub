/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * DicomViewer.tsx is responsible for rendering the DICOM viewport.
 */
import { taskApi } from '../api'
import GridViewSharpIcon from '@mui/icons-material/GridViewSharp'
import KeyboardArrowDown from '@mui/icons-material/KeyboardArrowDown'
import Card from '@mui/joy/Card'
import Divider from '@mui/joy/Divider'
import Grid from '@mui/joy/Grid'
import Option from '@mui/joy/Option'
import Select from '@mui/joy/Select'
import Stack from '@mui/joy/Stack'
import Container from '@mui/joy/Container'
import AlertItem from '../components/AlertItem'
import { Alerts } from '../interfaces/components.interface'
import * as React from 'react'
import { useQuery } from 'react-query'

import DicomViewerToolbar from '../components/DicomViewerTools'
import initCornerstone from '../utils/InitCornerstone'
import { TaskOut } from '../generated-client/exam'

import * as cornerstone from 'cornerstone-core';
import cornerstoneWADOImageLoader from 'cornerstone-wado-image-loader';


initCornerstone()  // initialize cornerstone before first render cycle


function DicomViewer({task_id}: {task_id: string | undefined} ) {

  if (task_id === undefined) {
    return (
      <Container maxWidth={false} sx={{ width: '50%', mt: 5, justifyContent: 'center' }}>
        <AlertItem title='Please select a reconstruction or processing task with a result to show a DICOM image.' type={Alerts.Info} />
      </Container>
    )
  }

  // Query the result by id
  const {
    data: task,
    // refetch: refetchResult,
    isError,
  } = useQuery<TaskOut, Error>({
    queryKey: ['task', task_id],
    queryFn: async () => {
      return await taskApi.getTaskApiV1ExamTaskTaskIdGet(task_id).then((result) => {
        return result.data
      })
    },
  })

  if (task === undefined || isError){
    <Container maxWidth={false} sx={{ width: '50%', mt: 5, justifyContent: 'center' }}>
      <AlertItem title={'Could not load task with ID: ' + task_id} type={Alerts.Error} />
    </Container>
  }
  
  if (task?.results && task.results.length > 0){
    console.log("Task result: ", task.results[task.results.length-1].directory, task.results[task.results.length-1].filename)
  }

  // Set state variables
  const [numberViewports, setNumberViewports] = React.useState<number>(1)
  const [activeViewportIndex, setActiveViewportIndex] = React.useState<number>(0)

  // Define viewport reference
  const dicomElement = React.useRef<HTMLDivElement>(null);

  // const dicomImageId = 'wadouri:marketing.webassets.siemens-healthineers.com/fcc5ee5afaaf9c51/b73cfcb2da62/Vida_Head.MR.Comp_DR-Gain_DR.1005.1.2021.04.27.14.20.13.818.14380335.dcm'
  const dicomImageId = 'wadouri:http://localhost:8080/api/v1/exam/dicom/' + task?.results[task.results.length-1].id
  console.log("viewportData: ", dicomImageId)


  React.useEffect(() => {
    cornerstoneWADOImageLoader.external.cornerstone = cornerstone;

    // cornerstoneWADOImageLoader.configure({useWebWorkers: true})

    const enableViewport = async () => {
      if (!dicomElement.current) return;

      cornerstone.enable(dicomElement.current);

      const image = await cornerstone.loadAndCacheImage(dicomImageId);
      cornerstone.displayImage(dicomElement.current, image)

    }
    enableViewport();

  }, [task])

  return (
    <Stack
      gap={1}
      sx={{
        display: 'flex',
        flexDirection: 'column',
        flexGrow: 1,
        width: '100%',
        height: 'calc(100vh - var(--Navigation-height))',
        p: 1,
      }}
    >
      <Card sx={{ display: 'flex', flexDirection: 'row', p: 0.4, pl: 1 }}>
        <Select
          variant='plain'
          indicator={<KeyboardArrowDown />}
          startDecorator={<GridViewSharpIcon />}
          defaultValue={1}
          onChange={(event, ids) => {
            if (ids) {
              setNumberViewports(ids)
            }
          }}
        >
          <Option value={1}>1 view</Option>
          <Option value={2}>2 views</Option>
          {/* <Option value={3}>3 views</Option> */}
        </Select>
        <Divider orientation='vertical' />
        <DicomViewerToolbar />
      </Card>

      {/* Cornerstone viewports */}
      <Grid container spacing={1} alignItems='stretch' direction='row' sx={{ height: '100%' }}>
        {Array.from(Array(numberViewports).keys()).map((index) => (
          <Grid xs={12 / numberViewports} key={index}>
            <Card
              variant={index === activeViewportIndex ? 'outlined' : 'plain'}
              color={index === activeViewportIndex ? 'primary' : 'neutral'}
              sx={{ p: 0.5, bgcolor: '#000000', height: '100%', border: '5px solid' }}
            >
              <div
                ref={dicomElement}
                id="dicomViewport"
                style={{width: '100%', height: '100%', backgroundColor: 'black'}}
              />
            </Card>
          </Grid>
        ))}
      </Grid>
    </Stack>
  )
}

export default DicomViewer
