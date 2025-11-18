---
description: >-
  Learn how to build your Dashboard and various analytics options for APIs and
  applications
---

# Dashboards

## Overview <a href="#the-dashboard" id="the-dashboard"></a>

The Gravitee Dashboard is an area in the UI where you can create custom dashboards reflecting API performance, status, lifecycle stage, etc. The Dashboard is comprised of 3 modules: **Overview**, **APIs health-check**, and **My tasks**.

<figure><img src="../../../../../../.gitbook/assets/dashboard_overview (1).png" alt=""><figcaption><p>Dashboard overview</p></figcaption></figure>

* **Overview:** Shows a summary of API metrics for the selected time interval via configurable charts and information, followed by a paginated list of API events
* **APIs health-check:** Shows API status and availability data based on filter criteria and the selected time interval
* **My tasks:** Starting with the most recent, shows the list of tasks to be validated

## Create a dashboard

You can configure your Gravitee Dashboard by creating dashboard charts for three different categories: **Platform**, **API**, and **Applications**. To create a chart:

1. Log in to your APIM Console
2. Click on **Settings** in the left nav
3. Click on **Analytics** in the inner left nav
4.  Choose to **ADD A NEW PLATFORM DASHBOARD**, **ADD A NEW API DASHBOARD**, or **ADD A NEW APPLICATION DASHBOARD**

    <figure><img src="../../../../../../.gitbook/assets/dashboard_add (1).png" alt=""><figcaption><p>Add a dashboard to a category</p></figcaption></figure>
5.  Define your **Dashboard name** and **Query filter** (optional), then click **SAVE**

    <figure><img src="../../../../../../.gitbook/assets/dashboard_create (1).png" alt=""><figcaption><p>Add a dashboard</p></figcaption></figure>
6. Click the plus icon at the bottom of the screen to add a widget
7.  Click the pencil icon to configure the widget:

    <figure><img src="../../../../../../.gitbook/assets/dashboard_configure widget (1).png" alt=""><figcaption><p>Configure your widget</p></figcaption></figure>

    * Give your widget a **Name** and (optionally) a **Subtitle**
    * Select a **Widget type** from the drop-down menu, e.g., **table**
    * Select a **Field** from the drop-down menu, e.g., **API**, or use a custom field
    * Choose the information to display for your selected field
    * Click **SAVE**
8. (Optional) Click **ENABLE PREVIEW** to preview your new dashboard and widget

## View your dashboard

To view your new dashboard and chart:

1. Log in to your APIM Console
2. Click on **Analytics** in the left nav
3.  Under the **Dashboard** header, select your dashboard from the **Select a dashboard** drop-down menu

    <figure><img src="../../../../../../.gitbook/assets/dashboard_view (1).png" alt=""><figcaption><p>View your dashboard</p></figcaption></figure>

## Edit an existing dashboard

To modify existing dashboards:

1. Log in to your APIM Console
2. Click on **Settings** in the left nav
3. Click on **Analytics** in the inner left nav
4. Click on the hyperlink of an existing dashboard
5. Use the pencil icons to edit widget settings, or the plus icon to add a new widget
6. Click **SAVE**
