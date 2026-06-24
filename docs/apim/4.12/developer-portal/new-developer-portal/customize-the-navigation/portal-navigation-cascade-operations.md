---
description: Manage portal navigation folders and API sections with cascade publish, unpublish, and delete operations that affect all nested content.
---

# Portal Navigation Cascade Operations

## Overview

Portal navigation management enables you to organize and control the structure of the Developer Portal. You can publish, unpublish, and delete folders and API sections along with all their nested content in a single action, streamlining portal content management and reducing the need for manual, item-by-item operations.

## Key Concepts

### Cascade Publication

When a folder or API section is published or unpublished, the action propagates to all nested items. When you publish a folder, all documentation pages, sub-folders, and APIs within it become visible to portal users. When you unpublish a folder, all nested content is removed from the portal. This ensures consistent visibility across hierarchical content structures.

The following table describes the effect of cascade operations on nested items:

| Action | Effect on Nested Items |
|:-------|:-----------------------|
| Publish folder | All nested documentation and APIs are published |
| Unpublish folder | All nested documentation and APIs are unpublished |
| Publish API section | All nested documentation is published |
| Unpublish API section | All nested documentation is unpublished |

### Cascade Deletion

When you delete a folder or API section, the container and all its descendants are removed recursively. This includes nested folders, documentation pages, and their associated content. After deletion, sibling items at the same level are automatically reordered to maintain a continuous sequence. Deletion is permanent and can't be undone.

## Prerequisites

Before managing portal navigation items, ensure you have the following:

* Access to the Management Console with portal navigation management permissions
* Existing portal navigation structure with folders, API sections, or documentation pages

## Create Portal Navigation Items

Portal navigation items are created through the Management Console's portal navigation interface. The interface displays a hierarchical tree structure where folders, API sections, and documentation pages can be added, organized, and configured. Each item can be published or unpublished individually, with visibility settings controlling whether content appears in the Developer Portal.

## Manage Portal Navigation Items

### Publish and Unpublish Content

To publish or unpublish a folder or API section with all its nested content:

1. Navigate to the portal navigation tree in the Management Console.
2. Select the folder or API section you want to publish or unpublish.
3. Click the **publish** or **unpublish** action from the item menu.
4. Review the confirmation dialog that describes the cascade effect on nested items.
5. Confirm the action to apply the visibility change to the entire subtree.

When you publish a folder, the confirmation dialog states: "Publishing this folder will also publish all nested documentation and APIs. Do you want to proceed?" When you unpublish a folder, the dialog warns: "Unpublishing this folder will also unpublish all nested documentation and APIs. This action can't be undone automatically. Do you want to proceed?"

The following table describes the visibility propagation rules for publish and unpublish actions:

| Visibility Change | Propagation Behavior |
|:------------------|:---------------------|
| `PRIVATE` to `PUBLIC` | No propagation; nested items retain their current visibility |
| `PUBLIC` to `PRIVATE` | All nested items inherit `PRIVATE` visibility |

### Delete Folders and API Sections

To delete a folder or API section and all its nested content:

1. Navigate to the portal navigation tree in the Management Console.
2. Select the folder or API section you want to delete.
3. Click the **Delete** button from the item menu.
4. Review the confirmation dialog.
5. Confirm the deletion to permanently remove the item and all its descendants.

The **Delete** button is now enabled for all items regardless of whether they contain nested content. For items with children, the confirmation dialog displays: "This [item type] and all its nested items will be permanently deleted. This can't be undone." For items without children, the dialog states: "This [item type] will no longer appear on your site."

When a folder or API section is deleted, all nested folders, documentation pages, and APIs are removed recursively. Associated page content is also deleted. Sibling items at the same level are automatically reordered to fill gaps in the sequence.
