---
description: An overview about create and configure kafka clusters.
metaLinks:
  alternates:
    - create-and-configure-kafka-clusters.md
---

# Create and Configure Kafka Clusters

## Overview

{% hint style="warning" %}
This feature is in tech preview. Contact your customer team to request access to this feature.
{% endhint %}

The Kafka UI is accessible from the APIM Console. It is the user interface from which you can create and manage Kafka clusters and virtual clusters, configure cluster connection information, manage cluster lifecycle (deploy, undeploy, delete), and manage user access and permissions.

The console navigation includes a **Kafka** menu with three sub-items:

* **Standalone**
* **Clusters**
* **Virtual Clusters**

## Prerequisites

{% hint style="warning" %}
Kafka Console is currently only available for self-hosted deployments and not compatible with next-gen cloud.
{% endhint %}

* You must have an Enterprise License with the apim-cluster feature. For more information about Gravitee Enterprise Edition, see [enterprise-edition.md](../readme/enterprise-edition.md "mention").

## Create a Kafka Cluster

1.  From the Dashboard, click **Kafka Cluster**.

    <figure><img src="../.gitbook/assets/83D2B577-1393-4048-8E93-56DB9E8CFB8E_1_201_a.jpeg" alt=""><figcaption></figcaption></figure>
2.  Click **+ Add cluster**.

    <figure><img src="../.gitbook/assets/902A4021-EA90-4AB6-84B4-C0F9E995F54E_1_201_a (1).jpeg" alt=""><figcaption></figcaption></figure>
3. In the **Create a new cluster** pop-up window, complete the following sub-steps:
   1. In the **Cluster name** field, enter a name for your cluster (required, max 512 characters).
   2. (Optional) In the description field, enter a description for your cluster (max 1024 characters).
   3. In the **Connections** section, add one or more named connections. For each connection:
      1. Enter a **Name** for the connection.
      2. In the **Bootstrap Servers** field, enter the bootstrap servers for your cluster (comma-separated list of `host:port` pairs).
      3. Select a **Security Protocol** (`PLAINTEXT`, `SASL_PLAINTEXT`, `SASL_SSL`, or `SSL`).
      4. If the protocol is `SASL_PLAINTEXT` or `SASL_SSL`, select a **SASL Mechanism** (`PLAIN`, `SCRAM-SHA-256`, `SCRAM-SHA-512`, `AWS_MSK_IAM`, `GSSAPI`, `OAUTHBEARER`, `OAUTHBEARER_TOKEN`, or `DELEGATE_TO_BROKER`).
   4.  Click **Create**. You are brought to the cluster's configuration screen. The cluster is created in the `UNDEPLOYED` state.

       <figure><img src="../.gitbook/assets/F7727719-AE67-4E84-A45B-478A4D66E2F5_1_201_a.jpeg" alt=""><figcaption></figcaption></figure>

**Kafka Cluster Configuration Reference:**

| Field | Description | Example |
|:------|:------------|:--------|
| Name | Cluster name | `us-east-kafka` |
| Description | Optional cluster description | `Production Kafka cluster in US East` |
| Connections | Array of named connections | `[{ name: "primary", bootstrapServers: "broker1:9092,broker2:9092", security: {...} }]` |
| Bootstrap Servers | Comma-separated broker addresses | `broker1:9092,broker2:9092` |
| Security Protocol | Connection security protocol | `SASL_SSL` |
| SASL Mechanism | SASL authentication mechanism (if protocol is `SASL_*`) | `PLAIN` |

## Create a Kafka Virtual Cluster

1. Navigate to **Kafka > Virtual Clusters** in the console.
2. Click **Add Virtual Cluster**.
3. In the **Create a new virtual cluster** pop-up window, complete the following sub-steps:
   1. In the **Name** field, enter a name for your virtual cluster (required, max 512 characters).
   2. (Optional) In the **Description** field, enter a description for your virtual cluster (max 1024 characters).
   3. In the **Backends** section, add one or more backend references. For each backend:
      1. Select a **Cluster** from the autocomplete dropdown (filters to deployed `KAFKA_CLUSTER` instances).
      2. Select a **Connection** from the autocomplete dropdown (filters to connections within the selected cluster).
   4. Click **Create**. The virtual cluster is created in the `UNDEPLOYED` state.

**Kafka Virtual Cluster Configuration Reference:**

| Field | Description | Example |
|:------|:------------|:--------|
| Name | Virtual cluster name | `global-kafka` |
| Description | Optional virtual cluster description | `Aggregated view of US and EU clusters` |
| Backends | Array of backend cluster references | `[{ clusterCrossId: "abc123", connectionCrossId: "conn1" }]` |
| Cluster | Deployed cluster to reference | `us-east-kafka` |
| Connection | Connection within the selected cluster | `primary` |

## Configure your Kafka cluster

The configuration for your Kafka cluster is divided into the following sections:

* [#general](create-and-configure-kafka-clusters.md#general "mention")
* [#configuration](create-and-configure-kafka-clusters.md#configuration "mention")
* [#user-permissions](create-and-configure-kafka-clusters.md#user-permissions "mention")

### General

In the **General** tab, you can perform the following actions:

* View or edit the name of the cluster.
* View or edit the description of the cluster.
* View the day and time that the cluster was created.
* View the day and time that the cluster was last updated.
* View the read-only **Cross ID** field.

#### Deploy a cluster

To deploy a cluster, navigate to the **Danger Zone** section, and then click **Deploy**. The cluster transitions to `PENDING` and then `DEPLOYED` once the configuration is propagated to all gateways. Deployed clusters are available for selection in virtual cluster backends and API endpoint configurations.

The gateway retries bind failures up to 3 times with exponential backoff (50ms, 100ms, 200ms). Persistent bind failures fail gateway boot after 350ms.

#### Undeploy a cluster

To undeploy a cluster, navigate to the **Danger Zone** section, and then click **Undeploy**. The cluster transitions to `PENDING` and then `UNDEPLOYED` once all gateways release cached endpoints and pooled connections. Undeployed clusters are removed from virtual cluster backend autocomplete dropdowns.

{% hint style="warning" %}
Deployed clusters (`KAFKA_CLUSTER`, `KAFKA_VIRTUAL_CLUSTER`) must be undeployed before deletion. Direct API calls must invoke `POST /clusters/{id}/_undeploy` before `DELETE /clusters/{id}`.
{% endhint %}

#### Delete a cluster

To delete the cluster, complete the following steps:

{% hint style="warning" %}
Once you delete a cluster, this action cannot be undone. If the cluster is `DEPLOYED` or `PENDING`, it will be undeployed and then deleted.
{% endhint %}

1. Navigate to the **Danger Zone** section, and then click **Delete**.
2. In the **Delete Cluster** pop-up window, enter the name of the Kafka cluster.
3.  Click **Yes, delete it.**

    <figure><img src="../.gitbook/assets/42CDC273-4677-4127-A6DF-FBB3B7F53842_1_201_a.jpeg" alt=""><figcaption></figcaption></figure>

### Configuration

In the **Configuration** tab, you can configure the following elements of the cluster:

* The Bootstrap Servers.
* Security. By Default, the security protocol is set to **PLAINTEXT**. You can choose from the following security protocols for your cluster:
  * SASL\_PLAINTEXT
  * SASL\_SSL
  *   SSL

      <figure><img src="../.gitbook/assets/9FAEF4B2-47B4-4D19-B2D2-D063ED96CAED_1_201_a.jpeg" alt=""><figcaption></figcaption></figure>

The cluster autocomplete only lists clusters in `DEPLOYED` state; undeployed and pending clusters are hidden.

### User permissions

In the **User Permissions** tab, you can configure the following elements related to users:

* [#manage-groups](create-and-configure-kafka-clusters.md#manage-groups "mention")
* [#transfer-ownership](create-and-configure-kafka-clusters.md#transfer-ownership "mention")
* [#add-members](create-and-configure-kafka-clusters.md#add-members "mention")

#### Manage groups

To add a group to your Kafka cluster, complete the following steps:

1. From the **User Permissions** tab, click **Manage groups**.
2. In the **Manage groups** pop-up window, click the **Groups** drop-down menu, and then select the group or groups that you want to add to your cluster.
3.  Click **Save**.

    <figure><img src="../.gitbook/assets/00 kafkaUI 1.png" alt=""><figcaption></figcaption></figure>

#### Transfer ownership

To transfer ownership of your Kafka cluster to another user, complete the following steps:

{% hint style="warning" %}
Once you transfer ownership of a cluster, this action cannot be undone.
{% endhint %}

1. From the **User Permissions** tab, click **Transfer ownership**.
2. Under **Choose a new Primary Owner**, click either **Cluster member** or **Other user**.
3. Specify the new primary owner.
   1. If you clicked **Cluster member**, use the drop-down menu to select another member of the cluster as the primary owner.
   2. If you clicked **Other user**, use the search field to find the user you want to set as the primary owner.
4. Use the **New role for current Primary Owner** drop-down menu to select either **User** or **Owner** as the new cluster role for the current primary owner.
5.  Click **Transfer**.

    <figure><img src="../.gitbook/assets/00 kafkaUI 2.png" alt=""><figcaption></figcaption></figure>

#### Add members

To add members to your Kafka cluster, complete the following steps:

1. From the **User Permissions** tab, click **+ Add members**.
2. In the **Select users** pop-up window, search for users by name or email. You can add multiple users at a time.
3.  Click **Select**.

    <figure><img src="../.gitbook/assets/00 kafkaUI 4.png" alt=""><figcaption></figcaption></figure>

## Virtual cluster restrictions

* Transactional producers are not supported on virtual clusters.
* Only the `PLAIN` SASL mechanism supports credential replay for cross-cluster operations. `AWS_MSK_IAM`, `SCRAM-SHA-*`, and `GSSAPI` mechanisms are not captured and cannot be replayed on backend connections.
* Virtual clusters strip the share-group API (KIP-932) from `ApiVersions` responses; share groups are not supported.
* Backend connection pooling is scoped per-API, not process-wide. Multiple APIs targeting the same backend cluster open separate connection pools.
* Virtual cluster metadata (controller ID, cluster ID) is cached after the first metadata merge. Until then, frame rewriters fall back to per-cluster values, which may cause instability across client reconnects.

