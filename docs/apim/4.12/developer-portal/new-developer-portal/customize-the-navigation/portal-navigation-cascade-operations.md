# Portal Navigation Cascade Operations

## Overview

Portal navigation management enables API administrators to organize and control the structure of the developer portal. Administrators can publish, unpublish, and delete folders and API sections along with all their nested content in a single action, streamlining portal content management and reducing the need for manual, item-by-item operations.

## Key Concepts

### Cascade Publishing

When a folder or API section is published or unpublished, the action propagates to all nested items. Publishing a folder makes all documentation pages, sub-folders, and APIs within it visible to portal users. Unpublishing a folder removes all nested content from the portal. This ensures consistent visibility across hierarchical content structures.

| Action | Effect on Nested Items |
|:-------|:-----------------------|
| Publish folder | All nested documentation and APIs are published |
| Unpublish folder | All nested documentation and APIs are unpublished |
| Publish API section | All nested documentation is published |
| Unpublish API section | All nested documentation is unpublished |

### Cascade Deletion

Deleting a folder or API section removes the container and all its descendants recursively. This includes nested folders, documentation pages, and their associated content. Previously, folders that contained children could not be deleted—the delete button was disabled and displayed a tooltip stating "Only empty folders can be deleted." The delete button is now enabled for all items regardless of child count. After deletion, sibling items at the same level are automatically reordered to maintain a continuous sequence. Deletion is permanent and cannot be undone.

### Tree Expansion State

The portal navigation tree preserves the user's collapsed and expanded folder state after publish, unpublish, delete, or move actions. The tree expands all folders by default on initial page load, but subsequent operations maintain the user's current view state.

## Prerequisites

Before managing portal navigation items, ensure you have:

* Access to the API Management Console with portal navigation management permissions
* Existing portal navigation structure with folders, API sections, or documentation pages

## Creating Portal Navigation Items

Portal navigation items are created through the API Management Console's portal navigation interface. The interface displays a hierarchical tree structure where folders, API sections, and documentation pages can be added, organized, and configured. Each item can be published or unpublished individually, with visibility settings controlling whether content appears in the developer portal.

## Managing Portal Navigation Items

### Publishing and Unpublishing Content

To publish or unpublish a folder or API section with all its nested content:

1. Navigate to the portal navigation tree in the API Management Console.
2. Select the folder or API section you want to publish or unpublish.
3. Click the publish or unpublish action from the item menu.
4. Review the confirmation dialog that describes the cascade effect on nested items.
5. Confirm the action to apply the visibility change to the entire subtree.

When publishing a folder, the confirmation dialog states: "Publishing this folder will also publish all nested documentation and APIs. Do you want to proceed?" When unpublishing, the dialog warns: "Unpublishing this folder will also unpublish all nested documentation and APIs. This action cannot be undone automatically. Do you want to proceed?"

**Visibility propagation rules:**

| Visibility Change | Propagation Behavior |
|:------------------|:---------------------|
| PRIVATE → PUBLIC | No propagation; nested items retain their current visibility |
| PUBLIC → PRIVATE | All nested items inherit PRIVATE visibility |

### Deleting Folders and API Sections

To delete a folder or API section and all its nested content:

1. Navigate to the portal navigation tree in the API Management Console.
2. Select the folder or API section you want to delete.
3. Click the **Delete** button from the item menu.
4. Review the confirmation dialog.
5. Confirm the deletion to permanently remove the item and all its descendants.

The delete button is now enabled for all items regardless of whether they contain nested content. Previously, folders that contained children could not be deleted—the delete button was disabled for non-empty containers. For items with children, the confirmation dialog displays: "This [item type] and all its nested items will be permanently deleted. This cannot be undone." For items without children, the dialog states: "This [item type] will no longer appear on your site."

When a folder or API section is deleted, all nested folders, documentation pages, and APIs are removed recursively. Associated page content is also deleted. Sibling items at the same level are automatically reordered to fill gaps in the sequence.
