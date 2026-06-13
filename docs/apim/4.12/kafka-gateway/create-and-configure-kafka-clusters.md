---
description: An overview about create and configure kafka clusters.
metaLinks:
  alternates:
    - create-and-configure-kafka-clusters.md
---

# Create and Configure Kafka Clusters

## Overview

The Kafka UI is accessible from the APIM Console. It is the user interface from which you can create and manage Kafka clusters, configure cluster connection information, and manage user access and permissions.

A Kafka Cluster is a reusable connection profile to a single backend Kafka cluster. Multiple APIs can reference the same Cluster entity, and updates to the Cluster propagate to all referencing APIs.

A Kafka Virtual Cluster aggregates multiple Kafka Cluster entities into a single virtual cluster, enabling you to present multiple backend Kafka clusters as one unified cluster to client applications. This capability allows you to distribute topics across separate physical clusters while maintaining a single client connection point.

Both Kafka Cluster and Kafka Virtual Cluster entities are governed by a single **CLUSTER** environment-scoped permission (mask 4000).

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
   1. In the **Cluster name** field, enter a name for your cluster. This field is required. If you do not enter a name, you will receive the validation error "Name is required."
   2. (Optional) In the description field, enter a description for your cluster.
   3. In the **Bootstrap Servers** field, enter the bootstrap servers for your cluster in the format `host1:port1,host2:port2,...`.
   4.  Click **Create**. You are brought to the cluster's configuration screen.

       <figure><img src="../.gitbook/assets/F7727719-AE67-4E84-A45B-478A4D66E2F5_1_201_a.jpeg" alt=""><figcaption></figcaption></figure>

       <figure><img src="../.gitbook/assets/kafka-cluster-add-dialog.png" alt="Create a new cluster dialog with fields for cluster name, description, and bootstrap servers"><figcaption></figcaption></figure>

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
* Enter a **Cross ID** for external references. The Cross ID is auto-generated via lowercase, alphanumeric characters plus hyphens, with no leading or trailing dashes if not provided. The Cross ID must be unique within the environment. If you attempt to create a cluster with a duplicate Cross ID, you will receive the validation error "A cluster with crossId '{crossId}' already exists in this environment." The Cross ID is immutable after creation. If you attempt to update the Cross ID, you will receive the validation error "CrossId is immutable and cannot be changed after creation."

To delete the cluster, complete the following steps:

{% hint style="warning" %}
Once you delete a cluster, this action cannot be undone.
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

#### Add a connection

You can configure one or more connections to the backend cluster. To add a connection, complete the following steps:

1. Click **Add Connection**.
2. Enter a **Connection Name**. Connection names must be unique within a Kafka Cluster. If you attempt to create a connection with a duplicate name, you will receive the validation error "Connection names must be unique. Duplicates found: [list]".
3. Enter a **Connection Cross ID**. The Connection Cross ID is auto-generated if not provided. Connection crossIds must be unique within a cluster. If you attempt to create a connection with a duplicate crossId, you will receive the validation error "Connection crossIds must be unique within a cluster. Duplicates found: {list}".
4. Enter **Bootstrap Servers** in the format `host1:port1,host2:port2,...`.
5. Select a **Security Protocol** from the dropdown: **PLAINTEXT**, **SSL**, **SASL_PLAINTEXT**, or **SASL_SSL**.
6. If **SASL_PLAINTEXT** or **SASL_SSL** is selected, configure the **SASL Mechanism** and credentials:
   * **SASL Mechanism**: Select **PLAIN**, **SCRAM-SHA-256**, **SCRAM-SHA-512**, **OAUTHBEARER**, **OAUTHBEARER_TOKEN**, **AWS_MSK_IAM**, **GSSAPI**, or **Delegate To Broker**.
   * For **PLAIN**, **SCRAM-SHA-256**, or **SCRAM-SHA-512**: Enter **Username** and **Password**.
   * For **OAUTHBEARER**: Configure token endpoint and credentials.
   * For **Delegate To Broker**: No additional credentials required (gateway replays client credentials).
7. If **SSL** or **SASL_SSL** is selected, configure SSL settings:
   * **Truststore**: Upload a JKS file or paste PEM-encoded certificates.
   * **Keystore**: Upload a JKS file or paste PEM-encoded key and certificate.
   * **Key Password**: Enter the keystore key password.
8. Click **Save** to add the connection.

The following table describes the configuration fields for Kafka clusters and connections:

| Field | Description | Example |
|:------|:------------|:--------|
| **Name** | Human-readable cluster name (required) | `eu-prod` |
| **Cross ID** | Portable identifier for cross-environment references (auto-generated from name if not provided; immutable after creation; must be unique within environment) | `eu-prod` |
| **Description** | Optional cluster description | `Production cluster in EU region` |
| **Connection Name** | Human-readable connection name (must be unique within cluster) | `sasl-ssl-9095` |
| **Connection Cross ID** | Portable identifier for connection (auto-generated from connection name if not provided; must be unique within cluster) | `sasl-ssl-9095` |
| **Bootstrap Servers** | Comma-separated list of broker addresses | `broker1.example.com:9092,broker2.example.com:9092` |
| **Security Protocol** | Transport security mode | `SASL_SSL` |
| **SASL Mechanism** | SASL authentication mechanism | `SCRAM-SHA-256` |
| **Username** | SASL username | `kafka-user` |
| **Password** | SASL password | `********` |
| **Truststore** | SSL truststore (JKS path or PEM content) | `/path/to/truststore.jks` |
| **Keystore** | SSL keystore (JKS path or PEM content) | `/path/to/keystore.jks` |
| **Key Password** | Keystore key password | `********` |

### User permissions

In the **User Permissions** tab, you can configure the following elements related to users:

* [#manage-groups](create-and-configure-kafka-clusters.md#manage-groups "mention")
* [#transfer-ownership](create-and-configure-kafka-clusters.md#transfer-ownership "mention")
* [#add-members](create-and-configure-kafka-clusters.md#add-members "mention")

You can grant USER role on this cluster to specific subjects. This role is used by the Kafka Console UI to scope visibility.

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
