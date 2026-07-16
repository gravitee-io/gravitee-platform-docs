---
description: Configuration guide for avro to json.
metaLinks:
  alternates:
    - avro-to-json.md
---

# Avro to JSON

## Phases <a href="#user-content-phases" id="user-content-phases"></a>

| onRequest | onResponse | onMessageRequest | onMessageResponse |
| --------- | ---------- | ---------------- | ----------------- |
| X         | X          | X                | X                 |

The policy is also compatible with native Kafka APIs, where it runs on the publish and subscribe phases.

## Description <a href="#user-content-description" id="user-content-description"></a>

You can use the `avro-json` policy to apply a transformation (or mapping) on the request, response, or message content. The same policy transforms content in both directions:

* `avro-to-json` deserializes Avro binary content into JSON.
* `json-to-avro` serializes JSON content into Avro binary.

Set the direction with the `conversion` configuration option.

The policy is compatible with Proxy APIs, Message APIs, and native Kafka APIs.

This policy uses the [Avro](https://avro.apache.org/docs/1.11.1/) library.

To serialize data in Avro, you need a [schema](https://avro.apache.org/docs/1.11.1/#schemas). There are two ways to provide a schema:

* inlined in the policy configuration.
* with a Schema Registry.

### Inline Schema <a href="#user-content-inline-schema" id="user-content-inline-schema"></a>

You can provide the schema to use directly in the configuration of the policy.

The following example converts Avro to JSON with an inline schema:

```json
{
    "name": "avro-2-json",
    "policy": "avro-json",
    "configuration": {
        "conversion": "avro-to-json",
        "schemaLocation": "inline",
        "schemaDefinition": "{\"namespace\": \"io.confluent.examples.clients.basicavro\", \"type\": \"record\", \"name\": \"Payment\", \"fields\": [{\"name\": \"id\", \"type\": \"string\"}, {\"name\": \"amount\", \"type\": \"double\"}]}"
    }
}
```

The following example converts JSON to Avro with an inline schema:

```json
{
    "name": "json-2-avro",
    "policy": "avro-json",
    "configuration": {
        "conversion": "json-to-avro",
        "schemaLocation": "inline",
        "serializationFormat": "simple",
        "valueMapping": {
            "schemaDefinition": "{\"namespace\": \"io.confluent.examples.clients.basicavro\", \"type\": \"record\", \"name\": \"Payment\", \"fields\": [{\"name\": \"id\", \"type\": \"string\"}, {\"name\": \"amount\", \"type\": \"double\"}]}",
            "source": "{#jsonPath(#message.content, '$.value')}"
        }
    }
}
```

### Schema Registry <a href="#user-content-schema-registry" id="user-content-schema-registry"></a>

To use a schema registry to fetch a schema, declare a Gravitee resource in your API in addition to this policy.

Gravitee provides a resource to interact with Confluent Schema Registry. Find the plugin [here](https://download.gravitee.io/#graviteeio-ee/apim/plugins/resources/gravitee-resource-schema-registry-confluent/).

```json
{
    "name": "avro-2-json",
    "policy": "avro-json",
    "configuration": {
        "conversion": "avro-to-json",
        "schemaLocation": "schema-registry",
        "serializationFormat": "confluent",
        "resourceName": "confluent-schema-registry"
    }
}
```

The policy extracts the schema ID from the binary and uses it to fetch the schema in the registry. When a schema references other schemas, the policy resolves those transitive references during the fetch.

| Warning | The use of Schema Registry is only available to transform message on the `onMessageResponse` phase. |
| ------- | --------------------------------------------------------------------------------------------------- |

### Serialization format <a href="#user-content-serialization-format" id="user-content-serialization-format"></a>

The policy supports the following serialization formats:

* `simple`: the binary contains only the serialized Avro.
* `confluent`: the binary has been generated using [Confluent serialization format](https://docs.confluent.io/platform/current/schema-registry/serdes-develop/index.html#wire-format).

### JSON encoding

Avro unions can be represented in JSON in two ways. The `jsonEncoding` option controls which representation the policy uses, in both directions:

* `WRAPPED` (default): Apache Avro spec format. A nullable or multi-branch union is tagged with its type. For example, a field declared as `["null", "string"]` with the value `"hello"` is rendered as `{"message": {"string": "hello"}}`. Use this when the other side speaks Apache Avro JSON.
* `UNWRAPPED`: natural JSON. The union branch is inferred from the value type. For example, `{"message": "hello"}`. Use this when consumers are C#, TypeScript, or any client that doesn't speak Avro JSON natively.

### Unknown fields handling

When `jsonEncoding` is `UNWRAPPED`, the `unknownFields` option controls how the policy reacts to JSON fields that aren't declared in the Avro schema:

* `STRICT` (default): the policy fails when the incoming JSON contains a field that isn't declared in the Avro schema. This matches the `WRAPPED` behavior.
* `LENIENT`: the policy ignores the extra fields. This is useful when producers emit new fields ahead of consumer schema updates.

### Null fields handling

For `avro-to-json` conversion, the `nullFields` option controls how the policy renders object fields whose value is null:

* `KEEP` (default): null-valued fields are emitted as `"field": null`.
* `OMIT`: null-valued object fields are removed from the output. Null elements inside arrays are preserved.

## Errors <a href="#user-content-errors" id="user-content-errors"></a>

| Phase | Code  | Error template key              | Description                                                                                                                                          |
| ----- | ----- | ------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| \*    | `500` | INVALID\_AVRO\_TRANSFORMATION   | When the transformation fails to be applied to the payload.                                                                                          |
| \*    | `500` | UNSUPPORTED\_CONFIGURATION\_KEY | When the policy configuration isn't supported. For example, when the policy needs a schema registry but also uses the `simple` serialization format. |
