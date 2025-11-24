---
description: Overview of Notification.
---

# Notification

The Notification resource lets you configure event-based notifications within Gravitee and targets the Gravitee Console UI. Notifications are triggered by API-related events, and then sent to specific users or groups based on the configuration.

## Overview

This CRD lets you define automated notifications that are triggered when specific API lifecycle events occur. These notifications can be routed to the Gravitee Console interface to help teams stay informed of critical API changes, subscription activities, and other relevant occurrences.

## Example

### Notify a group of users

Groups created from a Group Custom Resource can be referenced using the `groups` property of the Notification Custom Resource. Starting with 4.9.0, groups created through the APIM Console can also be referenced using the `groups` property of the Notification Custom Resource.

In the following example, `groupRefs` defines a reference to a [Group](group.md) Custom Resource in the same namespace. Both the group developers and the members of the `product` group managed through the APIM Console are notified when either the `API_STARTED` or `API_STOPPED` event occurs.

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

{% hint style="info" %}
As of APIM 4.9, only `console` is available as a target, and only `api` is available as an event type.
{% endhint %}

### Enable the notification on an API

For the notification to be effective on an API, two conditions must be met:

* The notification must be referenced in the notificationRefs list of the API
* The groups attached to the notification MUST also be part of the API

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

The following `apiEvents` values are allowed when configuring notifications for API-related events:

* `APIKEY_EXPIRED`
* `APIKEY_RENEWED`
* `APIKEY_REVOKED`
* `SUBSCRIPTION_NEW`
* `SUBSCRIPTION_ACCEPTED`
* `SUBSCRIPTION_CLOSED`
* `SUBSCRIPTION_PAUSED`
* `SUBSCRIPTION_RESUMED`
* `SUBSCRIPTION_REJECTED`
* `SUBSCRIPTION_TRANSFERRED`
* `SUBSCRIPTION_FAILED`
* `NEW_SUPPORT_TICKET`
* `API_STARTED`
* `API_STOPPED`
* `API_UPDATED`
* `API_DEPLOYED`
* `NEW_RATING`
* `NEW_RATING_ANSWER`
* `MESSAGE`
* `ASK_FOR_REVIEW`
* `REVIEW_OK`
* `REQUEST_FOR_CHANGES`
* `API_DEPRECATED`
* `NEW_SPEC_GENERATED`

> 💡 Use these values under the `console.apiEvents` field to define which events trigger a notification.

{% hint style="info" %}
**For more information:**

* The `Notification` CRD API reference is documented [here](../../reference/api-reference.md).
{% endhint %}
