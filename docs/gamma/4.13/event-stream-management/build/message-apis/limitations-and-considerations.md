---
hidden: false
noIndex: false
description: What to know before you run Message APIs from Event Stream Management, including which component reaches which system, what the console doesn't edit, and what it stores.
---

# Limitations and considerations

Event Stream Management configures v4 Message APIs. This page lists the network paths to plan for, the settings and actions that the console doesn't offer, and the data to handle with care.

## Network paths

* The gateway connects to the backends of the endpoints, such as your Kafka brokers or MQTT servers. Open the network path from the gateway, not from the console.
* The Management API fetches a definition that you import from a URL, and it polls the HTTP source of dynamic properties. Both need network access from the Management API.
* The Management API sends the email and webhook notifications of a Message API. A webhook URL must be reachable from the Management API.

## Settings that the console doesn't edit

The console has no field for the following settings. Except for the context paths, it keeps the values that a Message API already has, for example from an imported definition.

* **Several context paths or virtual hosts.** The **Context path** field sets one path, and editing it replaces every path of the HTTP listener with that path. An imported definition that listens on several paths or on virtual hosts loses them when you edit the context path.
* **The connection settings of a single endpoint.** Every endpoint that the console creates inherits the connection settings of its group, and the console has no form for the connection settings of a single endpoint. See [Configure endpoints and failover](configure-endpoints-and-failover.md).
* **Endpoint weights.** Every endpoint that the console creates has a weight of 1.
* **Plan details beyond the plan form.** The general conditions, characteristics, tags, excluded groups, and subscription comment settings of a plan.
* **The webhook settings of a Push plan subscription.** The **Create subscription** panel doesn't collect them, so it can't create a subscription to a Push plan.

## Actions that the console doesn't offer

The following actions are missing from the console, or don't work on a Message API.

* **Duplicating a Message API.** The **Settings** page offers **Duplicate**, but the copy keeps the context path of the original, so the Management API refuses it because the path is already in use.
* **Adding an endpoint to a group.** A new endpoint starts with empty settings that the console doesn't let you fill in. See [Configure endpoints and failover](configure-endpoints-and-failover.md).
* **Rolling back a deployment.** The **Deployment History** page compares deployments but has no rollback.

## Irreversible actions

* A closed plan can't be published again.
* The console offers no way to undo the deprecation of a Message API.

## Sensitive data

* An encrypted API property can't be read back. Keep the value elsewhere if you need it later.
* **Message content** in the reporter settings writes message bodies to the log store as-is. Turn it on only when you need it, and only for data that you're allowed to store.
* Span attribute redaction rules apply to trace attributes only. They don't redact the message payloads written to the runtime logs.

## Related pages

* [Create a Message API](create-a-message-api.md)
* [Start, stop, and deploy a Message API](start-stop-and-deploy-a-message-api.md)
