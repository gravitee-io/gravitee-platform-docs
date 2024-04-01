---
description: This page discusses improvements to plan selection
---

# Plan selection

## Overview

For both execution engines, the plan selection workflow parses all published plans in the following order: JWT, OAuth2, API Key, Keyless. Each plan type has specific rules.

<details>

<summary>JWT</summary>

* Retrieve JWT from `Authorization` Header or query parameters
* Ignore empty `Authorization` Header or any type other than Bearer
* While it was previously ignored, **an empty Bearer token is now considered invalid**

</details>

<details>

<summary>OAuth2</summary>

* Retrieve OAuth2 from `Authorization` Header or query parameters
* Ignore empty `Authorization` Header or any type other than Bearer
* While it was previously ignored, **an empty Bearer token is now considered invalid**

</details>

<details>

<summary>API Key</summary>

* Retrieve the API key from the request header or query parameters (default header: `X-Gravitee-Api-Key` and default query parameter: `api-key`)
* While it was previously ignored, **an empty API key is now considered invalid**

</details>

<details>

<summary>Keyless</summary>

* Will ignore any type of security (API key, Bearer token, etc.)
* **If another plan has detected a security token, valid or invalid, all flows assigned to the Keyless plan will be ignored.** Therefore, if an API has multiple plans of different types and the incoming request contains a token or an API key that does not match any of the existing plans, then the Keyless plan will not be activated and the user will receive a generic `401` response without any details.

</details>

The parsed plan is selected for execution if all the following conditions are met:

* The request contains a token corresponding to the plan type (e.g., `X-Gravitee-Api-Key` header for API Key plans)
* The plan condition rule is valid or not set
* There is an active subscription matching the incoming request

{% hint style="warning" %}
There is an exception for OAuth2 plans executed on the legacy engine as detailed in the next section.
{% endhint %}

## Legacy execution engine behavior

With the legacy execution engine, the OAuth2 plan is selected even if the incoming request does not match a subscription.

No JWT token introspection is done during OAuth2 plan selection.

Multiple OAuth2 plans can lead to the selection of the wrong plan.

## Reactive execution engine improvements

When using the reactive execution engine, the OAuth2 plan is _not_ selected if the incoming request does not match a subscription.

During OAuth2 plan selection, a token introspection is completed to retrieve the `client_id`, which allows searching for a subscription.

If there are performance concerns, a cache system is available to avoid completing the same token introspection multiple times. Where possible, it is recommended to use selection rules if there are multiple OAuth2 plans to avoid any unnecessary token introspection.
