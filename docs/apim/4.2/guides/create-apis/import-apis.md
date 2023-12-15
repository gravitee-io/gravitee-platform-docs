---
description: Learn how to import APIs onto your Gravitee Gateway
---

# Import APIs

## Introduction

{% @arcade/embed flowId="h1mdR0FKFbW9OS2CB0mQ" url="https://app.arcade.software/share/h1mdR0FKFbW9OS2CB0mQ" %}

Gravitee supports importing APIs as:

* Files (YML, YAML, JSON, WSDL, XML)
* Swagger/OpenAPI spec (URL)
* API definition (URL)
* WSDL (URL)

{% hint style="info" %}
As of Gravitee 4.1, APIs using the v2 and v4 API definitions can be imported as JSON files.
{% endhint %}

## Import your API

To import your API, head to the **APIs** page and select **+ Add API.** You'll be presented with three options for creating APIs. Select **Import an existing API**.

You'll be presented with the following options:

* **Upload a file:** This allows you to import an API as an uploaded file. You can import YML, YAML, JSON, WSDL, and XML files. Once you've uploaded your file, select **Import.** If the import runs smoothly, you'll be brought to the newly created API's details page.
* **Swagger / OpenAPI:** If you choose this option, you'll need to provide a Swagger descriptor URL and choose your configuration options. These include:
  * Create documentation: This will overwrite documentation if there is only one existing, or create it if it does not exist yet.
  * Create the path mapping for analytics: This will overwrite all the path-mappings.
  * Create policies on paths: This will overwrite all the policies. Policies that you can create upon import include:
    * **JSON Validation policy**
    * **Mock policy**
    * **REST to SOAP transformer**
    * **Validate Request policy**
    * **XML Validation policy**

{% hint style="info" %}
**Vendor extensions**

You can use a vendor extension to add more information to OpenAPI specifications about your API. To do this, you need to add the `x-graviteeio-definition` field at the root of the specification. The value of this field is an `object` that follows this [JSON Schem](https://raw.githubusercontent.com/gravitee-io/gravitee-api-management/master/gravitee-apim-rest-api/gravitee-apim-rest-api-service/src/main/resources/schema/xGraviteeIODefinition.json)a:

Please keep the following in mind:

* Categories must contain either a key or an ID.
* Only existing categories are imported.
* Import will fail if virtualHosts are already in use by other APIs.
* If set, virtualHosts will override contextPath.
* Groups must contain group names. Only existing groups are imported.
* metadata.format is case-sensitive. Possible values are:
  * STRING
  * NUMERIC
  * BOOLEAN
  * DATE
  * MAIL
  * URL
* Picture only accepts Data-URI format. Please see the example below:

```
openapi: "3.0.0"
info:
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
```
{% endhint %}

* **API definition:** If you choose this option, you'll need to include a URL that links to your API definition.
* **WSDL:** If you choose this option, you'll need to provide a WSDL descriptor URL. Like the Swagger/OpenAPI option, you'll be able to configure the following prior to import:
  * Create documentation: This will overwrite documentation if there is only one existing, or create it if it does not exist yet.
  * Create the path mapping for analytics: This will overwrite all the path-mappings.
  * Create policies on paths: This will overwrite all the policies. Policies that you can create upon import include:
    * **JSON Validation policy**
    * **Mock policy**
    * **REST to SOAP transformer**
    * **Validate Request policy**
    * **XML Validation policy**

{% hint style="success" %}
**Success!**

Once you've imported your API, it will be created as a private API, and you will be brought to that APIs menu and details page. From here, you can further [configure your API](../api-configuration/), [design policies for that API](../policy-design/), [expose that API](../api-exposure-plans-applications-and-subscriptions/), etc.
{% endhint %}
