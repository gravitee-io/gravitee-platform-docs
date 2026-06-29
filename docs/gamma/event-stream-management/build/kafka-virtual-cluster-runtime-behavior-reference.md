---
hidden: false
noIndex: true
---
<-- to be published -->
# Virtual Cluster runtime behavior
<!-- GAP-STRUCTURAL: Missing procedural content source -->

This page describes what happens when a Virtual Cluster is active on the Event Gateway — how it handles client requests, routes them across backends, and presents a unified view to clients.

## Cluster lifecycle

A Virtual Cluster moves through three states:

| State | Description |
|:------|:------------|
| **Undeployed** | The Virtual Cluster configuration exists but is not active. Client connections are refused. |
| **Deployed** | The Virtual Cluster is active. The Event Gateway routes requests to backends and merges responses. |
| **Pending** | The configuration has been updated since the last deployment. Changes take effect after redeployment. |

To deploy or undeploy a Virtual Cluster, use the row actions on the **Virtual Clusters** list and click **Deploy** or **Undeploy**.

## Topic routing

When a client requests metadata or sends produce/consume requests, the Event Gateway:

1. Fetches metadata from all backend clusters in the Virtual Cluster.
2. Merges the topic lists into a single view, removing internal topics.
3. Routes each request to the backend that owns the relevant topic.

If two backends have a topic with the same name, the Event Gateway routes to the first backend in configuration order. Keep topic names distinct across backends to avoid ambiguity.

## Consumer groups

The Event Gateway supports consumer groups that subscribe to topics spanning multiple backends within a Virtual Cluster. It coordinates subscriptions across backends so the client sees a single, unified consumer group — no client-side coordination is required.

Consumer groups scoped to a single backend behave the same as a direct backend connection.

## Creating a Kafka Service on a Virtual Cluster

1. From the Gamma console sidebar, select **Event Stream Management**.
2. Navigate to **Kafka Services**.
3. Select **Create Kafka Service**.
4. In the **Endpoint** step, select the **Virtual Cluster** binding mode and choose a Virtual Cluster.
5. Complete the remaining wizard steps and select **Create Kafka Service**.
6. Configure security plans and policies on the service's overview page.

For a full walkthrough, see [Create a Kafka service with a Virtual Cluster](create-a-kafka-service-with-a-virtual-cluster.md).
