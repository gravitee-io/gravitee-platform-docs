# Creating and Managing Kafka Virtual Clusters

## Creating a Kafka Virtual Cluster

1. Navigate to **Console → Kafka Virtual Clusters → Add**.
2. Enter a **Name** for the virtual cluster (e.g., `multi-region-mesh`).
3. (Optional) Enter a **Cross ID** — a portable identifier for cross-environment references or config-as-code. If not provided, the gateway auto-generates it from the virtual cluster name.
4. (Optional) Enter a **Description**.
5. Click **Save**. The virtual cluster is created with no backends.
6. Open the virtual cluster and navigate to the **Configuration** tab.
7. Click **Add Backend**.
8. Select a **Kafka Cluster** from the dropdown. The dropdown is filtered to show only `KAFKA_CLUSTER` type entities.
9. Select a **Connection** from the second dropdown. The dropdown is populated with connections from the selected cluster.
10. Click **Save** to add the backend.
11. Repeat steps 7–10 to add additional backends. A minimum of two backends is required to exercise the MESH multiplex functionality.

**Backend Configuration Reference:**

| Field | Description |
|:------|:------------|
| Cluster Cross ID | The cross ID of the referenced Kafka Cluster entity |
| Connection Cross ID | The cross ID of the connection within that cluster |

### Deploying and Undeploying Virtual Clusters

Deploying and undeploying Kafka Virtual Clusters follows the same procedure as Kafka Clusters. See [Deploying a Cluster](#deploying-a-cluster) and [Undeploying a Cluster](#undeploying-a-cluster) for step-by-step instructions.

Virtual cluster lifecycle states (`UNDEPLOYED`, `DEPLOYED`, `PENDING`) and version management work identically to Kafka Clusters. When you update the configuration of a deployed virtual cluster (e.g., add a backend), the lifecycle state changes to `PENDING`. Click **Deploy** again to apply the changes to the gateway. The version number increments and the state returns to `DEPLOYED`.
