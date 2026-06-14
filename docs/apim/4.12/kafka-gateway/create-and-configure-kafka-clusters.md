---
description: An overview about create and configure kafka clusters.
metaLinks:
  alternates:
    - create-and-configure-kafka-clusters.md
---

# Create and Configure Kafka Clusters

## Overview

The Kafka UI is accessible from the APIM Console. It is the user interface from which you can create and manage Kafka clusters, configure cluster connection information, and manage user access and permissions.

## Prerequisites

{% hint style="warning" %}
Kafka Console is currently only available for self-hosted deployments and not compatible with next-gen cloud.
{% endhint %}

* You must have an Enterprise License with the apim-cluster feature. For more information about Gravitee Enterprise Edition, see [enterprise-edition.md](../introduction/enterprise-edition.md "mention").

## Create a Kafka Cluster

1.  From the APIM Console Dashboard, click **Kafka Cluster**.

    <figure><img src="../.gitbook/assets/83D2B577-1393-4048-8E93-56DB9E8CFB8E_1_201_a.jpeg" alt=""><figcaption></figcaption></figure>
2.  Click **+ Add cluster**.

    <figure><img src="../.gitbook/assets/902A4021-EA90-4AB6-84B4-C0F9E995F54E_1_201_a (1).jpeg" alt=""><figcaption></figcaption></figure>
3. In the **Create a new cluster** pop-up window, complete the following sub-steps:
   1. In the **Cluster name** field, enter a name for your cluster.
   2. (Optional) In the **Cross ID** field, enter a portable identifier for external references or configuration-as-code workflows. If omitted, the system auto-generates one from the name. The Cross ID is immutable after creation.
   3. (Optional) In the **Description** field, enter a description for your cluster.
   4.  Click **Create**. The cluster is created with no connections. You are brought to the cluster's configuration screen.

       <figure><img src="../.gitbook/assets/F7727719-AE67-4E84-A45B-478A4D66E2F5_1_201_a.jpeg" alt=""><figcaption></figcaption></figure>

## Configure your Kafka cluster

The configuration for your Kafka cluster is divided into the following sections:

* [#general](create-and-configure-kafka-clusters.md#general "mention")
* [#configuration](create-and-configure-kafka-clusters.md#configuration "mention")
* [#user-permissions](create-and-configure-kafka-clusters.md#user-permissions "mention")

### General

In the **General** tab, you can perform the following actions:

* View or edit the name of the cluster.
* View or edit the Cross ID of the cluster.
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

In the **Configuration** tab, you can configure connections to the backend Kafka cluster. Each cluster can have multiple connections to the same backend cluster (e.g., different listeners with different authentication profiles).

#### Add a Connection

1. From the **Configuration** tab, click **Add Connection**.
2. In the **Connection Name** field, enter a human-readable name for this connection. Connection names must be unique within the cluster.
3. (Optional) In the **Connection Cross ID** field, enter a portable identifier for this connection. If omitted, the system auto-generates one from the name. Connection Cross IDs must be unique within the cluster.
4. In the **Bootstrap Servers** field, enter the bootstrap servers for your cluster in the format `host1:port1,host2:port2,...`.
5. From the **Security Protocol** drop-down menu, select the protocol for client-broker communication. Valid values are:
   * PLAINTEXT
   * SSL
   * SASL_PLAINTEXT
   * SASL_SSL
6. If you selected SASL_PLAINTEXT or SASL_SSL, complete the following sub-steps:
   1. From the **SASL Mechanism** drop-down menu, select the SASL mechanism for authentication. Valid values are:
      * PLAIN
      * SCRAM-SHA-256
      * SCRAM-SHA-512
      * OAUTHBEARER
      * OAUTHBEARER_TOKEN
      * AWS_MSK_IAM
      * GSSAPI
      * DELEGATE_TO_BROKER
   2. Provide the required SASL credentials (username, password, token, or AWS credentials depending on the mechanism).
7. If you selected SSL or SASL_SSL, complete the following sub-steps:
   1. Configure the **Truststore** (JKS path or inline PEM) for SSL/TLS.
   2. (Optional) Configure the **Keystore** (JKS path or inline PEM) for mutual TLS.
   3. (Optional) Enter the **Key Password** for the SSL keystore.
8. Click **Save** to add the connection.
9. Repeat steps 1–8 to add additional connections to the same backend cluster.

    <figure><img src="../.gitbook/assets/9FAEF4B2-47B4-4D19-B2D2-D063ED96CAED_1_201_a.jpeg" alt=""><figcaption></figcaption></figure>

#### Connection configuration reference

| Field | Description | Required |
|:------|:------------|:---------|
| **Connection Name** | Human-readable name for this connection. Must be unique within the cluster. | Yes |
| **Connection Cross ID** | Portable identifier for this connection. Auto-generated from name if not provided. Must be unique within the cluster. | No |
| **Bootstrap Servers** | Comma-separated list of Kafka broker addresses (e.g., `kafka.example.com:9092`). | Yes |
| **Security Protocol** | Protocol for client-broker communication. Valid values: PLAINTEXT, SSL, SASL_PLAINTEXT, SASL_SSL. | Yes |
| **SASL Mechanism** | SASL mechanism for authentication. Valid values: NONE, PLAIN, SCRAM-SHA-256, SCRAM-SHA-512, OAUTHBEARER, OAUTHBEARER_TOKEN, AWS_MSK_IAM, GSSAPI, DELEGATE_TO_BROKER. Required when Security Protocol is SASL_PLAINTEXT or SASL_SSL. | Conditional |
| **SASL Credentials** | Credentials for SASL authentication (username, password, token, or AWS credentials depending on mechanism). | Conditional |
| **SSL Truststore** | Truststore configuration (JKS path or inline PEM) for SSL/TLS. Required when Security Protocol is SSL or SASL_SSL. | Conditional |
| **SSL Keystore** | Keystore configuration (JKS path or inline PEM) for mutual TLS. | No |
| **SSL Key Password** | Password for the SSL keystore. | No |

### User permissions

In the **User Permissions** tab, you can configure the following elements related to users:

* [#manage-groups](create-and-configure-kafka-clusters.md#manage-groups "mention")
* [#transfer-ownership](create-and-configure-kafka-clusters.md#transfer-ownership "mention")
* [#add-members](create-and-configure-kafka-clusters.md#add-members "mention")

You can grant USER role on the cluster to specific subjects to control visibility in the Kafka Console UI.

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

## Deploy the cluster

After configuring connections and user permissions, click **Deploy** to activate the cluster on the gateway. The lifecycle state transitions to DEPLOYED, the version number increments, and the deployment timestamp is set.
