# Creating and Managing Virtual Cluster Entities

## Overview

The Kafka cluster configuration form supports the DELEGATE_TO_BROKER SASL mechanism, which allows the gateway to forward client SASL authentication directly to the backend Kafka broker without intermediate processing. This release also corrects conditional display logic for SASL and SSL configuration sections in the Kafka cluster configuration form.

## Managing Kafka Virtual Clusters

A Kafka Virtual Cluster fans out client requests across multiple backend Kafka clusters, presenting them as a single virtual cluster. Virtual clusters are meaningful only when you have two or more Kafka Cluster entities to span.

1. Navigate to **Console → Kafka → Standalone → Virtual Clusters**.
2. Click **Add**.

    <figure><img src="../.gitbook/assets/kafka-virtual-cluster-add-dialog.png" alt="Add virtual cluster dialog with fields for name, description, and backend cluster selection"><figcaption></figcaption></figure>

3. Enter a **Name**.
4. (Optional) Enter a **Cross ID** (external identifier for GKO or config-as-code).
5. (Optional) Enter a **Description**.
6. Click **Save**.
7. Open the virtual cluster and navigate to the **Configuration** tab.
8. Add backends by selecting a Kafka Cluster from the dropdown (filtered to show only entities with cluster type `KAFKA_CLUSTER`).
9. Select one of that cluster's connections from a second dropdown.
10. Repeat for each backend. A minimum of two backends is required to exercise the MESH multiplex capability.

{% hint style="info" %}
The virtual cluster stores only references (`clusterCrossId` and `connectionCrossId` pairs) — it does not duplicate broker addresses or credentials. Changes to the underlying Kafka Cluster entities propagate to the virtual cluster automatically.
{% endhint %}

### Kafka Cluster Entity

A Kafka Cluster is a reusable connection profile to a real Kafka backend. Each cluster owns a name and one or more connections, where each connection specifies bootstrap servers and security settings (PLAINTEXT, SSL, SASL_PLAINTEXT, or SASL_SSL). Multiple APIs can reference the same cluster — changes to the cluster propagate to all referencing APIs.

### Conditional Display Logic

SASL configuration fields appear only when the security protocol is SASL_PLAINTEXT or SASL_SSL. SSL configuration fields appear only when the security protocol is SASL_SSL or SSL. The form uses relative JSON path references to evaluate these conditions. This fix affects only form rendering logic in the UI and does not require data migration for existing Kafka cluster configurations.

<figure><img src="../.gitbook/assets/kafka-virtual-cluster-add-dialog.png" alt="Add virtual cluster dialog with fields for name, description, and backend cluster selection"><figcaption></figcaption></figure>

<figure><img src="../.gitbook/assets/kafka-virtual-cluster-add-dialog.png" alt="Add virtual cluster dialog with fields for name, description, and backend cluster selection"><figcaption></figcaption></figure>

<figure><img src="../.gitbook/assets/kafka-virtual-cluster-add-dialog.png" alt="Add virtual cluster dialog with fields for name, description, and backend cluster selection"><figcaption></figcaption></figure>

<figure><img src="../.gitbook/assets/kafka-virtual-cluster-add-dialog.png" alt="Add virtual cluster dialog with fields for name, description, and backend cluster selection"><figcaption></figcaption></figure>
