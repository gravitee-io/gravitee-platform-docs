# Creating and Managing Kafka Virtual Clusters

## Creating a Kafka Virtual Cluster

Navigate to **Kafka → Virtual Clusters** and click **Add Kafka Virtual Cluster**. Enter the cluster name, optional Cross ID (auto-generated from name if left empty), and optional description. Click **Save** to create the virtual cluster in UNDEPLOYED state with no backends.

Open the virtual cluster and navigate to the **Configuration** tab. Add one or more backends using the following fields:

| Field | Description | Example |
|:------|:------------|:--------|
| **Cluster Cross ID** | Cross-environment identifier of the referenced Kafka Cluster (dropdown filtered by `clusterType=KAFKA_CLUSTER`) | `eu-prod` |
| **Connection Cross ID** | Cross-environment identifier of the connection within the referenced cluster (dropdown populated from selected cluster) | `eu-prod-internal` |

Backend references must be unique within the virtual cluster. Duplicate backend references trigger an error: "Backend references must be unique within a virtual cluster. Duplicates found: [...]"

A virtual cluster requires at least two backends to exercise MESH multiplex. The pragmatic upper bound is 5–10 backends — every consumer-group RPC fans out across all backends.

Navigate to the **General** tab and click **Deploy** in the danger zone to activate the virtual cluster on the gateway. The lifecycle state changes to DEPLOYED, the version increments to 1, and the deployedAt timestamp is set. Updating a deployed virtual cluster sets the state to PENDING — redeploy to propagate changes.
