---
hidden: false
noIndex: false
---
<--- to be published --->

# Create a Kafka service with a registered cluster
<!-- Source: gravitee-gamma-module-esm/src/main/ui/features/kafka-apis/components/create/CreateNativeApiWizard.tsx -->

A Kafka Service is the client-facing endpoint managed by Gravitee. It is the Event Stream Management equivalent of an API proxy — the Kafka Service is the governance layer that enforces authentication, security plans, ACLs, and quotas before routing traffic to the backend infrastructure. 

The backend infrastructure can be a standalone broker list, a specific connection on a registered physical cluster, or a Virtual Cluster.

{% hint style="info" %}
For a simplified walkthrough that covers just the basics, see [Create your first Kafka service](../get-started/create-your-first-kafka-service.md).
{% endhint %}

## How Kafka services work

When you create a Kafka Service, you define how clients connect to it (the **Listener**) and how the service reaches Kafka (the **Endpoint Binding**). The Event Gateway enforces the service's configuration at runtime — every produce and consume operation passes through the gateway, where security plans, authorization policies, and rate limits are evaluated.

A single Kafka Service can route to multiple clusters by binding to a Virtual Cluster, or multiple Kafka Services can bind to the same registered cluster to provide different governance tiers.

## Prerequisites

* Access to a running Gamma console instance
* At least one registered Kafka cluster (see [Register your Kafka clusters](../import/register-your-kafka-clusters.md))

## Create a Kafka service

1. From the Gamma console sidebar, select **Event Stream Management**.
2. Navigate to **Kafka Services**.
3. Select **Create Kafka Service**.

### 1. Identity

| Field            | Description                                                                          |
| ---------------- | ------------------------------------------------------------------------------------ |
| **Name**         | A human-readable name that identifies this Kafka Service in the console and Catalog. |
| **Version**      | The version of this service (e.g., 1.0).                                             |
| **Description**  | Optional. A description of the service's purpose.                                    |

### 2. Listener

The listener defines the entrypoint that Kafka clients will connect to. 

| Field           | Description                                                                                                  |
| --------------- | ----------------------------------------------------------------------------------------------------------- |
| **Host prefix** | A single DNS label (lowercase letters, digits, and hyphens; max 63 characters). The Event Gateway appends its configured domain, and clients connect on the gateway's SNI port — for example `orders.<gateway-domain>:<sni-port>`. The port is a gateway-level setting and is not configured here. |

### 3. Endpoint

The endpoint binding determines how the Kafka Service reaches Kafka. Choose one of the following modes:

* **Standalone**: Manually provide a comma-separated list of `host:port` bootstrap servers.
* **Managed cluster**: Select a registered Kafka cluster and one of its configured connections.
* **Virtual Cluster**: Select a Virtual Cluster to route traffic through a unified namespace or Kafka Mesh.

### 4. Review and create

1. Review the service identity, listener, and endpoint binding.
2. Select **Create Kafka Service**.

The console creates the Kafka Service and redirects you to its overview page.

## Configure Plans and Policies

After creating the Kafka Service, you must configure a **Plan** to allow clients to consume from or produce to the service.

The following security plan types are available:
* **Keyless (Public)**
* **API Key**
* **OAuth2**
* **JWT**
* **mTLS**

Plans support **Subscription validation** (Auto or Manual) and advanced **Port-based routing** (Bootstrap port, broker range start, broker range end) for gateways running in port routing mode without SNI.

Once a plan is established, you can apply **Policies** to enforce quotas, message filtering, or access controls.

## Expose as a Kafka API Tool

Once a Kafka Service is running, you can expose its topics as **Kafka API Tools** in the Catalog, bridging your event infrastructure to the AI agent layer. Kafka API Tools become available as building blocks in MCP Studio alongside other tools, resources, and prompts.

## Next steps

* **Provision a Virtual Cluster** — Add multi-tenant isolation on top of your Kafka Service. See [Establish a virtual cluster](establish-a-virtual-cluster.md).
* **Create topics** — Set up Kafka topics for producing and consuming messages.
