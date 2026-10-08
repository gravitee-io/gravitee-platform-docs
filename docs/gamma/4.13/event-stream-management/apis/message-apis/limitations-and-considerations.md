---
hidden: false
noIndex: false
description: What to know before you run Message APIs from Event Stream Management, including which component reaches which system, what the console doesn't edit, how it handles Kubernetes-managed APIs, and what it stores.
---

# Limitations and considerations

Event Stream Management configures v4 Message APIs. This page lists the network paths to plan for, the settings and actions that the console doesn't offer, the Message APIs that it keeps read-only, and the data to handle with care.

## Network paths

* The gateway connects to the backends of the endpoints, such as your Kafka brokers or MQTT servers. Open the network path from the gateway, not from the console.
* The Management API fetches a definition that you import from a URL, and it polls the HTTP source of dynamic properties. Both need network access from the Management API.
* The Management API sends the email and webhook notifications of a Message API, and the broadcasts sent by **HTTP POST**. A webhook URL or a broadcast URL must be reachable from the Management API. When the Management API restricts the URLs of its webhook notifiers, the URL must also be allowed. See [Broadcast messages to consumers](broadcast-messages-to-consumers.md).
* Alert Engine sends the notifications of the alerts of a Message API. The webhook URL or the SMTP server of an alert notification must be reachable from Alert Engine. See [Configure alerts](configure-alerts.md).

## Settings that the console doesn't edit

The console has no field for the following settings. It keeps the values that a Message API already has, for example from an imported definition.

* **Plan details beyond the plan form.** The general conditions and the excluded groups of a plan.

## Actions that the console doesn't offer

The following actions are missing from the console, or don't work on a Message API.

* **Alerting on messages.** Alerts watch the requests of a Message API. No alert metric counts or inspects messages. See [Configure alerts](configure-alerts.md).
* **Validating subscription metadata.** The metadata that you edit on a subscription isn't validated against the subscription form of the Message API, and the console doesn't cap the number of entries. See [Manage subscriptions](manage-subscriptions.md).

## Kubernetes-managed Message APIs

When the Gravitee Kubernetes Operator manages a Message API, the console makes its definition, plans, members, metadata, and lifecycle read-only. Subscriptions, notifications, alerts, deployment, and rollback stay available. To edit the Message API in the console, detach it from Kubernetes first. The operator overwrites the changes made while it was detached when the Message API is attached again. See [Manage general settings](manage-general-settings.md#kubernetes-managed-message-apis).

## Irreversible actions

* A closed plan can't be published again.
* The console offers no way to undo the deprecation of a Message API.

## Sensitive data

* An encrypted API property can't be read back. Keep the value elsewhere if you need it later.
* **Message content** in the reporter settings writes message bodies to the log store as-is, and **OTel logs** exports them as OpenTelemetry log records. Select them only when you need them, and only for data that you're allowed to store.
* Span attribute redaction rules apply to trace attributes only. They don't redact the message payloads written to the runtime logs or exported by **OTel logs**.

## Related pages

* [Create a Message API](create-a-message-api.md)
* [Start, stop, and deploy a Message API](start-stop-and-deploy-a-message-api.md)
