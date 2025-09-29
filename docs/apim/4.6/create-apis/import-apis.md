---
description: Learn how to import APIs onto your Gravitee Gateway
---

# Import APIs

## Introduction

Gravitee supports importing APIs as:

* Files (YML, YAML, JSON, WSDL, XML)
* Swagger/OpenAPI spec (URL)
* API definition (URL)
* WSDL (URL)

Additional information that applies to importing an OpenAPI specification can be found [below](import-apis.md#importing-an-openapi-spec).

{% hint style="warning" %}
When you import an API with a JSON payload that has duplicate keys, APIM keeps the last key.&#x20;

To avoid any errors because of duplicate keys, apply the JSON threat protection policy to the API. For more information about the JSON threat protection policy, see [json-threat-protection.md](../policies/json-threat-protection.md "mention").
{% endhint %}

## Import your API

To import your API:

1. Log in to your API Console
2. Select **APIs** from the left nav
3.  Select **+ Add API**&#x20;

    <figure><img src="../.gitbook/assets/import_add api.png" alt=""><figcaption></figcaption></figure>
4.  In the **Import an API definition** tile, click **Import**&#x20;

    <figure><img src="../.gitbook/assets/import_import.png" alt=""><figcaption></figcaption></figure>
5. Choose and configure an import option:
   * **Upload a file:** Import a YML, YAML, JSON, WSDL, or XML file
   * **Swagger / OpenAPI:**&#x20;
     * Provide a **Swagger descriptor URL**
     * **Create documentation:** Overwrites existing documentation or create it if it does not exist
     * **Create the path mapping for analytics:** Overwrites all of the path-mappings
     * **Create policies on paths:** Overwrites all of the policies. Policies that you can create upon import include **JSON Validation**, **Mock**, **Request Validation**, **REST to SOAP**, and **XML Validation**.
   * **API definition:** Provide a URL that links to your API definition
   * **WSDL:**&#x20;
     * Provide a **WSDL descriptor URL**
     * **Create documentation:** Overwrites existing documentation or create it if it does not exist
     * **Create the path mapping for analytics:** Overwrites all of the path-mappings
     * **Create policies on paths:** Overwrites all of the policies. Policies that you can create upon import include **JSON Validation**, **Mock**, **Request Validation**, **REST to SOAP**, and **XML Validation**.
6. Click **Import**

{% hint style="success" %}
Once you've imported your API, it will be created as a private API and you will be brought to the API menu and details page.
{% endhint %}

## Importing an OpenAPI spec

### **Context-path resolution**

<table><thead><tr><th>Spec version</th><th>Definition</th><th>Example</th><th>Context-path</th></tr></thead><tbody><tr><td>Swagger (V2)</td><td><code>basePath</code> field, if it exists.</td><td><pre><code>{
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
</code></pre></td><td>/v2</td></tr><tr><td>If not, lowercase trimmed <code>info.title</code>.</td><td><pre><code>{
  "swagger": "2.0",
  "info": {
    "description": "...",
    "version": "1.0.5",
    "title": "Swagger Petstore"
  },
  "host": "petstore.swagger.io",

  ...
}
</code></pre></td><td>/swaggerpetstore</td><td></td></tr><tr><td>OpenAPI (V3)</td><td>Path of the first <code>servers.url</code>, if it exists, without "/".<br></td><td><pre><code>openapi: "3.0.0"
info:
  version: 1.0.0
  title: Swagger Petstore
  license:
    name: MIT
servers:
  - url: http://petstore.swagger.io/v1
paths:
...
</code></pre></td><td>/v1</td></tr><tr><td>If not, lowercase trimmed <code>info.title</code>.</td><td><pre><code>openapi: "3.0.0"
info:
  version: 1.0.0
  title: Swagger Petstore
  license:
    name: MIT
servers:
  - url: http://petstore.swagger.io/
paths:
  ...
</code></pre></td><td>/swaggerpetstore</td><td></td></tr></tbody></table>

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
For more information, see the JSON Validation policy in the [policy reference](../policies/policy-reference/).
{% endtab %}

{% tab title="REST to SOAP" %}
For each operation, if the definition contains specific vendor extensions, a REST to SOAP policy can be configured. These extensions are:

* `x-graviteeio-soap-envelope`: Contains the SOAP envelope
* `x-graviteeio-soap-action`: Contains the SOAP action

For more information, see the REST to SOAP policy in the [policy reference](../policies/policy-reference/).
{% endtab %}

{% tab title="Mock" %}
For each operation, a mock policy is configured, based on the `example` field if it exists, or by generating a random value for the type of attribute to mock.\
\
For more information, see the Mock policy in the [policy reference](../policies/policy-reference/).
{% endtab %}

{% tab title="Request Validation" %}
For each operation, `NOT` `NULL` rules are created with query parameters and headers.\
\
For more information, see the Request Validation policy in the [policy reference](../policies/policy-reference/).
{% endtab %}

{% tab title="XML Validation" %}
For each operation, if a `application/xml` request body exists, then a XSD schema is computed from this body to configure an XML Validation policy.&#x20;

For more information, see the XML Validation policy in the [policy reference](../policies/policy-reference/).
{% endtab %}
{% endtabs %}
