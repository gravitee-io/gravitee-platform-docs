---
description: An overview about create and configure kafka clusters.
metaLinks:
  alternates:
    - create-and-configure-kafka-clusters.md
---

# Create and Configure Kafka Clusters

## Overview

The Kafka UI is accessible from the APIM Console. It is the user interface from which you can create and manage Kafka clusters, configure cluster connection information, and manage user access and permissions.

Kafka Virtual Clusters enable you to present multiple independent Kafka backends as a single unified cluster to client applications. For more information, see [Kafka Virtual Clusters](kafka-virtual-clusters-overview.md#kafka-virtual-clusters-overview).

## Prerequisites

{% hint style="warning" %}
Kafka Console is currently only available for self-hosted deployments and not compatible with next-gen cloud.
{% endhint %}

* You must have an Enterprise License with the apim-cluster feature. For more information about Gravitee Enterprise Edition, see [enterprise-edition.md](../introduction/enterprise-edition.md "mention").

## Create a Kafka Cluster

1.  From the Dashboard, click **Kafka Cluster**.

    <figure><img src="../.gitbook/assets/83D2B577-1393-4048-8E93-56DB9E8CFB8E_1_201_a.jpeg" alt=""><figcaption></figcaption></figure>
2.  Click **+ Add cluster**.

    <figure><img src="../.gitbook/assets/902A4021-EA90-4AB6-84B4-C0F9E995F54E_1_201_a (1).jpeg" alt=""><figcaption></figcaption></figure>
3. In the **Create a new cluster** pop-up window, complete the following sub-steps:
   1. In the **Cluster name** field, enter a name for your cluster.
   2. (Optional) In the **Cross ID** field, enter an external identifier for GKO or config-as-code. If not provided, the gateway auto-generates it from the cluster name.
   3. (Optional) In the **Description** field, enter a description for your cluster.
   4.  Click **Create**. The cluster is created with no connections. You are brought to the cluster's configuration screen.

       <figure><img src="../.gitbook/assets/F7727719-AE67-4E84-A45B-478A4D66E2F5_1_201_a.jpeg" alt=""><figcaption></figcaption></figure>

{% hint style="info" %}
Cross ID is immutable after creation.
{% endhint %}

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

To delete the cluster, complete the following steps:

{% hint style="warning" %}
Once you delete a cluster, this action cannot be undone.
{% endhint %}

1. Navigate to the **Danger Zone** section, and then click **Delete**.
2. In the **Delete Cluster** pop-up window, enter the name of the Kafka cluster.
3.  Click **Yes, delete it.**

    <figure><img src="../.gitbook/assets/42CDC273-4677-4127-A6DF-FBB3B7F53842_1_201_a.jpeg" alt=""><figcaption></figcaption></figure>

### Configuration

In the **Configuration** tab, you can configure connections to your Kafka cluster.

#### Add a connection

To add a connection to your Kafka cluster, complete the following steps:

1. From the **Configuration** tab, click **Add Connection**.
2. In the **Name** field, enter a name for the connection.
3. (Optional) In the **Cross ID** field, enter a portable identifier for cross-environment references. If not provided, the gateway auto-generates it from the connection name.
4. In the **Bootstrap Servers** field, enter a comma-separated list of broker addresses.
5. Use the **Security Protocol** drop-down menu to select a security protocol for your connection. You can choose from the following security protocols:
   * PLAINTEXT
   * SSL
   * SASL_PLAINTEXT
   * SASL_SSL
6. If you selected a SASL protocol, use the **SASL Mechanism** drop-down menu to select a SASL authentication mechanism. You can choose from the following SASL mechanisms:
   * PLAIN
   * SCRAM-SHA-256
   * SCRAM-SHA-512
   * OAUTHBEARER
   * OAUTHBEARER_TOKEN
   * AWS_MSK_IAM
   * GSSAPI
   * Delegate to Broker
7. If you selected a SASL mechanism other than Delegate to Broker, enter the required credentials (username/password for PLAIN, token for OAUTHBEARER, etc.).
8. If you selected an SSL protocol, configure the **Truststore** and **Keystore** (JKS path or inline PEM).
9.  Click **Save** to add the connection.

    <figure><img src="../.gitbook/assets/9FAEF4B2-47B4-4D19-B2D2-D063ED96CAED_1_201_a.jpeg" alt=""><figcaption></figcaption></figure>

Repeat these steps to add additional connections to the cluster.

{% hint style="info" %}
Connection names within a Kafka Cluster must be unique. The connections array can be empty (minimum 0 items).
{% endhint %}

#### Connection configuration reference

<table><thead><tr><th>Field</th><th>Description</th><th>Example</th></tr></thead><tbody><tr><td>Name</td><td>Identifier for this connection within the cluster</td><td><code>internal-plaintext</code></td></tr><tr><td>Cross ID</td><td>Portable identifier for cross-environment references</td><td><code>internal-plaintext</code></td></tr><tr><td>Bootstrap Servers</td><td>Comma-separated list of broker addresses</td><td><code>kafka1.example.com:9092,kafka2.example.com:9092</code></td></tr><tr><td>Security Protocol</td><td>Connection security mode</td><td><code>SASL_SSL</code></td></tr><tr><td>SASL Mechanism</td><td>SASL authentication mechanism (if SASL protocol selected)</td><td><code>SCRAM-SHA-256</code></td></tr><tr><td>SASL Credentials</td><td>Username, password, or token (mechanism-dependent)</td><td><code>user=admin, password=secret</code></td></tr><tr><td>Truststore</td><td>SSL truststore configuration (if SSL protocol selected)</td><td>JKS path or inline PEM</td></tr><tr><td>Keystore</td><td>SSL keystore configuration (if SSL protocol selected)</td><td>JKS path or inline PEM</td></tr></tbody></table>

### User permissions

In the **User Permissions** tab, you can configure the following elements related to users:

* [#manage-groups](create-and-configure-kafka-clusters.md#manage-groups "mention")
* [#transfer-ownership](create-and-configure-kafka-clusters.md#transfer-ownership "mention")
* [#add-members](create-and-configure-kafka-clusters.md#add-members "mention")

You can also grant USER role on this cluster to specific subjects to scope visibility in the Kafka Console UI.

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
