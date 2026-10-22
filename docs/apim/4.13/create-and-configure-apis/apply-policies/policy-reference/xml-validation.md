---
description: The XML Validation policy validates XML against an XSD schema in API Management 4.13, rejecting bad requests. Learn how to configure it.
metaLinks:
  alternates:
    - xml-validation.md
---

# XML Validation

## Overview

The `xml-validation` policy validates XML against an XSD schema. This policy uses `javax.xml`. The schema is set in the policy or read from a schema registry through an [HTTP Schema Registry](../resources.md#http-schema-registry) resource. A request whose body doesn't match the schema fails with a `400` error, described in [Errors](#errors). It also injects processing report messages into request metrics for analytics.

## Examples

{% hint style="warning" %}
This policy can be applied to v2 APIs and v4 HTTP proxy APIs. It cannot be applied to v4 message APIs or v4 TCP proxy APIs.
{% endhint %}

{% tabs %}
{% tab title="HTTP proxy API example" %}
Sample policy configuration:

```json
{
    "errorMessage":"XML payload is improperly formatted",
    "xsdSchema":"<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<xs:schema xmlns:xs=\"http://www.w3.org/2001/XMLSchema\" attributeFormDefault=\"unqualified\"\n           elementFormDefault=\"qualified\">\n    <xs:element name=\"root\" type=\"rootType\">\n    </xs:element>\n\n    <xs:complexType name=\"rootType\">\n        <xs:sequence>\n            <xs:element name=\"companies\" type=\"companiesType\"/>\n        </xs:sequence>\n    </xs:complexType>\n\n    <xs:complexType name=\"companiesType\">\n        <xs:sequence>\n            <xs:element name=\"company\" type=\"companyType\" maxOccurs=\"unbounded\" minOccurs=\"0\"/>\n        </xs:sequence>\n    </xs:complexType>\n\n    <xs:complexType name=\"companyType\">\n        <xs:sequence>\n            <xs:element type=\"xs:string\" name=\"name\"/>\n            <xs:element type=\"xs:integer\" name=\"employeeNumber\"/>\n            <xs:element type=\"xs:long\" name=\"sales\"/>\n            <xs:element type=\"xs:string\" name=\"CEO\"/>\n        </xs:sequence>\n    </xs:complexType>\n</xs:schema>"
}
```
{% endtab %}
{% endtabs %}

## Configuration

### Phases

The phases checked below are supported by the `xml-validation` policy:

<table data-full-width="false"><thead><tr><th width="209">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="202.41136671177264">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>false</td><td>onRequest</td><td>true</td></tr><tr><td>onResponse</td><td>false</td><td>onResponse</td><td>false</td></tr><tr><td>onRequestContent</td><td>true</td><td>onMessageRequest</td><td>false</td></tr><tr><td>onResponseContent</td><td>false</td><td>onMessageResponse</td><td>false</td></tr></tbody></table>

### Options

The `xml-validation` policy can be configured with the following options:

<table><thead><tr><th width="160">Property</th><th data-type="checkbox">Required</th><th width="248">Description</th><th>Type</th><th>Default</th></tr></thead><tbody><tr><td>schemaSource</td><td>false</td><td>Where the policy reads the XSD schema: <code>inline</code> from <code>xsdSchema</code>, or <code>registry</code> from a schema registry. Labeled <strong>Schema source</strong> in the Console, with the options <strong>Inline XSD</strong> and <strong>Schema registry</strong>.</td><td>string</td><td>inline</td></tr><tr><td>xsdSchema</td><td>false</td><td>The XSD schema. Required when <code>schemaSource</code> is <code>inline</code>. Labeled <strong>XSD schema</strong> in the Console.</td><td>string</td><td></td></tr><tr><td>registryResource</td><td>false</td><td>The name of the HTTP Schema Registry resource that the policy reads the schema through. Required when <code>schemaSource</code> is <code>registry</code>. Labeled <strong>The name of the Schema Registry resource</strong> in the Console.</td><td>string</td><td></td></tr><tr><td>groupId</td><td>false</td><td>The group of the root schema in the registry. Required when <code>schemaSource</code> is <code>registry</code>. Labeled <strong>Group ID</strong> in the Console.</td><td>string</td><td></td></tr><tr><td>artifactId</td><td>false</td><td>The artifact ID of the root schema in the registry. Required when <code>schemaSource</code> is <code>registry</code>. Labeled <strong>Artifact ID</strong> in the Console.</td><td>string</td><td></td></tr><tr><td>version</td><td>false</td><td>The version of the root schema in the registry, or a value that the registry resolves to a version, such as <code>branch=latest</code>. Required when <code>schemaSource</code> is <code>registry</code>. Labeled <strong>Version</strong> in the Console.</td><td>string</td><td></td></tr><tr><td>errorMessage</td><td>false</td><td>The message of the response when the request body doesn't match the schema. Supports Gravitee Expression Language. When it's empty, a default message applies, described in <a href="#errors">Errors</a>. Labeled <strong>Http error message</strong> in the Console.</td><td>string</td><td></td></tr></tbody></table>

### Schema registry

To read the XSD schema from a schema registry, add an [HTTP Schema Registry](../resources.md#http-schema-registry) resource to the API. Then set **Schema source** to **Schema registry**, and set the resource name, **Group ID**, **Artifact ID**, and **Version** of the root schema. The schema registry source works on v4 HTTP proxy APIs only. Saving a v2 API or a v4 message API whose policy uses it fails. Saving also fails when no resource of the API has the name you set, when a registry field is empty, or when **XSD schema** also holds a schema.

The following configuration reads version `1.0.0` of the schema `order` in the group `orders`, through the resource named `xsd-registry`:

```json
{
    "schemaSource": "registry",
    "registryResource": "xsd-registry",
    "groupId": "orders",
    "artifactId": "order",
    "version": "1.0.0"
}
```

The schema is read when the first request reaches the policy, not when you deploy the API. The resource also fetches the schemas that the root schema references in the registry. Each `xs:import` and `xs:include` resolves to the reference whose name matches its `schemaLocation`, or the file name at the end of it. A `schemaLocation` that's an `http`, `https`, or `file` URL isn't downloaded, and the schema fails to compile.

The resource caches the schemas it fetches. To pick up a newer schema without redeploying the API, for example with **Version** set to `branch=latest`, set **Byte cache TTL (ms)** on the resource. After the cached entry expires, the next request fetches the schema again, and the policy validates against the new content.

If the registry stops answering after the policy compiled a schema, the policy keeps validating against that schema. Until the first successful fetch, requests fail with the errors listed in [Errors](#errors).

## Compatibility matrix

The following is the compatibility matrix for APIM and the `xml-validation` policy:

<table data-full-width="false"><thead><tr><th>Plugin Version</th><th>Supported APIM versions</th></tr></thead><tbody><tr><td>1.x</td><td>All</td></tr><tr><td>2.x</td><td>4.13 and later</td></tr></tbody></table>

APIM bundles version 2.x of the policy from 4.13.0 onward. The schema registry source and the list of violations in the error response were added in version 2.1.0.

## Errors

When the request body doesn't match the schema, the request fails with `400` and the error key `XML_VALIDATION_FAILED`. A body that's empty, isn't well-formed XML, or declares a `DOCTYPE` fails the same way. The response body is a JSON object. Its `message` holds **Http error message**, or `XML validation failed` when that field is empty. Its `violations` array lists up to 20 problems, each with its `line`, `column`, `element`, and `message`, plus its `path` and `code` when they're known:

```json
{
    "message": "XML validation failed",
    "violations": [
        {
            "line": 1,
            "column": 51,
            "element": "quantity",
            "path": "/order/item/quantity",
            "message": "cvc-maxInclusive-valid: Value '500' is not facet-valid with respect to maxInclusive '100' for type 'Quantity'.",
            "code": "cvc-maxInclusive-valid"
        }
    ]
}
```

The response has the `application/json` content type when the request's `Accept` header includes `application/json` or `*/*`, and `text/plain` otherwise. The body is the JSON object above in both cases. This response applies to v4 HTTP proxy APIs and to v2 APIs in [emulation mode](../../gravitee-api-definitions/execution-engine.md#v2-gateway-api-emulation-mode).

With emulation mode disabled, a v2 API responds with **Http error message**, or a text summary of the violations when that field is empty, and the error key `XML_INVALID_PAYLOAD`. When the request's `Accept` header includes `application/json` or `*/*`, the body is a JSON object with that message in `message` and the status code in `http_status_code`, and the content type is `application/json`. Otherwise, the body is the message alone, and the content type is `text/plain`.

With **Schema source** set to **Schema registry**, the following errors occur when the policy can't read or compile the schema. The response body is a JSON object whose `message` holds the message in the table:

<table data-full-width="false"><thead><tr><th width="100">HTTP status code</th><th>Error key</th><th>Message</th><th>Cause</th></tr></thead><tbody><tr><td><code>400</code></td><td><code>XML_VALIDATION_SCHEMA_CONFIGURATION_INVALID</code></td><td>XML validation schema configuration is invalid</td><td>The resource that the policy names is disabled, or isn't an HTTP Schema Registry resource.</td></tr><tr><td><code>500</code></td><td><code>XML_VALIDATION_SCHEMA_ARTIFACT_NOT_FOUND</code></td><td>Referenced schema artifact was not found</td><td>The registry has no schema for the group, artifact ID, and version, or a schema that it references is missing.</td></tr><tr><td><code>500</code></td><td><code>XML_VALIDATION_SCHEMA_COMPILE_FAILED</code></td><td>Unable to compile the XSD schema</td><td>The schema isn't a valid XSD, imports or includes a schema that isn't among its references, or uses an <code>http</code>, <code>https</code>, or <code>file</code> URL as <code>schemaLocation</code>.</td></tr><tr><td><code>500</code></td><td><code>XML_VALIDATION_SCHEMA_CLOSURE_LIMIT_EXCEEDED</code></td><td>Schema closure exceeds the maximum artifacts limit, Schema closure exceeds the maximum bytes limit, or Schema closure exceeds the maximum import depth limit</td><td>The schema and the schemas it references exceed <strong>Max artifacts in closure</strong>, <strong>Max total closure bytes</strong>, or <strong>Max import depth</strong> on the resource.</td></tr><tr><td><code>500</code></td><td><code>XML_VALIDATION_SCHEMA_CONFIGURATION_INVALID</code></td><td>Unable to resolve the XSD schema</td><td>The registry returns an empty schema or a list of references that can't be read, or answers with a status that isn't <code>2xx</code>, <code>401</code>, <code>403</code>, <code>404</code>, or <code>5xx</code>.</td></tr><tr><td><code>503</code></td><td><code>XML_VALIDATION_SCHEMA_REGISTRY_UNREACHABLE</code></td><td>Schema registry is temporarily unavailable</td><td>The registry can't be reached, doesn't answer in time, or answers with <code>401</code>, <code>403</code>, or a <code>5xx</code> status. The error repeats until <strong>Negative cache TTL (ms)</strong> of the resource has passed.</td></tr><tr><td><code>503</code></td><td><code>XML_VALIDATION_SCHEMA_REGISTRY_NOT_READY</code></td><td>Schema registry is not ready</td><td>The resource hasn't started.</td></tr></tbody></table>

The `500` and `503` errors occur only until the policy compiles a schema for the first time. After that, when fetching the schema again fails, the policy keeps validating against the last schema it compiled. Use these error keys in [response templates](../../../analyze-and-monitor-apis/gateway-error-key-reference.md#use-error-keys-in-response-templates) to change the responses.

{% hint style="warning" %}
Saving an API doesn't check an inline schema. If **XSD schema** doesn't hold a valid XSD, or holds an `xs:import` or `xs:include` whose `schemaLocation` is an `http`, `https`, or `file` URL, the schema doesn't compile. Requests fail with `500` and the error key `XML_VALIDATION_SCHEMA_COMPILE_FAILED`, and don't reach the backend. The message is `Unable to compile the XSD schema`. On v4 HTTP proxy APIs and on v2 APIs in emulation mode, the body is a JSON object whose `message` holds that text. With emulation mode disabled, the body is the message alone, with the `text/plain` content type, unless the request's `Accept` header includes `application/json` or `*/*`. In that case, the body is a JSON object with that message in `message` and the status code in `http_status_code`, and the content type is `application/json`. After you deploy an API with an inline schema, send a request that doesn't match the schema and check that it's rejected.
{% endhint %}
