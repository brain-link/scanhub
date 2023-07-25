// Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
// SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

// SequenceViewer.tsx is responsible for rendering an mri sequence.

import { useQuery } from "react-query"
import { useNavigate } from "react-router-dom";
import React from "react"
import Plot from 'react-plotly.js';
import { PlotData, MRISequence } from '../../interfaces/mri-data.interface';
import Box from '@mui/joy/Box';
import Stack from '@mui/joy/Stack';
import ArrowBackSharpIcon from '@mui/icons-material/ArrowBackSharp';
import FileDownloadSharpIcon from '@mui/icons-material/FileDownloadSharp';
import IconButton from '@mui/joy/IconButton';
import { SequenceViewerProps } from "../../interfaces/components.interface";
import sequenceClient from '../../client/sequence-api';
import Typography from "@mui/joy/Typography";



function SequenceViewer({sequence_id}: SequenceViewerProps) {
    
    const navigate = useNavigate();

    const { data: sequencePlot, isLoading: sequencePlotIsLoading, isError: sequencePlotIsError } = useQuery<PlotData>({
        queryKey: ['sequence-plot', sequence_id], 
        queryFn: () => sequenceClient.getSequencePlot(sequence_id)
    });

    const { data: sequenceMeta, isLoading: sequenceMetaIsLoading, isError: sequenceMetaIsError } = useQuery<MRISequence>({
        queryKey: ['sequence-meta', sequence_id], 
        queryFn: () => sequenceClient.getSequenceMeta(sequence_id)
    });


    React.useEffect(() => {
        if (sequencePlot) {
            sequencePlot.layout.width = window.innerWidth;
            sequencePlot.layout.height = window.innerHeight - 150;
        }
    }, [sequencePlot])

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
                sequenceMeta && !sequenceMetaIsLoading && !sequenceMetaIsError &&
                <Box
                    sx={{
                        rowGap: 0.4,
                        columnGap: 4,
                        p: 2,
                        display: 'grid',
                        gridTemplateColumns: 'auto 1fr',
                        '& > *:nth-child(odd)': { 
                            color: 'text.secondary' 
                        },
                    }}
                >

                    <Typography level="body2">Sequence</Typography>
                    <Typography level="body2" textColor="text.primary">
                        { sequenceMeta.name }
                    </Typography>

                    <Typography level="body2">Uploaded</Typography>
                    <Typography level="body2" textColor="text.primary">
                        { sequenceMeta.created_at ? new Date(sequenceMeta.created_at).toDateString() : '-' }
                    </Typography>
                </Box>
            }
            
            { 
                // Wait until sequences is loaded
                sequencePlotIsLoading ? <div>Loading sequence...</div> : (
                    // Check for errors if sequence has been loaded
                    sequencePlotIsError ? <div>No sequence...</div> : 
                        <Plot data={sequencePlot?.data} layout={sequencePlot?.layout} useResizeHandler={true} />
                )                     
            }

        </Stack>
    );
}

export default SequenceViewer;
