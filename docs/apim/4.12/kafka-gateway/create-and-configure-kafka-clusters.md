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

The Kafka UI is accessible from the APIM Console. It is the user interface from which you can create and manage Kafka clusters, Kafka virtual clusters, configure cluster connection information, and manage user access and permissions.

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
   1. In the **Cluster name** field, enter a name for your cluster.
   2. (Optional) In the **CrossId** field, enter an external identifier for GKO or config-as-code.
   3. (Optional) In the **Description** field, enter a description for your cluster.
   4. Click **Create**. The cluster is created empty with no connections.
4.  Open the cluster and navigate to the **Configuration** tab.

    <figure><img src="../.gitbook/assets/F7727719-AE67-4E84-A45B-478A4D66E2F5_1_201_a.jpeg" alt=""><figcaption></figcaption></figure>
5. Click **Add Connection** to add one or more connections.
6. For each connection, complete the following sub-steps:
   1. In the **Bootstrap Servers** field, enter the bootstrap servers for your cluster in the format `host1:port1,host2:port2,...`.
   2. Select a **Security Protocol** from the dropdown: PLAINTEXT, SSL, SASL_PLAINTEXT, or SASL_SSL.
   3. If SASL is selected, choose a **SASL Mechanism** (PLAIN, SCRAM-SHA-256, SCRAM-SHA-512, or OAUTHBEARER) and enter credentials.
   4. If SSL is selected, provide truststore, keystore, and key password (JKS path or inline PEM).

### Kafka Cluster Field Reference

<table><thead><tr><th>Field</th><th>Description</th><th>Example</th></tr></thead><tbody><tr><td><strong>Cluster Name</strong></td><td>Human-readable name for the cluster</td><td><code>eu-prod</code></td></tr><tr><td><strong>CrossId</strong></td><td>External identifier for GKO or config-as-code</td><td><code>eu-prod-cluster-001</code></td></tr><tr><td><strong>Description</strong></td><td>Optional description of the cluster</td><td><code>Production cluster in EU region</code></td></tr><tr><td><strong>Bootstrap Servers</strong></td><td>Comma-separated list of broker addresses</td><td><code>broker1.example.com:9092,broker2.example.com:9092</code></td></tr><tr><td><strong>Security Protocol</strong></td><td>Protocol for broker communication</td><td>PLAINTEXT, SSL, SASL_PLAINTEXT, SASL_SSL</td></tr><tr><td><strong>SASL Mechanism</strong></td><td>SASL authentication mechanism (if SASL protocol selected)</td><td>PLAIN, SCRAM-SHA-256, SCRAM-SHA-512, OAUTHBEARER</td></tr></tbody></table>

## Create a Kafka Virtual Cluster

1. Navigate to **Console → Kafka Virtual Clusters → Add**.
2. In the **Create a new virtual cluster** pop-up window, complete the following sub-steps:
   1. In the **Cluster name** field, enter a name for your virtual cluster.
   2. (Optional) In the **CrossId** field, enter an external identifier for GKO or config-as-code.
   3. (Optional) In the **Description** field, enter a description for your virtual cluster.
   4. Click **Save**. The virtual cluster is created empty with no backends.
3. Open the virtual cluster and navigate to the **Configuration** tab.
4. Click **Add Backend** to add one or more backends.
5. For each backend, complete the following sub-steps:
   1. Select a **Cluster** from the dropdown (filtered by `clusterType=KAFKA_CLUSTER`).
   2. Select a **Connection** from the second dropdown (lists connections from the selected Cluster).
   3. Repeat for every backend cluster you want the virtual cluster to span (minimum 2 backends recommended).

### Kafka Virtual Cluster Field Reference

<table><thead><tr><th>Field</th><th>Description</th><th>Example</th></tr></thead><tbody><tr><td><strong>Cluster Name</strong></td><td>Human-readable name for the virtual cluster</td><td><code>global-mesh</code></td></tr><tr><td><strong>CrossId</strong></td><td>External identifier for GKO or config-as-code</td><td><code>global-mesh-001</code></td></tr><tr><td><strong>Description</strong></td><td>Optional description of the virtual cluster</td><td><code>Virtual cluster spanning EU and US regions</code></td></tr><tr><td><strong>Cluster</strong></td><td>Reference to a Kafka Cluster entity</td><td><code>eu-prod</code></td></tr><tr><td><strong>Connection</strong></td><td>Reference to a connection within the selected Cluster</td><td><code>eu-prod-sasl-ssl</code></td></tr></tbody></table>

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
* Deploy or undeploy the cluster to the gateway.

#### Deploy and undeploy clusters

Click **Deploy this Cluster to the gateway** to transition the cluster from `UNDEPLOYED` to `DEPLOYED` state (via `PENDING`). Click **Undeploy this Cluster from the gateway** to transition from `DEPLOYED` to `UNDEPLOYED`.

{% hint style="info" %}
Only Kafka Cluster and Kafka Virtual Cluster entities support deployment. Standalone clusters (`KAFKA_CLUSTER_STANDALONE`) do not.
{% endhint %}

#### Delete a cluster

To delete the cluster, complete the following steps:

{% hint style="warning" %}
Once you delete a cluster, this action cannot be undone. If the cluster is deployed, it is automatically undeployed first.
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

### User permissions

In the **User Permissions** tab, you can configure the following elements related to users:

* [#manage-groups](create-and-configure-kafka-clusters.md#manage-groups "mention")
* [#transfer-ownership](create-and-configure-kafka-clusters.md#transfer-ownership "mention")
* [#add-members](create-and-configure-kafka-clusters.md#add-members "mention")

{% hint style="info" %}
User permissions granted on a cluster are used by the Kafka Console UI to scope visibility.
{% endhint %}

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
