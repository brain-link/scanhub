/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * AccordionWithMenu.tsx is responsible for rendering an accordion type element, that can fold and unfold.
 * It differs from the regular MUI Accordion in that it allows to add a dropdown menu on the accordion summary.
 */
import React from 'react';
import Stack from '@mui/joy/Stack';
import IconButton from '@mui/joy/IconButton';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore'
import KeyboardArrowRightIcon from '@mui/icons-material/KeyboardArrowRight';
import Tooltip from '@mui/joy/Tooltip'

import { AccordionWithMenuInterface } from '../interfaces/components.interface';


export default function AccordionWithMenu(props: AccordionWithMenuInterface) {

  const [expanded, setExpanded] = React.useState(false);

  return (
    <Stack direction='column' width='100%'>
      <Stack direction='row' alignItems='center'>
        <Tooltip
          placement='right'
          variant='outlined'
          describeChild={false}
          arrow
          title={ props.toolTipContent }
          modifiers={[
            { name: 'offset', options: { offset: [0, 64] } }, // skidding=8 (down), distance=20 (further right)
          ]}
        >
          <Stack direction='row' alignItems='center' flexGrow={1}>
            <IconButton
              onClick={() => setExpanded(!expanded)}
            >
              {expanded ? <ExpandMoreIcon /> : <KeyboardArrowRightIcon />}
            </IconButton>
            { props.accordionSummary }
          </Stack>
        </Tooltip>
        { props.accordionMenu }
      </Stack>
      <Stack
        direction='column'
        sx={{ paddingLeft: 2 }}
      >
        {expanded ? props.children : undefined}
      </Stack>
      
    </Stack>
  )
}