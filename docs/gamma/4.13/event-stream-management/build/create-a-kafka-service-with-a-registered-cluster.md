---
hidden: false
noIndex: false
description: Create a Kafka Service bound to a connection on a registered Kafka cluster, with security plans and policies. Follow the steps in the creation wizard.
---

# Create a Kafka service with a registered cluster

A Kafka Service is the client-facing endpoint managed by Gravitee. It is the Event Stream Management equivalent of an API proxy. The Kafka Service is the governance layer that enforces authentication, security plans, ACLs, and quotas before routing traffic to the backend infrastructure.

The backend infrastructure can be a standalone broker list, a specific connection on a registered physical cluster, or a Virtual Cluster.

{% hint style="info" %}
For a simplified walkthrough that covers just the basics, see [Create your first Kafka service](../get-started/create-your-first-kafka-service.md).
{% endhint %}

## How Kafka services work

When you create a Kafka Service, you define the **Listener** that clients connect to, and the **Endpoint binding** that determines how the service reaches Kafka. The Event Gateway enforces the service's configuration at runtime. Every produce and consume operation passes through the gateway, where security plans, authorization policies, and rate limits are evaluated.

A single Kafka Service can route to multiple clusters by binding to a Virtual Cluster. Alternatively, multiple Kafka Services can bind to the same registered cluster to provide different governance tiers.

## Prerequisites

* Access to a running Gamma console instance
* At least one registered Kafka cluster (see [Register your Kafka clusters](../import/register-your-kafka-clusters.md))

## Create a Kafka service

1. From the Gamma console sidebar, select **Event Stream Management**.
2. Navigate to **Kafka Services**.
3. Select **Create Kafka Service**.

The wizard has four steps. To configure the service, complete the following steps:

1. [Identity](#identity)
2. [Listener](#listener)
3. [Endpoint](#endpoint)
4. [Review and create](#review-and-create)

### Identity

| Field           | Description                                                                                          |
| --------------- | ---------------------------------------------------------------------------------------------------- |
| **Name**        | A human-readable name that identifies this Kafka Service in the Kafka Service list and detail views. |
| **Version**     | The version of this service, for example 1.0.                                                        |
| **Description** | Optional. A description of the service's purpose.                                                    |

### Listener

The listener defines the entrypoint that Kafka clients connect to.

| Field           | Description                                                                                                                                                                                                                                                    |
| --------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Host prefix** | A single DNS label of lowercase letters, digits, and hyphens, up to 63 characters. The Event Gateway appends its configured domain, and clients connect on the gateway's SNI port, for example `orders.<gateway-domain>:<sni-port>`. The port is a gateway-level setting and is not configured here. |

### Endpoint

The endpoint binding determines how the Kafka Service reaches Kafka. Choose one of the following modes:

* **Standalone**. Manually provide a comma-separated list of `host:port` bootstrap servers.
* **Managed cluster**. Select a registered Kafka cluster and one of its configured connections.
* **Virtual Cluster**. Select a Virtual Cluster to route traffic through a unified namespace or Kafka Mesh.

### Review and create

1. Review the service identity, listener, and endpoint binding.
2. Select **Create Kafka Service**.

The console creates the Kafka Service and redirects you to its overview page.

## Configure Plans and Policies

After creating the Kafka Service, you must configure a **Plan** to allow clients to consume from or produce to the service.

The following security plan types are available:

* **Keyless**
* **API key**
* **OAuth2**
* **JWT**
* **mTLS**

Every plan also carries a **Subscription validation** mode, set to either `AUTO` or `MANUAL`.

Once a plan is established, you can apply **Policies** to enforce quotas, message filtering, or access controls.

## Next steps

* **Provision a Virtual Cluster**. Add multi-tenant isolation on top of your Kafka Service. See [Establish a virtual cluster](establish-a-virtual-cluster.md).
* **Create topics**. Create Kafka topics for producing and consuming messages.
