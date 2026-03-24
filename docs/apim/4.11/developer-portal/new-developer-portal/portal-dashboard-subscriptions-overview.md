# Portal Dashboard subscriptions overview

## Overview

The Portal Dashboard provides a centralized interface for API consumers to view and manage their API subscriptions. Instead of navigating to individual APIs to find subscriptions, users can browse all subscriptions across applications, filter by API, application, or status, view detailed subscription information, and close active subscriptions.

## Accessing the Dashboard

To open the Dashboard, click your user avatar in the top-right corner of the Developer Portal and select **Dashboard**. The Dashboard displays a sidebar with two navigation items: **Applications** and **Subscriptions**.

## Subscription statuses

Subscriptions display the following statuses in the Dashboard:

| Status | Description |
|:-------|:------------|
| Accepted | The subscription is active and the consumer has API access |
| Paused | The subscription is temporarily suspended |
| Closed | The subscription is permanently closed |
| Pending | The subscription is awaiting approval |
| Rejected | The subscription request was rejected |

Only Accepted and Paused subscriptions can be closed by the user.

## Subscription table

The Subscriptions page displays a table with the following columns:

| Column | Description |
|:-------|:------------|
| Subscribed API | Name of the API |
| Plan | Associated plan name |
| Application | Application name |
| Created | Subscription creation date |
| Status | Current subscription status |

Click any row to navigate to the subscription details page. The table supports filtering by API, application, and status, with multi-select capability for status filters.

## Empty states

The Dashboard distinguishes between two empty states:

* **No subscriptions exist:** When no subscriptions exist and no filters are applied, the Dashboard displays "No API subscriptions yet" with guidance to browse the catalog.
* **No filtered results:** When filters are applied but no results match, the Dashboard displays "No subscriptions found" with a button to clear filters.

## Close subscription dialog

A confirmation dialog prompts users before closing a subscription. The dialog displays the title "Close this subscription?" with the warning "You will lose access to the API." Confirm with "Yes, close" or cancel the action.
