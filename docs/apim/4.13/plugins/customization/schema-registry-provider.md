# Implement a schema registry provider

## Overview

A schema registry provider is a resource plugin that connects the Gateway to a schema registry. Schema-aware policies then fetch schemas through a common contract instead of talking to a specific registry product. This article describes the provider contract and the additions that version `1.1.0` of the contract introduces: schema type exposure, subject membership lookups, and version listing.

The contract lives in the `io.gravitee.resource:gravitee-resource-schema-registry-provider-api` Maven artifact. Gravitee's own implementation is the [Confluent Schema Registry resource](../../create-and-configure-apis/apply-policies/resources.md#confluent-schema-registry), an Enterprise Edition capability. For the common plugin scaffolding that applies to every plugin type, see [Customization](README.md).

## The provider contract

A provider extends the `SchemaRegistryResource` abstract class and implements the following five methods. Each one resolves a `Schema`, or empty when the registry doesn't hold a match.

| Method                                       | Description                                                                 |
| -------------------------------------------- | --------------------------------------------------------------------------- |
| `getSchemaById(id)`                          | Fetch a schema using its id.                                                |
| `getSchema(subject)`                         | Fetch the latest version of a schema for a subject.                         |
| `getSchema(subject, ignoreCache)`            | Fetch the latest version, optionally bypassing the provider's cache.        |
| `getSchema(subject, version)`                | Fetch a specific version of a schema for a subject.                         |
| `getSchema(subject, version, ignoreCache)`   | Fetch a specific version, optionally bypassing the provider's cache.        |

A `Schema` exposes its `content`, `id`, `subject`, `version`, `references`, and `dependencies`.

## Expose schema types

From contract version `1.1.0`, the `SchemaType` enum names the serialization formats a registry reports: `AVRO`, `JSON`, `PROTOBUF`, and `UNKNOWN`. The `Schema.getType()` accessor returns the format of the schema, so a consumer detects the payload format from the registry instead of guessing it.

`getType()` carries a default implementation that returns `UNKNOWN`, for providers and registries that don't expose a type. A provider that knows the format overrides the accessor.

## Answer subject membership lookups

From contract version `1.1.0`, `lookupUnderSubject(subject, schemaContent)` checks whether the given schema content is registered under the subject, independently of which version is `latest`. The following two outcomes exist:

* The content is registered under the subject: the method resolves the registered `Schema`, carrying its id, version, and type, in one round-trip.
* The content isn't registered under the subject: the method resolves empty.

The default implementation resolves empty for registries that don't support membership lookups. A caller treats "no membership info" as "not a member" and falls back to its own comparison logic.

## List subject versions

From contract version `1.1.0`, `getVersions(subject)` lists the version identifiers registered under a subject. The default implementation resolves an empty list for registries that don't support it.

## Compatibility with existing providers

Every `1.1.0` addition ships with a default implementation, so a provider compiled against contract version `1.0.x` compiles and runs unchanged against `1.1.0`. `getType()` is a default interface method, and `lookupUnderSubject()` and `getVersions()` are concrete methods on the abstract class.

## The Confluent implementation

The Confluent Schema Registry resource implements the `1.1.0` surface from plugin version `5.1.0`, which is bundled with APIM 4.13:

* It reports the type of each schema from the registry response. When the registry omits the type, the resource reports `AVRO`, because Confluent registries omit the type for Avro schemas.
* It answers membership lookups against the registry. A successful lookup is cached per subject and schema content, without expiry, for the life of the deployed resource. An empty result isn't cached, so repeating a non-member lookup reaches the registry each time.
* The membership lookup request carries only the schema content, not a schema type.
* It lists subject versions. Version listings aren't cached, so each call reaches the registry.

## Verification

To verify a provider implementation is working as expected, follow these steps:

1. Package the provider as a resource plugin and deploy it to the Gateway, following the structure described in [Customization](README.md).
2. Create the resource on an API and reference it from a schema-aware policy.
3. Send a request that triggers a schema fetch. The policy resolves the schema through your provider, and `getType()` returns the format your registry reported.
