---
hidden: false
noIndex: false
description: Create a Kafka Service in Event Stream Management backed by a Virtual Cluster, so that Kafka clients reach topics spread across several clusters through one endpoint. Follow the steps to build it in the wizard.
---

# Create a Kafka Service with a Virtual Cluster

A Kafka Service backed by a Virtual Cluster gives Kafka clients one endpoint for topics spread across several Kafka backends. The Virtual Cluster federates the connections of your registered clusters, and the Kafka Service adds the plans, the policies, and the observability on top of that endpoint.

Use this approach when clients work with topics that live on several clusters, and you don't want them to manage a connection per cluster.

{% hint style="info" %}
To bind a Kafka Service to a single connection of a registered cluster instead, or to bootstrap servers, see [Create a Kafka Service with a registered cluster](create-a-kafka-service-with-a-registered-cluster.md).
{% endhint %}

## How it works

Clients connect to the Kafka Service's listener. The Event Gateway resolves which backend of the Virtual Cluster owns each topic, and routes each operation to that backend. Clients see one Kafka endpoint.

Several Kafka Services can bind to the same Virtual Cluster, each with its own plans and policies.

## Prerequisites

* Access to a running Gamma console instance, with an environment role that can create APIs.
* A Virtual Cluster with at least one backend, in the **Deployed** state. Its backends are connections of deployed registered clusters. See [Establish a Virtual Cluster](../../kafka-infrastructure/virtual-clusters/establish-a-virtual-cluster.md).

The wizard lists only deployed Virtual Clusters. A Virtual Cluster that is undeployed, or has changes waiting to be deployed, doesn't appear.

## Create the Kafka Service

1. From the Gamma console, open **Event Stream Management**.
2. In the **APIs** group of the sidebar, click **Kafka Services**.
3. Click **Create Kafka Service**.

The wizard has five steps. The button that moves forward names the next step, for example **Next: Listener**.

### 1. Identity

Enter the **Name** of the Kafka Service, up to 255 characters, and its **Version**, pre-filled with `1.0`. Both are required. The **Description** is optional.

### 2. Listener

Enter the **Host prefix**. The Event Gateway appends its configured domain, and clients connect on the gateway's SNI port.

The prefix uses lowercase letters, digits, hyphens, and underscores, with dots to separate labels. Its first label has at most 49 characters, the whole prefix has at most 241 characters, and no other API in the environment can use it. The console checks the availability of the host while you type. See [Listener](create-a-kafka-service-with-a-registered-cluster.md#listener) for every rule.

### 3. Endpoint

1. Select the **Virtual Cluster** binding mode.
2. In **Virtual Cluster**, select the Virtual Cluster that the Kafka Service routes through.

With no deployed Virtual Cluster, the step shows **No deployed Virtual Clusters. Deploy a Virtual Cluster first, then bind to it here.**

### 4. Security

The step adds a **Keyless plan**, which is published at creation. Keep it, or remove it and add a plan of another type. Plans other than Keyless are created in **Staging** and are finished on the **Plans** page. See [Security](create-a-kafka-service-with-a-registered-cluster.md#security).

### 5. Review

1. Check the identity, the listener, the binding, and the plans.
2. Optional: Select **Deploy now** to start the Kafka Service on the gateway right after creation. When the environment uses the API review workflow, the step offers **Ask for review** instead.
3. Click **Create Kafka Service**.

The console confirms with **Kafka Service created** and opens the **Overview** page of the Kafka Service. Without **Deploy now**, the Kafka Service is created stopped.

## When the Virtual Cluster isn't deployed

A Kafka Service can't start while its Virtual Cluster isn't deployed. When you open such a Kafka Service, a **Virtual Cluster not deployed** banner names the Virtual Cluster and links to it, and the **Start** button of the page header, the **Start Kafka Service** tile of the **Settings** page, and the **Start** action of its row in the **Kafka Services** list are disabled. Deploy the Virtual Cluster, then start the Kafka Service.

## Verification

To verify the Kafka Service, follow these steps:

1. Open the Kafka Service.
2. On the **Overview** page, check that **Backend binding** reads **Virtual Cluster**.
3. When the Kafka Service is started, check that the **Bootstrap server** card shows the address that clients use.

## Next steps

* **Finish the plans**. See [Manage plans](manage-plans.md).
* **Apply policies**. See [Design flows in the Policy Studio](design-flows-in-the-policy-studio.md).
* **Understand the Virtual Cluster's runtime behavior**. Topic routing, consumer groups, and the operations that a Virtual Cluster refuses. See [Virtual Cluster runtime behavior reference](../../kafka-infrastructure/virtual-clusters/kafka-virtual-cluster-runtime-behavior-reference.md).
* **Monitor the Kafka Service**. Open its **Dashboard**, **Logs**, and **Tracing** from the **Observability** group of its sidebar. See [Observability](../../observability/README.md).
