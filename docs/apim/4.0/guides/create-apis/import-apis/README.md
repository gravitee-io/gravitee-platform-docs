---
description: Learn how to import APIs onto your Gravitee Gateway
---

# Import APIs

## Introduction

{% @arcade/embed flowId="h1mdR0FKFbW9OS2CB0mQ" url="https://app.arcade.software/share/h1mdR0FKFbW9OS2CB0mQ" %}

Gravitee supports importing APIs as:

* Files (json, yml, yaml, wsdl, xml)
* Swagger/OpenAPI spec (URL)
* API definition (URL)
* WSDL (URL)

{% hint style="info" %}
Product limitation

There is an existing limitation around API import. As of Gravitee 4.0, APIs using the v4 API definition cannot be imported.
{% endhint %}

## Import your API

To import your API, head to the **APIs** page and select **+ Add API.** You'll be presented with three options for creating APIs. Select **Import an existing API.**

You'll be presented with the following options:

* **Upload a file:** This allows you to import an API as an uploaded file. You can import yml, yaml, json, wsdl, and xml files. Once you've uploaded your file, select **Import.** If the import runs smoothly, you'll be brought to the newly created APIs details page.
* **Swagger / OpenAPI:** If you choose this option, you'll need to provide a Swagger descriptor URL and choose your configuration options. These include:
  * Create documentation: This will overwrite documentation if there is only one existing, or create it if it does not exist yet.
  * Create the path mapping for analytics: This will overwrite all the path-mappings.
  * Create policies on paths: This will overwrite all the policies. Policies that you can create upon import include:
    * **JSON Validation policy**
    * **Mock policy**
    * **REST to SOAP transformer**
    * **Validate Request policy**
    * **XML Validation policy**
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

Once you've imported your API, it will be created as a private API, and you will be brought to that APIs menu and details page. From here, you can further [configure your API](../../api-configuration/README.md), [design policies for that API](../../policy-studio/README.md), [expose that API](../../api-exposure-plans-applications-and-subscriptions/README.md), etc.
{% endhint %}
