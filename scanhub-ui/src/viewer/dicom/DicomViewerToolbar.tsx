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
import { Enums } from '@cornerstonejs/tools';
import { getToolGroup, tools } from './cornerstone/toolgroups';
import { ViewLayout } from './cornerstone/viewLayouts';
import { GridIcon } from './icons/LayoutIcons';


interface DicomViewerToolbarProps {
  onLayoutChange: (layout: ViewLayout) => void;
  currentLayout: ViewLayout;
  onDownloadDicom?: () => void;
  onExportToXnat?: () => void;
}



function DiconViewerToolbar({ onLayoutChange, currentLayout, onDownloadDicom, onExportToXnat }: DicomViewerToolbarProps) {
  const [activeTool, setActiveTool] = React.useState<string | null>(null)

  const toolGroup = React.useMemo(() => getToolGroup(), [])

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
        spacing={0.5}
        value={currentLayout}
        onChange={(_event, layout: ViewLayout | null) => {
          if (layout) onLayoutChange(layout);
        }}
        aria-label="layout selection"
      >
        <Tooltip title="Single view" variant="soft">
          <IconButton value="1x1" aria-label="1x1 Layout">
            <GridIcon rows={1} cols={1} fontSize='small' padding={4} />
          </IconButton>
        </Tooltip>
        <Tooltip title="Three orthogonal views" variant="soft">
          <IconButton value="1x3" aria-label="1x3 Layout">
            <GridIcon rows={1} cols={3} fontSize='small' padding={4} />
          </IconButton>
        </Tooltip>
        <Tooltip title="MPR + 3D" variant="soft">
          <IconButton value="2x2" aria-label="2x2 Layout">
            <GridIcon rows={2} cols={2} fontSize='small' padding={4} />
          </IconButton>
        </Tooltip>
        <Tooltip title="All slices" variant="soft">
          <IconButton value="all-slices" aria-label="All slices">
            <GridIcon rows={2} cols={4} fontSize='small' padding={4} gap={2} />
          </IconButton>
        </Tooltip>
      </ToggleButtonGroup>

      <Divider orientation="vertical" />

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
            size='sm'
          >
            <Icon sx={{ fontSize: 'var(--IconFontSize)' }} />
          </IconButton>
        ))}
      </ToggleButtonGroup>

      {(onDownloadDicom || onExportToXnat) && (
        <>
          <Divider orientation="vertical" />
          <Dropdown>
            <MenuButton
              slots={{ root: IconButton }}
              slotProps={{ root: { size: 'sm', variant: 'outlined', color: 'neutral', title: 'Share / Export' } }}
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
