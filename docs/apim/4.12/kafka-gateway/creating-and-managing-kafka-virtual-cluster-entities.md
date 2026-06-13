# Creating and Managing Kafka Virtual Cluster Entities

## Creating a Kafka Virtual Cluster

A Kafka Virtual Cluster aggregates multiple Kafka Cluster entities into a single virtual cluster. Each backend reference selects one Cluster and one of its Connections.

{% hint style="info" %}
A Virtual Cluster requires at least 2 Kafka Cluster entities to provide value. With a single backend, use a Cluster endpoint directly.
{% endhint %}

1. Navigate to **Console → Kafka → Standalone → Virtual Clusters**.
2. Click **Add** to create a new virtual cluster.
3. Enter a **Name** (required).
4. (Optional) Enter a **Cross ID** for external references. If not provided, the Cross ID is auto-generated from the name. Cross ID must be unique within the environment and is immutable after creation.
5. (Optional) Enter a **Description**.
6. Click **Save** to create the virtual cluster.
7. Open the virtual cluster and navigate to the **Configuration** tab.
8. Click **Add Backend** to add a backend cluster reference.
9. Select a **Cluster** from the dropdown (filtered to show only Kafka Cluster entities).
10. Select a **Connection** from the dropdown (shows connections defined in the selected Cluster).
11. Repeat steps 8–10 for each backend cluster you want to include. Minimum 2 backends recommended; practical ceiling is ~5–10 backends.
12. Click **Save** to apply the configuration.

| Field | Description | Example |
|:------|:------------|:--------|
| **Name** | Human-readable virtual cluster name (required) | `global-mesh` |
| **Cross ID** | Portable identifier for cross-environment references (auto-generated from name if not provided; immutable after creation; must be unique within environment) | `global-mesh` |
| **Description** | Optional virtual cluster description | `Virtual cluster spanning US and EU regions` |
| **Cluster** | Reference to a Kafka Cluster entity | `eu-prod` |
| **Connection** | Reference to a connection within the selected Cluster | `sasl-ssl-9095` |

{% hint style="warning" %}
**Validation errors:**
- **Name is required**: Name field cannot be empty.
- **Type is required**: Type field must be specified.
- **Configuration is required**: Configuration field must be specified.
- **Duplicate Cross ID**: `"A cluster with crossId '{crossId}' already exists in this environment."`
- **Immutable Cross ID**: `"CrossId is immutable and cannot be changed after creation."`
- **Duplicate backend references**: `"Backend references must be unique within a virtual cluster. Duplicates found: [list]"`
{% endhint %}

### Lifecycle Operations

Kafka Virtual Clusters support the same lifecycle operations as Kafka Clusters:

- **Deploy**: Deploys the virtual cluster configuration to the gateway. Increments the version number.
- **Undeploy**: Removes the virtual cluster configuration from the gateway.

| Lifecycle State | Description |
|:----------------|:------------|
| **DEPLOYED** | Virtual cluster is active on the gateway |
| **PENDING** | Virtual cluster configuration has been updated but not yet deployed |
| **UNDEPLOYED** | Virtual cluster is not active on the gateway |
