---
description: >-
  Filter the Gateways list on the Gravitee Cloud Dashboard to find gateways by
  configuration, provider, region, version, environment, or status.
---

# Filter the Gateways list

## Overview

The **Gateways** section of the Gravitee Cloud **Dashboard** lists your gateways. To find specific gateways, filter the list by the values of the following columns:

* **Configuration**
* **Provider**
* **Region**
* **Version**
* **Environment**
* **Status**

## Filter the list

To filter the Gateways list, complete the following steps:

1. In Gravitee Cloud, open **Dashboard**.
2. Scroll to the **Gateways** section.
3.  In the header of the column to filter by, click the filter icon.

    <!-- TODO: Screenshot of the filter icon and open filter menu in a Gateways list column header -->

    <figure><img src="../.gitbook/assets/PLACEHOLDER-gateway-list-filter-menu.png" alt=""><figcaption><p>Filter menu in a column header</p></figcaption></figure>
4. Select one or more values. The menu stays open, so you select several values in a row.

Each selected value appears as a chip above the list. A gateway stays in the list when it matches at least one selected value in every filtered column. For example, when you select two regions and one environment, the list shows the gateways in either region that also belong to that environment.

The filter menus offer the following values:

* The **Configuration**, **Provider**, **Region**, **Version**, and **Environment** menus list the values that are present in your Gateways list.
* The **Status** menu lists **Connected**, **Not connected**, **Unknown (legacy token)**, and **Unknown (unavailable)**.
* When at least one gateway has no value for a column, the menu for that column also lists **N/A**. Select **N/A** to show the gateways without a value for that column. For example, Hybrid gateways show **N/A** in the **Provider** and **Region** columns.

Gravitee Cloud saves your filter selections in your browser. When you come back to the **Dashboard** or refresh the page, your selections stay applied.

## Remove filters

Each active filter appears as a chip above the list that shows the column name and the selected value, for example, **Status: Connected**.

* To remove one filter, click the remove icon on its chip.
* To remove every filter, click **Clear all filters**.

If no gateways match the active filters, the list shows the message `No gateways match the current filters`. Remove one or more filters, or click **Clear all filters**, to show your gateways again.

## Verification

To verify that filtering the Gateways list is working as expected, follow these steps:

1. In the **Gateways** section, click the filter icon in the **Environment** column header.
2. Select an environment.
3.  The list shows only the gateways that belong to that environment, and a chip with the environment name appears above the list.

    <!-- TODO: Screenshot of the filtered Gateways list with an active Environment filter chip -->

    <figure><img src="../.gitbook/assets/PLACEHOLDER-gateway-list-filter-chips.png" alt=""><figcaption><p>Filtered Gateways list with an active filter chip</p></figcaption></figure>
