import React from 'react';
import Stack from '@mui/joy/Stack';
import IconButton from '@mui/joy/IconButton';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore'
import KeyboardArrowLeftIcon from '@mui/icons-material/KeyboardArrowLeft';

import { AccordionWithMenuInterface } from '../interfaces/components.interface';


export default function AccordionWithMenu(props: AccordionWithMenuInterface) {

    const [expanded, setExpanded] = React.useState(false);

    return (
        <Stack direction='column' width='100%'>
            <Stack direction='row' alignItems='center' justifyContent='space-between'>
                {props.accordionSummary}
                <Stack direction='row' alignItems='center'>
                    {props.accordionMenu}
                    <IconButton
                        onClick={() => setExpanded(!expanded)}
                    >
                        {expanded ? <ExpandMoreIcon /> : <KeyboardArrowLeftIcon />}
                    </IconButton>
                </Stack>
            </Stack>
            <Stack
                direction='column'
                sx={{ paddingLeft: 3 }}
            >
                {expanded ? props.children : undefined}
            </Stack>
        </Stack>
    )
}