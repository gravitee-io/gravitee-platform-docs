---
hidden: false
noIndex: false
description: Event Stream Management governs Kafka clusters, event-driven data flows, and streaming infrastructure. Learn what it does and how it fits Gamma.
---
# Event Stream Management overview

Event Stream Management is Gravitee's product line for governing Kafka clusters, event-driven data flows, and streaming infrastructure. Within Gamma, Event Stream Management provides a dedicated console for publishing Kafka as governed APIs, registering the Kafka clusters behind them, and observing their traffic.

<figure><img src="../.gitbook/assets/gamma-esm-dashboard.png" alt="The Event Stream Management Overview page, with the APIs, Kafka Infrastructure, and Observability sections and one card per area"><figcaption><p>The Overview page of Event Stream Management. Its sections follow the sidebar groups: APIs, Kafka Infrastructure, and Observability.</p></figcaption></figure>

## What Event Stream Management does

Event Stream Management sits between your Kafka infrastructure and the teams and agents that produce and consume event data. The **Event Gateway** enforces runtime policy on every event interaction, such as authentication, authorization, rate limiting, and protocol mediation, while the **Gamma console** provides the control plane where you register clusters, build APIs, and inspect traffic.

The Event Stream Management sidebar groups these capabilities by object:

* **General**. The [**Overview**](../general/use-the-overview-page.md) page counts what the environment holds and links to every area.
* **APIs**. The two API types that Event Stream Management governs:
  * **Kafka Services**. Define a governed Kafka endpoint, with plans, policies, and access controls. Kafka clients keep speaking the Kafka protocol to the Event Gateway, which reaches Kafka through bootstrap servers that you enter, a registered cluster, or a Virtual Cluster. A Kafka Service is analogous to an [API proxy](../../api-management/build/create-an-api-proxy.md) in API Management. See [Kafka Services](../apis/kafka-services/README.md).
  * **Message APIs**. Expose an event stream over HTTP, so a client publishes and subscribes without speaking the Kafka protocol. A Message API pairs HTTP entrypoints, such as HTTP POST, HTTP GET, SSE, or a webhook, with a broker endpoint on the other side, and carries the same plans, subscriptions, and policies as a Kafka Service. See [Message APIs](../apis/message-apis/README.md).
* **Kafka Infrastructure**. The Kafka estate that the environment can reach:
  * **Clusters**. Register existing Kafka clusters with Gamma, each with one or more named connections, so Kafka Services and Virtual Clusters can be built on them. See [Register your Kafka clusters](../kafka-infrastructure/clusters/register-your-kafka-clusters.md).
  * **Virtual Clusters**. Compose the connections of one or more registered clusters behind a single endpoint. The gateway runs every Virtual Cluster as a Kafka Mesh. See [Virtual Clusters](../kafka-infrastructure/virtual-clusters/README.md).
  * **Explorer**. Read the live brokers, topics, consumer groups, and messages of a registered cluster, a Kafka Service, or a broker address through saved connections. See [Kafka Explorer](../kafka-infrastructure/kafka-explorer/README.md).
* **Observability**. Dashboards, logs, and traces for your Kafka Services and Message APIs. See [Observability](../observability/README.md).

## How Event Stream Management fits into Gamma

Gamma unifies four product lines, API Management, Event Stream Management, Agent Management, and Authorization Management, under a shared platform. All four share the following:

* **A common Catalog**. This catalog holds APIs, events, tools, agents, MCP servers, and models.
* **A common authorization engine**. This engine defines fine-grained policies against those cataloged assets.
* **Common enforcement points**. The AI Gateway, API Gateway, and Event Gateway evaluate the same policies at the wire level.

## Next steps

* [**Register your first cluster**](register-your-first-cluster.md). Register a Kafka cluster and deploy it, so Kafka Services and Virtual Clusters can use it.
* [**Create your first Kafka Service**](create-your-first-kafka-service.md). Create a governed Kafka Service and start it on the Event Gateway.
* [**Create your first Virtual Cluster**](create-your-first-virtual-cluster.md). Put one or more cluster connections behind a single endpoint.
