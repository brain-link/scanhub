// Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
// SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

// SequenceViewer.tsx is responsible for rendering an mri sequence.

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

    return (
        <Stack sx={{ overflow: 'clip' }}>

            <Box sx={{ m: 2, gap: 2, display: 'flex', justifyContent: 'space-between'}}>
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
            
            { 
                // Wait until sequences is loaded
                isLoading ? <div>Loading sequence...</div> : (
                    // Check for errors if sequence has been loaded
                    isError ? <div>No sequence...</div> : <Plot data={data?.data} layout={data?.layout} useResizeHandler={true} />
                )                     
            }

        </Stack>
    );
}

export default SequenceViewer;
