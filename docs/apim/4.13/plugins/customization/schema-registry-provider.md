# Implement a schema registry provider

## Overview

A schema registry provider is a resource plugin that connects the Gateway to a schema registry. Schema-aware policies then fetch schemas through a common contract instead of talking to a specific registry product.

The contract lives in the `io.gravitee.resource:gravitee-resource-schema-registry-provider-api` Maven artifact. Gravitee's own implementation is the [Confluent Schema Registry resource](../../create-and-configure-apis/apply-policies/resources.md#confluent-schema-registry), an Enterprise Edition capability. For the common plugin scaffolding that applies to every plugin type, see [Customization](README.md).

## Verification

To verify a provider implementation is working as expected, follow these steps:

1. Package the provider as a resource plugin and deploy it to the Gateway, following the structure described in [Customization](README.md).
2. Create the resource on an API and reference it from a schema-aware policy.
3. Send a request that triggers a schema fetch. The policy resolves the schema through your provider.
