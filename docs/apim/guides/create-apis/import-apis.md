---
description: This article is for x,y, and z
---

# Import APIs

## Introduction

{% @arcade/embed flowId="h1mdR0FKFbW9OS2CB0mQ" url="https://app.arcade.software/share/h1mdR0FKFbW9OS2CB0mQ" %}

Gravitee supports importing APIs as:

* Files (json, yml, yaml, wsdl, xml)
* Swagger/OpenAPI spec (URL)
* API definition (URL)
* WSDL (URL)

###

## Import ypur API

To import your API, head to the **APIs** page and select **+ Add API.** You'll be presented with three options for creating APIs. Select **Import an existing API.**&#x20;

<figure><img src="../../.gitbook/assets/Import API first steps.gif" alt=""><figcaption></figcaption></figure>

You'll be presented with the following options:

* **Upload a file:** this allows you to import an API as an uploaded file. You can import yml, yaml, json, wsdl, and xml files. Once you've uploaded your file, select **Import.** If the import runs smoothly, you'll be brought to the newly created APIs details page.&#x20;
* **Swagger / OpenAPI:** if you choose this option, you'll need to provide a Swagger descriptor URL and choose your confoguration options. These include:
  * Create documentation: This will overwrite documentation if there is only one existing, or create it if it does not exist yet.
  * Create the path mapping for analytics: This will overwrite all the path-mappings.
  * Create policies on paths: This will overwrite all the policies. Policies that you can create upon import include:
    * JSON validation policy
    * Mock Policy
    * REST to SOAP transformer
    * Validate REquest Policy
    * XML Validation policy
* **API defintion:**
* **WSDL:**
