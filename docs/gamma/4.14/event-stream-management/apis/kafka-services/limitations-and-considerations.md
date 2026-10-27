---
hidden: false
noIndex: false
description: What to know before you run Kafka Services from Event Stream Management, including plan coexistence, Virtual Cluster client behavior, alerts that need analytics, and what the console doesn't offer.
---

# Limitations and considerations

Event Stream Management configures Kafka Services, the native Kafka APIs of the Event Gateway. This page lists the rules that constrain plans and alerts, the client behavior to expect on a Virtual Cluster, and the actions that the console doesn't offer.

## Plans and subscriptions

* **One kind of security at a time.** Keyless, mTLS, and authentication plans (API key, JWT, and OAuth2) can't be live together, and a Kafka Service has at most one live Keyless plan. A deprecated plan counts as live. Publishing a plan of another kind closes the live plans that block it, together with their active subscriptions. See [Manage plans](manage-plans.md).
* **Plan details beyond the plan form.** The plan form has no general conditions and no excluded groups.
* **Custom API keys.** The **Custom API key (optional)** field shows for every API key plan, whatever the environment setting for custom API keys.
* **Subscription metadata.** Values edited on the **Metadata** card of a subscription aren't validated against the subscription form, and the 25-entry limit of the portal form isn't enforced there. See [Manage subscriptions](manage-subscriptions.md).

## Alerts

* **Most alert rules need analytics.** The **Topic traffic**, **Operations**, **Policy rejections**, and **Authentication** rules only receive events while analytics are on for the Kafka Service, with **Aggregated metrics** in its reporter settings. Only the **Connection** rules work with analytics off. See [Configure alerts](configure-alerts.md).
* **No consumer lag alerts.** The alert catalogue has no consumer lag rule.
* **No alert on a clean disconnection.** Connection events are sent when a connection is established and when it fails, not when a client disconnects cleanly.

## Kafka Services on a Virtual Cluster

A Kafka Service whose endpoint is a Virtual Cluster presents the clusters of the Virtual Cluster to Kafka clients as one cluster. The following limits apply to Kafka clients of such a Kafka Service:

* **Transactions stay on one cluster.** A transactional producer must keep all the topics of a transaction on a single cluster of the Virtual Cluster. A transaction that spans clusters is refused with `INVALID_TXN_STATE`, before any data is written. A read-process-write transaction also needs the consumer group's coordinator on the same cluster as the output topic.
* **Consumer group assignors.** A consumer group whose topics span clusters must use the `range` or `roundrobin` assignor, or the consumer group protocol (`group.protocol=consumer`). The sticky assignors and custom assignors are refused with `INCONSISTENT_GROUP_PROTOCOL`. Consumer groups confined to one cluster aren't affected.
* **Shadow consumer groups.** A consumer group that spans clusters is served by one group per cluster, named `<group>__shadow-c<N>`. Expect these groups when you inspect a cluster directly rather than through the Kafka Service. The names are reserved: a client that joins a group whose ID ends with `__shadow-c` followed by digits is refused with `INVALID_GROUP_ID`.
* **No share groups.** Share groups (KIP-932) aren't available through a Virtual Cluster.
* **No ACL management.** ACL operations are refused with `SECURITY_DISABLED`. Manage ACLs directly on each cluster.
* **The Virtual Cluster must be deployed.** A Kafka Service can't start while its Virtual Cluster isn't deployed.

For the full runtime behavior, including topic routing and topic name collisions, see [Virtual Cluster runtime behavior](../../kafka-infrastructure/virtual-clusters/kafka-virtual-cluster-runtime-behavior-reference.md).

## Actions that the console doesn't offer

* **Editing a Kubernetes-managed Kafka Service.** A Kafka Service managed by the Gravitee Kubernetes Operator is read-only until you detach it, and the console shows no banner about it. See [Detach a Kubernetes-managed Kafka Service](manage-general-settings.md#detach-a-kubernetes-managed-kafka-service).
* **Publishing a Kafka Service.** The Kafka Service pages unpublish a published Kafka Service, but don't publish or deprecate it, and don't change its visibility. See [Unpublish the Kafka Service](manage-general-settings.md#unpublish-the-kafka-service).
* **Deploying from the Policy Studio.** Saving flows in the Policy Studio doesn't deploy them. Deploy the Kafka Service afterward. See [Start, stop, and deploy a Kafka Service](start-stop-and-deploy-a-kafka-service.md).

## Irreversible actions

* A closed plan can't be published again, and closing a plan closes its active subscriptions.
* Deleting a Kafka Service removes its plans, its subscriptions, and its analytics data.

## Related pages

* [Manage plans](manage-plans.md)
* [Configure alerts](configure-alerts.md)
* [Start, stop, and deploy a Kafka Service](start-stop-and-deploy-a-kafka-service.md)
