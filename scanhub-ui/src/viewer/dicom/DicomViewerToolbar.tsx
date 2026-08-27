/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * DicomViewerTools.tsx is responsible for rendering a toolbar for the dicom viewer.
 */
import React from 'react'

// Icons
import IconButton from '@mui/joy/IconButton'
import ToggleButtonGroup from '@mui/joy/ToggleButtonGroup'
import Stack from '@mui/joy/Stack';
import Tooltip from '@mui/joy/Tooltip';
import Divider from '@mui/joy/Divider';
import Dropdown from '@mui/joy/Dropdown';
import Menu from '@mui/joy/Menu';
import MenuButton from '@mui/joy/MenuButton';
import MenuItem from '@mui/joy/MenuItem';
import FileDownloadIcon from '@mui/icons-material/FileDownload';
import OpenInNewIcon from '@mui/icons-material/OpenInNew';
import SaveIcon from '@mui/icons-material/Save';
import StraightenIcon from '@mui/icons-material/Straighten';
import { Enums } from '@cornerstonejs/tools';
import { getToolGroup, tools } from './cornerstone/toolgroups';
import { ViewLayout } from './cornerstone/viewLayouts';
import { GridIcon } from './icons/LayoutIcons';


// Joy's IconButton paints its own background for `[aria-pressed="true"]`
// regardless of the `variant`/`color` props, which fights the outlined
// look we want for a selected button — strip it explicitly, and give every
// button a consistent light hover highlight. Buttons stay square because
// they all share `size="sm"` — Joy's IconButton is square by design; adding
// an `aspectRatio` override here fights that and stretches the box instead.
const toolbarButtonSx = {
  '&[aria-pressed="true"]': { backgroundColor: 'transparent' },
  '&:hover': { backgroundColor: 'neutral.plainHoverBg' },
} as const;

interface DicomViewerToolbarProps {
  onLayoutChange: (layout: ViewLayout) => void;
  currentLayout: ViewLayout;
  /** Whether the loaded result is volumetric (multiple slices) — gates the MPR-only layouts. */
  allow3DLayouts: boolean;
  onDownloadDicom?: () => void;
  onExportToXnat?: () => void;
}



function DiconViewerToolbar({ onLayoutChange, currentLayout, allow3DLayouts, onDownloadDicom, onExportToXnat }: DicomViewerToolbarProps) {
  const [activeTool, setActiveTool] = React.useState<string | null>(null)

  const toolGroup = React.useMemo(() => getToolGroup(), [])

  const manipulationTools = React.useMemo(() => tools.filter(t => t.category !== 'measurement'), [])
  const measurementTools = React.useMemo(() => tools.filter(t => t.category === 'measurement'), [])
  const activeMeasurementTool = measurementTools.find(t => t.Tool.toolName === activeTool)

  React.useEffect(() => {
    if (activeTool && toolGroup) {
      // Set all tools passive
      tools.forEach(({ Tool }) => toolGroup.setToolPassive(Tool.toolName, { removeAllBindings: [{ mouseButton: Enums.MouseBindings.Primary }] }));
      // Activate selected tool
      toolGroup.setToolActive(activeTool, {
        bindings: [{ mouseButton: Enums.MouseBindings.Primary }],
      });
    }
  }, [activeTool, toolGroup])

  return (
    <Stack direction="row" gap={2} sx={{ p: 0, m: 0 }}>

      {/* --- Layout Selection --- */}
      <ToggleButtonGroup
        variant="plain"
        color="neutral"
        size="sm"
        spacing={0.5}
        value={currentLayout}
        onChange={(_event, layout: ViewLayout | null) => {
          if (layout) onLayoutChange(layout);
        }}
        aria-label="layout selection"
      >
        <Tooltip title="Single view" variant="soft">
          <IconButton
            value="1x1"
            aria-label="1x1 Layout"
            color={currentLayout === ViewLayout.Single ? 'primary' : 'neutral'}
          >
            <GridIcon rows={1} cols={1} fontSize='small' padding={4} />
          </IconButton>
        </Tooltip>
        {allow3DLayouts && (
          <>
            <Tooltip title="Three orthogonal views" variant="soft">
              <IconButton
                value="1x3"
                aria-label="1x3 Layout"
                color={currentLayout === ViewLayout.OneByThree ? 'primary' : 'neutral'}
              >
                <GridIcon rows={1} cols={3} fontSize='small' padding={4} />
              </IconButton>
            </Tooltip>
            <Tooltip title="MPR + 3D" variant="soft">
              <IconButton
                value="2x2"
                aria-label="2x2 Layout"
                color={currentLayout === ViewLayout.TwoByTwo ? 'primary' : 'neutral'}
              >
                <GridIcon rows={2} cols={2} fontSize='small' padding={4} />
              </IconButton>
            </Tooltip>
          </>
        )}
        <Tooltip title="All slices" variant="soft">
          <IconButton
            value="all-slices"
            aria-label="All slices"
            color={currentLayout === ViewLayout.AllSlices ? 'primary' : 'neutral'}
          >
            <GridIcon rows={2} cols={4} fontSize='small' padding={4} gap={2} />
          </IconButton>
        </Tooltip>
      </ToggleButtonGroup>

      <Divider orientation="vertical" />

      <ToggleButtonGroup
        variant="plain"
        color="neutral"
        size="sm"
        spacing={0.5}
        value={activeTool}
        onChange={(_event, tool: string | null) => {
          setActiveTool(tool) // tool may be null on deselect
        }}
        aria-label="viewer tools"
      >
        {manipulationTools.map(({ Tool, Icon, label }) => (
          <IconButton
            key={Tool.toolName}
            value={Tool.toolName}
            aria-label={label ?? Tool.toolName}
            title={label ?? Tool.toolName}
            color={activeTool === Tool.toolName ? 'primary' : 'neutral'}
          >
            <Icon sx={{ fontSize: 'var(--IconFontSize)' }} />
          </IconButton>
        ))}
      </ToggleButtonGroup>

      {/* --- Measurement tools --- */}
      <Dropdown>
        <MenuButton
          slots={{ root: IconButton }}
          slotProps={{
            root: {
              size: 'sm',
              variant: activeMeasurementTool ? 'solid' : 'plain',
              color: activeMeasurementTool ? 'primary' : 'neutral',
              title: activeMeasurementTool?.label ?? 'Measurement tools',
              'aria-label': 'Measurement tools',
              // sx: toolbarButtonSx,
            },
          }}
        >
          {activeMeasurementTool
            ? <activeMeasurementTool.Icon sx={{ fontSize: 'var(--IconFontSize)' }} />
            : <StraightenIcon sx={{ fontSize: 'var(--IconFontSize)' }} />}
        </MenuButton>
        <Menu size='sm' placement='bottom-start'>
          {measurementTools.map(({ Tool, Icon, label }) => (
            <MenuItem
              key={Tool.toolName}
              selected={activeTool === Tool.toolName}
              onClick={() => setActiveTool(Tool.toolName)}
            >
              <Icon sx={{ fontSize: 'var(--IconFontSize)' }} />
              {label ?? Tool.toolName}
            </MenuItem>
          ))}
        </Menu>
      </Dropdown>

      {(onDownloadDicom || onExportToXnat) && (
        <>
          <Divider orientation="vertical" />
          <Dropdown>
            <MenuButton
              slots={{ root: IconButton }}
              slotProps={{ root: { size: 'sm', variant: 'outlined', color: 'neutral', title: 'Share / Export', sx: toolbarButtonSx } }}
            >
              <SaveIcon sx={{ fontSize: 'var(--IconFontSize)' }} />
            </MenuButton>
            <Menu size='sm' placement='bottom-end'>
              {onDownloadDicom && (
                <MenuItem onClick={onDownloadDicom}>
                  <FileDownloadIcon sx={{ fontSize: 'var(--IconFontSize)' }} />
                  Download DICOM
                </MenuItem>
              )}
              {onExportToXnat && (
                <MenuItem onClick={onExportToXnat}>
                  <OpenInNewIcon sx={{ fontSize: 'var(--IconFontSize)' }} />
                  Export to XNAT
                </MenuItem>
              )}
            </Menu>
          </Dropdown>
        </>
      )}
    </Stack>

  )
}

export default DiconViewerToolbar
