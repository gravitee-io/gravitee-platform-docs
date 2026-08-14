# Catalog

## Overview

Catalog allows consumers to discover APIs published in the New Developer Portal.

The catalog is part of the New Developer Portal itself, not the APIM Console. Consumers reach it from the **Catalog** button in the portal navigation bar, which serves the `/catalog` path of your portal URL. On a mobile screen, **Catalog** sits in the panel that opens from the menu button.

To reach the catalog from the Console, click **Open Website**, and then click **Catalog**. For more information about that button, see [configure-the-new-portal.md](configure-the-new-portal.md "mention").

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

The catalog header carries a **Category** dropdown, alongside the card and list view toggle and the search bar. It filters the catalog to a single category, it reads `Category: All` until a consumer picks one, and it lists only the categories an administrator made visible. Opening the dropdown reveals a search field for narrowing a long category list, and a **Clear Selection** button that returns the consumer to the full catalog.

<!-- TODO: Screenshot of the catalog header with the Category dropdown open -->
<figure><img src="../../.gitbook/assets/PLACEHOLDER-devportal-catalog-category-dropdown.png" alt=""><figcaption><p>Category dropdown in the catalog header</p></figcaption></figure>

Selecting a category narrows the catalog to the APIs assigned to it and clears the search bar. API Products are left out of the results while a category filter is applied.

For more information about creating categories and assigning APIs to them, see [manage-new-developer-portal-categories.md](manage-new-developer-portal-categories.md "mention").

### Share a filtered catalog view

The selected category is carried in the `category` query parameter of the catalog URL, so copying the address bar shares or bookmarks that exact view. Opening a link whose `category` value doesn't match a visible category shows the catalog error state instead of results.
