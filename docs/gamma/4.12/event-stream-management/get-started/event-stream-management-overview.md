---
description: >-
  Event Stream Management governs the Kafka clusters you already run, through
  Registered Clusters, Virtual Clusters, and Kafka Services. Learn what it does
  and how it fits Gamma.
---

# Event Stream Management overview

Event Stream Management is Gravitee's product line for governing Kafka traffic. Gravitee doesn't host Kafka. It sits in front of the clusters you already run, so producers and consumers reach them through a governed endpoint instead of a bootstrap address and a credential passed around by hand.

Within Gamma, Event Stream Management provides a dedicated console for registering Kafka clusters, federating them into Virtual Clusters, and publishing governed Kafka Services.

<figure><img src="../.gitbook/assets/gamma-esm-dashboard.png" alt="Event Stream Management dashboard showing Kafka Services, Virtual Clusters, and Clusters cards with counts and status breakdowns"><figcaption><p>The Event Stream Management dashboard. The three cards cover Kafka Service lifecycle management, Virtual Cluster composition for Kafka Mesh, and multi-connection cluster registrations.</p></figcaption></figure>

## Why Event Stream Management exists

Kafka gives you topics, partitions, and ACLs. It doesn't give you a governance layer, so an estate that grows past its first cluster runs into the following problems:

* **Access is granted out of band.** A team that needs a topic receives a bootstrap address and a SASL credential over chat. Nothing approves the request, nothing revokes it, and nothing records who holds what.
* **Policy lives in as many places as there are clusters.** Authentication, authorization, and quotas are configured per broker, so the same rule is written again for every cluster and drifts between the copies.
* **Isolation is bought with more infrastructure.** Separating two tenants means standing up separate clusters, and the operational cost multiplies with every tenant added.
* **Clients carry the topology.** An application that reads from three clusters holds three connections and three sets of credentials, and it breaks whenever a topic moves between backends.

## What Event Stream Management does

Event Stream Management sits between your Kafka infrastructure and the teams, applications, and agents that produce and consume event data. The **Event Gateway** enforces runtime policy on every event interaction, including authentication, authorization, rate limiting, and protocol mediation. The **Gamma console** provides the control plane where you register clusters, compose Virtual Clusters, and publish Kafka Services.

Event Stream Management provides the following key capabilities:

* **Kafka cluster registration**. Import an existing Kafka cluster into Gamma so it becomes governable, composable, and visible from one console. A single registration holds one or more named connections, each with its own bootstrap servers and security protocol. See [Register your Kafka clusters](../import/register-your-kafka-clusters.md).
* **Kafka Service creation**. Publish a governed Kafka Service, with security plans, policies, and access controls, backed by a standalone broker list, a named connection on a registered cluster, or a Virtual Cluster. A Kafka Service is the Event Stream Management equivalent of an [API proxy](../../api-management/build/create-an-api-proxy.md) in API Management. See [Create a Kafka service with a registered cluster](../build/create-a-kafka-service-with-a-registered-cluster.md).
* **Virtual Clusters**. Federate several Kafka backends into one endpoint, so a client connects once and reaches topics spread across any number of registered clusters. See [Virtual Clusters overview](../build/kafka-virtual-clusters-overview.md).

## The building blocks

Three objects carry the whole model, and each one builds on the one before it:

| Building block | What it is | Start here |
| --- | --- | --- |
| **Registered Cluster** | A reusable connection profile for a real Kafka backend, holding the bootstrap addresses and security settings of one or more named connections. Several Kafka Services and Virtual Clusters reference the same registration, so an update propagates to all of them. | [Register your Kafka clusters](../import/register-your-kafka-clusters.md) |
| **Virtual Cluster** | A configuration object that federates the backends of several registered clusters into one logical cluster. The Event Gateway merges their topic metadata into a single view and routes each request to the backend that owns the topic. | [Establish a Virtual Cluster](../build/establish-a-virtual-cluster.md) |
| **Kafka Service** | The client-facing endpoint Gravitee manages. It carries the listener that clients connect to, the endpoint binding that reaches Kafka, and the plans and policies enforced on every produce and consume operation. | [Create a Kafka service with a registered cluster](../build/create-a-kafka-service-with-a-registered-cluster.md) |

Gravitee doesn't run your brokers, so every one of these objects depends on a Kafka cluster that's already reachable from the Gamma platform.

## Where each task lives in the console

The Event Stream Management sidebar groups its pages by what you do with them:

| Sidebar group | Page | What it covers |
| --- | --- | --- |
| **Overview** | **Dashboard** | Totals and status breakdowns for Kafka Services, Virtual Clusters, and Clusters, with a banner when a deployment is pending or a service is out of sync. |
| **Manage** | **Clusters** | The registered Kafka clusters in this environment, their connections, and their lifecycle state. |
| **Build** | **Kafka Services** | The governed endpoints clients connect to, with their listeners, endpoint bindings, plans, and policies. |
| **Build** | **Virtual Clusters** | The federated clusters composed from registered backends, and their deployment state. |

## Use cases for Event Stream Management

Each of the following tables pairs an outcome with the feature that delivers it.

### Govern a cluster you already run

| Outcome | Feature |
| --- | --- |
| An existing Kafka cluster is reachable through Gamma, with its bootstrap addresses and credentials held once instead of copied into every team's configuration. | [Register your Kafka clusters](../import/register-your-kafka-clusters.md) |
| Clients reach that cluster through a governed endpoint that authenticates them and applies policy, rather than through a bootstrap address handed out by hand. | [Create a Kafka service with a registered cluster](../build/create-a-kafka-service-with-a-registered-cluster.md) |
| A second governance tier is added over the same cluster, so two sets of consumers get different plans and policies against one backend. | [Create a Kafka service with a registered cluster](../build/create-a-kafka-service-with-a-registered-cluster.md) |

### Share one cluster across teams

| Outcome | Feature |
| --- | --- |
| Several Kafka backends appear to clients as one cluster, so an application connects once and reads topics that live on different backends. | [Establish a Virtual Cluster](../build/establish-a-virtual-cluster.md) |
| A consumer group subscribes to topics spanning several backends, and the Event Gateway coordinates it without any client-side work. | [Virtual Cluster runtime behavior](../build/kafka-virtual-cluster-runtime-behavior-reference.md) |
| One Kafka Service, with one security plan, governs an entire federation instead of one service per backend. | [Create a Kafka service with a Virtual Cluster](../build/create-a-kafka-service-with-a-virtual-cluster.md) |

### Secure and publish consumer access

| Outcome | Feature |
| --- | --- |
| Consumers authenticate against a Kafka Service with a Keyless, API Key, OAuth2, JWT, or mTLS plan. | [Create a Kafka service with a registered cluster](../build/create-a-kafka-service-with-a-registered-cluster.md) |
| A connection to a broker is secured with `PLAINTEXT`, `SASL_PLAINTEXT`, `SASL_SSL`, or `SSL`, and the setting is stored with the registration rather than with each consumer. | [Register your Kafka clusters](../import/register-your-kafka-clusters.md) |
| A cluster registration is updated in one place, and every Kafka Service and Virtual Cluster built on it picks up the change. | [Register your Kafka clusters](../import/register-your-kafka-clusters.md) |

## Security plans for a Kafka Service

A Kafka Service carries one or more plans, and a plan decides how a client authenticates and how its subscription is approved. The following plan types are available:

| Plan type | How the client authenticates |
| --- | --- |
| **Keyless** | No credential. Open access to the service. |
| **API Key** | A key issued to a subscribing application. |
| **OAuth2** | A token issued by an authorization server. |
| **JWT** | A signed token the client presents. |
| **mTLS** | A client certificate presented at the TLS handshake. |

Plans of different kinds don't mix freely on one service, and subscription validation is either automatic or manual. For the rules and the configuration steps, see [Create a Kafka service with a registered cluster](../build/create-a-kafka-service-with-a-registered-cluster.md).

## How Event Stream Management fits into Gamma

Gamma unifies its product lines under one platform: API Management, Event Stream Management, Agent Management, and Authorization Management. They share the following foundations:

* **A common Catalog**. This catalog holds APIs, events, tools, agents, MCP servers, and models.
* **A common authorization engine**. [Authorization Management](../../authorization-management/get-started/authorization-management-overview.md) defines fine-grained policies against those cataloged assets.
* **Common enforcement points**. The AI Gateway, API Gateway, and Event Gateway evaluate the same policies at the wire level.

Event Stream Management contributes Kafka APIs and event streams to the Catalog. Because the Catalog is shared, a Kafka stream governed here becomes reachable from the agent layer through the same entry that [API Management](../../api-management/get-started/api-management-overview.md) uses for its REST, GraphQL, gRPC, and WebSocket APIs, without a separate registry to maintain.

For the platform as a whole, and for the modules Event Stream Management sits beside, see the [Gamma overview](../../platform-management/overview.md).

## Next steps

If you're new to Event Stream Management, work through the following quickstarts in order:

1. [**Register your first cluster**](register-your-first-cluster.md). Connect Gamma to a Kafka cluster you already run.
2. [**Create your first Kafka service**](create-your-first-kafka-service.md). Publish a governed Kafka service in under five minutes.
3. [**Create your first Virtual Cluster**](create-your-first-virtual-cluster.md). Federate two backends into a single endpoint.

To install or configure the platform underneath, see the [installation guides](../../platform-management/install/README.md).
