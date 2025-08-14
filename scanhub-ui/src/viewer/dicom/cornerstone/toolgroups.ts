/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * toolgroups.ts registers all the tools and create a linked tool group.
 */
import {
  addTool,
  Enums,
  ToolGroupManager,
  PanTool,
  ZoomTool,
  WindowLevelTool,
  StackScrollTool,
  CrosshairsTool,
  ReferenceLinesTool,
} from '@cornerstonejs/tools';

const TOOL_GROUP_ID = 'linked';


export function registerDefaultTools() {
  // Register tool classes with the global registry (once)
 addTool(PanTool);
 addTool(ZoomTool);
 addTool(WindowLevelTool);
 addTool(StackScrollTool);
 addTool(CrosshairsTool);
 addTool(ReferenceLinesTool);
}

/**
 * (Re)creates a tool group with the given id and returns the id.
 * If a group with the same id exists, it is destroyed first.
 */
export function getLinkedToolGroup() {

  const existing = ToolGroupManager.getToolGroup(TOOL_GROUP_ID);
  if (existing) return existing;

  const toolGroup = ToolGroupManager.createToolGroup(TOOL_GROUP_ID);
  if (!toolGroup) throw new Error('Failed to create ToolGroup');

  // Add tools to this group by their static toolName
  toolGroup.addTool(PanTool.toolName);
  toolGroup.addTool(ZoomTool.toolName);
  toolGroup.addTool(WindowLevelTool.toolName);
  toolGroup.addTool(StackScrollTool.toolName);
  toolGroup.addTool(CrosshairsTool.toolName);
  toolGroup.addTool(ReferenceLinesTool.toolName);

  // Activate with sensible bindings:
  // Left mouse: Window/Level
  toolGroup.setToolActive(WindowLevelTool.toolName, {
    bindings: [{ mouseButton: Enums.MouseBindings.Primary }],
  });

  // Right mouse: Pan
  toolGroup.setToolActive(PanTool.toolName, {
    bindings: [{ mouseButton: Enums.MouseBindings.Secondary }],
  });

  // Ctrl + Left mouse: Zoom
  toolGroup.setToolActive(ZoomTool.toolName, {
    bindings: [
      {
        mouseButton: Enums.MouseBindings.Primary,
        modifierKey: Enums.KeyboardBindings.Ctrl,
      },
    ],
  });

  // Mouse Wheel: Stack Scroll
  toolGroup.setToolActive(StackScrollTool.toolName, {
    bindings: [{ mouseButton: Enums.MouseBindings.Wheel }],
  });

  // Overlay/sync tools enabled
  // toolGroup.setToolEnabled(ReferenceLinesTool.toolName);
  // toolGroup.setToolEnabled(CrosshairsTool.toolName);

  return toolGroup;
}


/** Attach all current viewports to the shared group. */
export function attachViewportsToLinkedGroup(renderingEngineId: string, viewportIds: string[]) {
  const toolGroup = getLinkedToolGroup();
  viewportIds.forEach((vpId) => toolGroup.addViewport(vpId, renderingEngineId));
}

/** Detach & destroy the shared group (safe to call at unmount). */
export function destroyLinkedToolGroup() {
  const existing = ToolGroupManager.getToolGroup(TOOL_GROUP_ID);
  if (existing) ToolGroupManager.destroyToolGroup(TOOL_GROUP_ID);
}
