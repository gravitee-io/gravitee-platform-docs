---
hidden: false
noIndex: false
description: Create and manage Message APIs in Event Stream Management, the v4 APIs that connect clients to message backends such as Kafka, MQTT 5.x, Solace, and RabbitMQ. Pick the task you need.
---

# Message APIs

A Message API is a v4 API that connects clients to a message backend. Its entrypoints, for example **HTTP GET**, **Server-Sent Events**, or **Webhook**, set how clients connect. Its endpoints, for example **Kafka** or **MQTT 5.x**, set the backend that it produces to and consumes from. The **Message APIs** item of the **Build** group lists them. Each Message API opens on a sidebar with the groups **General**, **Design**, **Consumers**, **Monitoring**, **Observability**, and **Operations**, and these guides follow that sidebar.

* [**Create a Message API**](create-a-message-api.md). Build a Message API with the creation wizard, or import one from a Gravitee API definition.
* [**Follow the setup checklist**](follow-the-setup-checklist.md). Track what a Message API still needs on its **Overview** page.
* [**Manage general settings**](manage-general-settings.md). Rename a Message API, set its labels, categories, and images, export or import its definition, and delete it.
* [**Publish and review a Message API**](publish-and-review-a-message-api.md). Publish, deprecate, and change the visibility of a Message API, and take it through the API review workflow.
* [**Manage user permissions**](manage-user-permissions.md). Add members, change their roles, give access to groups, and transfer the ownership.
* [**Configure API metadata**](configure-api-metadata.md). Add metadata entries, and override the ones inherited from the environment.
* [**Configure entrypoints**](configure-entrypoints.md). Choose how clients connect, and set the context path.
* [**Design flows in the Policy Studio**](design-flows-in-the-policy-studio.md). Apply policies to the initial connection and to the messages that clients publish and consume.
* [**Configure endpoints and failover**](configure-endpoints-and-failover.md). Configure the backends, and retry calls that fail.
* [**Configure response templates**](configure-response-templates.md). Replace the errors that the gateway returns.
* [**Configure resources**](configure-resources.md). Add the caches, OAuth2 providers, and other resources that policies use.
* [**Configure API properties**](configure-api-properties.md). Define the key-value pairs that policies read, and sync them from an HTTP source.
* [**Configure CORS**](configure-cors.md). Allow browser clients from other origins.
* [**Manage plans**](manage-plans.md). Decide how consumers access the Message API, and publish, deprecate, or close plans.
* [**Manage subscriptions**](manage-subscriptions.md). Handle the subscriptions of applications and their API keys.
* [**Broadcast messages to consumers**](broadcast-messages-to-consumers.md). Send a one-off message to subscribers or to the members of subscribed applications.
* [**Configure notifications**](configure-notifications.md). Get notified by email or by webhook when events happen, and choose the events of your console notifications.
* [**Configure alerts**](configure-alerts.md). Set up runtime alerts on the traffic of the Message API.
* [**Review audit logs**](review-audit-logs.md). Review the history of changes made to the Message API.
* [**Review the API Score**](review-the-api-score.md). Evaluate the Message API against the scoring rules of the environment.
* [**Start, stop, and deploy a Message API**](start-stop-and-deploy-a-message-api.md). Run the Message API on the gateway, choose its gateways with sharding tags, and compare its deployments.
* [**Configure reporter settings**](configure-reporter-settings.md). Choose the runtime logs, the message sampling, and the traces that the Message API reports.
* [**Limitations and considerations**](limitations-and-considerations.md). Network paths, settings that the console doesn't edit, and sensitive data.

The **Monitoring** group also shows **Webhooks** when the Message API has a **Webhook** entrypoint and you can read its logs, and **API Score** when the environment uses API Score. The **Observability** group opens the **Dashboard**, **Logs**, and **Tracing** of the Message API in a new tab. See [Observability](../../observability/README.md).
