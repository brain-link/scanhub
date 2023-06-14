import { useQuery } from "react-query"
import { useNavigate } from "react-router-dom";
import React from "react"
import Plot from 'react-plotly.js';
import { PlotData } from '../../interfaces/mri-data.interface';
import Box from '@mui/joy/Box';
import Stack from '@mui/joy/Stack';
import ArrowBackSharpIcon from '@mui/icons-material/ArrowBackSharp';
import FileDownloadSharpIcon from '@mui/icons-material/FileDownloadSharp';
import IconButton from '@mui/joy/IconButton';
import { SequenceViewerProps } from "../../interfaces/components.interface";
import sequenceClient from '../../client/mri-queries';
import Typography from "@mui/joy/Typography";



function SequenceViewer({sequence_id}: SequenceViewerProps) {
    
    const navigate = useNavigate();

    const { data, isLoading, isError } = useQuery<PlotData>({
        queryKey: ['sequence-plot', sequence_id], 
        queryFn: () => sequenceClient.getSequencePlot(sequence_id)
    });


    React.useEffect(() => {
        if (data) {
            data.layout.width = window.innerWidth;
            data.layout.height = window.innerHeight - 150;
        }
    }, [data])


    if (isLoading) {
        return (
            <div>Loading sequence...</div>
        )
    }

    if (data && !isError) {
        return (
            <Stack sx={{ overflow: 'clip' }}>

                <Box sx={{ m: 2, display: 'flex', justifyContent: 'space-between'}}>
                    <IconButton
                        variant='soft'
                        onClick={ () => { navigate(-1); } }
                    >
                        <ArrowBackSharpIcon/>
                    </IconButton>

                    <IconButton
                        variant='soft'
                        onClick={ () => {} }
                    >
                        <FileDownloadSharpIcon/>
                    </IconButton>
                </Box>
                
                <Plot data={data.data} layout={data.layout} useResizeHandler={true} />

            </Stack>
        );
    } else {
        return (
            <div>No sequence...</div>
        )
    }
}

export default SequenceViewer;
