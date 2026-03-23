# Managing API Subscriptions in the Portal Dashboard

## Empty States

The UI distinguishes between two empty states. When no subscriptions exist and no filters are applied, the system displays "No API subscriptions yet" with guidance to browse the catalog. When filters are applied but no results match, it shows "No subscriptions found" with a button to clear filters.

## Close Subscription Dialog

A shared confirmation dialog prompts users before closing a subscription. The dialog displays the title "Close this subscription?" with the warning "You will lose access to the API." Users confirm with "Yes, close" or cancel the action. The dialog is reusable across the dashboard and [API subscriptions tab](../applications/subscriptions.md).

## Prerequisites

Before managing API subscriptions in the Portal Dashboard, ensure the following:

* User must be authenticated
* User must have at least one application with API subscriptions to view the subscriptions list
* Subscriptions must be in Active or Suspended status to enable the close action

## Viewing and Managing Subscriptions

1. Navigate to the dashboard and select the **Subscriptions** tab to view all subscriptions across your applications.
2. Apply filters using the **API**, **Application**, or **Status** dropdowns to narrow results. Status supports multi-select.
3. Click any subscription row to view detailed information including authentication type, quota, rate-limit, and timestamps.
4. To close an active or suspended subscription, click **Close subscription** in the details view, confirm the action in the dialog, and the subscription status updates to Closed.
5. Use the pagination controls (Previous/Next buttons or page number selectors) to navigate large result sets, with configurable page sizes of 10, 20, 50, or 100 items.

{% hint style="info" %}
The close button is visible only for subscriptions in Active or Suspended status. Subscriptions in Pending, Rejected, or Closed status cannot be closed via the UI.
{% endhint %}

## End-User Configuration

### Subscription List API

**Endpoint:** `GET /subscriptions`

**Query Parameters:**

| Parameter | Type | Description | Example |
|:----------|:-----|:------------|:--------|
| `apiIds` | string[] | Filter by API IDs | `['api-123', 'api-456']` |
| `applicationIds` | string[] | Filter by application IDs | `['app-789']` |
| `statuses` | SubscriptionStatusEnum[] | Filter by subscription statuses | `['ACCEPTED', 'PAUSED']` |
| `size` | number | Page size (-1 for all) | `20` |
| `page` | number | Page number (1-indexed) | `1` |

**Response Schema:**

```typescript
{
  data: Subscription[];
  metadata: SubscriptionMetadata;
  links: { self: string };
}
```
