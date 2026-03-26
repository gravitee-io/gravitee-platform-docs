---
description: An overview about avro to protobuf.
---

# Avro to Protobuf

## Phases <a href="#user-content-phases" id="user-content-phases"></a>

| onRequest | onResponse | onMessageRequest | onMessageResponse |
| --------- | ---------- | ---------------- | ----------------- |
| X         | X          | X                | X                 |

## Description <a href="#user-content-description" id="user-content-description"></a>

You can use the `avro-protobuf` policy to apply a transformation (or mapping) on the request and/or response and/or message content.

This policy is using the [Avro](https://avro.apache.org/docs/1.11.1/) library.

To serialize data in Avro, you need a [schema](https://avro.apache.org/docs/1.11.1/#schemas). There are two ways to provide a schema:

* inlined in the policy configuration.
* with a Schema Registry.

To serialize data in Protobuf, you need a schema. There are two ways to provide a schema:

* inlined in the policy configuration.
* with a Schema Registry.

## Inline Schema <a href="#user-content-inline-schema" id="user-content-inline-schema"></a>

You can provide the Schema to use directly in the configuration of the policy:

```
{
    "name": "avro-2-protobuf",
    "policy": "avro-protobuf",
    "configuration": {
        "conversion": "avro-to-protobuf",
        "avro": {
            "inlineConfig": {
                "schemaDefinition": "{\"namespace\": \"io.confluent.examples.clients.basicavro\", \"type\": \"record\", \"name\": \"Payment\", \"fields\": [{\"name\": \"id\", \"type\": \"string\"}, {\"name\": \"amount\", \"type\": \"double\"}]}\n",
                "serializationFormat": "confluent"
            }
        },
        "protobuf": {
            "inlineConfig": {
                "schemaDefinition": "syntax = \"proto2\"; package test; message Payment {required string id = 1; required double amount = 2; }",
                "serializationFormat": "confluent"
            }
        }
    }
}
```

### Schema Registry <a href="#user-content-schema-registry" id="user-content-schema-registry"></a>

To use a schema registry to fetch a schema, you will need to declare a Gravitee resource in your API in addition to this policy.

Currently we only provide a resource to interact with Confluent Schema Registry. You can find the plugin [here](https://download.gravitee.io/#graviteeio-ee/apim/plugins/resources/gravitee-resource-schema-registry-confluent/).

```
{
    "name": "avro-2-protobuf",
    "policy": "avro-protobuf",
    "configuration": {
        "conversion": "avro-to-protobuf",
        "avro": {
            "schemaRegistryConfig": {
                "resourceName": "confluent-schema-registry"
            }
        },
        "protobuf": {
            "schemaRegistryConfig": {
                "resourceName": "confluent-schema-registry",
                "schemaIdConfig": {
                    "schemaIdLocation": "inline",
                    "schemaId": 1
                }
            }
        }
    }
}
```

Currently, we only support [Confluent serialization format](https://docs.confluent.io/platform/current/schema-registry/serdes-develop/index.html#wire-format). The policy will extract the schema id from the binary and will use it to fetch the Schema in the registry.

| Warning | The use of Schema Registry is only available to transform message on the `onMessageResponse` phase. |
| ------- | --------------------------------------------------------------------------------------------------- |

### Serialization format <a href="#user-content-serialization-format" id="user-content-serialization-format"></a>

The policy is supporting the serialization formats:

* `simple`: the binary contains only the serialized Protobuf/Avro.
* `confluent`: the binary has been generated using [Confluent serialization format](https://docs.confluent.io/platform/current/schema-registry/serdes-develop/index.html#wire-format).

## Errors <a href="#user-content-errors" id="user-content-errors"></a>

| Phase | Code  | Error template key                | Description                                                                                                                                          |
| ----- | ----- | --------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| \*    | `500` | INVALID\_PROTOBUF\_TRANSFORMATION | When the transform fail to be applied to the payload.                                                                                                |
| \*    | `500` | UNSUPPORTED\_CONFIGURATION\_KEY   | When the policy configuration is not supported. For example, when the policy needs a schema registry but also use the `simple` serialization format. |
