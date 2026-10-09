---
hidden: false
noIndex: false
description: Create and manage Kafka Services in Event Stream Management, the native Kafka APIs that expose a registered cluster, a Virtual Cluster, or Kafka brokers to Kafka clients. Pick the task you need.
---

# Kafka Services

A Kafka Service is a native Kafka API. Kafka clients connect to it with the Kafka protocol, and the Event Gateway applies its plans and policies before it forwards their requests to a registered cluster, a Virtual Cluster, or Kafka brokers. The **Kafka Services** item of the **APIs** group lists them. Each Kafka Service opens on a sidebar with the groups **General**, **Design**, **Consumers**, **Monitoring**, **Observability**, and **Operations**, and these guides follow that sidebar.

A Kafka Service managed by the Gravitee Kubernetes Operator is read-only in Event Stream Management until you detach it. See [Detach a Kubernetes-managed Kafka Service](manage-general-settings.md#detach-a-kubernetes-managed-kafka-service).

* [**Create a Kafka Service with a registered cluster**](create-a-kafka-service-with-a-registered-cluster.md). Build a Kafka Service with the creation wizard, or import one from a Gravitee API definition.
* [**Create a Kafka Service with a Virtual Cluster**](create-a-kafka-service-with-a-virtual-cluster.md). Give clients one endpoint for topics spread across several clusters.
* [**Duplicate a Kafka Service**](duplicate-a-kafka-service.md). Copy an existing Kafka Service with a new name, version, and listener host prefix.
* [**Follow the setup checklist**](follow-the-setup-checklist.md). Track what a Kafka Service still needs on its **Overview** page, and find its bootstrap server.
* [**Manage general settings**](manage-general-settings.md). Rename a Kafka Service, set its labels, categories, and images, export or import its definition, start or stop it, unpublish it, detach it from the Kubernetes Operator, and delete it.
* [**Review a Kafka Service**](publish-and-review-a-kafka-service.md). Take a Kafka Service through the API review workflow.
* [**Manage user permissions**](manage-user-permissions.md). Add members, change their roles, give access to groups, and transfer the ownership.
* [**Configure API metadata**](configure-api-metadata.md). Add metadata entries, and override the ones inherited from the environment.
* [**Configure the entrypoint**](configure-the-entrypoint.md). Change the listener host prefix that Kafka clients connect to.
* [**Design flows in the Policy Studio**](design-flows-in-the-policy-studio.md). Apply Kafka policies to connections, interactions, and the messages that clients produce and consume.
* [**Configure endpoints**](configure-endpoints.md). Bind the Kafka Service to Kafka brokers, a registered cluster, or a Virtual Cluster, and pin endpoints to gateway tenants.
* [**Configure resources**](configure-resources.md). Add the caches, OAuth2 providers, and other resources that policies use.
* [**Configure API properties**](configure-api-properties.md). Define the key-value pairs that policies read, and sync them from an HTTP source.
* [**Manage plans**](manage-plans.md). Create, publish, deprecate, and close plans, and replace a live plan with a plan of another security type.
* [**Manage subscriptions**](manage-subscriptions.md). Review, create, approve, pause, transfer, and close subscriptions, and manage their API keys and metadata.
* [**Broadcast messages to consumers**](broadcast-messages-to-consumers.md). Send a one-off message to the subscribers of a Kafka Service, or post it to a URL.
* [**Configure notifications**](configure-notifications.md). Get notified by email or by webhook when events happen on a Kafka Service.
* [**Configure alerts**](configure-alerts.md). Set up runtime alerts on connections, topic traffic, operations, policy rejections, and authentications.
* [**Review audit logs**](review-audit-logs.md). See who changed a Kafka Service, and the patch each change applied.
* [**Review the API Score**](review-the-api-score.md). Evaluate a Kafka Service against the scoring rulesets of the environment.
* [**Manage deployments**](manage-deployments.md). Choose the gateways that load a Kafka Service with sharding tags, and compare and roll back its deployments.
* [**Start, stop, and deploy a Kafka Service**](start-stop-and-deploy-a-kafka-service.md). Run a Kafka Service on the Event Gateway, and push your changes to it.
* [**Limitations and considerations**](limitations-and-considerations.md). What to know before you run Kafka Services, including Virtual Cluster client behavior.
