---
description: Configuration and usage guide for types of plans.
---

# Types of plans

Plans provide a service and access layer on top of your API that specifies access limits, subscription validation modes, and other configurations to tailor it to an application. Here are the plans that you can apply to your APIs:

<details>

<summary>Keyless</summary>

#### Introduction

A Keyless (public) plan does not require authentication and allows public access to an API. By default, keyless plans offer no security and are most useful for quickly and easily exposing your API to external users.

#### Configuration

A Keyless plan does not require configuration other than general plan settings and restrictions.

Due to not requiring a subscription and the lack of a consumer identifier token, Keyless consumers are set as `unknown application` in the API analytics section.

You can configure basic authentication for Keyless plans by associating a [Basic Authentication policy](../policy-studio/policies-for-your-apis/a-c/basic-authentication.md) that uses either an LDAP or inline resource.

</details>

<details>

<summary>API Key</summary>

#### Introduction

The API key authentication type enforces verification of API keys during request processing, allowing only applications with approved API keys to access an API. This plan type ensures that API keys are valid, i.e., not revoked or expired, and are approved to consume the specific resources associated with the API.

#### Configuration

An API Key plan offers only basic security, acting more like a unique identifier than a security token.

<img src="broken-reference" alt="API Key configuration" data-size="original">

* **Propagate API Key to upstream API:** Toggle ON to ensure the request to the backend API includes the API key header sent by the API consumer. This is useful for backend APIs that already have integrated API key authentication.
* **Additional selection rule:** Allows you to use Gravitee Expression Language (EL) to filter plans of the same type by contextual data (request headers, tokens, attributes, etc.). For example, if there are multiple API key plans, you can set different selection rules on each plan to determine which plan handles each request.

#### **API Key generation**

By default, API keys are randomly generated for each subscription, but Gravitee also offers custom API key generation and shared API key generation. Both of these settings can be enabled at the environment level:

1. Log in to your APIM Console
2. Select Settings from the left nav
3.  Select Settings from the inner left nav:

    <figure><img src="broken-reference" alt=""><figcaption><p>API key generation settings</p></figcaption></figure>

**Custom API key**

You can specify a custom API key for an API Key plan. This is particularly useful when you want to silently migrate to APIM and have a pre-defined API key. When prompted, you can choose to provide your custom API key or let APIM generate one for you by leaving the field empty.

The custom API key must have between 8 and 64 characters and be URL-compliant. `^ # % @ \ / ; = ? | ~ ,`and the 'space' character are invalid.

You can provide a custom API key when:

*   Creating a subscription

    <figure><img src="broken-reference" alt=""><figcaption><p>Manually create a subscription</p></figcaption></figure>
* Accepting a subscription
*   Renewing a subscription

    <figure><img src="broken-reference" alt=""><figcaption><p>Renew a subscription</p></figcaption></figure>

**Shared API key**

The shared API key mode allows consumers to reuse the same API key across all API subscriptions of an application. On their application's second subscription, the consumer is asked to choose between reusing their key across all subscriptions or generating one different API key for each subscription (default). This is known as the application API key type, which cannot be modified.

**Shared API key limitations**

API keys can only be shared across API Key plans that belong to distinct Gateway APIs. If you attempt to subscribe to two API Key plans on the same Gateway API, no prompt will be made to choose the application API key type and the default mode will be used automatically.

![Subscribing in the Developer Portal](https://docs.gravitee.io/images/apim/3.x/api-publisher-guide/plans-subscriptions/shared-api-key-2-portal.png) ![Subscribing in the APIM Console](broken-reference)

To select the API key type, the shared API key mode must be [enabled](subscriptions.md#api-key-plans) before creating an application. To enable this option, create a new application and subscribe to two API Key plans.

If shared API key mode is disabled, applications that have already been configured to use a shared key will continue to do so, but consumers will no longer be asked to choose between modes on their second subscription.

**Modifying shared API keys**

A shared API key may be used to call APIs that are owned by other API publishers. Consequently:

* Shared API keys cannot be edited from an API publisher's subscriptions
*   API publishers can read shared API keys, but cannot renew or revoke them

    <figure><img src="broken-reference" alt=""><figcaption><p>Shared API key administration limitations</p></figcaption></figure>
*   Shared API keys can only be renewed/revoked by the application owner, from the subscription view of their APIM Console or Developer Portal

    <figure><img src="broken-reference" alt=""><figcaption><p>Manage shared API keys in APIM Console</p></figcaption></figure>

    <figure><img src="broken-reference" alt=""><figcaption><p>Manage shared API keys in the Developer Portal</p></figcaption></figure>

</details>

<details>

<summary>OAuth2</summary>

#### Introduction

OAuth 2.0 is an open standard that applications can use to provide client applications with secure, delegated access. OAuth 2.0 works over HTTPS and authorizes devices, APIs, servers, and applications via access tokens instead of credentials.

The OAuth2 authentication type checks access token validity during request processing using token introspection. If the access token is valid, the request is allowed to proceed. If not, the process stops and rejects the request.

#### Configuration

To configure an OAuth2 plan, you must first create an [OAuth2 client resource](../resources/oauth2.md) that represents your OAuth 2.0 authorization server.

Configuring an OAuth2 plan presents the following options:

<img src="broken-reference" alt="OAuth2 plan configuration" data-size="original">

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

#### Subscription requirements

During the OAuth2 plan selection, a token introspection is completed to retrieve the `client_id` which allows searching for a subscription. Any applications wanting to subscribe to an OAuth2 plan must have an existing client with a valid `client_id` registered in the OAuth 2.0 authorization server. The `client_id` will be used to establish a connection between the OAuth 2.0 client and the APIM consumer application.

To mitigate performance concerns, a cache system is available to avoid completing the same token introspection multiple times. If there are multiple OAuth2 plans, it is recommended to use selection rules to avoid any unnecessary token introspection.

</details>

<details>

<summary>JWT</summary>

#### Introduction

A JSON Web Token (JWT) is an open method for representing claims securely between two parties. It is digitally signed using an HMAC shared key or RSA public/private key pair. The JWT authentication type ensures that a JWT issued by a third party is valid by verifying its signature and expiration date. Only applications with approved JWTs can access APIs associated with a JWT plan.

#### Configuration

APIM uses client IDs to recognize applications that have subscribed to a JWT plan. The inbound JWT payload must include the `client_id` claim to establish a connection between the JWT and the APIM application subscription.

A JWT plan presents the following configuration options:

<img src="broken-reference" alt="JWT plan configuration" data-size="original">

* **Signature:** Select the algorithm used to hash and encrypt your JWT
* **JWKS resolver:** Select a method to retrieve the JSON Web Key (JWK), which is often stored inside a JSON Web Key Set (JWKS) and required by the Gateway to validate the signature of the JWT:
  * **GIVEN\_KEY**: Provide a signature key as a resolver parameter according to the signature algorithm (`ssh-rsa`, `pem`, `crt` or `public-key` format
  *   **GATEWAY\_KEYS:** Search for public keys set in the API Gateway `gravitee.yml` configuration that match the authorization server `iss` (issuer) and `kid` (key ID) claims of the incoming JWT

      \{% code title="gravitee.yml" %\}

      ```yaml
      jwt:
        issuer:
          my.authorization.server:
            default: ssh-rsa myValidationKey anEmail@domain.com
            kid-2016: ssh-rsa myCurrentValidationKey anEmail@domain.com
      ```

      \{% endcode %\} \* **JWKS\_URL**: Provide a URL ending with `/.well-known/jwks.json` from which the Gateway can retrieve the JWKS
* **Use system proxy:** When using **JWKS\_URL**, optionally make the HTTP call through a system-wide proxy configured in `gravitee.yml`
*   **Extract JWT Claims:** Allow claims to be accessed in the `jwt.claims` context attribute during request/response via Gravitee Expression Language (EL), e.g., extract the issuer claim from the JWT:

    ```
    {#context.attributes['jwt.claims']['iss']}
    ```
* **Propagate Authorization header:** Propagate the header containing the JWT token to the backend APIs
* **User claim:** Set the payload claim where the user can be extracted. The default `sub` value is standard with JWTs.
* **Client ID claim:** Override the default claim where the client ID can be extracted. By default, the Gateway checks the `azp` claim, then the `aud` claim, and finally the `client_id` claim.
* **Ignore missing CNF:** Ignores CNF validation if the token doesn't contain any CNF information
* **Enable certificate bound thumbprint validation:** Validates the certificate thumbprint extracted from the `access_token` against the one provided by the client
* **Extract client certificate from headers:** Extracts the client certificate from the request header (provided in **Header name** field). Necessary when the mTLS connection is handled by a proxy.
* **Additional selection rule:** Allows you to use the EL to filter by contextual data (request headers, tokens, attributes, etc.) for plans of the same type (e.g., for two JWT plans, you can set different selection rules on each plan to determine which plan handles each request)

Once JWT configuration is complete and the plan is created and published, your API will be JWT-secured and subscribed consumers must call the API with an `Authorization: Bearer your-JWT` HTTP header.

</details>

<details>

<summary>Push</summary>

#### Introduction

A Push plan is used when an API contains an entrypoint that sends message payloads to API consumers (e.g., Webhook). This type of plan is unique in that the security configuration is defined by the API consumer, in the subscription request created in the Developer Portal. For example, when subscribing to a Webhook entrypoint, the API consumer specifies the target URL and authentication for the Gateway to use when sending messages.

Push plans do not apply to SSE entrypoints. Although messages are pushed from the server, the client application initiates message consumption.

#### Configuration

Push plans have the same configuration options as [Keyless plans](types-of-plans.md#keyless) in APIM. The bulk of the configuration for a Push plan is set by the API consumer in the Developer Portal, and the content of the configuration varies by entrypoint type.

Gravitee currently supports Push plans for Webhook entrypoints

</details>
