---
description: This page details the go-forward strategy for supporting v1 APIs in APIM
---

# Support for v1 APIs

This page details Gravitee’s strategy for supporting v1 APIs in API Management (APIM). 

{% hint style="info" %}
Gravitee deprecated v1 APIs in version 4.4.0 of APIM. From version 4.12.0, there is no support for v1 APIs. 
{% endhint %}

## Create and import v1 APIs

If you run version 3.20 or later of APIM, you cannot create v1 APIs.

If you run version 3.20 of APIM, you can import your v1 API, and then upgrade the API to v2. If you run version 4.0.0 or later, you cannot import v1 APIs.

## Upgrade to APIM 4.x.x with v1 APIs

Depending on which version of Gravitee that you upgrade to, you have to complete different actions for your v1 APIs. Follow the steps for your upgrade:
* [Upgrade to versions 4.0.0 to 4.11.x](link)

### Upgrade to versions 4.0.0 to 4.11.x.

When you upgrade an existing APIM environment to version 4.0.0 up to 4.11.x, here is how your environment interacts with v1 APIs:

* v1 APIs continue to run on the Gateway.
* Client applications can still call the v1 APIs that you deployed.
* v1 APIs appear as read-only. Gravitee prompts you to upgrade the API to a v2 definition.
* If you run version 4.0.0 of APIM, you can create, publish, deprecate, and close plans for v1 APIs.

### Upgrade to version 4.12.x

From 4.12.0 of APIM, Gravitee no longer supports v1 APIs. Before you upgrade to version 4.12.0, ensure that you migrate all v1 APIs to at least a v2 API definition. If you upgrade to 4.12.0 with a v1 API, here is how Gravitee interacts with v1 APIs

* Gravitee removes the v1 API code from the APIM codebase.
* The APIM Gateway ignores v1 APIs.
* The Management API automatically stops running v1 APIs.
* In the UI, v1 APIs display an error indicating an invalid version.
