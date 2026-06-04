# Kafka Virtual Cluster Restrictions and Limitations

## Restrictions

- **SASL Replay mechanism limitation**: SASL Replay is limited to the PLAIN mechanism. AWS_MSK_IAM, SCRAM, and GSSAPI mechanisms are not captured for cross-cluster fan-outs.
- **Producer ID session persistence**: Producer ID sessions are lost on gateway pod failover without a distributed `CacheManager` (Hazelcast or Redis), causing `PRODUCER_FENCED` errors for idempotent producers. Applications using idempotent producers against virtual clusters must handle `PRODUCER_FENCED` errors by recreating the producer instance (not retrying with the same instance).
- **Virtual Cluster metadata merge**: Virtual Cluster `DescribeCluster` responses are not merged across backends; AdminClient sees only the connected backend's brokers.
- **KIP-848 / KIP-932 group API support**: Virtual Clusters strip `CONSUMER_GROUP_DESCRIBE`, `CONSUMER_GROUP_HEARTBEAT`, and `SHARE_*` APIs from `ApiVersions` responses because the multiplex layer cannot fan out these requests (KIP-848 / KIP-932 group APIs).
- **Deployed cluster deletion**: Deployed clusters (`DEPLOYED` or `PENDING` state) are automatically undeployed before deletion. If undeploy fails, deletion is aborted.
- **Endpoint Type step visibility**: The "Endpoint Type" step (Step 3.1) is shown for `NATIVE` APIs but not for `MESSAGE`, `PROXY`, `LLM_PROXY`, or `A2A_PROXY` APIs.
- **Cluster type validation**: Cluster type validation is enforced server-side. The UI does not prevent users from creating clusters with invalid `type` values.
- **mTLS plan routing constraint**: mTLS plans force HOST routing mode (SNI handshake is required for client-cert validation).
- **Cluster type rename**: Cluster type `KAFKA_CLUSTER_STANDALONE` was renamed from `KAFKA_CLUSTER_CONNECTION` in version 4.12.0. Existing clusters are migrated automatically.
