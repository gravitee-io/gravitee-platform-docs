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
When you import an API with a JSON payload that has duplicate keys, APIM keeps the last key.

To avoid any errors because of duplicate keys, apply the JSON threat protection policy to the API. For more information about the JSON threat protection policy, see [json-threat-protection.md](../policies/json-threat-protection.md "mention").
{% endhint %}

## Import your API

To import your API:

1. Log in to your API Console
2. Select **APIs** from the left nav
3.  Select **+ Add API**

    <figure><img src="../.gitbook/assets/import_add api.png" alt=""><figcaption></figcaption></figure>
4.  In the **Import an API definition** tile, click **Import**

    <figure><img src="../.gitbook/assets/import_import.png" alt=""><figcaption></figcaption></figure>
5. Choose and configure an import option:
   * **Upload a file:** Import a YML, YAML, JSON, WSDL, or XML file
   * **Swagger / OpenAPI:**
     * Provide a **Swagger descriptor URL**
     * **Create documentation:** Overwrites existing documentation or create it if it does not exist
     * **Create the path mapping for analytics:** Overwrites all of the path-mappings
     * **Create policies on paths:** Overwrites all of the policies. Policies that you can create upon import include **JSON Validation**, **Mock**, **Request Validation**, **REST to SOAP**, and **XML Validation**.
   * **API definition:** Provide a URL that links to your API definition
   * **WSDL:**
     * Provide a **WSDL descriptor URL**
     * **Create documentation:** Overwrites existing documentation or create it if it does not exist
     * **Create the path mapping for analytics:** Overwrites all of the path-mappings
     * **Create policies on paths:** Overwrites all of the policies. Policies that you can create upon import include **JSON Validation**, **Mock**, **Request Validation**, **REST to SOAP**, and **XML Validation**.
6. Click **Import**

{% hint style="success" %}
Once you've imported your API, it will be created as a private API and you will be brought to the API menu and details page.
{% endhint %}

## Programmatic API Import using the Management API

### Overview

In addition to UI-based imports, you can programmatically import and update APIs using the Gravitee Management API. This is particularly useful for CI/CD workflows where you need to deploy APIs across multiple environments (development, staging, production).

### API Definition and CrossID

An API definition is a JSON representation of an API and its content, including plans, pages, metadata, etc. You can get the API definition by exporting it from the APIM Console or using the export endpoint [`GET /apis/{api.id}/export`](https://gravitee-io-labs.github.io/mapi-v1-docs/#tag/api-definition/get/organizations/{orgId}/environments/{envId}/apis/{api}/definition).

Each entity (API, plan, or page) in an API definition contains a crossId and a technical ID.

{% tabs %}
{% tab title="crossId" %}
Uniquely identifies an entity (API, plan, or page) across environments. An entity will use the same `crossId` for all environments.

You can find an API using the `getApis` endpoint and the `crossId` query param: [`GET /apis?crossId=my-cross-id`](https://gravitee-io-labs.github.io/mapi-v1-docs/#tag/apis/get/organizations/{orgId}/environments/{envId}/apis).
{% endtab %}

{% tab title="Technical ID" %}
Uniquely identifies an entity in one environment only. The same entity will have a different technical ID for each environment.

The API import process uses the `crossId` to match existing entities with those in the API definition. The technical ID is not used during the import process unless the `crossId` isn't defined, e.g., in the case of an old exported API definition.
{% endtab %}
{% endtabs %}

### Importing Endpoints

Importing endpoints allows you to import an API from an API definition. The HTTP request body can contain either the JSON API definition or an HTTP link to the JSON API definition. The link requires the target organization and environment in the prefix: `/organizations/{organization.id}/environments/{environment.id}/`

#### Creating a new API from an API definition

To create a new API from an API definition, use [`POST /api/import`](https://gravitee-io-labs.github.io/mapi-v1-docs/#tag/apis/post/organizations/{orgId}/environments/{envId}/apis/import).

* In the API definition, set the `crossId` that will identify your API (and related entities) across environments. You can assign any string to this `crossId`.

{% hint style="info" %}
An error will be raised if there is already an existing API in the target environment with the same `crossId`.
{% endhint %}

* Do not include a technical ID in your API definition. The server will automatically generate an ID for the newly created API. Even if you provide a technical ID, it will not be used.

#### Updating an existing API from an API definition

To update an existing API from an API definition, use [`PUT /api/import`](https://gravitee-io-labs.github.io/mapi-v1-docs/#tag/apis/put/organizations/{orgId}/environments/{envId}/apis/import).

* Including the technical ID in the URL is not mandatory. The `crossId` in your API definition will be used to find the target API. This allows you to use the same URL to update your API across all environments.

{% hint style="info" %}
Alternatively, you can use the URL containing the API technical ID: [`PUT /api/{api.id}/import`](https://gravitee-io-labs.github.io/mapi-v1-docs/#tag/apis/put/organizations/{orgId}/environments/{envId}/apis/{api}/import). An error will be raised if the `crossId` of your definition matches another API in the target environment.
{% endhint %}

### API Content Behavior

This section describes how API content behaves during import.

{% tabs %}
{% tab title="Plans" %}
* A plan in an API definition that already exists in the target API will be updated. This will not change the status of the plan.
* A plan in an API definition that does not exist in the target API will be created.
* A plan without subscriptions that exists in the target API and does not exist in the API definition will be deleted. An error would be raised if the plan accrued subscriptions.
{% endtab %}

{% tab title="Pages" %}
* A page in an API definition that already exists in the target API will be updated.
* A page in an API definition that does not exist in the target API will be created.
* A page in a target API that is not present in the API definition will not change.
{% endtab %}

{% tab title="Groups, members, & roles" %}
How groups, members, and roles are imported depends on the installation.

* **When using the import feature to update or create an API for the same environment members:** Groups and roles can be edited, and group memberships are preserved.
* **When importing to another environment:** Groups that are unknown to the target environment will be created, but their memberships will not be preserved.
* **When importing to another environment that runs on the same APIM instance (same database):** Direct members will be preserved in the target environment.
* **When importing to another environment that runs on a separate APIM instance:** Direct members will not be preserved, and groups that are unknown to the target environment will be created without preserving their memberships.
{% endtab %}
{% endtabs %}

## CI/CD Use Case Examples

<details>

<summary>Create your API in a development environment</summary>

Use the APIM Console.

</details>

<details>

<summary>Push your API to a production environment</summary>

* Get your API definition by exporting it from the APIM Console or using the export endpoint. For example:

```bash
curl -H "Authorization: Bearer MY-ACCESS-TOKEN" \
     -H "Content-Type:application/json;charset=UTF-8" \
     -X GET \
     https://[GRAVITEEIO-APIM-MGT-API-HOST]/management/organizations/[ORGANIZATION_ID]/environments/[ENVIRONMENT_ID]/apis/35a1b7d4-b644-43d1-a1b7-d4b64493d134/export
```

* For each environment where you want to create your API, call the POST endpoint. For example:

```bash
curl -H "Authorization: Bearer MY-ACCESS-TOKEN" \
     -H "Content-Type:application/json;charset=UTF-8" \
     -X POST \
     -d '{
            "name": "my-api",
            "crossId": "3e645da6-039c-4cc0-a45d-a6039c1cc0d3",
            "version": "1",
            [....]
        }' \
     https://[GRAVITEEIO-APIM-MGT-API-HOST]/management/organizations/[ORGANIZATION_ID]/environments/[ENVIRONMENT_ID]/apis/import
```

</details>

<details>

<summary>Update your API in a production environment</summary>

* Update your API definition manually or by re-exporting the source API from the development environment.
* For each environment where you want to update your API, call the PUT endpoint. For example:

```bash
curl -H "Authorization: Bearer MY-ACCESS-TOKEN" \
     -H "Content-Type:application/json;charset=UTF-8" \
     -X PUT \
     -d '{
            "name": "my-updated-api",
            "crossId": "3e645da6-039c-4cc0-a45d-a6039c1cc0d3",
            "version": "1",
            [....]
        }' \
     https://[GRAVITEEIO-APIM-MGT-API-HOST]/management/organizations/[ORGANIZATION_ID]/environments/[ENVIRONMENT_ID]/apis/import
```

</details>

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

url: http://petstore.swagger.io/v1
paths:
...
</code></pre></td><td>/v1</td></tr><tr><td>If not, lowercase trimmed <code>info.title</code>.</td><td><pre><code>openapi: "3.0.0"
info:
version: 1.0.0
title: Swagger Petstore
license:
name: MIT
servers:
url: http://petstore.swagger.io/
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
For more information, see the JSON Validation policy in the [policy reference](../policies/policy-reference/README.md).
{% endtab %}

{% tab title="REST to SOAP" %}
For each operation, if the definition contains specific vendor extensions, a REST to SOAP policy can be configured. These extensions are:

* `x-graviteeio-soap-envelope`: Contains the SOAP envelope
* `x-graviteeio-soap-action`: Contains the SOAP action

For more information, see the REST to SOAP policy in the [policy reference](../policies/policy-reference/README.md).
{% endtab %}

{% tab title="Mock" %}
For each operation, a mock policy is configured, based on the `example` field if it exists, or by generating a random value for the type of attribute to mock.\
\
For more information, see the Mock policy in the [policy reference](../policies/policy-reference/README.md).
{% endtab %}

{% tab title="Request Validation" %}
For each operation, `NOT` `NULL` rules are created with query parameters and headers.\
\
For more information, see the Request Validation policy in the [policy reference](../policies/policy-reference/README.md).
{% endtab %}

{% tab title="XML Validation" %}
For each operation, if a `application/xml` request body exists, then a XSD schema is computed from this body to configure an XML Validation policy.

For more information, see the XML Validation policy in the [policy reference](../policies/policy-reference/README.md).
{% endtab %}
{% endtabs %}
