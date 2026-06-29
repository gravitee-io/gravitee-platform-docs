---
hidden: false
noIndex: false
---
<-- to be published -->
# Create your first Kafka service
<!-- Source: gravitee-gamma-module-esm/src/main/ui/features/kafka-apis/components/create/CreateNativeApiWizard.tsx -->

This quickstart walks you through creating a governed Kafka Service in the Gamma console. You'll use the simplest configuration — a standalone endpoint with a keyless plan — to get a working Kafka Service in under five minutes.

{% hint style="info" %}
For a complete reference on all configuration options, see [Create a Kafka service with a registered cluster](../build/create-a-kafka-service-with-a-registered-cluster.md).
{% endhint %}

## Prerequisites

* Access to a running Gamma console instance
* A running Kafka cluster accessible from the Gamma platform (e.g., `kafka.example.com:9092`)

## Step 1: Open the Kafka Service wizard

1. From the Gamma console sidebar, select **Event Stream Management**.
2. Navigate to **Kafka Services**.
3. Select **Create Kafka Service**.

The console opens the Kafka Service creation wizard.

## Step 2: Configure the Kafka Service

The wizard guides you through the identity, listener, and endpoint configuration.

### Identity

| Field            | Value                     | Notes                                                        |
| ---------------- | ------------------------- | ------------------------------------------------------------ |
| **Name**         | `My First Kafka Service`  | Required. Identifies the service in the console and Catalog. |
| **Version**      | `1.0`                     | Required. The version of the service.                        |
| **Description**  | Leave blank               | Optional.                                                    |

Select **Next** to proceed.

### Listener

The listener is the address clients will use to connect to your Kafka Service.

| Field           | Value     | Notes                                                                                                       |
| --------------- | --------- | ----------------------------------------------------------------------------------------------------------- |
| **Host prefix** | `orders`  | Required. A single DNS label (lowercase letters, digits, and hyphens; max 63 characters). The Event Gateway appends its configured domain, and clients connect on the gateway's SNI port — for example `orders.<gateway-domain>:<sni-port>`. |

Select **Next** to proceed.

### Endpoint

The endpoint tells the Event Gateway how to reach your actual Kafka cluster.

1. For the binding mode, select **Standalone**.
2. In the **Bootstrap servers** field, enter your Kafka broker address (e.g., `kafka.example.com:9092`).

Select **Next** to proceed.

### Review and create

1. Review the identity, listener, and endpoint binding.
2. Select **Create Kafka Service**.

The console creates the Kafka Service and redirects you to its overview page.

## Step 3: Attach a Keyless Plan

To allow consumers to connect without authentication:

1. On the Kafka Service overview page, navigate to **Plans**.
2. Select **Create plan**.
3. Set the **Security type** to **Keyless (Public)**.
4. Name the plan `Public Plan`.
5. Select **Create plan**.

{% hint style="warning" %}
Keyless plans are intended for testing and internal use. For production Kafka Services, attach an appropriate security plan (like API Key, OAuth2, JWT, or mTLS).
{% endhint %}

## Step 4: Verify your Kafka Service

Once the plan is created and published, your Kafka Service is active. You can now configure your Kafka clients to connect to the listener address (`orders.<gateway-domain>:<sni-port>`) to interact with your cluster through the Event Gateway.

## Next steps

* **Create a Virtual Cluster** — Provision a logically isolated Kafka environment on top of your service. See [Establish a virtual cluster](../build/establish-a-virtual-cluster.md).
* **Create a topic** — Start producing and consuming messages.
* **Explore all configuration options** — Security plans, policies, and advanced settings. See [Create a Kafka service with a registered cluster](../build/create-a-kafka-service-with-a-registered-cluster.md).
