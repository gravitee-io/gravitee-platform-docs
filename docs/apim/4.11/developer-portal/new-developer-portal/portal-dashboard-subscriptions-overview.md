# Portal Dashboard Subscriptions Overview

## Overview

The Portal Dashboard provides a centralized interface for API consumers to view and manage their API subscriptions. Users can browse all subscriptions across applications, filter by API or status, view detailed subscription information, and close active subscriptions. This feature is designed for developers and application owners who need to monitor and control their API access.

## Key Concepts

### Dashboard Navigation

The dashboard uses a tabbed navigation structure with a subscriptions route. Breadcrumbs display the current context (e.g., "Subscription {subscriptionId}") and support clickable navigation back to parent views. The dashboard enforces authentication via route guards (`redirectGuard`, `authGuard`) applied to all child routes.

### Subscription status lifecycle

Subscriptions display user-friendly status labels mapped from internal states. The system recognizes five statuses:

| Internal Status | User-Visible Label |
|:----------------|:-------------------|
| `ACCEPTED` | Active |
| `PAUSED` | Suspended |
| `CLOSED` | Closed |
| `PENDING` | Pending |
| `REJECTED` | Rejected |

Only Active and Suspended subscriptions can be closed by the user.

### Subscription Metadata

Each subscription includes metadata for associated APIs and applications. API metadata contains a `name` and `apiVersion` field, while application metadata contains only a `name`. The UI retrieves metadata by ID and falls back to displaying the raw ID if metadata is unavailable.

### Subscription Table

The subscriptions table displays five columns:

| Column | Description |
|:-------|:------------|
| Subscribed API | Name of the API |
| Plan | Associated plan name |
| Application | Application name |
| Created | Subscription creation date |
| Status | Current subscription status |

Rows are clickable and navigate to the subscription details page. The table supports filtering by API, application, and status, with multi-select capability for status filters.

### Empty States

The UI distinguishes between two empty states:

* **No subscriptions exist:** When no subscriptions exist and no filters are applied, the system displays "No API subscriptions yet" with guidance to browse the catalog.
* **No filtered results:** When filters are applied but no results match, it shows "No subscriptions found" with a button to clear filters.

### Close Subscription Dialog

A shared confirmation dialog prompts users before closing a subscription. The dialog displays the title "Close this subscription?" with the warning "You will lose access to the API." Users confirm with "Yes, close" or cancel the action. The dialog is reusable across the dashboard and API subscriptions tab.
