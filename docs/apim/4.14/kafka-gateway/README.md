---
description: The Kafka Gateway applies API Management 4.13 capabilities directly to native Kafka. Learn what it addresses for security and control.
metaLinks:
  alternates:
    - ./
---

# Kafka Gateway

The Gravitee Kafka Gateway applies Gravitee's API management capabilities directly to native Kafka to address the security, cost, and scalability issues that exist in traditional Kafka deployments.

With the Kafka Gateway, you can apply [policies](create-and-configure-kafka-apis/configure-kafka-apis/policies.md) on native Kafka topics at runtime. These policies are designed for Kafka-specific use cases. For example, you can restrict topic access to approved tenants or require client certificates for mTLS as an additional security layer.

Kafka APIs support multi-tenant endpoint configurations, allowing a single API definition to route to different backend clusters based on gateway tenant assignment. For details, see [Multi-tenant endpoint support](create-and-configure-kafka-apis/configure-kafka-apis/endpoints.md#multi-tenant-endpoint-support).

The Kafka Gateway is linked to Gravitee's Developer Portal to facilitate topic availability and knowledge sharing. For example, you can publish [documentation](create-and-configure-kafka-apis/configure-kafka-apis/documentation.md) on Kafka topics, infrastructure, and client connections, or use a self-service mechanism to manage [subscriptions](../secure-and-expose-apis/subscriptions/README.md) to Kafka topics.

The Kafka Gateway natively supports the Kafka protocol and is treated like a traditional Kafka broker by consumers and producers. As a Gravitee user, you expose Kafka topics using the Gravitee concept of an API, called a [Kafka API](create-and-configure-kafka-apis/create-kafka-apis.md#introduction). However, consumers and producers see a regular client connection to a Kafka bootstrap server, so don't need to change existing application logic.

You can expose multiple Kafka topics within a single Kafka API, and expose multiple Kafka APIs through the Gravitee Kafka Gateway. Using the Kafka Gateway, data is processed in real time, and virtual topics and partitions enable scalable, cost-effective deployments.

## Kafka protocol support

The Kafka Gateway embeds the Apache Kafka 4.4 client libraries.

The Kafka Gateway doesn't pin a fixed protocol version range. When a client connects, the Kafka Gateway negotiates the version of each Kafka protocol API dynamically. For each API, the Kafka Gateway advertises the version range that both the backend Kafka cluster and the Kafka Gateway support, and it doesn't advertise APIs that it doesn't serve. Clients then select a mutually supported version through standard Kafka version negotiation.

Share groups, and the streams groups of Kafka Streams applications, go through the Kafka Gateway when the backend Kafka cluster serves them. The policies that act on consumed records also act on the records that share group consumers receive.

For client requirements and setup, see [Configure the Kafka Client & Gateway](configure-the-kafka-client-and-gateway.md).

### Oldest supported clients

The Kafka Gateway follows the Kafka 4.x protocol baseline, which drops the oldest versions of the Kafka protocol APIs. A request at a dropped version, such as a produce request below version 3 or a fetch request below version 4, is refused whatever the version of the backend Kafka cluster. The Kafka Gateway closes the connection without an answer. Java clients from Kafka 2.1 aren't affected. To find the clients that the Kafka Gateway refuses, see [Troubleshoot Kafka client connections](troubleshoot-kafka-client-connections.md#the-client-cant-connect).

### Tested brokers and clients

The Kafka Gateway is tested in front of the following backend Kafka clusters:

| Backend Kafka cluster | Kafka API | Virtual Cluster backend |
| --- | --- | --- |
| Kafka 2.1 | Tested | Refused |
| Kafka 2.8 | Tested | Tested |
| Kafka 3.6 | Tested | Tested |
| Kafka 3.9 | Tested | Tested |
| Kafka 4.4 | Tested | Tested |
| Azure Event Hubs | Tested | Refused |

A Virtual Cluster backend needs Kafka 2.8 or later. With an older backend, or with Azure Event Hubs, the Kafka Gateway closes the connections of the Virtual Cluster's clients and logs an error that names the backend.

The following clients are tested through the Kafka Gateway:

| Client | Version | Result |
| --- | --- | --- |
| Java client | 0.10.2 | Refused |
| Java client | 2.1.0, 3.9.2, and 4.4.0 | Tested |
| Java client, consuming in a share group | 4.4.0 | Tested |
| `librdkafka` | 1.8.2 | Tested |
| `confluent-kafka-python` | 2.16.2 | Tested |
| `kafka-python` | 3.0.13 | Tested |

### Virtual Clusters

A Virtual Cluster serves each Kafka protocol API at the versions that every one of its backends serves. Share groups and streams groups therefore need every backend to serve them.

A Virtual Cluster doesn't advertise the following requests, and refuses them with `UNSUPPORTED_VERSION`, even with a single backend:

* Cluster and quorum administration: partition reassignments, leader elections, replica log directory changes, the description of the quorum and changes to its voters, feature updates, and the removal of a broker.
* Delegation tokens, client quotas, and SCRAM credentials.
* Describing and listing transactions.

Send these requests to each backend Kafka cluster directly.

A streams group runs on the backend that holds its source topics. The Kafka Gateway refuses the group's topology with `STREAMS_INVALID_TOPOLOGY` in each of these cases:

* Its source topics are on several backends.
* One of its source topics exists on several backends.
* One of its internal topics exists on a backend other than the one that holds its source topics.

A Virtual Cluster served by several Gateway instances needs a distributed cache. See [Virtual cluster (MESH) mode caveat](deploy-the-kafka-gateway-for-high-availability.md#virtual-cluster-mesh-mode-caveat).

To learn more about the Kafka Gateway, see the following articles:

<table data-view="cards"><thead><tr><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td>Configure the Kafka Client &#x26; gateway</td><td><a href="configure-the-kafka-client-and-gateway.md">configure-the-kafka-client-and-gateway.md</a></td></tr><tr><td>Create &#x26; Configure Kafka APIs</td><td><a href="create-and-configure-kafka-apis/">create-and-configure-kafka-apis</a></td></tr><tr><td>Plans</td><td><a href="plans.md">plans.md</a></td></tr><tr><td>Applications</td><td><a href="../secure-and-expose-apis/applications/create-an-application.md">create-an-application.md</a></td></tr><tr><td>Subscriptions</td><td><a href="subscriptions.md">subscriptions.md</a></td></tr><tr><td>Other ways Gravitee supports Kafka</td><td><a href="other-ways-gravitee-supports-kafka.md">other-ways-gravitee-supports-kafka.md</a></td></tr></tbody></table>
