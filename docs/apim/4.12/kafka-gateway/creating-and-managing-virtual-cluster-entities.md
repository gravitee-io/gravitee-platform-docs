# Creating and Managing Virtual Cluster Entities

## Creating a Virtual Cluster

A Virtual Cluster requires at least two Kafka Cluster entities to be configured in the environment before creation.

1. Navigate to Console → Kafka Virtual Clusters → **Add**.
2. Enter a **Name** (e.g., `global-mesh`).
3. (Optional) Enter a **Cross ID** for external identification (config-as-code or GKO integration).
4. (Optional) Enter a **Description**.
5. Click **Save**. The Virtual Cluster is created with no backends.
6. Open the Virtual Cluster and navigate to the **Configuration** tab.
7. Click **Add Backend**.
8. Select a **Kafka Cluster** from the dropdown (filtered to show only `KAFKA_CLUSTER` type entities).
9. Select a **Connection** from the second dropdown (populated with connections from the selected Kafka Cluster).
10. Click **Save** to add the backend.
11. Repeat steps 7–10 to add additional backends. A minimum of two backends is required for multi-cluster routing.

### Configuration Reference

| Field | Description | Example |
|:------|:------------|:--------|
| **Name** | Human-readable Virtual Cluster name. | `global-mesh` |
| **Cross ID** | External identifier for config-as-code or GKO integration. | `vcluster-global-001` |
| **Description** | Optional Virtual Cluster description. | `Virtual cluster spanning EU and US regions` |
| **Kafka Cluster** | Reference to a Kafka Cluster entity. | `eu-prod` |
| **Connection** | Reference to a connection within the selected Kafka Cluster. | `internal-plaintext` |
