# Kafka Topic Mapping

## Description <a href="#user-content-description" id="user-content-description"></a>

The Kafka Topic Mapping policy lets you map one Kafka topic to another topic so that the Kafka client can use a topic name that is different from the one used in the Kafka broker.

## Configuration <a href="#user-content-configuration" id="user-content-configuration"></a>

You can configure the policy with the following options:

<table><thead><tr><th width="183">Property</th><th>Required</th><th>Description</th><th>Type</th><th>Default</th></tr></thead><tbody><tr><td><code>mappings</code></td><td>No</td><td>A list of mappings between the client topic and the broker topic.</td><td>Array</td><td></td></tr><tr><td><code>mappings.client</code></td><td>No</td><td>The name provided on the client side that will be mapped in something else.</td><td>String</td><td></td></tr><tr><td><code>mappings.broker</code></td><td>No</td><td>The name that will be sent on the broker side. Supports EL expressions.</td><td>String</td><td></td></tr></tbody></table>

{% hint style="info" %}
## Policy order <a href="#user-content-supported-kafka-apikeys" id="user-content-supported-kafka-apikeys"></a>

When using the Kafka Topic Mapping policy together with the Kafka ACL policy, it is important to place the Kafka ACL policy **before** the Kafka Topic Mapping policy, as shown below.
{% endhint %}

<figure><img src="../../.gitbook/assets/policy order.png" alt=""><figcaption><p>Screenshot of the Kafka ACL policy placed before the Kafka Topic Mapping policy</p></figcaption></figure>

## Examples <a href="#user-content-supported-kafka-apikeys" id="user-content-supported-kafka-apikeys"></a>

The following examples demonstrate how to expose a broker-side (internal) topic name with a consumer-friendly client-side (external) topic name.

### Example 1: I want to map an internal topic name to something else (externally)

If you have a broker-side topic called `abcdef.topic.name.internal-only.some-id`, and you want to expose that as a consumer-friendly name, then configure the Kafka Topic Mapping policy as follows:

* Client-side name: `myFriendlyTopicName`
* Broker-side name: `abcdef.topic.name.internal-only.some-id`

<div align="center" data-full-width="false"><figure><img src="../../.gitbook/assets/image (158).png" alt="" width="375"><figcaption><p>UI configuration of the Kafka Topic Mapping policy</p></figcaption></figure></div>

Kafka clients will now be able to specify the mapped topic name (`myFriendlyTopicName`) in their connection configuration.  For example: `kafka-console-consumer.sh --bootstrap-server foo.kafka.local:9092 --consumer.config config/client.properties --topic myFriendlyTopicName`

Below is a sample policy configuration:

{% code fullWidth="false" %}
```json
{
  "api": {
    ...
  },
  "plans: [
    {
      "flows": [
        {
          ...
          "interact": [
            {
              "name": "Kafka Topic Mapping",
              "enabled": true,
              "policy": "kafka-topic-mapping",
              "configuration": {
                "mappings": [
                  {
                    "client": "myFriendlyTopicName",
                    "broker": "abcdef.topic.name.internal-only.some-id"
                   }
                ]
              }
            }
          ]
        }
      ]
    }
  ]
}
```
{% endcode %}

### Example 2: I want to simplify multiple internal-only topic names as a single external-friendly topic name (with support from an OAuth2 provider)

The broker-side (internal) topic name includes a user-specific organization ID that has been added to the topic name, e.g., `internal.organization-updates.12345`.  In this example, the organization ID ("`12345`") will be included in the OAuth2 `access_token` supplied by the identity server.   &#x20;

In the Kafka Topic Mapping policy, the broker-side topic name will be  `internal.organization-updates.{orgId}`.  The `{orgId}` is dynamically replaced at runtime by extracting a custom claim value (e.g., `rf_org`) from the user's OAuth2 `access_token` via Gravitee's Expression Language.

We can now keep the client-side (external) topic name simple & generic:  `organization-updates`.

<figure><img src="../../.gitbook/assets/image (153).png" alt=""><figcaption><p>UI configuration of the Kafka Topic Mapping policy</p></figcaption></figure>

Below is a sample policy configuration:

{% code fullWidth="false" %}
```json
{
  "api": {
    ...
  },
  "plans: [
    {
      "flows": [
        {
          ...
          "interact": [
            {
              "name": "Kafka Topic Mapping",
              "enabled": true,
              "policy": "kafka-topic-mapping",
              "configuration": {
                "mappings": [
                  {
                    "client": "organization-updates",
                    "broker": "integrator.organization-updates.{#jsonPath(#context.attributes['oauth.payload'], '$.rf_org')}"
                   }
                ]
              }
            }
          ]
        }
      ]
    }
  ]
}
```
{% endcode %}

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
