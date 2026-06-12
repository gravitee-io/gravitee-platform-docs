# Creating Kafka APIs with Cluster and Virtual Cluster References

## Creating a Kafka API with Cluster References

1. Navigate to **Console → APIs → Add API → Create API**.
2. Choose the **Native Kafka** protocol.
3. Complete steps 1–4 (name, version, entrypoint configuration).
4. At step 5 (**Configure Endpoint**), select one of three endpoint connector types:
   * **Broker** (`native-kafka`): Stores bootstrap servers directly in the API. Use for one-off APIs where the broker configuration will not be reused.
   * **Cluster** (`native-kafka-cluster`): References a Kafka Cluster entity by `clusterCrossId` and `connectionCrossId`. Use when multiple APIs share the same backend configuration. Changes to the cluster propagate to all referencing APIs.
   * **Virtual Cluster** (`native-kafka-virtual-cluster`): References a Kafka Virtual Cluster entity by `virtualClusterCrossId`. Use to fan out the API across multiple backend clusters.

The Cluster and Virtual Cluster endpoint forms render dropdowns filtered by entity type (`clusterType: "KAFKA_CLUSTER"` or `clusterType: "KAFKA_VIRTUAL_CLUSTER"`).

For HOST routing mode (the default), configure the **Default Kafka Domain** at **Console → Organization → Entrypoints & Sharding Tags**. The gateway maps each API's host prefix to `<prefix>.<defaultDomain>:9092`. mTLS plans require HOST mode because the SNI handshake is required for client certificate validation.

## SSL Configuration Schema

Test expectations for SSL configuration objects now include `openSsl` and `alpn` fields in addition to `trustAll`, `hostnameVerifier`, `trustStore`, and `keyStore`. This reflects the complete SSL configuration schema used in V2 to V4 API migration.
