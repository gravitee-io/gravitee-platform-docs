= Avro to Protobuf transformation policy

ifdef::env-github[]
image:https://img.shields.io/static/v1?label=Available%20at&message=Gravitee.io&color=1EC9D2["Gravitee.io", link="https://download.gravitee.io/#graviteeio-apim/plugins/policies/gravitee-policy-transform-avro-protobuf/"]
image:https://img.shields.io/badge/License-Apache%202.0-blue.svg["License", link="https://github.com/gravitee-io/gravitee-policy-transform-avro-protobuf/blob/main/LICENSE.txt"]
image:https://img.shields.io/badge/semantic--release-conventional%20commits-e10079?logo=semantic-release["Releases", link="https://github.com/gravitee-io/gravitee-policy-transform-avro-protobuf/releases"]
image:https://dl.circleci.com/status-badge/img/gh/gravitee-io/gravitee-policy-transform-avro-protobuf/tree/main.svg?style=svg["CircleCI", link="https://dl.circleci.com/status-badge/redirect/gh/gravitee-io/gravitee-policy-transform-avro-protobuf/tree/main"]
endif::[]


== Phases

[cols="4*", options="header"]
|===
^|onRequest
^|onResponse
^|onMessageRequest
^|onMessageResponse

^.^| X
^.^| X
^.^| X
^.^| X
|===

== Description

You can use the `avro-protobuf` policy to apply a transformation (or mapping) on the request and/or response and/or
message content.

This policy is using the https://avro.apache.org/docs/1.11.1/[Avro] library.

To serialize data in Avro, you need a https://avro.apache.org/docs/1.11.1/#schemas[schema]. There are two ways to provide a schema:

- inlined in the policy configuration.
- with a Schema Registry.

To serialize data in Protobuf, you need a https://avro-protobuf.dev/overview/[schema]. There are two ways to provide a schema:

- inlined in the policy configuration.
- with a Schema Registry.

=== Inline Schema

You can provide the Schema to use directly in the configuration of the policy:

[source, json]
----
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
----

=== Schema Registry

To use a schema registry to fetch a schema, you will need to declare a Gravitee resource in your API in addition to this policy.

Currently we only provide a resource to interact with Confluent Schema Registry. You can find the plugin https://download.gravitee.io/#graviteeio-ee/apim/plugins/resources/gravitee-resource-schema-registry-confluent/[here].

[source, json]
----
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
----

Currently, we only support https://docs.confluent.io/platform/current/schema-registry/serdes-develop/index.html#wire-format[Confluent serialization format]. The policy will extract the schema id from the binary and will use it to fetch the Schema in the registry.

WARNING: The use of Schema Registry is only available to transform message on the `onMessageResponse` phase.

=== Serialization format

The policy is supporting the serialization formats:

- `simple`: the binary contains only the serialized Protobuf/Avro.
- `confluent`: the binary has been generated using https://docs.confluent.io/platform/current/schema-registry/serdes-develop/index.html#wire-format[Confluent serialization format].

== Errors
|===
|Phase | Code | Error template key | Description

.^| *
.^| ```500```
.^| INVALID_PROTOBUF_TRANSFORMATION
.^| When the transform fail to be applied to the payload.
.^| *
.^| ```500```
.^| UNSUPPORTED_CONFIGURATION_KEY
.^| When the policy configuration is not supported. For example, when the policy needs a schema registry but also use the `simple` serialization format.

|===
