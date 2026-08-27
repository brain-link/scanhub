import React from 'react'
import Box from '@mui/joy/Box'
import Grid from '@mui/joy/Grid'
import DeviceView from './DeviceView'
import SequenceView from './SequenceView'
import TemplatesView from './TemplatesView'

function LibraryView() {
    return (
        <Grid container columns={2} sx={{ flex: 1, width: '100%', height: '100%', overflow: 'hidden' }}>
            {/* Left column: DeviceView (top) and SequenceView (bottom) */}
            <Grid xs={1} sx={{
                height: '100%',
                borderRight: '1px solid',
                borderColor: 'divider',
                display: 'flex',
                flexDirection: 'column',
                overflow: 'hidden',
            }}>
                <Box sx={{
                    height: '50%',
                    borderBottom: '1px solid',
                    borderColor: 'divider',
                    overflow: 'auto',
                    display: 'flex',
                    flexDirection: 'column',
                }}>
                    <DeviceView />
                </Box>
                <Box sx={{
                    height: '50%',
                    overflow: 'auto',
                    display: 'flex',
                    flexDirection: 'column',
                }}>
                    <SequenceView />
                </Box>
            </Grid>

            {/* Right column: TemplatesView */}
            <Grid xs={1} sx={{
                height: '100%',
                overflow: 'hidden',
                display: 'flex',
                flexDirection: 'column',
            }}>
                <TemplatesView />
            </Grid>
        </Grid>
    )
}

export default LibraryView;
