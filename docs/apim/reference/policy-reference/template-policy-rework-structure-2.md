---
description: This page provides the technical details of the AVRO <> JSON policy
---

# AVRO <> JSON

{% hint style="warning" %}
**This feature requires** [**Gravitee's Enterprise Edition**](../../overview/introduction-to-gravitee-api-management-apim/ee-vs-oss.md)**.**
{% endhint %}

## Overview

Functional and implementation information for the AVRO <> JSON policy is organized into the following sections:

* [Configuration](template-policy-rework-structure-2.md#configuration)
* [Errors](template-policy-rework-structure-2.md#errors)

You can use the `avro-json` policy to apply a transformation (or mapping) on the request and/or response and/or message content. This policy is using the [Avro](https://avro.apache.org/docs/1.11.1/) library.

To serialize data in Avro, you need a [schema](https://avro.apache.org/docs/1.11.1/#schemas). There are two ways to provide a schema:

* Inlined in the policy configuration
* With a Schema Registry

## Configuration

Policies can be added to flows that are assigned to an API or to a plan. Gravitee supports configuring policies [through the Policy Studio](../../guides/policy-design/) in the Management Console or interacting directly with the Management API.

When using the Management API, policies are added as flows either directly to an API or to a plan. To learn more about the structure of the Management API, check out the [reference documentation here.](../management-api-reference/)

### Inline Schema <a href="#user-content-inline-schema" id="user-content-inline-schema"></a>

You can provide the Schema to use directly in the configuration of the policy:

```
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

### Schema Registry <a href="#user-content-schema-registry" id="user-content-schema-registry"></a>

To use a schema registry to fetch a schema, you will need to declare a Gravitee resource in your API in addition to this policy.

Currently we only provide a resource to interact with Confluent Schema Registry. You can find the plugin [here](https://download.gravitee.io/#graviteeio-ee/apim/plugins/resources/gravitee-resource-schema-registry-confluent/).

```
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

Currently, we only support [Confluent serialization format](https://docs.confluent.io/platform/current/schema-registry/serdes-develop/index.html#wire-format). The policy will extract the schema id from the binary and will use it to fetch the Schema in the registry.

{% hint style="warning" %}
The use of Schema Registry is only available to transform message on the `onMessageResponse` phase.
{% endhint %}

#### Serialization format <a href="#user-content-serialization-format" id="user-content-serialization-format"></a>

The policy is supporting the serialization formats:

* `simple`: the binary contains only the serialized Avro.
* `confluent`: the binary has been generated using [Confluent serialization format](https://docs.confluent.io/platform/current/schema-registry/serdes-develop/index.html#wire-format).

### Phases

Policies can be applied to the request or the response of a Gateway API transaction. The request and response are broken up into phases that depend on the [Gateway API version](../../overview/gravitee-api-definitions-and-execution-engines.md). Each policy is compatible with a subset of the available phases.

The phases checked below are supported by the AVRO <> JSON policy:

<table data-full-width="false"><thead><tr><th width="209">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="188.41136671177264">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>true</td><td>onRequest</td><td>true</td></tr><tr><td>onResponse</td><td>true</td><td>onResponse</td><td>true</td></tr><tr><td>onRequestContent</td><td>false</td><td>onMessageRequest</td><td>true</td></tr><tr><td>onResponseContent</td><td>false</td><td>onMessageResponse</td><td>true</td></tr></tbody></table>

## Errors

<table><thead><tr><th width="179">Code</th><th>Error template key</th><th>Description</th></tr></thead><tbody><tr><td><code>500</code></td><td>INVALID_AVRO_TRANSFORMATION</td><td>When the transform fail to be applied to the payload.</td></tr><tr><td><code>500</code></td><td>UNSUPPORTED_CONFIGURATION_KEY</td><td>When the policy configuration is not supported. For example, when the policy needs a schema registry but also use the <code>simple</code> serialization format.</td></tr></tbody></table>
