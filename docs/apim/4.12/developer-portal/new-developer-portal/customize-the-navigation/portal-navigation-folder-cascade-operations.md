# Portal Navigation Folder Cascade Operations

## Overview

Portal navigation folders support cascade operations for publishing, unpublishing, and deletion. When you publish or unpublish a folder, the action propagates to all nested documentation pages, APIs, and subfolders. Deleting a folder removes the entire subtree in a single operation. The navigation tree preserves your expansion state across all operations, maintaining your view context as you manage content.

## Key Concepts

### Cascade Publishing

Publishing or unpublishing a folder applies the same state to all descendants. When you publish a folder, all nested documentation pages, APIs, and subfolders become published. When you unpublish a folder, all descendants become unpublished. Individual pages do not propagate their publish state—only folders trigger cascade behavior.

### Cascade Deletion

Deleting a folder permanently removes the folder and its entire subtree, including all nested folders, pages, and associated content. The operation cannot be undone. The delete button is always enabled regardless of folder contents.

### Visibility Propagation

Changing a folder's visibility from PUBLIC to PRIVATE propagates the PRIVATE state to all nested items. Changing from PRIVATE to PUBLIC does not propagate—nested items retain their current visibility settings.

### Tree Expansion State

The portal navigation tree preserves your collapsed and expanded folder states after publish, unpublish, delete, or move operations. On initial page load, all folders expand by default. Subsequent operations maintain your current expansion state.

## Prerequisites

Before managing portal navigation folders, ensure the following:

* Portal navigation is enabled in your environment
* You have permissions to manage portal navigation items
* For legacy items created before v4.12.0 without a root ID index, cascade operations use recursive parent-child traversal instead of optimized queries

## Creating Portal Navigation Items

Portal navigation items are created through the portal navigation management interface. The creation workflow is unchanged by this feature—cascade operations apply only to existing folders during publish, unpublish, and delete actions.

## Managing Portal Navigation Folders

### Publishing and Unpublishing Folders

To publish or unpublish a folder:

1. Select the folder in the navigation tree.
2. Choose the publish or unpublish action from the context menu.
3. Review the confirmation dialog:
   * **Publishing a folder**: "Publishing this folder will also publish all nested documentation and APIs. Do you want to proceed?"
   * **Unpublishing a folder**: "Unpublishing this folder will also unpublish all nested documentation and APIs. This action cannot be undone automatically. Do you want to proceed?"
4. Confirm the action.

The publish state propagates to all descendants. Publishing a page (leaf item) does not trigger propagation.

### Deleting Folders

To delete a folder:

1. Select the folder in the navigation tree.
2. Choose **Delete** from the context menu.
3. Review the confirmation dialog:
   * **For folders with children**: "This folder and all its nested items will be permanently deleted. This cannot be undone."
   * **For empty folders or pages**: "This page will no longer appear on your site."
4. Confirm the deletion.

The folder and its entire subtree are permanently removed. The operation uses batch deletion with 500-item batches for JDBC environments.

### Legacy Item Handling

Items created before v4.12.0 may lack a root ID index. For these items, cascade operations use recursive parent-child traversal instead of the optimized query. This may result in slower performance for deep hierarchies. The system automatically detects legacy items and applies the appropriate deletion strategy.

### Tree Expansion Behavior

The navigation tree preserves your expansion state across all operations. When you publish, unpublish, delete, or move items, the tree maintains which folders are collapsed or expanded. On initial page load, all folders expand by default. The expansion state is tracked using each node's unique identifier and persists through data refreshes.
