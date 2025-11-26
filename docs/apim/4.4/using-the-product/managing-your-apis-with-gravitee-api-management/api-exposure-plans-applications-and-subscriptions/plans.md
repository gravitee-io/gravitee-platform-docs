---
description: Configuration guide for Applying Plans to your APIs.
---

# Applying Plans to your APIs

## Introduction

To expose your API to internal or external consumers, it must have at least one plan. A plan provides a service and access layer on top of your API that specifies access limits, subscription validation modes, and other configurations to tailor it to an application. Example access scenarios APIM can manage with plans include:

* Read-only access and limited request traffic for potential customers to discover and try out your APIs
* Premium access with public resources and access limits for your partners
* Unlimited access to your internal enterprise applications

<div align="center"><figure><img src="../../../.gitbook/assets/plan-diagram.png" alt="" width="375"><figcaption><p>High-level plan diagram</p></figcaption></figure></div>

Each plan must include at least one security type by which subscribers can be authenticated. A security type is a policy integrated directly into a plan. Once a plan is created, the security type can not be changed. However, you can add additional security at the API or plan level with policies.

{% hint style="info" %}
For more information about the types of plans that you can apply to your APIs, see [types-of-plans.md](types-of-plans.md "mention").
{% endhint %}

The sections below describe:

* [How to create a plan](plans.md#create-a-plan)
* [How to publish a plan](plans.md#publish-a-plan)
* [How plans are selected](plans.md#plan-selection-rules)

## Create a plan

To create a plan:

1. Log in to your APIM Console
2. Select **APIs** from the left nav
3. Select your API
4. Select **Consumers** from the inner left nav
5.  Under the **Plans** header tab, click **+ Add new plan** and select your plan security type:

    <figure><img src="../../../.gitbook/assets/plan_select security type.png" alt=""><figcaption><p>Add a new plan</p></figcaption></figure>
6.  Configure the general plan settings:

    <figure><img src="../../../.gitbook/assets/plan_general.png" alt=""><figcaption><p>Configure general plan settings</p></figcaption></figure>

    * **Name:** Enter a name for your plan
    * **Description:** Enter a description of your plan
    * **Characteristics:** Define labels used to tag your plan
    * **Page of General Conditions:** Select a published [Documentation](../configuring-apis-with-the-gravitee-api-management/v4-api-configuration/documentation.md) page whose terms must be accepted by the user to finalize the subscription process
    * Toggle **Auto validate subscription** ON to accept all subscriptions to a plan without the API publisher's approval
    * Toggle **Consumer must provide a comment when subscribing to the plan** ON to require an explanation for the subscription request, with the option to leave a **Custom message to display to consumer**
    * **Sharding tags:** Selectively deploy the plan to particular APIs using available [sharding tags](../../using-the-gravitee-api-management-components/general-configuration/sharding-tags.md)
    * **Groups excluded:** Prevent specified [user groups](../../administration/user-management-and-permissions.md) from accessing your plan
7. Click **Next**
8.  Define the security configuration details appropriate to and required by your selected security type, e.g., OAuth2. See [**OAuth2**,](../policy-studio/policies-for-you-apis/l-p/oauth2/README.md) [**JWT**](../../most-common-use-cases/configure-jwt-security-with-apim.md), [**API Key**](../policy-studio/policies-for-you-apis/a-c/api-key.md), [**Keyless (public)**](../policy-studio/policies-for-you-apis/i-k/keyless.md), or [**Push plan**](plans.md#push) for more information.

    <figure><img src="../../../.gitbook/assets/plan_oauth2.png" alt=""><figcaption><p>OAuth2 configuration</p></figcaption></figure>
9.  Select any plan restrictions:

    <figure><img src="../../../.gitbook/assets/plan_restrictions.png" alt=""><figcaption><p>Select plan restrictions</p></figcaption></figure>

    * **Rate limiting:** Intended to help avoid unmanageable spikes in traffic by limiting the number of requests an application can make in a given time period.
    * **Quota:** Limits the number of requests an application can make in a given time period. Generally used to tier access to APIs based on subscription level.
    * **Resource Filtering:** Limits access to API resources according to whitelist and/or blacklist rules.
10. Click **Create**

## Plan stages

A plan can exist in one of four stages: **STAGING**, **PUBLISHED**, **DEPRECATED**, and **CLOSED**:

{% tabs %}
{% tab title="STAGING" %}
This is the draft mode of a plan, where it can be configured but won’t be accessible to users.
{% endtab %}

{% tab title="PUBLISHED" %}
API consumers can view a published plan on the Developer Portal. Once subscribed, they can use it to consume the API. A published plan can still be edited.
{% endtab %}

{% tab title="DEPRECATED" %}
A deprecated plan won’t be available on the Developer Portal and API consumers won’t be able to subscribe to it. This cannot be undone. Existing subscriptions are not impacted, giving current API consumers time to migrate without breaking their application.
{% endtab %}

{% tab title="CLOSED" %}
Once a plan is closed, all associated subscriptions are closed. API consumers subscribed to this plan won’t be able to use the API. This cannot be undone.
{% endtab %}
{% endtabs %}

Depending on the stage it's in, a plan can be edited, published, deprecated, or closed via the icons associated with it:

{% tabs %}
{% tab title="Edit" %}
To edit a plan, click on the pencil icon:

<figure><img src="../../../.gitbook/assets/plan_edit.png" alt=""><figcaption><p>Edit a plan</p></figcaption></figure>
{% endtab %}

{% tab title="Publish" %}
To publish a plan, click on the icon of a cloud with an arrow:

<figure><img src="../../../.gitbook/assets/plan_publish.png" alt=""><figcaption><p>Publish a plan</p></figcaption></figure>

Once a plan has been published, it must be redeployed.
{% endtab %}

{% tab title="Deprecate" %}
To deprecate a plan, click on the icon of a cloud with an 'x':

<figure><img src="../../../.gitbook/assets/plan_deprecate.png" alt=""><figcaption><p>Deprecate a plan</p></figcaption></figure>
{% endtab %}

{% tab title="Close" %}
To close a plan, click on the 'x' icon:

<figure><img src="../../../.gitbook/assets/plan_close.png" alt=""><figcaption><p>Close a plan</p></figcaption></figure>
{% endtab %}
{% endtabs %}

## Plan selection rules

APIM automatically routes each API request to the correct plan. The plan selection workflow parses all published plans in the following order: **JWT**, **OAuth2**, **API Key**, **Keyless**.

{% hint style="warning" %}
This workflow only applies to [v4 APIs and v2 APIs in emulation mode.](../../../overview/plugins-and-api-definitions-for-gravitee-api-management/gravitee-api-definitions-and-execution-engines/engine-comparisons.md#plan-selection)
{% endhint %}

The parsing rules for each plan type are detailed below:

{% tabs %}
{% tab title="JWT" %}
* Retrieve JWT from the `Authorization` header or query parameters
* Ignore an empty `Authorization` header or any type other than Bearer
* An empty Bearer token is considered invalid
{% endtab %}

{% tab title="OAuth2" %}
* Retrieve OAuth2 from the `Authorization` header or query parameters
* Ignore an empty `Authorization` header or any type other than Bearer
* An empty Bearer token is considered invalid
{% endtab %}

{% tab title="API Key" %}
* Retrieve the API key from the request header or query parameters (default header: `X-Gravitee-Api-Key`; default query parameter: `api-key`)
* An empty Bearer token is considered invalid
{% endtab %}

{% tab title="Keyless" %}
* Will ignore any type of security (API key, Bearer token, etc.)
* If another plan has detected a security token, valid or invalid, all flows assigned to the Keyless plan will be ignored
  * If an API has multiple plans of different types and the incoming request contains a token or an API key that does not match any of the existing plans, then the Keyless plan will not be activated and the user will receive a generic `401` response without any details
{% endtab %}
{% endtabs %}

The parsed plan is selected for execution if all the following conditions are met:

* The request contains a token corresponding to the plan type (e.g., an `X-Gravitee-Api-Key` header for an API Key plan)
* The plan condition rule is valid or not set
* There is an active subscription matching the incoming request

## Types of Plans

<details>

<summary>Keyless</summary>

**Introduction**

A Keyless (public) plan does not require authentication and allows public access to an API. By default, keyless plans offer no security and are most useful for quickly and easily exposing your API to external users.

**Configuration**

A Keyless plan does not require configuration other than general plan settings and restrictions.

Due to not requiring a subscription and the lack of a consumer identifier token, Keyless consumers are set as `unknown application` in the API analytics section.

You can configure basic authentication for Keyless plans by associating a [Basic Authentication policy](../policy-studio/policies-for-you-apis/a-c/basic-authentication.md) that uses either an LDAP or inline resource.

</details>

<details>

<summary>API Key</summary>

**Introduction**

The API key authentication type enforces verification of API keys during request processing, allowing only applications with approved API keys to access an API. This plan type ensures that API keys are valid, i.e., not revoked or expired, and are approved to consume the specific resources associated with the API.

**Configuration**

An API Key plan offers only basic security, acting more like a unique identifier than a security token.

<img src="../../../.gitbook/assets/plan_api key.png" alt="API Key configuration" data-size="original">

* **Propagate API Key to upstream API:** Toggle ON to ensure the request to the backend API includes the API key header sent by the API consumer. This is useful for backend APIs that already have integrated API key authentication.
* **Additional selection rule:** Allows you to use Gravitee Expression Language (EL) to filter plans of the same type by contextual data (request headers, tokens, attributes, etc.). For example, if there are multiple API key plans, you can set different selection rules on each plan to determine which plan handles each request.

**API Key generation**

By default, API keys are randomly generated for each subscription, but Gravitee also offers custom API key generation and shared API key generation. Both of these settings can be enabled at the environment level:

1. Log in to your APIM Console
2. Select Settings from the left nav
3.  Select Settings from the inner left nav:

    <figure><img src="../../../.gitbook/assets/plan_key generation.png" alt=""><figcaption><p>API key generation settings</p></figcaption></figure>

**Custom API key**

You can specify a custom API key for an API Key plan. This is particularly useful when you want to silently migrate to APIM and have a pre-defined API key. When prompted, you can choose to provide your custom API key or let APIM generate one for you by leaving the field empty.

The custom API key must have between 8 and 64 characters and be URL-compliant. `^ # % @ \ / ; = ? | ~ ,`and the 'space' character are invalid.

You can provide a custom API key when:

*   Creating a subscription

    <figure><img src="../../../.gitbook/assets/plan_create subscription.png" alt=""><figcaption><p>Manually create a subscription</p></figcaption></figure>
* Accepting a subscription
*   Renewing a subscription

    <figure><img src="../../../.gitbook/assets/plan_renew api key.png" alt=""><figcaption><p>Renew a subscription</p></figcaption></figure>

**Shared API key**

The shared API key mode allows consumers to reuse the same API key across all API subscriptions of an application. On their application's second subscription, the consumer is asked to choose between reusing their key across all subscriptions or generating one different API key for each subscription (default). This is known as the application API key type, which cannot be modified.

**Shared API key limitations**

API keys can only be shared across API Key plans that belong to distinct Gateway APIs. If you attempt to subscribe to two API Key plans on the same Gateway API, no prompt will be made to choose the application API key type and the default mode will be used automatically.

<figure><img src="https://docs.gravitee.io/images/apim/3.x/api-publisher-guide/plans-subscriptions/shared-api-key-2-portal.png" alt="Subscribing in the Developer Portal"><figcaption></figcaption></figure>

<figure><img src="../../../.gitbook/assets/Screen Shot 2023-03-16 at 11.44.51 AM (1).png" alt="Subscribing in the APIM Console"><figcaption></figcaption></figure>

To select the API key type, the shared API key mode must be [enabled](subscriptions.md#api-key-plans) before creating an application. To enable this option, create a new application and subscribe to two API Key plans.

If shared API key mode is disabled, applications that have already been configured to use a shared key will continue to do so, but consumers will no longer be asked to choose between modes on their second subscription.

**Modifying shared API keys**

A shared API key may be used to call APIs that are owned by other API publishers. Consequently:

* Shared API keys cannot be edited from an API publisher's subscriptions
*   API publishers can read shared API keys, but cannot renew or revoke them

    <figure><img src="../../../.gitbook/assets/shared-api-key-3.png" alt=""><figcaption><p>Shared API key administration limitations</p></figcaption></figure>
*   Shared API keys can only be renewed/revoked by the application owner, from the subscription view of their APIM Console or Developer Portal

    <figure><img src="../../../.gitbook/assets/shared-api-key-4.png" alt=""><figcaption><p>Manage shared API keys in APIM Console</p></figcaption></figure>

    <figure><img src="../../../.gitbook/assets/shared-api-key-4-portal.png" alt=""><figcaption><p>Manage shared API keys in the Developer Portal</p></figcaption></figure>

</details>

<details>

<summary>OAuth2</summary>

**Introduction**

OAuth 2.0 is an open standard that applications can use to provide client applications with secure, delegated access. OAuth 2.0 works over HTTPS and authorizes devices, APIs, servers, and applications via access tokens instead of credentials.

The OAuth2 authentication type checks access token validity during request processing using token introspection. If the access token is valid, the request is allowed to proceed. If not, the process stops and rejects the request.

**Configuration**

To configure an OAuth2 plan, you must first create an [OAuth2 client resource](../configuring-apis-with-the-gravitee-api-management/resources.md) that represents your OAuth 2.0 authorization server.

Configuring an OAuth2 plan presents the following options:

<img src="../../../.gitbook/assets/plan_oauth2 configuration.png" alt="OAuth2 plan configuration" data-size="original">

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

**Subscription requirements**

During the OAuth2 plan selection, a token introspection is completed to retrieve the `client_id` which allows searching for a subscription. Any applications wanting to subscribe to an OAuth2 plan must have an existing client with a valid `client_id` registered in the OAuth 2.0 authorization server. The `client_id` will be used to establish a connection between the OAuth 2.0 client and the APIM consumer application.

To mitigate performance concerns, a cache system is available to avoid completing the same token introspection multiple times. If there are multiple OAuth2 plans, it is recommended to use selection rules to avoid any unnecessary token introspection.

</details>

<details>

<summary>JWT</summary>

**Introduction**

A JSON Web Token (JWT) is an open method for representing claims securely between two parties. It is digitally signed using an HMAC shared key or RSA public/private key pair. The JWT authentication type ensures that a JWT issued by a third party is valid by verifying its signature and expiration date. Only applications with approved JWTs can access APIs associated with a JWT plan.

**Configuration**

APIM uses client IDs to recognize applications that have subscribed to a JWT plan. The inbound JWT payload must include the `client_id` claim to establish a connection between the JWT and the APIM application subscription.

A JWT plan presents the following configuration options:

<img src="../../../.gitbook/assets/plan_jwt configure.png" alt="JWT plan configuration" data-size="original">

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

**Introduction**

A Push plan is used when an API contains an entrypoint that sends message payloads to API consumers (e.g., Webhook). This type of plan is unique in that the security configuration is defined by the API consumer, in the subscription request created in the Developer Portal. For example, when subscribing to a Webhook entrypoint, the API consumer specifies the target URL and authentication for the Gateway to use when sending messages.

Push plans do not apply to SSE entrypoints. Although messages are pushed from the server, the client application initiates message consumption.

**Configuration**

Push plans have the same configuration options as [Keyless plans](README.md) in APIM. The bulk of the configuration for a Push plan is set by the API consumer in the Developer Portal, and the content of the configuration varies by entrypoint type.

Gravitee currently supports Push plans for Webhook entrypoints

</details>
