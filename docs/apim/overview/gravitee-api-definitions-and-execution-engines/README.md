---
layout:
  title:
    visible: true
  description:
    visible: false
  tableOfContents:
    visible: true
  outline:
    visible: true
  pagination:
    visible: true
---

# Gravitee API Definitions and Execution Engines

## Overview

A Gravitee API definition is very similar to an API specification (e.g., OpenAPI, AsyncAPI) except it is a specification for your Gravitee API Management (APIM) Gateway_._ It’s a JSON representation of everything that the APIM Gateway needs to know for it to proxy, apply policies to, create plans for, etc., your APIs and their traffic.

To execute your Gateway APIs and policy flows, the Gateway needs a runtime environment, or engine. This is generally referred to as the execution engine. As of APIM 4.0, there is support for both the v2 and v4 Gravitee API definitions, where v2 API definitions run on the legacy execution engine and v4 API definitions run on the reactive execution engine.

{% hint style="warning" %}
You can run v2 Gateway APIs in [emulation mode](./#v2-gateway-api-emulation-mode), which emulates some of the execution flow improvements of the reactive execution engine.&#x20;
{% endhint %}

The [v2 API Creation Wizard ](../../guides/create-apis/how-to/v2-api-creation-wizard.md)creates v2 Gateway APIs compatible with the legacy execution engine that can be augmented with flows designed in the [v2 Policy Studio](../../guides/policy-design/v2-api-policy-design-studio.md). The [v4 API Creation Wizard](../../guides/create-apis/how-to/v4-api-creation-wizard.md) creates v4 APIs compatible with the reactive execution engine that can be augmented with flows designed in the [v4 Policy Studio](../../guides/policy-design/v4-api-policy-design-studio.md).

This guide is a deep dive into the differences between the new reactive execution engine and the existing legacy execution engine. Additionally, guidance is provided on managing changes in system behavior when switching to the reactive policy execution engine or enabling compatibility mode with a v2 API. The information is grouped by functional area.

## lan selection

For both execution engines, the plan selection workflow parses all the published plans in the following order: JWT, OAuth2, API Key, Keyless. Each plan type has the following rules:

* JWT
  * Retrieve JWT from `Authorization` Header or query parameters
  * Ignore empty `Authorization` Header or any type other than Bearer
  * While it was previously ignored, **an empty Bearer token is now considered invalid**
* OAuth2
  * Retrieve OAuth2 from `Authorization` Header or query parameters
  * Ignore empty `Authorization` Header or any type other than Bearer
  * While it was previously ignored, **an empty Bearer token is now considered invalid**
* API Key
  * Retrieve the API key from the request header or query parameters (default header: `X-Gravitee-Api-Key` and default query parameter: `api-key`)
  * While it was previously ignored, **an empty API key is now considered invalid**
* Keyless
  * Will ignore any type of security (API key, Bearer token, etc.)
  * **If another plan has detected a security token, valid or invalid, all flows assigned to the Keyless plan will be ignored.** Therefore, if an API has multiple plans of different types and the incoming request contains a token or an API key that does not match any of the existing plans, then the Keyless plan will not be activated and the user will receive a generic `401` response without any details.

The parsed plan is selected for execution if all the following conditions are met:

* The request contains a token corresponding to the plan type (e.g., `X-Gravitee-Api-Key` header for API Key plans).
* The plan condition rule is valid or not set.
* There is an active subscription matching the incoming request.

{% hint style="warning" %}
There is an exception for OAuth2 plans executed on the legacy engine as detailed in the next section.
{% endhint %}

### Legacy execution engine behavior

With the legacy execution engine, the OAuth2 plan is selected even if the incoming request does not match a subscription.

No JWT token introspection is done during OAuth2 plan selection.

If there are multiple OAuth2 plans, that could lead to the selection of the wrong plan.

### Reactive execution engine improvements

With the reactive execution engine, the Oauth2 plan is _not_ selected if the incoming request does not match a subscription.

During the OAuth2 plan selection, a token introspection is completed to retrieve the `client_id` which allows searching for a subscription.

If there are performance concerns, a cache system is available to avoid completing the same token introspection multiple times. Where possible, it is recommended to use selection rules if there are multiple OAuth2 plans to avoid any unnecessary token introspection.
