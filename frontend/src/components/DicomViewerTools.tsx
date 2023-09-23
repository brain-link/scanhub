import * as React from 'react'

import IconButton from '@mui/joy/IconButton'
import ToggleButtonGroup from '@mui/joy/ToggleButtonGroup'
import Divider from '@mui/joy/Divider'

// Icons
import StraightenSharpIcon from '@mui/icons-material/StraightenSharp'
import SquareFootSharpIcon from '@mui/icons-material/SquareFootSharp'
import AutoFixNormalSharpIcon from '@mui/icons-material/AutoFixNormalSharp'
import VerticalAlignCenterSharpIcon from '@mui/icons-material/VerticalAlignCenterSharp'
import ZoomInSharpIcon from '@mui/icons-material/ZoomInSharp'
import PanToolSharpIcon from '@mui/icons-material/PanToolSharp'
import RotateLeftSharpIcon from '@mui/icons-material/RotateLeftSharp'
import ContrastSharpIcon from '@mui/icons-material/ContrastSharp'
import HighlightAltSharpIcon from '@mui/icons-material/HighlightAltSharp'

import * as cornerstoneTools from 'cornerstone-tools'

// Todo: Add tools only once in CornerstoneInit.ts
export const tools = [
  // Mouse
  'Pan',
  'Zoom',
  'Rotate',
  'Wwwc',
  'Length',
  'Angle',
  'Bidirectional',
  'FreehandRoi',
  'Eraser',
  // Scroll
  {
    name: 'StackScrollMouseWheel',
    mode: 'active',
  },
  // Right click zoom
  {
    name: 'Zoom',
    mode: 'active',
    modeOptions: { mouseButtonMask: 2 },
  },
  // Touch
  {
    name: 'PanMultiTouch',
    mode: 'active',
  },
  {
    name: 'ZoomTouchPinch',
    mode: 'active',
  },
  {
    name: 'StackScrollMultiTouch',
    mode: 'active',
  },
]

function DicomViewerToolbar() {
  const [activeTool, setActiveTool] = React.useState<string | null>(null)

  React.useEffect(() => {
    if (activeTool) {
      cornerstoneTools.setToolActive(activeTool, { mouseButtonMask: 1 })
      console.log('Set active tool: ', activeTool)
    }
  }, [activeTool])

  return (
    <ToggleButtonGroup
      variant='plain'
      spacing={0.5}
      value={activeTool}
      onChange={(event, tool) => {
        setActiveTool(tool)
      }}
      aria-label='text alignment'
    >
      <IconButton value='Pan' aria-label='Pan image'>
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
      </IconButton>
    </ToggleButtonGroup>
  )
}

export default DicomViewerToolbar
