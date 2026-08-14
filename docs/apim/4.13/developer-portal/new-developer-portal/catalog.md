# Catalog

## Overview

Catalog allows consumers to discover APIs published in the New Developer Portal.

## Prerequisites

* Enable the New Developer Portal. For more information about enabling the New Developer Portal, see [configure-the-new-portal.md](configure-the-new-portal.md "mention").
* Publish APIs. For more information about how to publish APIs in the New Developer Portal, see [#customizing-your-navigation](customize-the-navigation/#customizing-your-navigation "mention").

## Display APIs in the Catalog

The catalog allows you to see the APIs in two view modes:

1. Card view

<figure><img src="../../.gitbook/assets/devportal-new-portal-catalog-258.png" alt=""><figcaption></figcaption></figure>

2. List view

<figure><img src="../../.gitbook/assets/devportal-new-portal-catalog-259.png" alt=""><figcaption></figcaption></figure>

You can also use the search bar to narrow your selection by your query.

Here are the criteria that are taken into account in the search:

* API name
* Labels
* Owner
* API Type
* Sharding Tags
* Description

In list view, a **Category** column shows the categories each API belongs to. The column is hidden on mobile screens.

## Filter the catalog by category

The **Category** dropdown at the top of the catalog filters the catalog to a single category. It reads `Category: All` until you pick one, and it lists only the categories an administrator made visible. For more information about creating categories and assigning APIs to them, see [manage-new-developer-portal-categories.md](manage-new-developer-portal-categories.md "mention").

1.  Click the **Category** dropdown.<br>

    <!-- TODO: Screenshot of the catalog header with the Category dropdown closed -->
    <figure><img src="../../.gitbook/assets/PLACEHOLDER-devportal-catalog-category-dropdown.png" alt=""><figcaption><p>Category dropdown on the catalog</p></figcaption></figure>
2.  Optional: Type part of a category title in the search field to narrow the list.<br>

    <!-- TODO: Screenshot of the open Category dropdown with its search field and options -->
    <figure><img src="../../.gitbook/assets/PLACEHOLDER-devportal-catalog-category-dropdown-open.png" alt=""><figcaption><p>Open Category dropdown</p></figcaption></figure>
3. Select a category.

The catalog then lists only the APIs assigned to that category. Selecting a category clears the search bar, and API Products are left out of the results while a category filter is applied.

To return to the full catalog, open the dropdown and click **Clear Selection**.

### Share a filtered catalog view

The selected category is carried in the `category` query parameter of the catalog URL, so copying the address bar shares or bookmarks that exact view. Opening a link whose `category` value doesn't match a visible category shows the catalog error state instead of results.
