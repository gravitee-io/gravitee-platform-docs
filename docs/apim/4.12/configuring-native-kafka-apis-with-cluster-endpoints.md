# Configuring Native Kafka APIs with Cluster Endpoints

## Creating a Kafka Cluster

1. Navigate to **Console → Kafka → Standalone → Clusters**.
2. Click **Add cluster** in the upper right corner.

    <figure><img src=".gitbook/assets/kafka-cluster-add-dialog.png" alt="Create a new cluster dialog with empty fields for cluster name, description, and bootstrap servers"><figcaption></figcaption></figure>

3. Enter a **Cluster name** (for example, `eu-prod`).
4. (Optional) Enter a **Description** (for example, `Production Kafka cluster for EU region`).
5. Enter **Bootstrap Servers** in the format `host1:port1,host2:port2,...` (for example, `kafka.example.com:9092`). The field supports EL and Secrets.
6. Click **Create**.

    <figure><img src=".gitbook/assets/kafka-cluster-basic-info.png" alt="Create a new cluster dialog with cluster name eu-prod, description Production Kafka cluster for EU region, and bootstrap servers field visible"><figcaption></figcaption></figure>

The cluster is created with a default connection. To configure security settings:

7. Open the cluster and navigate to the **Configuration** tab.
8. Select a **Security Protocol** from the dropdown: PLAINTEXT, SSL, SASL_PLAINTEXT, or SASL_SSL.
9. If the protocol is SASL_PLAINTEXT or SASL_SSL, select a **SASL Mechanism** from the "Select SASL mechanism" dropdown: NONE, AWS_MSK_IAM, GSSAPI, OAUTHBEARER, OAUTHBEARER_TOKEN, PLAIN, SCRAM-SHA-256, SCRAM-SHA-512, or DELEGATE_TO_BROKER.
10. If the SASL mechanism is DELEGATE_TO_BROKER, no additional SASL configuration is required. For other SASL mechanisms, provide the required credentials (JAAS config or mechanism-specific fields).
11. If the protocol is SASL_SSL or SSL, configure the **Truststore**, **Keystore**, and **Key Password** (JKS path or inline PEM).

(Optional) Navigate to the **User Permissions** tab to grant USER role on this cluster to specific subjects. This controls visibility in the Kafka Console UI.

| Field | Description | Example |
|:------|:------------|:--------|
| **Bootstrap Servers** | Comma-separated list of Kafka broker addresses | `broker1.example.com:9092,broker2.example.com:9092` |
| **Security Protocol** | Transport security mode | SASL_SSL |
| **SASL Mechanism** | Authentication mechanism (visible when protocol is SASL_PLAINTEXT or SASL_SSL) | DELEGATE_TO_BROKER |
| **Truststore** | SSL trust material (visible when protocol is SASL_SSL or SSL) | JKS path or PEM content |
| **Keystore** | SSL client certificate (visible when protocol is SASL_SSL or SSL) | JKS path or PEM content |

A single cluster can contain multiple connections to model different listeners on the same backend — for example, port 9091 PLAINTEXT for internal clients and port 9095 SASL_SSL for external partners. APIs referencing the cluster can select the appropriate connection without duplicating the cluster entity.

<figure><img src=".gitbook/assets/kafka-cluster-add-dialog.png" alt="Create a new cluster dialog with empty fields for cluster name, description, and bootstrap servers"><figcaption></figcaption></figure>

<figure><img src=".gitbook/assets/kafka-cluster-basic-info.png" alt="Create a new cluster dialog with cluster name eu-prod, description Production Kafka cluster for EU region, and bootstrap servers field visible"><figcaption></figcaption></figure>

<figure><img src=".gitbook/assets/kafka-cluster-add-dialog.png" alt="Create a new cluster dialog with empty fields for cluster name, description, and bootstrap servers"><figcaption></figcaption></figure>

<figure><img src=".gitbook/assets/kafka-cluster-basic-info.png" alt="Create a new cluster dialog with cluster name eu-prod, description Production Kafka cluster for EU region, and bootstrap servers field visible"><figcaption></figcaption></figure>

<figure><img src=".gitbook/assets/kafka-cluster-add-dialog.png" alt="Create a new cluster dialog with empty fields for cluster name, description, and bootstrap servers"><figcaption></figcaption></figure>

<figure><img src=".gitbook/assets/kafka-cluster-basic-info.png" alt="Create a new cluster dialog with cluster name eu-prod, description Production Kafka cluster for EU region, and bootstrap servers field visible"><figcaption></figcaption></figure>

<figure><img src=".gitbook/assets/kafka-cluster-add-dialog.png" alt="Create a new cluster dialog with empty fields for cluster name, description, and bootstrap servers"><figcaption></figcaption></figure>

<figure><img src=".gitbook/assets/kafka-cluster-basic-info.png" alt="Create a new cluster dialog with cluster name eu-prod, description Production Kafka cluster for EU region, and bootstrap servers field visible"><figcaption></figcaption></figure>

<figure><img src=".gitbook/assets/kafka-cluster-add-dialog.png" alt="Create a new cluster dialog with empty fields for cluster name, description, and bootstrap servers"><figcaption></figcaption></figure>

<figure><img src=".gitbook/assets/kafka-cluster-basic-info.png" alt="Create a new cluster dialog with cluster name eu-prod, description Production Kafka cluster for EU region, and bootstrap servers field visible"><figcaption></figcaption></figure>
