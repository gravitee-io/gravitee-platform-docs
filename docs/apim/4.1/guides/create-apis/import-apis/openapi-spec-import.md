---
description: An overview about OpenAPI Spec Import.
---

# OpenAPI Spec Import

## Overview

A powerful APIM feature is the ability to import an OpenAPI specification to create an API. When you import an existing specification, you do not have to manually populate all of the required fields.

To import an API from OpenAPI:

* If the OpenAPI specification is a file, select **IMPORT FILE** and browse your file system

<figure><img src="https://docs.gravitee.io/images/apim/3.x/api-publisher-guide/manage-apis/graviteeio-import-openapi-file.png" alt=""><figcaption></figcaption></figure>

* If the OpenAPI specification is a link, select **IMPORT FROM LINK**, choose **Swagger / OpenAPI**, and enter the definition URL

<figure><img src="https://docs.gravitee.io/images/apim/3.x/api-publisher-guide/manage-apis/graviteeio-import-openapi-link.png" alt=""><figcaption></figcaption></figure>

## **Context-path resolution**

<table><thead><tr><th>Spec version</th><th>Definition</th><th>Example</th><th>Context-path</th></tr></thead><tbody><tr><td>Swagger (V2)</td><td><code>basePath</code> field, if it exists.</td><td><pre><code>{
</code></pre></td><td></td></tr><tr><td>"swagger": "2.0",</td><td></td><td></td><td></td></tr><tr><td>"info": {</td><td></td><td></td><td></td></tr></tbody></table>

```
"description": "...",
"version": "1.0.5",
"title": "Swagger Petstore"
```

}, "host": "petstore.swagger.io", "basePath": "/v2", ... } | /v2 | | If not, lowercase trimmed `info.title`. |

```
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

\| /swaggerpetstore | | | OpenAPI (V3) |

Path of the first `servers.url`, if it exists, without "/".

|

```
openapi: "3.0.0"
info:
version: 1.0.0
title: Swagger Petstore
license:
name: MIT
servers:

url: http://petstore.swagger.io/v1
paths:
...
```

\| /v1 | | If not, lowercase trimmed `info.title`. |

```
openapi: "3.0.0"
info:
version: 1.0.0
title: Swagger Petstore
license:
name: MIT
servers:
url: http://petstore.swagger.io/
paths:
...
```

\| /swaggerpetstore | |

## Vendor Extensions

You can use a vendor extension to add more information about your API to an OpenAPI specification.

{% hint style="info" %}
To learn how some policies can be defined in the OpenAPI spec as a vendor extension, see [Policies on path](openapi-spec-import.md#policies-on-path).
{% endhint %}

To use a vendor extension, add the `x-graviteeio-definition` field at the root of the specification. The value of this field is an `object` that follows this [JSON Schema](https://raw.githubusercontent.com/gravitee-io/gravitee-api-management/master/gravitee-apim-rest-api/gravitee-apim-rest-api-service/src/main/resources/schema/xGraviteeIODefinition.json).

Consider that:

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

Example configuration:

<pre class="language-yaml"><code class="lang-yaml"><strong>openapi: "3.0.0"
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

## Policies on path

When importing an OpenAPI definition, you can select the option **Create policies on path** to specify that all routes declared in the OpenAPI specification will be automatically created in APIM. To verify, navigate to the policy management view.

<figure><img src="https://docs.gravitee.io/images/apim/3.x/api-publisher-guide/manage-apis/graviteeio-import-openapi-policies-path.png" alt=""><figcaption></figcaption></figure>

You can also choose to activate policies (below) that will be configured using the OpenAPI specification:

{% tabs %}
{% tab title="JSON Validation" %}
For each operation, if an `application/json` request body exists, a JSON schema is computed from this body to configure a JSON Validation policy.\
\
For more information, see the [JSON Validation policy](../../../reference/policy-reference/json-validation.md) reference.
{% endtab %}

{% tab title="REST to SOAP" %}
For each operation, if the definition contains specific vendor extensions, a REST to SOAP policy can be configured. These extensions are:

* `x-graviteeio-soap-envelope`: Contains the SOAP envelope
* `x-graviteeio-soap-action`: Contains the SOAP action

For more information, see the [REST to SOAP policy](../../../reference/policy-reference/rest-to-soap.md) reference.
{% endtab %}

{% tab title="Mock" %}
For each operation, a mock policy is configured, based on the `example` field if it exists, or by generating a random value for the type of attribute to mock.\
\
For more information, see the [Mock policy](../../../reference/policy-reference/mock.md) reference.
{% endtab %}

{% tab title="Request Validation" %}
For each operation, `NOT` `NULL` rules are created with query parameters and headers.\
\
For more information, see the [Request Validation policy](../../../reference/policy-reference/request-validation.md) reference.
{% endtab %}

{% tab title="XML Validation" %}
For each operation, if a `application/xml` request body exists, then a XSD schema is computed from this body to configure an XML Validation policy.

For more information, see the [XML Validation policy](../../../reference/policy-reference/xml-validation.md) reference.
{% endtab %}
{% endtabs %}
