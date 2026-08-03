---
description: Overview of Event Stream Management, the Gamma product line for governing Kafka clusters, event-driven data flows, and streaming infrastructure.
hidden: false
noIndex: false
---
# Event Stream Management overview

Event Stream Management is Gravitee's product line for governing Kafka clusters, event-driven data flows, and streaming infrastructure. Within Gamma, Event Stream Management provides a dedicated console for registering Kafka clusters, creating governed Kafka Services, and provisioning Virtual Clusters for multi-tenant isolation.

<figure><img src="../../.gitbook/assets/gamma-esm-dashboard.png" alt="Event Stream Management dashboard showing Kafka Services, Virtual Clusters, and Clusters cards with counts and status breakdowns"><figcaption><p>The Event Stream Management dashboard. The three cards cover Kafka Service lifecycle management, Virtual Cluster composition for Kafka Mesh, and multi-connection cluster registrations.</p></figcaption></figure>

## What Event Stream Management does

Event Stream Management sits between your Kafka infrastructure and the teams and agents that produce and consume event data. The **Event Gateway** enforces runtime policy on every event interaction — authentication, authorization, rate limiting, and protocol mediation — while the **Gamma console** provides the control plane where you register clusters, build services, and inspect traffic.

Event Stream Management provides the following key capabilities:

* **Kafka cluster registration**. Import existing Kafka clusters into Gamma so they can be governed, monitored, and composed into higher-level services.
* **Kafka Service creation**. Define a governed Kafka Service, with security plans, policies, and access controls, backed by either a Registered Cluster directly or a Virtual Cluster for isolation. A Kafka Service is analogous to an [API proxy](../../api-management/build/create-an-api-proxy.md) in API Management.
* **Virtual Clusters**. Provision logically isolated Kafka environments on shared infrastructure for multi-tenant workloads.

## How Event Stream Management fits into Gamma

Gamma unifies four product lines — API Management, Event Stream Management, Agent Management, and Authorization Management — under a shared platform. All four share the following:

* **A common Catalog**. This catalog holds APIs, events, tools, agents, MCP servers, and models.
* **A common authorization engine**. This engine defines fine-grained policies against those cataloged assets.
* **Common enforcement points**. The AI Gateway, API Gateway, and Event Gateway evaluate the same policies at the wire level.

Event Stream Management contributes Kafka APIs and event streams to the Catalog.

## Next steps

* [**Create your first Kafka service**](create-your-first-kafka-service.md). Create a governed Kafka service in under five minutes.
