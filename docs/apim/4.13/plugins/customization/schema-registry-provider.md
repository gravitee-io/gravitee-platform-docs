# Implement a schema registry provider

## Overview

{% hint style="info" %}
This page is for plugin developers building a custom schema registry provider.
{% endhint %}

A schema registry provider is a resource plugin that connects the Gateway to a schema registry. Schema-aware policies then fetch schemas through a common contract instead of talking to a specific registry product. This article describes the provider contract and the additions that version `1.1.0` of the contract introduces: schema type exposure, subject membership lookups, and version listing.

The contract lives in the `io.gravitee.resource:gravitee-resource-schema-registry-provider-api` Maven artifact. The [Confluent Schema Registry resource](../../create-and-configure-apis/apply-policies/resources.md#confluent-schema-registry), an Enterprise Edition capability, implements the full `1.1.0` contract. For the common plugin scaffolding that applies to every plugin type, see [Customization](README.md).

## The provider contract

A provider extends the `SchemaRegistryResource` abstract class, typed with the configuration class of the resource:

```java
public abstract class SchemaRegistryResource<C extends ResourceConfiguration> extends AbstractConfigurableResource<C>
```

### Required methods

The five fetch methods are abstract, so every provider implements them:

```java
public abstract Maybe<Schema> getSchemaById(String id);
public abstract Maybe<Schema> getSchema(String subject);
public abstract Maybe<Schema> getSchema(String subject, boolean ignoreCache);
public abstract Maybe<Schema> getSchema(String subject, String version);
public abstract Maybe<Schema> getSchema(String subject, String version, boolean ignoreCache);
```

| Method                                     | Description                                                                                    |
| ------------------------------------------ | ---------------------------------------------------------------------------------------------- |
| `getSchemaById(id)`                        | Fetch a schema from the registry using its id.                                                 |
| `getSchema(subject)`                       | Fetch the latest version of a schema for a subject.                                            |
| `getSchema(subject, ignoreCache)`          | Fetch the latest version of a schema for a subject, optionally bypassing the provider's cache. |
| `getSchema(subject, version)`              | Fetch a specific version of a schema for a subject.                                            |
| `getSchema(subject, version, ignoreCache)` | Fetch a specific version of a schema for a subject, optionally bypassing the provider's cache. |

### Optional methods

From contract version `1.1.0`, two lookup methods carry a concrete default implementation. A provider whose registry supports these lookups overrides them, and every other provider inherits the defaults:

```java
public Maybe<Schema> lookupUnderSubject(String subject, String schemaContent) {
    return Maybe.empty();
}

public Single<List<String>> getVersions(String subject) {
    return Single.just(List.of());
}
```

`lookupUnderSubject(subject, schemaContent)` checks whether the given schema content is registered under the subject, independently of which version is `latest`. The following two outcomes exist:

* The content is registered under the subject: the method resolves the registered `Schema`, carrying its id, version, and type.
* The content isn't registered under the subject: the method resolves empty.

The default implementation resolves empty for registries that don't support membership lookups. A caller treats "no membership info" as "not a member" and can fall back to its own comparison logic.

`getVersions(subject)` lists the version identifiers registered under a subject. The default implementation resolves an empty list for registries that don't support it.

## The `Schema` object

Each fetch method and membership lookup resolves a `Schema`, which exposes its `content`, `id`, `subject`, `version`, `references`, and `dependencies` through accessors.

From contract version `1.1.0`, the `Schema.getType()` accessor also returns the serialization format of the schema as a `SchemaType` value: `AVRO`, `JSON`, `PROTOBUF`, or `UNKNOWN`. A consumer detects the payload format from the registry instead of guessing it.

`getType()` carries a default implementation that returns `UNKNOWN`, for providers and registries that don't expose a type. A provider that knows the format overrides the accessor.

## Compatibility with existing providers

Every `1.1.0` addition ships with a default implementation, and no existing method changed. `getType()` is a default interface method, and `lookupUnderSubject()` and `getVersions()` are concrete methods on the abstract class, so a provider compiled against contract version `1.0.1` compiles and runs unchanged against `1.1.0`.

A provider compiled against contract version `1.0.0` first implements the `getReferences()` and `getDependencies()` accessors, which version `1.0.1` of the contract added to the `Schema` interface.

## Package and deploy the provider

To make a provider available to schema-aware policies, follow these steps:

1. Package the provider as a resource plugin and deploy it to the Gateway, following the structure described in [Customization](README.md).
2. Create the resource on an API, as described in [Resources](../../create-and-configure-apis/apply-policies/resources.md).
3. Reference the resource from a schema-aware policy.

## Verification

To verify a provider implementation is working as expected, follow these steps:

1. Send a request that triggers a schema fetch. The policy resolves the schema through your provider.
2. If your provider overrides `getType()`, fetch a schema and read its type. The accessor returns the format your registry reported instead of the `UNKNOWN` default.
3. If your provider overrides `lookupUnderSubject()`, call it with schema content that isn't registered under the subject. The lookup resolves empty.
