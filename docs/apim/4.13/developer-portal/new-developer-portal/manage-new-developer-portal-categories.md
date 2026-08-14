---
description: >-
  Group the APIs in your New Developer Portal catalog into categories that
  consumers filter on.
---

# Manage New Developer Portal categories

## Overview

A category groups related APIs in the New Developer Portal catalog. You create categories in the APIM Console, assign published APIs to them, and consumers then filter the catalog to one category at a time. An API belongs to as many categories as you assign it to.

Categories are scoped to an environment. Each environment has its own set of categories.

The categories on this page drive the New Developer Portal catalog. They're stored and managed apart from the categories under **Categories** in the environment **Settings**. Creating, renaming, hiding, or deleting a category on one screen doesn't change the other.

For the consumer-facing filter these categories drive, see [catalog.md](catalog.md "mention").

## Prerequisites

* Enable the New Developer Portal. For more information about enabling the New Developer Portal, see [configure-the-new-portal.md](configure-the-new-portal.md "mention").
* Add the APIs you want to categorize to the portal navigation and publish them. For more information, see [#customizing-your-navigation](customize-the-navigation.md#customizing-your-navigation "mention").

## Create a category

1. Open **Portal Settings**.
2.  Click **Catalog**.<br>

    <!-- TODO: Screenshot of the Catalog entry in the Portal Settings menu -->
    <figure><img src="../../.gitbook/assets/PLACEHOLDER-devportal-portal-settings-catalog-menu.png" alt=""><figcaption><p>Catalog in the Portal Settings menu</p></figcaption></figure>
3.  Click **Add Category**.<br>

    <!-- TODO: Screenshot of the Categories list with the Add Category button -->
    <figure><img src="../../.gitbook/assets/PLACEHOLDER-devportal-add-category-button.png" alt=""><figcaption><p>Add Category on the Categories list</p></figcaption></figure>
4. In the **Title** field, type a title for the category. The title is required, and it can't match the title of a category that already exists in this environment. The check ignores case, so `Payments` doesn't pass when `payments` exists.
5. Optional: In the **Description** field, type a description.
6. Optional: Turn off the **Visible** toggle to keep the category out of the New Developer Portal. New categories are visible by default.
7.  Click **Create**.<br>

    <!-- TODO: Screenshot of the category creation form with Title, Description, and Visible -->
    <figure><img src="../../.gitbook/assets/PLACEHOLDER-devportal-category-general-form.png" alt=""><figcaption><p>Category details</p></figcaption></figure>

The category opens for editing so you can add APIs to it.

## Add an API to a category

Only published API navigation items appear in the picker. An API that isn't published in the portal navigation can't be added to a category, and an API you already added to this category isn't offered again.

1. Open **Portal Settings**.
2. Click **Catalog**.
3. Click the **Edit** icon on the category row.
4.  In the **APIs** section, click **Add API to Category**.<br>

    <!-- TODO: Screenshot of the APIs section with the Add API to Category button -->
    <figure><img src="../../.gitbook/assets/PLACEHOLDER-devportal-add-api-to-category-button.png" alt=""><figcaption><p>APIs section of a category</p></figcaption></figure>
5.  In the **Add API to Category** dialog, type part of the API title in the `Search APIs...` field, and then select the API from the list.<br>

    <!-- TODO: Screenshot of the Add API to Category dialog with an API selected -->
    <figure><img src="../../.gitbook/assets/PLACEHOLDER-devportal-add-api-to-category-dialog.png" alt=""><figcaption><p>Add API to Category dialog</p></figcaption></figure>
6. Click **Add**.

The API appears in the **APIs** table with its name, version, and context path.

## Remove an API from a category

The **APIs** table lists the APIs assigned to the category, including any that were unpublished after they were assigned, so you can see and undo an assignment.

1. Open **Portal Settings**.
2. Click **Catalog**.
3. Click the **Edit** icon on the category row.
4. In the **APIs** table, click the **Remove API** icon on the API row.
5. In the **Remove API** confirmation dialog, click **Remove**.

Removing an API from a category doesn't unpublish it. The API stays in the catalog and loses only that category assignment.

## Hide a category from consumers

A hidden category doesn't appear in the New Developer Portal, so consumers can't filter on it. The APIs assigned to it stay in the catalog. Hiding a category is reversible, and it doesn't change any API assignment.

1. Open **Portal Settings**.
2. Click **Catalog**.
3.  Click the **Hide Category** icon on the category row. A **Hidden** badge appears next to the category title.<br>

    <!-- TODO: Screenshot of the Categories list showing a category with the Hidden badge -->
    <figure><img src="../../.gitbook/assets/PLACEHOLDER-devportal-hidden-category-badge.png" alt=""><figcaption><p>Hidden badge on the Categories list</p></figcaption></figure>

To make the category available again, click the **Show Category** icon on the category row.

## Delete a category

1. Open **Portal Settings**.
2. Click **Catalog**.
3. Click the **Delete** icon on the category row.
4. In the **Delete Category** confirmation dialog, click **Delete**.

The category stops appearing in the New Developer Portal catalog filter. The APIs that were assigned to it stay in the catalog.

## Categories migrated from the Classic Developer Portal

The first time a Management API node starts on APIM 4.13, Gravitee copies the categories of the Classic Developer Portal into New Developer Portal categories, once per environment. Each Classic category becomes a New Developer Portal category that takes the Classic category's name as its title and keeps its description. Every API assigned to the Classic category is assigned to the new category.

The migration is a one-time copy, and the two sets are independent from that point on. Editing a Classic category later doesn't change the New Developer Portal category it produced, and editing the New Developer Portal category doesn't change the Classic one.

Two Classic category fields have no New Developer Portal equivalent and aren't copied: the category picture and the linked documentation page. Migrated categories are always created visible, whatever the Classic category's hidden setting was.

If a category or an API assignment can't be copied, the migration reports a failure and runs again on the next Management API startup. The rerun matches categories by title, so it completes the copy instead of creating duplicates.

## Verification

To verify categories are working as expected, follow these steps:

1. Open **Portal Settings**.
2. Click **Catalog**.
3. Confirm the category appears in the list, without a **Hidden** badge.
4. Click the **Edit** icon on the category row, and confirm the API appears in the **APIs** table.
5. Open the New Developer Portal.
6. Click **Catalog** in the portal navigation bar.
7.  Open the **Category** dropdown in the catalog header, and then select the category. The catalog lists only the APIs assigned to that category.<br>

    <!-- TODO: Screenshot of the New Developer Portal catalog filtered to a category -->
    <figure><img src="../../.gitbook/assets/PLACEHOLDER-devportal-catalog-category-filter-applied.png" alt=""><figcaption><p>Catalog filtered to a category</p></figcaption></figure>
