= Gravitee Kafka Policy ACL

== Phases

This policy is executed during the onRequest phase of the Kafka reactor and also adds actionOnResponse if necessary.


== Kafka ApiKeys

Legend:

- ✅ Dev Done for Request
- ❇️ Dev Done for Response
- 🧪 Test Done
- 🚫 Not relevant for ACL policy. (Request is authorized)
- 🤨 Questionable / Not implemented yet / Somthing to check
- ⛔ Block the Kafka Request

ApiKeys:

- ✅🧪 ApiKeys.PRODUCE
- ✅🧪 ApiKeys.FETCH
- ✅🧪 ApiKeys.LIST_OFFSETS
- ✅❇️🧪 ApiKeys.METADATA -> Depending on version ext.. calculate `ClusterAuthorizedOperations`, and `TopicAuthorizedOperations` for response
- ✅🧪 ApiKeys.LEADER_AND_ISR
- ✅🧪 ApiKeys.STOP_REPLICA
- ✅🧪 ApiKeys.UPDATE_METADATA
- ✅🧪 ApiKeys.CONTROLLED_SHUTDOWN
- ✅🧪 ApiKeys.OFFSET_COMMIT
- ✅🧪 ApiKeys.OFFSET_FETCH
- ✅🧪 ApiKeys.FIND_COORDINATOR
- ✅🧪 ApiKeys.JOIN_GROUP
- ✅🧪 ApiKeys.HEARTBEAT
- ✅🧪 ApiKeys.LEAVE_GROUP
- ✅🧪 ApiKeys.SYNC_GROUP
- ✅❇️🧪 ApiKeys.DESCRIBE_GROUPS -> Calculate `ClusterAuthorizedOperations` for response
- ✅❇️🧪 ApiKeys.LIST_GROUPS
- 🚫 ApiKeys.SASL_HANDSHAKE
- 🚫 ApiKeys.API_VERSIONS
- ✅❇️🧪 ApiKeys.CREATE_TOPICS
- ✅🧪 ApiKeys.DELETE_TOPICS
- ✅🧪 ApiKeys.DELETE_RECORDS
- ✅🧪 ApiKeys.INIT_PRODUCER_ID
- ✅🧪 ApiKeys.OFFSET_FOR_LEADER_EPOCH
- ✅🧪 ApiKeys.ADD_PARTITIONS_TO_TXN
- ✅🧪 ApiKeys.ADD_OFFSETS_TO_TXN
- ✅🧪 ApiKeys.END_TXN
- ✅🧪 ApiKeys.WRITE_TXN_MARKERS
- ✅🧪 ApiKeys.TXN_OFFSET_COMMIT
- ✅🧪 ApiKeys.DESCRIBE_ACLS
- ✅🧪 ApiKeys.CREATE_ACLS
- ✅🧪 ApiKeys.DELETE_ACLS
- ✅🧪 ApiKeys.ALTER_CONFIGS
- ✅🧪 ApiKeys.DESCRIBE_CONFIGS
- ✅🧪 ApiKeys.ALTER_REPLICA_LOG_DIRS
- ✅🧪 ApiKeys.DESCRIBE_LOG_DIRS
- 🚫 ApiKeys.SASL_AUTHENTICATE
- ✅🧪 ApiKeys.CREATE_PARTITIONS
- ✅⛔️🧪 ApiKeys.CREATE_DELEGATION_TOKEN
- ✅⛔🧪 ApiKeys.RENEW_DELEGATION_TOKEN
- ✅⛔🧪 ApiKeys.EXPIRE_DELEGATION_TOKEN
- ✅⛔🧪 ApiKeys.DESCRIBE_DELEGATION_TOKEN
- ✅🧪 ApiKeys.DELETE_GROUPS
- ✅🧪 ApiKeys.ELECT_LEADERS
- ✅🧪 ApiKeys.INCREMENTAL_ALTER_CONFIGS
- ✅🧪 ApiKeys.ALTER_PARTITION_REASSIGNMENTS
- ✅🧪 ApiKeys.LIST_PARTITION_REASSIGNMENTS
- ✅🧪 ApiKeys.OFFSET_DELETE
- ✅🧪 ApiKeys.DESCRIBE_CLIENT_QUOTAS
- ✅🧪 ApiKeys.ALTER_CLIENT_QUOTAS
- ✅🧪 ApiKeys.DESCRIBE_USER_SCRAM_CREDENTIALS
- ✅🧪 ApiKeys.ALTER_USER_SCRAM_CREDENTIALS
- ✅🧪 ApiKeys.ALTER_PARTITION
- 🚫 ApiKeys.UPDATE_FEATURES
- ✅🧪 ApiKeys.ENVELOPE
- ❇️🧪 ApiKeys.DESCRIBE_CLUSTER -> Calculate `ClusterAuthorizedOperations` for response
- ✅🧪 ApiKeys.DESCRIBE_PRODUCERS
- 🚫 ApiKeys.UNREGISTER_BROKER
- ✅❇️🧪 ApiKeys.DESCRIBE_TRANSACTIONS -> Filter topics inside transactionStates of the response
- ❇️🧪 ApiKeys.LIST_TRANSACTIONS -> Filter transactions of the response
- ✅🧪 ApiKeys.ALLOCATE_PRODUCER_IDS
- 🚫 ApiKeys.DESCRIBE_QUORUM
- ✅🧪 ApiKeys.CONSUMER_GROUP_HEARTBEAT
- ✅❇️🧪 ApiKeys.CONSUMER_GROUP_DESCRIBE -> Calculate `ClusterAuthorizedOperations` for response
- 🤨 ApiKeys.DESCRIBE_TOPIC_PARTITIONS -> To add with 3.8.0 of Kafka. Add request and response - https://github.com/apache/kafka/blob/76a1af984b39d9890fe26954aff36bb1a321af77/core/src/main/java/kafka/server/handlers/DescribeTopicPartitionsRequestHandler.java#L96
- 🚫 ApiKeys.GET_TELEMETRY_SUBSCRIPTIONS
- 🚫 ApiKeys.PUSH_TELEMETRY
- ✅🧪 ApiKeys.LIST_CLIENT_METRICS_RESOURCES
- 🚫 ApiKeys.ADD_RAFT_VOTER
- 🚫 ApiKeys.REMOVE_RAFT_VOTER
- 🤨 ApiKeys.SHARE_GROUP_HEARTBEAT -> To add with 4.0.0 of Kafka
- 🤨 ApiKeys.SHARE_GROUP_DESCRIBE -> To add with 4.0.0 of Kafka
- 🤨 ApiKeys.SHARE_FETCH -> To add with 4.0.0 of Kafka
- 🤨 ApiKeys.SHARE_ACKNOWLEDGE -> To add with 4.0.0 of Kafka
- 🤨 ApiKeys.INITIALIZE_SHARE_GROUP_STATE -> To add with 4.0.0 of Kafka
- 🤨 ApiKeys.READ_SHARE_GROUP_STATE -> To add with 4.0.0 of Kafka
- 🤨 ApiKeys.WRITE_SHARE_GROUP_STATE -> To add with 4.0.0 of Kafka
- 🤨 ApiKeys.DELETE_SHARE_GROUP_STATE -> To add with 4.0.0 of Kafka
- 🤨 ApiKeys.READ_SHARE_GROUP_STATE_SUMMARY -> To add with 4.0.0 of Kafka



