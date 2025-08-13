/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * toolgroups.ts registers all the tools and create a linked tool group.
 */
import * as csTools from '@cornerstonejs/tools';

const TOOL_GROUP_ID = 'linked';


export function registerDefaultTools() {
  // Register tool classes with the global registry (once)
  csTools.addTool(csTools.PanTool);
  csTools.addTool(csTools.ZoomTool);
  csTools.addTool(csTools.WindowLevelTool);
  csTools.addTool(csTools.StackScrollTool);
  csTools.addTool(csTools.CrosshairsTool);
  csTools.addTool(csTools.ReferenceLinesTool);
}

/**
 * (Re)creates a tool group with the given id and returns the id.
 * If a group with the same id exists, it is destroyed first.
 */
export function getLinkedToolGroup(id = 'linked') {

  const existing = csTools.ToolGroupManager.getToolGroup(TOOL_GROUP_ID);
  if (existing) return existing;

  const toolGroup = csTools.ToolGroupManager.createToolGroup(TOOL_GROUP_ID);
  if (!toolGroup) throw new Error('Failed to create ToolGroup');

  // Add tools to this group by their static toolName
  toolGroup.addTool(csTools.PanTool.toolName);
  toolGroup.addTool(csTools.ZoomTool.toolName);
  toolGroup.addTool(csTools.WindowLevelTool.toolName);
  toolGroup.addTool(csTools.StackScrollTool.toolName);
  toolGroup.addTool(csTools.CrosshairsTool.toolName);
  toolGroup.addTool(csTools.ReferenceLinesTool.toolName);

  // Activate with sensible bindings:
  // Left mouse: Window/Level
  toolGroup.setToolActive(csTools.WindowLevelTool.toolName, {
    bindings: [{ mouseButton: csTools.Enums.MouseBindings.Primary }],
  });

  // Right mouse: Pan
  toolGroup.setToolActive(csTools.PanTool.toolName, {
    bindings: [{ mouseButton: csTools.Enums.MouseBindings.Secondary }],
  });

  // Ctrl + Left mouse: Zoom
  toolGroup.setToolActive(csTools.ZoomTool.toolName, {
    bindings: [
      {
        mouseButton: csTools.Enums.MouseBindings.Primary,
        modifierKey: csTools.Enums.KeyboardBindings.Ctrl,
      },
    ],
  });

  // Mouse Wheel: Stack Scroll
  toolGroup.setToolActive(csTools.StackScrollTool.toolName, {
    bindings: [{ mouseButton: csTools.Enums.MouseBindings.Wheel }],
  });

  // Overlay/sync tools enabled
  toolGroup.setToolEnabled(csTools.ReferenceLinesTool.toolName);
  toolGroup.setToolEnabled(csTools.CrosshairsTool.toolName);

  return toolGroup;
}


/** Attach all current viewports to the shared group. */
export function attachViewportsToLinkedGroup(renderingEngineId: string, viewportIds: string[]) {
  const tg = getLinkedToolGroup();
  viewportIds.forEach((vpId) => tg.addViewport(vpId, renderingEngineId));
}

/** Detach & destroy the shared group (safe to call at unmount). */
export function destroyLinkedToolGroup() {
  const existing = csTools.ToolGroupManager.getToolGroup(TOOL_GROUP_ID);
  if (existing) csTools.ToolGroupManager.destroyToolGroup(TOOL_GROUP_ID);
}
