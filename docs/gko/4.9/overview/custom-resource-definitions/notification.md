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
    groups:
      - product
```

In this example `groupRefs` defines a reference to a [Group](group.md) Custom Resource in the same namespace. The group developers will be notified when either the `API_STARTED` or `API_STOPPED` event occurs.

Starting from 4.9.0, groups created through the APIM console and not from a Group Custom Resource can be referenced as well using the `groups` property of the Notification Custom Resource. In the example, members of the `product` managed through the APIM console will be notified for the `API_STARTED` and `API_STOPPED` events as well.

Right now, only `console` is available as a target, and `api` as an even type.

### Enabling the notification on an API

For the notification to be effective on an API two conditions must be met:

  - The notification must be referenced in the notificationRefs list of the API
  - The groups attached to the notification MUST be part of the API as well

```yaml
apiVersion: gravitee.io/v1alpha1
kind: ApiV4Definition
metadata:
  name: api-v4-with-notification
spec:
  contextRef:
    name: "dev-ctx"
  name: "api-v4-with-notification"
  description: "API with notification referencing the produc and developers groups"
  ## [...]
  groups: 
    - product
  groupRefs:
    - name: developers
  notificationsRefs:
    - name: api-notification-groups
```

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
