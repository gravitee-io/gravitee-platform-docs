---
description: This page describes the OAuth2 authentication type
---

# OAuth2

## Introduction

OAuth 2.0 is an open standard that applications can use to provide client applications with secure, delegated access. OAuth 2.0 works over HTTPS and authorizes devices, APIs, servers, and applications via access tokens instead of credentials.

The OAuth2 authentication type checks access token validity during request processing using token introspection. If the access token is valid, the request is allowed to proceed. If not, the process stops and rejects the request.

## Configuration

{% hint style="warning" %}
To configure an OAuth2 plan, you must first create an [OAuth2 client resource](../../api-configuration/resources.md) that represents your OAuth 2.0 authorization server.
{% endhint %}

Configuring an OAuth2 plan presents the following options:

<figure><img src="../../../../../../.gitbook/assets/plan_oauth2 configuration (1).png" alt=""><figcaption><p>OAuth2 plan configuration</p></figcaption></figure>

* **OAuth2 resource:** Enter the name of the OAuth2 resource to use as the authorization server
* **Cache resource:** Optionally enter the name of the cache resource to store responses from the authorization server
*   **Extract OAuth2 payload:** Allows the OAuth2 payload to be accessed from the `oauth.payload` context attribute via Gravitee Expression Language (EL) during request/response, e.g. using:

    ```bash
    {#context.attributes['oauth.payload']}
    ```
* **Check scopes:** An authorization server can grant access tokens with a [scopes](https://tools.ietf.org/html/rfc6749#section-3.3) parameter, which the Gateway will check against the provided **Required scopes** to determine if the client application is allowed to access the API
* **Mode strict:** When disabled, the Gateway will validate the API call if the access token contains at least one scope from the **Required scopes** list. When enabled, strict mode requires the access token to contain all scopes from the **Required scopes** list.
* **Permit authorization header to the target endpoints:** Propagate the header containing the access token to the backend APIs
* **Additional selection rule:** Allows you to use the EL to filter by contextual data (request headers, tokens, attributes, etc.) for plans of the same type (e.g., for two OAuth2 plans, you can set different selection rules on each plan to determine which plan handles each request)

Once OAuth2 configuration is complete and the plan is created and published, your API will be OAuth2-secured and subscribed consumers must call the API with an `Authorization Bearer :token:` HTTP header to access the API resources.

## Subscription requirements

During the OAuth2 plan selection, a token introspection is completed to retrieve the `client_id` which allows searching for a subscription. Any applications wanting to subscribe to an OAuth2 plan must have an existing client with a valid `client_id` registered in the OAuth 2.0 authorization server. The `client_id` will be used to establish a connection between the OAuth 2.0 client and the APIM consumer application.

{% hint style="info" %}
To mitigate performance concerns, a cache system is available to avoid completing the same token introspection multiple times. If there are multiple OAuth2 plans, it is recommended to use selection rules to avoid any unnecessary token introspection.
{% endhint %}
