# Creating and Managing Kafka Virtual Cluster Entities

## Creating a Kafka Virtual Cluster

A Kafka Virtual Cluster requires at least two existing Kafka Cluster entities to reference. Create the underlying Kafka Cluster entities before proceeding.

1. Navigate to Console → Kafka Virtual Clusters → **Add**.
2. Enter a **Name** for the virtual cluster (e.g., `global-mesh`).
3. (Optional) Enter a **Cross ID** for external references or configuration-as-code workflows. If omitted, the system auto-generates one from the name.
4. (Optional) Enter a **Description**.
5. Click **Save**. The virtual cluster is created with no backends.
6. Open the virtual cluster and navigate to the **Configuration** tab.
7. Click **Add Backend** to reference a backend Kafka cluster.
8. Select a **Cluster Cross ID** from the dropdown. The dropdown is filtered to show only entities of type KAFKA_CLUSTER.
9. Select a **Connection Cross ID** from the dropdown. The dropdown shows connections defined within the selected Kafka Cluster.
10. Click **Save** to add the backend reference.
11. Repeat steps 7–10 to add additional backends. Each backend must reference a unique combination of Cluster Cross ID and Connection Cross ID.
12. Click **Deploy** to activate the virtual cluster on the gateway. The lifecycle state transitions to DEPLOYED, the version number increments, and the deployment timestamp is set.

### Virtual Cluster Configuration Reference

| Field | Description | Required |
|:------|:------------|:---------|
| **Name** | Human-readable name for the virtual cluster. | Yes |
| **Cross ID** | Portable identifier for cross-environment references. Auto-generated from name if not provided. Immutable after creation. | No |
| **Description** | Free-text description of the virtual cluster. | No |
| **Backends** | List of references to existing Kafka Cluster connections. Each backend is a (Cluster Cross ID, Connection Cross ID) pair. Minimum 2 backends required. | Yes (at least two) |

### Backend Reference Configuration

| Field | Description | Required |
|:------|:------------|:---------|
| **Cluster Cross ID** | Cross ID of the referenced Kafka Cluster entity. | Yes |
| **Connection Cross ID** | Cross ID of the connection within the referenced Kafka Cluster. | Yes |
