# Configuring Native Kafka APIs with Cluster Endpoints

## Configuring a Native Kafka API

Navigate to **APIs → Add API → Create API** and select the **Native Kafka** protocol. Complete steps 1–4 (name, version, entrypoint configuration). In step 5 (**Configure Endpoint**), select one of three endpoint connector types:

1. **Broker** (`native-kafka`): Enter bootstrap servers directly in the endpoint configuration. Use for one-shot APIs where the broker config is not reused elsewhere.

2. **Cluster** (`native-kafka-cluster`): Select a Kafka Cluster from the dropdown (filtered by `clusterType=KAFKA_CLUSTER`) and select one of its connections. The API references the cluster by crossId — updating the cluster propagates changes to all dependent APIs.

3. **Virtual Cluster** (`native-kafka-virtual-cluster`): Select a Kafka Virtual Cluster from the dropdown (filtered by `clusterType=KAFKA_VIRTUAL_CLUSTER`). The API fans out across all backend clusters referenced by the virtual cluster.

Complete the wizard and deploy the API. The gateway resolves cluster and virtual cluster references at runtime via the cluster registry.

### Cluster Deletion Rules

Clusters in DEPLOYED or PENDING state cannot be deleted. Undeploy the cluster before deletion. The system returns the error `"Cluster must be undeployed before deletion."` if deletion is attempted on a deployed or pending cluster.
