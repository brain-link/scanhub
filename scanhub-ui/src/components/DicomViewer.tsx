/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * DicomViewer.tsx is responsible for rendering the DICOM viewport.
 * 
 * 
 * const volumeImageIds = Array.from({ length: numberOfFrames }, (_, i) => `${imageIds[0]}$?frame=${i + 1}`);
 * 
 * 
 * 
 */
import React from 'react'
import { useQuery } from '@tanstack/react-query'

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

import * as cornerstone from 'cornerstone-core';
import cornerstoneWADOImageLoader from 'cornerstone-wado-image-loader';

import DicomViewerToolbar from '../components/DicomViewerTools'
import initCornerstone from '../utils/InitCornerstone'
import LoginContext from '../LoginContext'

import { AcquisitionTaskOut, DAGTaskOut, TaskType } from '../openapi/generated-client/exam'
import { taskApi } from '../api'


initCornerstone()  // initialize cornerstone before first render cycle


function DicomViewer({taskId}: {taskId: string | undefined} ) {

  const [user] = React.useContext(LoginContext)

  if (taskId === undefined) {
    return (
      <Container maxWidth={false} sx={{ width: '50%', mt: 5, justifyContent: 'center' }}>
        <AlertItem title='Please select a reconstruction or processing task with a result to show a DICOM image.' type={Alerts.Info} />
      </Container>
    )
  }

  const { data: dicomImageIds = [] } = useQuery<string[]>({
    queryKey: ['tasks', taskId],
    enabled: !!taskId,
    queryFn: async () => {
      const { data } = await taskApi.getTaskApiV1ExamTaskTaskIdGet(taskId);
      // Only DAG tasks with results
      if (!data || data.task_type !== TaskType.Dag || !('results' in data) || !data.results?.length) return [];
      // Pick newest by datetime_created
      const latest = data.results.reduce(
        (a: { datetime_created: string }, b: { datetime_created: string }) =>
          new Date(a.datetime_created) > new Date(b.datetime_created) ? a : b
      );
      const instances = (latest.meta as any)?.instances;
      console.log("INSTANCES: ", instances)
      return Array.isArray(instances) ? instances : [instances].filter(Boolean);
    },
  });

  // Set state variables
  const [numberViewports, setNumberViewports] = React.useState<number>(1)
  const [activeViewportIndex, ] = React.useState<number>(0)

  // Define viewport reference
  const dicomElement = React.useRef<HTMLDivElement>(null);

  // const dicomImageId = 'wadouri:https://localhost:8443/dicom-proxy/fcc5ee5afaaf9c51/b73cfcb2da62/Vida_Head.MR.Comp_DR-Gain_DR.1005.1.2021.04.27.14.20.13.818.14380335.dcm'

  // Build URL deterministically
  // const dicomImageId = React.useMemo(
  //   () => `wadouri:${window.location.origin}/api/v1/exam/dicom/${taskId}`,
  //   [taskId]
  // );



  const tokenRef = React.useRef<string | undefined>(undefined);
  React.useEffect(() => {
    tokenRef.current = user?.access_token;
  }, [user?.access_token]);


  // wire the loader once
  React.useEffect(() => {
    cornerstoneWADOImageLoader.external.cornerstone = cornerstone;
    cornerstoneWADOImageLoader.configure({
      // send auth header (+ cookies if you use them)
      beforeSend: (xhr: XMLHttpRequest) => {
        const t = tokenRef.current;
        if (t) xhr.setRequestHeader('Authorization', `Bearer ${t}`);

        // Disable caching
        xhr.setRequestHeader('Cache-Control', 'no-cache');

        // xhr.withCredentials = true; // only if you rely on cookies
      },
      // useWebWorkers: true, // enable if you’ve set up worker paths properly
    });
  }, []);

  // enable once
  React.useEffect(() => {
    const el = dicomElement.current;
    if (!el) 
      return;
    try { cornerstone.getEnabledElement(el) }
    catch { cornerstone.enable(el) }
    return () => { 
      try { cornerstone.disable(el) }
      catch (e) { console.error('Failed to disable DICOM element', e) }
    };
  }, []);

  // load whenever imageId changes
  React.useEffect(() => {
    const el = dicomElement.current;
    if (!el) return;
    let cancelled = false;
    (async () => {
      try {
        console.log('viewportData: ', `wadouri:${dicomImageIds[0]}`)
        const image = await cornerstone.loadAndCacheImage(`wadouri:${dicomImageIds[0]}`);
        if (!cancelled) cornerstone.displayImage(el, image);
      } catch (e) {
        console.error('Failed to load DICOM', e);
      }
    })();
    return () => { cancelled = true; };
  }, [dicomImageIds]);

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
                id='dicomViewport'
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
