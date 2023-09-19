import * as React from 'react';

import CornerstoneViewport from "react-cornerstone-viewport"

import Stack from '@mui/joy/Stack';
import Sheet from '@mui/joy/Sheet';
import Card from '@mui/joy/Card';
import Divider from '@mui/joy/Divider';
import GridViewSharpIcon from '@mui/icons-material/GridViewSharp';
import KeyboardArrowDown from '@mui/icons-material/KeyboardArrowDown';
import Select from '@mui/joy/Select';
import Option from '@mui/joy/Option';
import Grid from '@mui/joy/Grid';

import ExamTree from '../components/ExamTree';
import DicomViewerToolbar, {tools} from '../components/DicomViewerTools';
import initCornerstone from '../utils/InitCornerstone';

import { navigation } from '../utils/size_vars';


function Viewer () {
    
    // Initialize cornerstone only once, when component is rendered for the first time
    React.useEffect(() => {
        initCornerstone();
    }, []);
    
    // Set state variables
    const [viewportIds, setViewportIds] = React.useState<number[]>([0]);
    const [activeViewportIndex, setActiveViewportIndex] = React.useState<number>(0);
    const [viewportData, setViewportData] = React.useState<string[]>(["", "", ""]);

    // >> Debugging
    // const debugDataPath = "https://marketing.webassets.siemens-healthineers.com/1800000000016144/8de2b3a4af48/IMA08_1800000000016144.IMA"
    // React.useEffect(() => {
    //     console.log("Viewport Index: ", activeViewportIndex)
    // }, [activeViewportIndex])

    // React.useEffect(() => {
    //     console.log("Viewport data: ", viewportData)
    // }, [viewportData])


    const handleDatapathSet = (datapath: string) => {
        if (datapath !== "") {
            // Make a copy of the current viewport data
            const newData = [...viewportData];
            // Set the new datapath
            newData[activeViewportIndex] = datapath;
            // Set the new state
            setViewportData(newData);
        }
    }

    return (

        <Stack direction="row" gap={1} sx={{ display: 'flex', p: 1.5, width: '100%', height: `calc(100vh - ${navigation.height})` }}>
            
            <ExamTree setDataPath={ handleDatapathSet } />

            <Stack gap={1} sx={{ display: 'flex', flexDirection: 'column', flexGrow: 1, width: '100%' }}>

                <Card sx={{ display: 'flex', flexDirection: 'row', p: 0.4, pl: 1 }}>
                    <Select
                        variant='plain'
                        indicator={<KeyboardArrowDown />}
                        startDecorator={<GridViewSharpIcon />}
                        defaultValue={[0]}
                        onChange={(event, ids) => { ids ? setViewportIds(ids) : [0] }}
                    >
                        <Option value={[0]}>1 view</Option>
                        <Option value={[0, 1]}>2 views</Option>
                        <Option value={[0, 1, 2]}>3 views</Option>
                    </Select>
                    <Divider orientation="vertical" />
                    <DicomViewerToolbar />
                </Card>

                {/* Cornerstone viewports */}
                <Grid container spacing={1} alignItems="stretch" direction="row" sx={{ height: '100%' }}>
                    {
                        viewportIds.map((index) => (
                            <Grid xs={ 12 / viewportIds.length } key={index}>
                                <Card
                                    variant={ index === activeViewportIndex ? "outlined" : "plain" }
                                    color={ index === activeViewportIndex ? "primary" : "neutral" }
                                    sx={{p: 0.5, bgcolor: "#000000", height: '100%', border: '5px solid'}}
                                >
                                    {
                                        // The following condition checks, if some viewportData is defined for this index
                                        // If an invalid imageId is set to the CornerstoneViewport, the component does not work
                                        // properly. Thus the 
                                        viewportData[index] ? <CornerstoneViewport
                                            key={ index }
                                            imageIds={ [`dicomweb:${viewportData[index]}`] }
                                            tools={ tools }
                                            setViewportActive={ () => { setActiveViewportIndex(index); } }

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

                                        /> : <Sheet 
                                            onClick={ () => { setActiveViewportIndex(index); }}
                                            sx={{ width: '100%', height: '100%', bgcolor: '#000000'}}
                                        /> 

                                    }
                                </Card>
                            </Grid>
                        ))
                    }
                </Grid>
            </Stack>
        </Stack>
    );
}

export default Viewer;