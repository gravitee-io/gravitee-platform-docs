= Gravitee Kafka Policy Topic Mapping

== Description

This policy allows you to map a topic to another topic. People using the Kafka Client can use a topic name that is different from the one used in the Kafka Broker.

== Compatibility with APIM

|===
| Plugin version   | APIM version
| 1.1.x to latest  | 4.6.2 to latest
| 1.0.x            | 4.6.x to 4.6.2
|===

== Configuration

You can configure the policy with the following options:

[cols="5*", options=header]
|===
^| Property
^| Required
^| Description
^| Type
^| Default

| mappings
| No
| A list of mappings between the client topic and the broker topic.
| Array
|

| mappings.client
| No
| The name provided on the client side that will be mapped in something else.
| String
|

| mappings.broker
| No
| The name that will be sent on the broker side. Supports EL expressions.
| String
|
|===

== Supported Kafka ApiKeys

Legend:

- ✅ Supported
- 🚫 Not relevant (no topic involved)

This policy supports the following https://kafka.apache.org/0101/protocol.html#protocol_api_keys[Kafka ApiKeys]:

- ✅ PRODUCE
- ✅ FETCH
- ✅ LIST_OFFSETS
- ✅ METADATA
- ✅ LEADER_AND_ISR
- ✅ STOP_REPLICA
- ✅ UPDATE_METADATA
- ✅ CONTROLLED_SHUTDOWN
- ✅ OFFSET_COMMIT
- ✅ OFFSET_FETCH
- 🚫 FIND_COORDINATOR
- 🚫 JOIN_GROUP
- 🚫 HEARTBEAT
- 🚫 LEAVE_GROUP
- 🚫 SYNC_GROUP
- 🚫 DESCRIBE_GROUPS
- 🚫 LIST_GROUPS
- 🚫 SASL_HANDSHAKE
- 🚫 API_VERSIONS
- ✅ CREATE_TOPICS
- ✅ DELETE_TOPICS
- ✅ DELETE_RECORDS
- 🚫 INIT_PRODUCER_ID
- ✅ OFFSET_FOR_LEADER_EPOCH
- ✅ ADD_PARTITIONS_TO_TXN
- 🚫 ADD_OFFSETS_TO_TXN
- 🚫 END_TXN
- ✅ WRITE_TXN_MARKERS
- ✅ TXN_OFFSET_COMMIT
- ✅ DESCRIBE_ACLS
- ✅ CREATE_ACLS
- ✅ DELETE_ACLS
- ✅ DESCRIBE_CONFIGS
- ✅ ALTER_CONFIGS
- ✅ ALTER_REPLICA_LOG_DIRS
- ✅ DESCRIBE_LOG_DIRS
- 🚫 SASL_AUTHENTICATE
- ✅ CREATE_PARTITIONS
- 🚫 CREATE_DELEGATION_TOKEN
- 🚫 RENEW_DELEGATION_TOKEN
- 🚫 EXPIRE_DELEGATION_TOKEN
- 🚫 DESCRIBE_DELEGATION_TOKEN
- 🚫 DELETE_GROUPS
- ✅ ELECT_LEADERS
- ✅ INCREMENTAL_ALTER_CONFIGS
- ✅ ALTER_PARTITION_REASSIGNMENTS
- ✅ LIST_PARTITION_REASSIGNMENTS
- ✅ OFFSET_DELETE
- 🚫 DESCRIBE_CLIENT_QUOTAS
- 🚫 ALTER_CLIENT_QUOTAS
- 🚫 DESCRIBE_USER_SCRAM_CREDENTIALS
- 🚫 ALTER_USER_SCRAM_CREDENTIALS
- ✅ VOTE
- ✅ BEGIN_QUORUM_EPOCH
- ✅ END_QUORUM_EPOCH
- ✅ DESCRIBE_QUORUM
- ✅ ALTER_PARTITION
- 🚫 UPDATE_FEATURES
- 🚫 ENVELOPE
- ✅ FETCH_SNAPSHOT
- 🚫 DESCRIBE_CLUSTER
- ✅ DESCRIBE_PRODUCERS
- 🚫 BROKER_REGISTRATION
- 🚫 BROKER_HEARTBEAT
- 🚫 UNREGISTER_BROKER
- ✅ DESCRIBE_TRANSACTIONS
- 🚫 LIST_TRANSACTIONS
- 🚫 ALLOCATE_PRODUCER_IDS
- ✅ CONSUMER_GROUP_HEARTBEAT
- ✅ CONSUMER_GROUP_DESCRIBE
- 🚫 CONTROLLER_REGISTRATION
- 🚫 GET_TELEMETRY_SUBSCRIPTIONS
- 🚫 PUSH_TELEMETRY
- ✅ ASSIGN_REPLICAS_TO_DIRS
- 🚫 LIST_CLIENT_METRICS_RESOURCES
