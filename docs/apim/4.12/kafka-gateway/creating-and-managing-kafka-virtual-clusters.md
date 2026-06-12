# Creating and Managing Virtual Cluster Entities

## Creating a Kafka Cluster

1. Navigate to **Kafka → Clusters** and click **Add Kafka Cluster**.
2. Enter the cluster name, optional crossId (auto-generated from name if left empty), and optional description.
3. Click **Save** to create the cluster in UNDEPLOYED state with no connections.
4. Open the cluster and navigate to the **Configuration** tab.
5. Add one or more connections using the following fields:

   | Field | Description | Example |
   |:------|:------------|:--------|
   | **Connection Name** | Unique name for this connection within the cluster | `eu-prod-internal` |
   | **Cross ID** | Portable identifier for cross-environment references (auto-generated from name if not provided) | `eu-prod-internal` |
   | **Bootstrap Servers** | Comma-separated list of broker addresses | `host1:9092,host2:9092` |
   | **Security Protocol** | Protocol for broker communication: PLAINTEXT, SSL, SASL_PLAINTEXT, or SASL_SSL | `SASL_SSL` |
   | **SASL Mechanism** (if SASL protocol selected) | Authentication mechanism: PLAIN, SCRAM-SHA-256, SCRAM-SHA-512, or OAUTHBEARER | `SCRAM-SHA-256` |
   | **SASL Credentials** (if SASL protocol selected) | Username and password for SASL authentication | — |
   | **SSL Truststore** (if SSL protocol selected) | Truststore configuration (JKS path or inline PEM) | — |
   | **SSL Keystore** (if SSL protocol selected) | Keystore configuration (JKS path or inline PEM) | — |

   Connection names and crossIds must be unique within the cluster. A single cluster can contain multiple connections to model different listeners on the same backend (e.g., port 9091 PLAINTEXT for internal, port 9095 SASL_SSL for partners).

6. Navigate to the **General** tab and click **Deploy** in the danger zone to activate the cluster on the gateway. The lifecycle state changes to DEPLOYED, the version increments to 1, and the deployedAt timestamp is set. Updating a deployed cluster sets the state to PENDING — redeploy to propagate changes.
7. (Optional) Navigate to the **User Permissions** tab to grant USER role on this cluster to specific subjects. User permissions scope visibility in the Kafka Console UI.
