# Managing API subscriptions in the Portal Dashboard

## Overview

The Portal Dashboard Subscriptions page provides a centralized view of all API subscriptions across your applications. From this page, filter subscriptions, view details, and close active subscriptions.

For an overview of the Dashboard subscriptions feature, see [Portal Dashboard subscriptions overview](../../developer-portal/new-developer-portal/portal-dashboard-subscriptions-overview.md).

## Prerequisites

- Authenticated user in the Developer Portal
- At least one application with API subscriptions
- Subscriptions in Accepted or Paused status to use the close action

## View and manage subscriptions

1. Click your user avatar in the top-right corner of the Developer Portal and select **Dashboard**.
2. Select **Subscriptions** in the sidebar to view all subscriptions across your applications.
3. Apply filters using the **API**, **Application**, or **Status** dropdowns to narrow results. The Status filter supports multi-select.
4. Click any subscription row to view detailed information including plan details, timestamps, and authentication credentials.
5. To close an active or paused subscription, click **Close subscription** in the details view and confirm the action in the dialog.

{% hint style="info" %}
The close button is visible only for subscriptions in Accepted or Paused status. Subscriptions in Pending, Rejected, or Closed status can't be closed from the Dashboard.
{% endhint %}

## Restrictions

- Only Accepted and Paused subscriptions can be closed from the Dashboard
- Subscriptions in Pending, Rejected, or Closed status don't display the close action
