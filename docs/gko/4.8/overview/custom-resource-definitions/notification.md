# Notification

The ``Notification resource allows you to configure event-based notifications within Gravitee, targeting the Gravitee Console UI. Notifications are triggered by API-related events and sent to specific users or groups based on the configuration.

## Overview

This CRD enables the definition of automated notifications when specific API lifecycle events occur. These notifications can be routed to users via the Gravitee Console interface, helping teams stay informed about critical API changes, subscription activities, and other relevant occurrences.

## Example

### Notifying a group of users

```yaml
apiVersion: gravitee.io/v1alpha1
kind: Notification
metadata:
  name: api-notification-groups
spec:
  target: console
  eventType: api
  console:
    apiEvents:
      - API_STARTED
      - API_STOPPED
    groupRefs:
      - name: developers
```

In this example groupRefs defines a reference to a [Group](group.md) custom resource in the same namespace. The group developers will be notified when either the `API_STARTED` or `API_STOPPED` event occurs.

Right now, only `console` is available as a target, and `api` as an even type.

### List of API-related events that trigger notifications

The following are the allowed values for `apiEvents` when configuring notifications for API-related events:

- `APIKEY_EXPIRED`
- `APIKEY_RENEWED`
- `APIKEY_REVOKED`
- `SUBSCRIPTION_NEW`
- `SUBSCRIPTION_ACCEPTED`
- `SUBSCRIPTION_CLOSED`
- `SUBSCRIPTION_PAUSED`
- `SUBSCRIPTION_RESUMED`
- `SUBSCRIPTION_REJECTED`
- `SUBSCRIPTION_TRANSFERRED`
- `SUBSCRIPTION_FAILED`
- `NEW_SUPPORT_TICKET`
- `API_STARTED`
- `API_STOPPED`
- `API_UPDATED`
- `API_DEPLOYED`
- `NEW_RATING`
- `NEW_RATING_ANSWER`
- `MESSAGE`
- `ASK_FOR_REVIEW`
- `REVIEW_OK`
- `REQUEST_FOR_CHANGES`
- `API_DEPRECATED`
- `NEW_SPEC_GENERATED`

> 💡 Use these values under the `console.apiEvents` field to define which events will trigger a notification.

{% hint style="info" %}
**For more information:**

* The `Notification` CRD API reference is documented [here](../../reference/api-reference.md).
{% endhint %}
