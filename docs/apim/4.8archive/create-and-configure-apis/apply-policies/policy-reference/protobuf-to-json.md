# Protobuf to JSON

{% hint style="warning" %}
**This feature requires** [**Gravitee's Enterprise Edition**](../../../../4.6/overview/gravitee-apim-enterprise-edition/)**.**
{% endhint %}

## Overview

You can use the `protobuf-json` policy to apply a transformation (or mapping) on the request and/or response and/or message content.

{% hint style="warning" %}
A JSON to Protobuf transformation policy is not yet available.
{% endhint %}

To serialize data in Protobuf, you need a [schema](https://protobuf.dev/overview/). There are two ways to provide a schema:

* Inline in the policy configuration
* With a schema registry

## Configuration

{% hint style="warning" %}
This policy can be applied to v2 APIs, v4 HTTP proxy APIs, and v4 message APIs. It cannot be applied to v4 TCP proxy APIs.
{% endhint %}

### Phases

The phases checked below are supported by the `protobuf-json` policy:

<table data-full-width="false"><thead><tr><th width="209">v2 Phases</th><th width="137" data-type="checkbox">Compatible?</th><th width="200.41136671177264">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>true</td><td>onRequest</td><td>true</td></tr><tr><td>onResponse</td><td>true</td><td>onResponse</td><td>true</td></tr><tr><td>onRequestContent</td><td>false</td><td>onMessageRequest</td><td>true</td></tr><tr><td>onResponseContent</td><td>false</td><td>onMessageResponse</td><td>true</td></tr></tbody></table>

### Inline Schema <a href="#user-content-inline-schema" id="user-content-inline-schema"></a>

You can provide the schema to use directly in the configuration of the `protobuf-json` policy:

```json
{
    "name": "protobuf-2-json",
    "policy": "protobuf-json",
    "configuration": {
        "conversion": "protobuf-to-json",
        "json": {
            "includingDefaultValueFields": false,
            "preservingProtoFieldNames": false,
            "sortingMapKeys": false,
            "omittingInsignificantWhitespace": false
    },
    "protobufIn": {
        "schemaLocation": "inline",
        "inlineIn": {
            "normalizeSchema": false,
            "serializationFormat": "confluent",
            "schemaDefinition": "syntax = \"proto2\";\npackage test;\n\nmessage Payment {\n  required string id = 1;\n  required double amount = 2;\n}"
        }
    }
  }
}
```

### Schema registry <a href="#user-content-schema-registry" id="user-content-schema-registry"></a>

To use a schema registry to fetch a schema, you will need to declare a Gravitee resource in your API, in addition to the `protobuf-json` policy.

Currently, we only provide a resource to interact with Confluent Schema Registry. You can find the plugin [here](https://download.gravitee.io/#graviteeio-ee/apim/plugins/resources/gravitee-resource-schema-registry-confluent/).

```json
{
    "name": "protobuf-2-json",
    "policy": "protobuf-json",
    "configuration": {
        "conversion": "json-to-protobuf",
        "protobufOut": {
            "schemaLocation": "schema-registry",
            "schemaRegistryOut": {
                "id": {
                    "origin": "inline",
                    "value": 2
                },
                "resourceName": "resource-name",
                "serializationFormat": "confluent"
            }
        }
    }
}
```

Currently, we only support [Confluent serialization format](https://docs.confluent.io/platform/current/schema-registry/serdes-develop/index.html#wire-format). The `protobuf-json` policy will extract the schema ID from the binary and use it to fetch the schema in the registry.

{% hint style="warning" %}
The use of a schema registry is only available to transform messages on the `onMessageResponse` phase.
{% endhint %}

### Serialization format <a href="#user-content-serialization-format" id="user-content-serialization-format"></a>

The `protobuf-json` policy supports the following serialization formats:

* `simple`: The binary contains only the serialized Protobuf
* `confluent`: The binary has been generated using [Confluent serialization format](https://docs.confluent.io/platform/current/schema-registry/serdes-develop/index.html#wire-format)

## Errors

<table><thead><tr><th width="95">Phase</th><th width="72">Code</th><th width="199">Error template key</th><th>Description</th></tr></thead><tbody><tr><td>*</td><td><code>500</code></td><td>INVALID_PROTOBUF_TRANSFORMATION</td><td>When the transformation fails to be applied to the payload.</td></tr><tr><td>*</td><td><code>500</code></td><td>UNSUPPORTED_CONFIGURATION_KEY</td><td>When the policy configuration is not supported. For example, when the policy needs a schema registry but also uses the <code>simple</code> serialization format.</td></tr></tbody></table>
