/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * DicomViewerTools.tsx is responsible for rendering a toolbar for the dicom viewer.
 */
import React from 'react'

// Icons
// import Divider from '@mui/joy/Divider'
import IconButton from '@mui/joy/IconButton'
import ToggleButtonGroup from '@mui/joy/ToggleButtonGroup'
import { Enums } from '@cornerstonejs/tools';
import { getLinkedToolGroup, tools } from './cornerstone/toolgroups';


function DiconViewerToolbar() {
  const [activeTool, setActiveTool] = React.useState<string | null>(null)

	const toolGroup = React.useMemo(() => getLinkedToolGroup(), [])

  React.useEffect(() => {
    if (activeTool && toolGroup) {
      // Set all tools passive
      tools.forEach(({ Tool }) => toolGroup.setToolPassive(Tool.toolName, {removeAllBindings: [{ mouseButton: Enums.MouseBindings.Primary }]}));
      // Activate selected tool
      toolGroup.setToolActive(activeTool, {
				bindings: [{ mouseButton: Enums.MouseBindings.Primary }],
			});
    }
  }, [activeTool, toolGroup])

  return (
    <ToggleButtonGroup
      variant="plain"
      spacing={0.5}
      value={activeTool}
      onChange={(_event, tool: string | null) => {
        setActiveTool(tool) // tool may be null on deselect
      }}
      aria-label="viewer tools"
    >
      {tools.map(({ Tool, Icon, label }) => (
        <IconButton
          key={Tool.toolName}
          value={Tool.toolName}
          aria-label={label ?? Tool.toolName}
          title={label ?? Tool.toolName}
        >
          <Icon fontSize="small"/>
        </IconButton>
      ))}
    </ToggleButtonGroup>
  )
}

      {/* <IconButton value='Pan' aria-label='Pan image'>
        <PanToolSharpIcon sx={{ p: 0.5 }} />
      </IconButton>

      <IconButton value='Zoom' aria-label='Zoom image'>
        <ZoomInSharpIcon />
      </IconButton>

      <IconButton value='Rotate' aria-label='Rotate image'>
        <RotateLeftSharpIcon />
      </IconButton>

      <IconButton value='Wwwc' aria-label='Contrast and brightness'>
        <ContrastSharpIcon sx={{ p: 0.2 }} />
      </IconButton>

      <Divider orientation='vertical' />

      <IconButton value='Length' aria-label='Measure length'>
        <StraightenSharpIcon />
      </IconButton>

      <IconButton value='Angle' aria-label='Measure angle'>
        <SquareFootSharpIcon />
      </IconButton>

      <IconButton value='Bidirectional' aria-label='Bidirectional'>
        <VerticalAlignCenterSharpIcon />
      </IconButton>

      <IconButton value='FreehandRoi' aria-label='Draw custom region of interest'>
        <HighlightAltSharpIcon sx={{ p: 0.2 }} />
      </IconButton>

      <IconButton value='Eraser' aria-label='Erase'>
        <AutoFixNormalSharpIcon sx={{ p: 0.2 }} />
      </IconButton> */}
//     </ToggleButtonGroup>
//   )
// }

export default DiconViewerToolbar
