---
description: An overview about import apis.
---

# Import APIs

## Overview

Gravitee supports importing APIs as either Gravitee API definitions or OpenAPI specifications. To import an API, the API file must be in YML, YAML, or JSON format.

Every API includes a context path, virtual host(s), or host(s). These values must be unique across all APIs in your environment. A unique custom API ID can be specified in the definition.

All items from the import bundle are imported, for example, groups, members, pages, plans, and metadata.

Additional information that applies to importing an OpenAPI specification can be found [below](import-apis.md#importing-an-openapi-spec).

{% hint style="warning" %}
When you import an API with a JSON payload that has duplicate keys, APIM keeps the last key.

To avoid any errors because of duplicate keys, apply the JSON threat protection policy to the API. For more information about the JSON threat protection policy, see [json-threat-protection.md](../apply-policies/policy-reference/json-threat-protection.md "mention").
{% endhint %}

## Import your API

To import your API:

1. Log in to your API Console.
2. Select **APIs** from the left nav.
3. Select **+ Add API**.
4.  In the **Create New API** tile, click **Import v4 API**.

    <figure><img src="../../.gitbook/assets/00 import 1.png" alt=""><figcaption></figcaption></figure>

    This loads the options for importing your API.

    <figure><img src="../../.gitbook/assets/00 import 2.png" alt=""><figcaption></figcaption></figure>
5. Choose an **API format**. You can select either **Gravitee definition** or **OpenAPI specification**.
6.  Choose a **File source**.

    <div data-gb-custom-block data-tag="hint" data-style="info" class="hint hint-info">
      <p><strong>Local file</strong> is currently the only supported <strong>File source</strong>.</p>
    </div>
7. Drag and drop your API file into the **File** panel. Supported file formats are YML, YAML, and JSON.
8. If you selected **OpenAPI specification** as the API format, you can choose to enable the following:
   *   **Create documentation page from spec.** This creates an API documentation page from the imported OpenAPI specification.

       <div data-gb-custom-block data-tag="hint" data-style="info" class="hint hint-info">
         <p>This page is published automatically, but can be unpublished from the <strong>API Documentation</strong> page in the Console.</p>
       </div>
   *   **Add OpenAPI Specification Validation:** This adds an [OpenAPI Specification Validation policy](../apply-policies/policy-reference/oas-validation.md) to the imported API.

       <div data-gb-custom-block data-tag="hint" data-style="info" class="hint hint-info">
         <p>All options are initially enabled, but can be disabled by editing the policy configuration.</p>
       </div>
9. Click **Import**

{% hint style="success" %}
Once you've imported your API, it will be created as a private API and you will be brought to the API menu and details page.
{% endhint %}

## Import an OpenAPI spec

{% hint style="info" %}
Gravitee v4 native APIs, for example, Kafka APIs, are currently not supported via OpenAPI spec import.
{% endhint %}

### **Context-path resolution**

#### Swagger (V2)

**Example 1:** The definition below uses the `basePath` field for context-path resolution. The value of the `basePath` field is the context-path, for example, `/v2`.

```json
{
  "swagger": "2.0",
  "info": {
    "description": "...",
    "version": "1.0.5",
    "title": "Swagger Petstore"
  },
  "host": "petstore.swagger.io",
  "basePath": "/v2",
  ...
}
```

**Example 2:** Instead of the `basePath` field, the lowercase trimmed `info.title` can be used for context-path resolution. In the following example, "Swagger Petstore" maps to the context-path `/swaggerpetstore`.

```json
{
  "swagger": "2.0",
  "info": {
    "description": "...",
    "version": "1.0.5",
    "title": "Swagger Petstore"
  },
  "host": "petstore.swagger.io",

  ...
}
```

#### OpenAPI (V3)

**Example 1:** If it exists without `/`, the path of the first `servers.url` can be used for context-path resolution, like in the following example. The value of the context-path follows the URL and starts with `/`, for example, `/v1`.

```json
openapi: "3.0.0"
info:
  version: 1.0.0
  title: Swagger Petstore
  license:
    name: MIT
servers:
  - url: http://petstore.swagger.io/v1
paths:
...
```

**Example 2:** Instead of the `servers.url` path, the lowercase trimmed `info.title` can be used for context-path resolution. In the following example, "Swagger Petstore" maps to the context-path `/swaggerpetstore`.

```json
openapi: "3.0.0"
info:
  version: 1.0.0
  title: Swagger Petstore
  license:
    name: MIT
servers:
  - url: http://petstore.swagger.io/
paths:
  ...
```

### Vendor Extensions

You can use a vendor extension to add more information about your API to an OpenAPI specification.

{% hint style="info" %}
To learn how some policies can be defined in the OpenAPI spec as a vendor extension, see [Policies on path](import-apis.md#policies-on-path).
{% endhint %}

To use a vendor extension, add the `x-graviteeio-definition` field at the root of the specification. The value of this field is an `object` that follows this [JSON Schema](https://raw.githubusercontent.com/gravitee-io/gravitee-api-management/master/gravitee-apim-rest-api/gravitee-apim-rest-api-service/src/main/resources/schema/xGraviteeIODefinition.json).

* Categories must contain either a key or an ID.
* Only existing categories are imported.
* Import will fail if `virtualHosts` are already in use by other APIs.
* If set, `virtualHosts` will override `contextPath`.
* Groups must contain group names. Only existing groups are imported.
* `metadata.format` is case-sensitive. Possible values are:
  * STRING
  * NUMERIC
  * BOOLEAN
  * DATE
  * MAIL
  * URL
* Picture only accepts Data-URI format. Please see the example below.

<pre class="language-yaml" data-title="Example"><code class="lang-yaml"><strong>openapi: "3.0.0"
</strong>info:
  version: 1.2.3
  title: Gravitee Echo API
  license:
    name: MIT
servers:
  - url: https://demo.gravitee.io/gateway/echo
x-graviteeio-definition:
  categories:
    - supplier
    - product
  virtualHosts:
    - host: api.gravitee.io
      path: /echo
      overrideEntrypoint: true
  groups:
    - myGroupName
  labels:
    - echo
    - api
  metadata:
    - name: relatedLink
      value: http://external.link
      format: URL
  picture: data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7
  properties:
    - key: customHttpHeader
      value: X-MYCOMPANY-ID
  tags:
    - DMZ
    - partner
    - internal
  visibility: PRIVATE
paths:
...
</code></pre>

### Policies on path

When importing an OpenAPI definition, you can select the option **Create policies on path** to specify that all routes declared in the OpenAPI specification will be automatically created in APIM. To verify, navigate to the policy management view.

<figure><img src="https://docs.gravitee.io/images/apim/3.x/api-publisher-guide/manage-apis/graviteeio-import-openapi-policies-path.png" alt=""><figcaption></figcaption></figure>

You can also choose to activate policies (below) that will be configured using the OpenAPI specification:

{% tabs %}
{% tab title="JSON Validation" %}
For each operation, if an `application/json` request body exists, a JSON schema is computed from this body to configure a JSON Validation policy.\
\
For more information, see the JSON Validation policy in the [policy reference](../apply-policies/policy-reference/README.md).
{% endtab %}

{% tab title="REST to SOAP" %}
For each operation, if the definition contains specific vendor extensions, a REST to SOAP policy can be configured. These extensions are:

* `x-graviteeio-soap-envelope`: Contains the SOAP envelope
* `x-graviteeio-soap-action`: Contains the SOAP action

For more information, see the REST to SOAP policy in the [policy reference](../apply-policies/policy-reference/README.md).
{% endtab %}

{% tab title="Mock" %}
For each operation, a mock policy is configured, based on the `example` field if it exists, or by generating a random value for the type of attribute to mock.\
\
For more information, see the Mock policy in the [policy reference](../apply-policies/policy-reference/README.md).
{% endtab %}

{% tab title="Request Validation" %}
For each operation, `NOT` `NULL` rules are created with query parameters and headers.\
\
For more information, see the Request Validation policy in the [policy reference](../apply-policies/policy-reference/README.md).
{% endtab %}

{% tab title="XML Validation" %}
For each operation, if a `application/xml` request body exists, then a XSD schema is computed from this body to configure an XML Validation policy.

For more information, see the XML Validation policy in the [policy reference](../apply-policies/policy-reference/README.md).
{% endtab %}
{% endtabs %}
