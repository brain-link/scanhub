/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 * 
 * DicomViewer.tsx is responsible for rendering the DICOM viewport.
 */

import GridViewSharpIcon from '@mui/icons-material/GridViewSharp'
import KeyboardArrowDown from '@mui/icons-material/KeyboardArrowDown'
import Card from '@mui/joy/Card'
import Divider from '@mui/joy/Divider'
import Grid from '@mui/joy/Grid'
import Option from '@mui/joy/Option'
import Select from '@mui/joy/Select'
import Sheet from '@mui/joy/Sheet'
import Stack from '@mui/joy/Stack'
import * as React from 'react'
import CornerstoneViewport from 'react-cornerstone-viewport'

import DicomViewerToolbar, { tools } from '../components/DicomViewerTools'
import initCornerstone from '../utils/InitCornerstone'
import { navigation } from '../utils/SizeVars'


function DicomViewer() {

  // Initialize cornerstone only once, when component is rendered for the first time
  React.useEffect(() => {
      initCornerstone()
  }, [])

  // Set state variables
  const [viewportIds, setViewportIds] = React.useState<number[]>([0])
  const [activeViewportIndex, setActiveViewportIndex] = React.useState<number>(0)
  // const [viewportData, setViewportData] = React.useState<string[]>(['', '', ''])
  
  // Set default viewport data for debugging
  const viewportData = [
    'https://marketing.webassets.siemens-healthineers.com/fcc5ee5afaaf9c51/b73cfcb2da62/Vida_Head.MR.Comp_DR-Gain_DR.1005.1.2021.04.27.14.20.13.818.14380335.dcm',
    'https://marketing.webassets.siemens-healthineers.com/fcc5ee5afaaf9c51/b73cfcb2da62/Vida_Head.MR.Comp_DR-Gain_DR.1005.1.2021.04.27.14.20.13.818.14380335.dcm'
  ]

  return (
      <Stack gap={1} sx={{ display: 'flex', flexDirection: 'column', flexGrow: 1, width: '100%', height: `calc(100vh - ${navigation.height})`, p: 1}}>
      <Card sx={{ display: 'flex', flexDirection: 'row', p: 0.4, pl: 1 }}>
        <Select
          variant='plain'
          indicator={<KeyboardArrowDown />}
          startDecorator={<GridViewSharpIcon />}
          defaultValue={[0]}
          onChange={(event, ids) => {
            ids ? setViewportIds(ids) : [0]
          }}
        >
          <Option value={[0]}>1 view</Option>
          <Option value={[0, 1]}>2 views</Option>
          {/* <Option value={[0, 1, 2]}>3 views</Option> */}
        </Select>
        <Divider orientation='vertical' />
        <DicomViewerToolbar />
      </Card>

      {/* Cornerstone viewports */}
      <Grid container spacing={1} alignItems='stretch' direction='row' sx={{ height: '100%' }}>
        {viewportIds.map((index) => (
          <Grid xs={12 / viewportIds.length} key={index}>
            <Card
              variant={index === activeViewportIndex ? 'outlined' : 'plain'}
              color={index === activeViewportIndex ? 'primary' : 'neutral'}
              sx={{ p: 0.5, bgcolor: '#000000', height: '100%', border: '5px solid' }}
            >
              {
                // The following condition checks, if some viewportData is defined for this index
                // If an invalid imageId is set to the CornerstoneViewport, the component does not work
                // properly. Thus the
                viewportData[index] ? (
                  <CornerstoneViewport
                    key={index}
                    imageIds={[`dicomweb:${viewportData[index]}`]}
                    tools={tools}
                    setViewportActive={() => {
                      setActiveViewportIndex(index)
                    }}

                    // >> Save the following code snippets for later, might be useful
                    // loadingIndicatorComponent={ CircularProgress }
                    // onWindowResize=
                    // imageIdIndex={ 0 }
                    // resizeRefreshMode={ "throttle" }
                    // loadingIndicatorComponent={CustomLoader}
                    // onElementEnabled={elementEnabledEvt => {
                    //     const cornerstoneElement = elementEnabledEvt.detail.element;
                    //     // Save this for later
                    //     setCornerstoneElement(cornerstoneElement);
                    //     // this.setState({
                    //     //     cornerstoneElement,
                    //     // });
                    //     // Wait for image to render, then invert it
                    //     cornerstoneElement.addEventListener(
                    //         'cornerstoneimagerendered',
                    //         imageRenderedEvent => {
                    //             const viewport = imageRenderedEvent.detail.viewport;
                    //             const invertedViewport = Object.assign({}, viewport, {
                    //                 invert: true,
                    //             });
                    //             cornerstone.setViewport(cornerstoneElement, invertedViewport);
                    //         }
                    //     );
                    // }}
                  />
                ) : (
                  <Sheet
                    onClick={() => {
                      setActiveViewportIndex(index)
                    }}
                    sx={{ width: '100%', height: '100%', bgcolor: '#000000' }}
                  />
                )
              }
            </Card>
          </Grid>
        ))}
      </Grid>
    </Stack>
  )
}

export default DicomViewer;