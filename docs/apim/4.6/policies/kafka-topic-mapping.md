---
hidden: true
---

# Kafka Topic Mapping

## Description <a href="#user-content-description" id="user-content-description"></a>



This policy allows you to map a topic to another topic. People using the Kafka Client can use a topic name that is different from the one used in the Kafka Broker.

## Configuration <a href="#user-content-configuration" id="user-content-configuration"></a>



You can configure the policy with the following options:

| Property        | Required | Description                                                                 | Type   | Default |
| --------------- | -------- | --------------------------------------------------------------------------- | ------ | ------- |
| mappings        | No       | A list of mappings between the client topic and the broker topic.           | Array  |         |
| mappings.client | No       | The name provided on the client side that will be mapped in something else. | String |         |
| mappings.broker | No       | The name that will be sent on the broker side. Supports EL expressions.     | String |         |

## Supported Kafka ApiKeys <a href="#user-content-supported-kafka-apikeys" id="user-content-supported-kafka-apikeys"></a>

Legend:

* ✅ Supported
* 🚫 Not relevant (no topic involved)

This policy supports the following [Kafka ApiKeys](https://kafka.apache.org/0101/protocol.html#protocol_api_keys):

* ✅ PRODUCE
* ✅ FETCH
* ✅ LIST\_OFFSETS
* ✅ METADATA
* ✅ LEADER\_AND\_ISR
* ✅ STOP\_REPLICA
* ✅ UPDATE\_METADATA
* ✅ CONTROLLED\_SHUTDOWN
* ✅ OFFSET\_COMMIT
* ✅ OFFSET\_FETCH
* 🚫 FIND\_COORDINATOR
* 🚫 JOIN\_GROUP
* 🚫 HEARTBEAT
* 🚫 LEAVE\_GROUP
* 🚫 SYNC\_GROUP
* 🚫 DESCRIBE\_GROUPS
* 🚫 LIST\_GROUPS
* 🚫 SASL\_HANDSHAKE
* 🚫 API\_VERSIONS
* ✅ CREATE\_TOPICS
* ✅ DELETE\_TOPICS
* ✅ DELETE\_RECORDS
* 🚫 INIT\_PRODUCER\_ID
* ✅ OFFSET\_FOR\_LEADER\_EPOCH
* ✅ ADD\_PARTITIONS\_TO\_TXN
* 🚫 ADD\_OFFSETS\_TO\_TXN
* 🚫 END\_TXN
* ✅ WRITE\_TXN\_MARKERS
* ✅ TXN\_OFFSET\_COMMIT
* ✅ DESCRIBE\_ACLS
* ✅ CREATE\_ACLS
* ✅ DELETE\_ACLS
* ✅ DESCRIBE\_CONFIGS
* ✅ ALTER\_CONFIGS
* ✅ ALTER\_REPLICA\_LOG\_DIRS
* ✅ DESCRIBE\_LOG\_DIRS
* 🚫 SASL\_AUTHENTICATE
* ✅ CREATE\_PARTITIONS
* 🚫 CREATE\_DELEGATION\_TOKEN
* 🚫 RENEW\_DELEGATION\_TOKEN
* 🚫 EXPIRE\_DELEGATION\_TOKEN
* 🚫 DESCRIBE\_DELEGATION\_TOKEN
* 🚫 DELETE\_GROUPS
* ✅ ELECT\_LEADERS
* ✅ INCREMENTAL\_ALTER\_CONFIGS
* ✅ ALTER\_PARTITION\_REASSIGNMENTS
* ✅ LIST\_PARTITION\_REASSIGNMENTS
* ✅ OFFSET\_DELETE
* ❏ DESCRIBE\_CLIENT\_QUOTAS
* ❏ ALTER\_CLIENT\_QUOTAS
* 🚫 DESCRIBE\_USER\_SCRAM\_CREDENTIALS
* 🚫 ALTER\_USER\_SCRAM\_CREDENTIALS
* ✅ VOTE
* ✅ BEGIN\_QUORUM\_EPOCH
* ✅ END\_QUORUM\_EPOCH
* ✅ DESCRIBE\_QUORUM
* ✅ ALTER\_PARTITION
* 🚫 UPDATE\_FEATURES
* 🚫 ENVELOPE
* ✅ FETCH\_SNAPSHOT
* 🚫 DESCRIBE\_CLUSTER
* ✅ DESCRIBE\_PRODUCERS
* 🚫 BROKER\_REGISTRATION
* 🚫 BROKER\_HEARTBEAT
* 🚫 UNREGISTER\_BROKER
* ✅ DESCRIBE\_TRANSACTIONS
* 🚫 LIST\_TRANSACTIONS
* 🚫 ALLOCATE\_PRODUCER\_IDS
* ✅ CONSUMER\_GROUP\_HEARTBEAT
* ✅ CONSUMER\_GROUP\_DESCRIBE
* 🚫 CONTROLLER\_REGISTRATION
* 🚫 GET\_TELEMETRY\_SUBSCRIPTIONS
* 🚫 PUSH\_TELEMETRY
* ✅ ASSIGN\_REPLICAS\_TO\_DIRS
* 🚫 LIST\_CLIENT\_METRICS\_RESOURCES
