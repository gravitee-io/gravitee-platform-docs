---
description: This page provides the technical details of the AVRO <> JSON policy
---

# AVRO <> JSON

{% hint style="warning" %}
**This feature requires** [**Gravitee's Enterprise Edition**](../../overview/ee-vs-oss/)**.**
{% endhint %}

## Overview

You can use the `avro-json` policy to apply a transformation (or mapping) on the request and/or response and/or message content.&#x20;

This policy uses the [Avro](https://avro.apache.org/docs/1.11.1/) library. To serialize data in Avro, you need a [schema](https://avro.apache.org/docs/1.11.1/#schemas). A schema can be provided inline in the policy configuration or with a schema registry.

Functional and implementation information for the `avro-json` policy is organized into the following sections:

* [Examples](avro-json.md#examples)
* [Configuration](avro-json.md#configuration)
* [Errors](avro-json.md#errors)

## Examples

{% hint style="warning" %}
The proxy API example also applies to v2 APIs. This policy can also be applied at the message level for v4 APIs.
{% endhint %}

{% tabs %}
{% tab title="Message APIs" %}
Example of inline publishing of Avro to JSON:

```json
{
    "id": "inline_publish_avro_to_json",
    "name": "inline_publish_avro_to_json",
    "apiVersion": "1.0",
    "definitionVersion": "4.0.0",
    "type": "message",
    "description": "inline_publish_avro_to_json",
    "listeners": [
        {
            "type": "http",
            "paths": [
                {
                    "path": "/inline_publish_avro_to_json"
                }
            ],
            "entrypoints": [
                {
                    "type": "http-post",
                    "configuration": {}
                }
            ]
        }
    ],
    "endpointGroups": [
        {
            "name": "default",
            "type": "kafka",
            "endpoints": [
                {
                    "name": "default",
                    "type": "kafka",
                    "weight": 1,
                    "inheritConfiguration": false,
                    "configuration": {
                        "bootstrapServers": "bootstrap-server"
                    },
                    "sharedConfigurationOverride": {
                        "producer": {
                            "enabled": true,
                            "topics": ["json-topic"]
                        }
                    }
                }
            ]
        }
    ],
    "flows": [
        {
            "name": "flow-1",
            "enabled": true,
            "selectors": [
                {
                    "type": "http",
                    "path": "/",
                    "pathOperator": "STARTS_WITH"
                }
            ],
            "request": [],
            "response": [],
            "subscribe": [],
            "publish": [
                {
                    "name": "avro-2-json",
                    "description": "avro-2-json",
                    "enabled": true,
                    "policy": "avro-json",
                    "configuration": {
                        "conversion": "avro-to-json",
                        "schemaLocation": "inline",
                        "schemaDefinition": "{\"namespace\": \"io.confluent.examples.clients.basicavro\", \"type\": \"record\", \"name\": \"Payment\", \"fields\": [{\"name\": \"id\", \"type\": \"string\"}, {\"name\": \"amount\", \"type\": \"double\"}]}\n"
                    }
                }
            ]
        }
    ],
    "analytics": {
        "enabled": false
    }
}
```
{% endtab %}
{% endtabs %}

## Configuration

### Inline schema <a href="#user-content-inline-schema" id="user-content-inline-schema"></a>

You can directly provide the schema to use in the policy configuration:

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

### Schema registry <a href="#user-content-schema-registry" id="user-content-schema-registry"></a>

To use a schema registry to fetch a schema, you will need to declare a Gravitee resource in your API in addition to this policy.

Currently, we only provide a resource to interact with Confluent Schema Registry. You can find the plugin [here](https://download.gravitee.io/#graviteeio-ee/apim/plugins/resources/gravitee-resource-schema-registry-confluent/).

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

The policy will extract the schema ID from the binary and will use it to fetch the schema in the registry.

### Serialization format

The `avro-json` policy supports the following serialization formats:

* `confluent`: The binary is generated using [Confluent serialization format](https://docs.confluent.io/platform/current/schema-registry/serdes-develop/index.html#wire-format). This is the serialization format used by Gravitee by default and by the `kafka-avro-serializer` library.
* `simple`: The binary contains only the serialized Avro. The `simple` format can only be used for inline schema. If you serialize data "manually" (without `kafka-serializer`), the policy may not able to deserialize the binary.

### Phases

Phases supported by the `avro-json` policy differ based on schema type.

#### **Inline schema phases**

Inline schema is not compatible with `onRequestContent` or `onResponseContent` (the body of v4 proxy APIs).

<table data-full-width="false"><thead><tr><th width="209">v2 Phases</th><th width="133" data-type="checkbox">Compatible?</th><th width="198.41136671177264">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>true</td><td>onRequest</td><td>true</td></tr><tr><td>onResponse</td><td>true</td><td>onResponse</td><td>true</td></tr><tr><td>onRequestContent</td><td>false</td><td>onMessageRequest</td><td>true</td></tr><tr><td>onResponseContent</td><td>false</td><td>onMessageResponse</td><td>true</td></tr></tbody></table>

#### **Schema registry phases**

The use of Confluent Schema Registry is only available to transform messages on the `onMessageResponse` phase.

<table data-full-width="false"><thead><tr><th width="209">v2 Phases</th><th width="133" data-type="checkbox">Compatible?</th><th width="198.41136671177264">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>false</td><td>onRequest</td><td>false</td></tr><tr><td>onResponse</td><td>false</td><td>onResponse</td><td>false</td></tr><tr><td>onRequestContent</td><td>false</td><td>onMessageRequest</td><td>false</td></tr><tr><td>onResponseContent</td><td>false</td><td>onMessageResponse</td><td>true</td></tr></tbody></table>

## Errors

<table><thead><tr><th width="99">Code</th><th width="301">Error template key</th><th>Description</th></tr></thead><tbody><tr><td><code>500</code></td><td>INVALID_AVRO_TRANSFORMATION</td><td>The transform fails to be applied to the payload</td></tr><tr><td><code>500</code></td><td>UNSUPPORTED_CONFIGURATION_KEY</td><td>The policy configuration is not supported. For example, the policy needs a schema registry but also uses the <code>simple</code> serialization format.</td></tr></tbody></table>
