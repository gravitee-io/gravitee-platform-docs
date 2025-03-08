---
description: How to expose your APIs
---

# Plans

To expose your API to internal or external consumers, it must have at least one plan. A plan provides a service and access layer on top of your APIs for consumer applications by specifying access limits, subscription validation modes, and other configurations to tailor it to a specific application.

## Create a plan

Plans are always created by the API publisher. You can create plans in the Management Console as part of the [API creation process](../create-apis/). You can also create them later with the **Portal > Plans** function as shown below.

{% @arcade/embed flowId="L3b4AWtxtYkNE89ZiR2Y" url="https://app.arcade.software/share/L3b4AWtxtYkNE89ZiR2Y" %}

Creating a plan begins by navigating to your API, selecting **Plans** in the sidebar, and then selecting **Add new plan** in the top right of the page.

<figure><img src="../../.gitbook/assets/Screen Shot 2023-03-15 at 1.36.23 PM.png" alt=""><figcaption><p>Create a new plan</p></figcaption></figure>

This will take you to the plan creation wizard.

Creating a plan is broken down into three main stages:

1. **General**
2. **Secure**
3. **Restrictions**

<figure><img src="../../.gitbook/assets/Screen Shot 2023-03-15 at 1.37.47 PM.png" alt=""><figcaption><p>Plan creation wizard</p></figcaption></figure>

### General

In the **General** stage, you enter basic details about your plan. The only requirement for this stage is providing a name for your plan.

The initial section lets you set a name, description, and characteristics for your plan. Characteristics are optional labels you can use to tag your plan.

<figure><img src="../../.gitbook/assets/Screen Shot 2023-03-15 at 12.49.56 PM.png" alt=""><figcaption><p>First step in plan creation</p></figcaption></figure>

The next section in the **General** stage is **Conditions.** Here you can optionally select a page containing the general conditions for use of your plan. If included, these conditions must be accepted by the user to finalize the subscription process. To associate general conditions of use with a plan, you need to specify a markdown page where these conditions are specified.

<figure><img src="../../.gitbook/assets/Screen Shot 2023-03-15 at 12.55.52 PM.png" alt=""><figcaption><p>Selecting general conditions for your plan</p></figcaption></figure>

To create a general conditions plan, navigate to the **Documentation** page and select the plus icon in the bottom right. You must create a markdown page and publish it to use as the general conditions page of your plan.

<figure><img src="../../.gitbook/assets/Screen Shot 2023-03-15 at 12.57.42 PM.png" alt=""><figcaption><p>Creating general conditions for a plan</p></figcaption></figure>

The **Subscriptions** section lets you configure basic settings around a subscription for plans requiring authentication.

<figure><img src="../../.gitbook/assets/Screen Shot 2023-03-15 at 1.07.37 PM.png" alt=""><figcaption><p>Basic subscription setting</p></figcaption></figure>

Toggling **Auto validate subscription** means you will accept any and all subscriptions to a plan without the API publisher's review. These subscriptions can be modified at any time.

You can require all subscription requests from API consumers to include a comment detailing their request. Additionally, with this option enabled, the API publisher can leave a default message explaining what is expected in the API consumer's comment.

The final two sections in the **General** stage are **Deployment** and **Access-Control**.

<figure><img src="../../.gitbook/assets/Screen Shot 2023-03-15 at 1.10.04 PM.png" alt=""><figcaption><p>Deployment and Access-Control settings</p></figcaption></figure>

The **Deployment** section allows you to selectively deploy the plan to particular APIs using sharding tags which you can learn more about [here](../../getting-started/configuration/configure-apim-gateway/sharding-tags.md).

**Access-Control** lets you prevent specified groups from accessing this plan. You can learn more about user management and how to configure groups here.

### Secure

During the **Secure** stage of plan creation, the API publisher selects one of five authentication types to secure their API. You can learn more about how to configure plan security in the [following section](plans.md#configure-plan-security).

<figure><img src="../../.gitbook/assets/Screen Shot 2023-03-15 at 1.49.42 PM.png" alt=""><figcaption><p>Select authentication type</p></figcaption></figure>

* **Keyless (public):** does _not_ require authentication and allows public access to the API. By default, keyless plans offer no security and are most useful for quickly and easily exposing your API to external users and getting their feedback.
* **API Key:** only allows apps with approved API keys to access your API. This plan type ensures that API keys are valid, are not revoked or expired, and are approved to consume the specific resources associated with your API.
* **JSON web token (JWT):** open method for representing claims securely between two parties. JWTs are digitally-signed using HMAC shared keys or RSA public/private key pairs. JWT plans allow you to verify the signature of the JWT and check if the JWT is still valid according to its expiry date.
* **OAuth 2.0:** open standard that apps can use to provide client applications with secure delegated access. OAuth works over HTTPS and authorizes devices, APIs, servers, and applications with access tokens rather than credentials.
* **Push:** used when the API has an entrypoint that sends message payloads to API consumers (e.g. Webhook). This type of plan is unique in that the security configuration is defined by the **API** **consumer** in the subscription request created in the Developer Portal. For example, when subscribing to a Webhook entrypoint of an API, the API consumer will specify the target URL and authentication for the Gateway to use when sending messages.

{% hint style="info" %}
Push plans do _not_ apply to Server Sent Event entrypoints. Even though messages are pushed from the server, the client application initiates consumption of messages from the entrypoint.
{% endhint %}

### Restrictions

Restrictions are just policies to regulate access to your APIs. Like any policy, restrictions can also be applied to a plan through the design studio. You can learn more about configuring these particular policies here.

<figure><img src="../../.gitbook/assets/Screen Shot 2023-03-15 at 1.52.54 PM.png" alt=""><figcaption><p>Configure restrictions</p></figcaption></figure>

* **Rate Limiting:** limit how many HTTP requests an application can make in a specified period of seconds or minutes. This policy is meant to help avoid unmanageable spikes in traffic.
* **Quota:** specifies the number of requests allowed to call an API backend during a specified time interval. The policy is generally used to tier access to APIs based on subscription level.
* **Resource Filtering:** limit access to a subset of API resources

## Configure plan security

The most important part of plan configuration is security. APIM supports the following five authentication types:

* Keyless (public)
* API Key
* JWT
* OAuth 2.0
* Push

{% hint style="info" %}
**Policies vs authentication types**

Authentication types are simply policies integrated directly into a plan. Once a plan is created, the authentication type can not be changed. However, you can always add additional security at the API or plan level with policies in the design studio by following the steps to add policies to a flow in the [Policy Studio](../policy-studio/).

There are some additional considerations when using a plan with JWT or OAuth 2.0 security. For example, if we create a JWT plan, the Gateway API won’t be accessible unless the JWT token is linked to a subscription. Therefore, for the request to succeed, the API consumer must subscribe to the API and embed the _client\_id_ in the JWT token when using a JWT plan as opposed to a JWT policy.
{% endhint %}

### Keyless plan

The Keyless authentication type does _not_ require authentication and allows public access to the API. By default, keyless plans offer no security and are most useful for quickly and easily exposing your API to external users and getting their feedback. Due to not requiring a subscription and a lack of a consumer identifier token, keyless consumers are set as `unknown application` in the API analytics section.

<figure><img src="../../.gitbook/assets/Screen Shot 2023-03-15 at 1.39.10 PM.png" alt=""><figcaption><p>Keyless authentication type</p></figcaption></figure>

{% hint style="info" %}
**Basic authentication and keyless plans**

You can configure basic authentication for keyless plans by associating a basic authentication policy with either an LDAP or inline resource. For more details, see the [Basic Authentication policy](../../reference/policy-reference/basic-authentication.md).
{% endhint %}

### API key plan

The API key authentication type enforces verification of API keys during request processing, allowing only apps with approved API keys to access your APIs. This plan type ensures that API keys are valid, are not revoked or expired, and are approved to consume the specific resources associated with your API.

API key plans offer only a basic level of security, acting more as a unique identifier than a security token. For a higher level of security, see JWT and OAuth 2.0 plans below.

When configuring API key authentication, there are two main options:

* **Propagate API key to upstream API:** toggling this setting on ensures the request to the backend API includes the API key header sent by the API consumer. This is setting is useful for backend APIs that already have integrated API key authentication.
* **Additional selection rule:** this setting allows you to use Gravitee Expression Language (EL) to filter by contextual data (request headers, tokens, attributes, etc.) for plans of the same type. For example, if you have two API key plans, you can set different selection rules on each plan to determine which plan handles each request.

<figure><img src="../../.gitbook/assets/Screen Shot 2023-03-15 at 3.22.29 PM.png" alt=""><figcaption><p>API key plan configuration</p></figcaption></figure>

Typically, API keys are randomly generated for each subscription. However, Gravitee provides two other options for API key generation: custom API key and shared API key. Both of these settings can be enabled at the environment level by selecting **Settings** in the main sidebar and then selecting **Settings** again under the **Portal** group in the nested sidebar.

<figure><img src="../../.gitbook/assets/Screen Shot 2023-03-15 at 3.49.04 PM.png" alt=""><figcaption><p>API key generation settings</p></figcaption></figure>

#### Custom API key

You can specify a custom API key for an API key plan. This is particularly useful when you want to silently migrate to APIM and have a pre-defined API key. The custom API key must have more than 8 characters, less than 64 characters, and be URL compliant. `^ # % @ \ / ; = ? | ~ , space` are all invalid characters.

When prompted, you can choose to provide your custom API key or let APIM generate one for you by leaving the field empty.

You can provide a custom API key when:

* Creating a subscription

<figure><img src="../../.gitbook/assets/Screen Shot 2023-03-15 at 3.54.21 PM.png" alt=""><figcaption><p>Manually creating a subscription</p></figcaption></figure>

* Accepting a subscription

<figure><img src="../../.gitbook/assets/Screen Shot 2023-03-15 at 3.57.18 PM.png" alt=""><figcaption><p>Accepting a subscription</p></figcaption></figure>

* Renewing a subscription

<figure><img src="../../.gitbook/assets/Screen Shot 2023-03-15 at 3.58.35 PM.png" alt=""><figcaption><p>Renewing a subscription</p></figcaption></figure>

#### Shared API key

The shared API key mode allows consumers to reuse the same API key across all API subscriptions of an application.

{% hint style="info" %}
**Shared API key limitations**

For technical reasons, in shared mode, API keys can only be shared across API key plans that belong to distinct Gateway APIs. Therefore, if you attempt to subscribe to two API key plans on the same Gateway API, no prompt will be made to choose the application API key type and the default mode will be used automatically.
{% endhint %}

With this mode enabled, consumers will be asked on their application's second subscription to choose between reusing their key across all subscriptions or generating one different API key for each subscription (which is the default mode). This is known as the application API key type.

<figure><img src="https://docs.gravitee.io/images/apim/3.x/api-publisher-guide/plans-subscriptions/shared-api-key-2-portal.png" alt=""><figcaption><p>Subscribing in the Developer Portal</p></figcaption></figure>

<figure><img src="../../.gitbook/assets/Screen Shot 2023-03-16 at 11.44.51 AM.png" alt=""><figcaption><p>Subscribing in the management UI</p></figcaption></figure>

This choice is _permanent_ for that application and consumers will not be able to switch between application API key types after the initial decision.

{% hint style="warning" %}
**Missing API key type selection menu?**

Shared API key mode must be [enabled in settings](plans.md#api-key-plan) **before** creating an application in order to have this option show up. If you are having issues, the best option is to create a new application and immediately subscribe to two API key plans.
{% endhint %}

When disabling the shared API key mode in environment settings, applications that have already been configured to use a shared key will continue to work this way, but consumers will stop being asked to choose between one mode or the other on their second subscription.

Shared API key mode also has an important consequence you should be aware of before enabling. Because the shared API key may be used to call APIs that are owned by another group of API publishers, shared API keys cannot be edited from the API publisher subscription view. So while shared API keys are still readable by API publishers, renewal and revocation of shared API keys cannot be performed by the API publisher when a subscription has been made in shared API key mode.

<figure><img src="https://docs.gravitee.io/images/apim/3.x/api-publisher-guide/plans-subscriptions/shared-api-key-3.png" alt=""><figcaption><p>Shared API key administration limitations</p></figcaption></figure>

Instead, it is the responsibility of the application owner to perform such operations, and for this reason, shared API keys can only be revoked from the application owner subscription view in either the Management Console or the Developer Portal.

<figure><img src="https://docs.gravitee.io/images/apim/3.x/api-publisher-guide/plans-subscriptions/shared-api-key-4.png" alt=""><figcaption><p>Manage shared API key in the Management Console</p></figcaption></figure>

<figure><img src="https://docs.gravitee.io/images/apim/3.x/api-publisher-guide/plans-subscriptions/shared-api-key-4-portal.png" alt=""><figcaption><p>Manage shared API key in the Developer Portal</p></figcaption></figure>

### JSON Web Token (JWT) plan

The JWT authentication type ensures that JWTs issued by third parties are valid. Only applications with approved JWTs can access APIs associated with a JWT plan.

[JSON Web Tokens](https://tools.ietf.org/html/rfc7519) are an open method for representing claims securely between two parties. JWTs are digitally signed using HMAC shared keys or RSA public/private key pairs. JWT plans allow you to verify the signature of the JWT and check if the JWT is still valid according to its expiry date.

JWT defines some [registered claim names](https://tools.ietf.org/html/rfc7519#section-4.1) including subject, issuer, audience, expiration time, and not-before time. In addition to these claims, the inbound JWT payload must include the `client_id` claim (see below) to establish a connection between the JWT and the APIM application subscription.

The policy searches for a client ID in the payload as follows:

* First in the `azp` claim
* Next in the `aud` claim
* Finally in the `client_id` claim

{% hint style="info" %}
**Client ID**

Client IDs are used to recognize applications that have subscribed to either a JWT or OAuth 2.0 plan. You can learn more under Subscriptions.
{% endhint %}

Configuring a JWT plan presents the following options:

<figure><img src="../../.gitbook/assets/JWT plan configuration.png" alt=""><figcaption><p>JWT plan configuration</p></figcaption></figure>

* **Signature:** select the algorithm used to hash and encrypt your JWT
* **JSON Web Key Set (JWKS) resolver:** to validate the signature of the JWT, the Gateway needs to use the associated authorization server's JSON web key (JWK) which is often stored inside a JSON web key set (JWKS). Gravitee has three methods for providing the JWK:
  * `GIVEN_KEY` : you provide the key in `ssh-rsa`, `pem`, `crt` or `public-key` format which must match the signature algorithm
  * `JWKS_URL` : you can provide a URL for the Gateway to retrieve the necessary JWKS (basically, a URL ending with `/.well-known/jwks.json` )
  * `GIVEN_ISSUER` : you can set public keys in the APIM Gateway `gravitee.yml` file that are associated with an authorization server. The Gateway will only accept JWTs with an`iss` (issuer) JWT payload [claim](https://auth0.com/docs/secure/tokens/json-web-tokens/json-web-token-claims) that matches an authorization server listed in the APIM Gateway `gravitee.yml`. Additionally, you can filter between an authorization server's keys based on the `kid` (key ID) JWT header [claim](https://auth0.com/docs/secure/tokens/json-web-tokens/json-web-token-claims).

{% code title="gravitee.yml" %}
```yaml
jwt:
  issuer:
    my.authorization.server:
      default: ssh-rsa myValidationKey anEmail@domain.com
      kid-2016: ssh-rsa myCurrentValidationKey anEmail@domain.com
```
{% endcode %}

* **Use system proxy:** when using a `jwks_url` as a JWKS resolver, optionally make the HTTP call through a system-wide proxy as configured in the `gravitee.yml` file
*   **Extract JWT claims:** allow claims to be accessed in the `jwt.claims` context attribute during request-response with the Gravitee Expression Language (EL). For example, when enabled, you can extract the issuer claim from JWT using the following EL statement:

    ```
    {#context.attributes['jwt.claims']['iss']}
    ```
* **Propagate Authorization header:** propagate the header containing the JWT token to the backend APIs
* **User claim:** payload claim where the user can be extracted. The default `sub` value is standard with JWTs
* **Client ID claim:** override the default claim where the client ID can be extracted. By default, the Gateway checks the `azp` claim, then the `aud` claim, and finally the `client_id` claim.
* **Additional selection rule:** this setting allows you to use the EL to filter by contextual data (request headers, tokens, attributes, etc.) for plans of the same type. For example, if you have two JWT plans, you can set different selection rules on each plan to determine which plan handles each request.

Once JWT configuration is complete and the plan is created and published, your API will be JWT secured and subscribed consumers must call the API with an `Authorization: Bearer your-JWT` HTTP header.

### OAuth 2.0

The OAuth 2.0 authentication type checks access token validity during request processing using token introspection. If the access token is valid, the request is allowed to proceed. If not, the process stops and rejects the request.

To configure an OAuth 2.0 plan for an API, you need to first create an OAuth 2.0 client resource that represents your OAuth 2.0 authorization server. Learn more about creating an OAuth resource here.

Configuring an OAuth 2.0 plan presents the following options:

<figure><img src="../../.gitbook/assets/OAuth plan configuration.png" alt=""><figcaption><p>Configuring OAuth 2.0 plan</p></figcaption></figure>

* **OAuth2 resource:** specify the name of the OAuth2 resource to use as the authorization server
* **Cache resource:** optionally specify the name of the cache resource to store responses from the authorization server
*   **Extract OAuth2 payload:** allow OAuth2 payload to be accessed in the `oauth.payload` context attribute during request-response with the Gravitee Expression Language (EL). For example, when enabled, you can access the payload using the following EL statement:

    ```
    {#context.attributes['oauth.payload']}
    ```
* **Check scopes:** an authorization server can grant access tokens with a [scopes](https://tools.ietf.org/html/rfc6749#section-3.3) parameter. With this setting enabled, the Gateway will check the scopes parameter against the provided **Required scopes** to determine if the client application is allowed to access the API
* **Mode strict:** enabled by default. With mode strict disabled, the Gateway will validate the API call if the access token contains _at least one_ scope from the **Required scopes** list. Strict mode requires the access token to contain _all_ scopes from the **Required scopes** list.
* **Propagate Authorization header:** propagate the header containing the access token to the backend APIs

Your API is now OAuth 2.0 secured and consumers must call the API with an `Authorization Bearer :token:` HTTP header to access the API resources.

{% hint style="info" %}
**Subscription requirements**

Any applications wanting to subscribe to an OAuth 2.0 plan must have an existing client with a valid `client_id` registered in the OAuth 2.0 authorization server. The `client_id` will be used to establish a connection between the OAuth 2.0 client and the APIM consumer application. You can learn more about setting up client applications here.
{% endhint %}

### Push

Push plans have the same configuration options as Keyless plans in APIM. The bulk of the configuration for a push plan is set by the API consumer in the Developer Portal, and the content of the configuration varies by entrypoint type.

{% hint style="info" %}
In APIM 4.0, Webhook is the only type of entrypoint that uses a push plan.
{% endhint %}

## Publish a plan

After creating a plan, it's initially in the first of the four stages of a plan: staging, published, deprecated, and closed.

* **Staging** - This is the first stage of a plan. View it as a draft mode. You can configure your plan but it won’t be accessible to users.
* **Published** - Once your plan is ready, you can publish it to let API consumers view and subscribe on the APIM Portal and consume the API through it. A published plan can still be edited.
* **Deprecated** - You can deprecate a plan so it won’t be available on the APIM portal and API Consumers won’t be able to subscribe to it. Existing subscriptions remain so it doesn’t impact your existing API consumers.
* **Closed** - Once a plan is closed, all associated subscriptions are closed too. This can not be undone. API consumers subscribed to this plan won’t be able to use your API.

<figure><img src="https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/optimized/2X/6/6333ad2d86aae2ceb0cac422dd9015c75c3e6fb5_2_689x197.png" alt=""><figcaption><p>Four stages of a plan</p></figcaption></figure>

{% hint style="info" %}
**The Benefits of Deprecation**

Deprecating plans allow consumers of the API time to migrate without breaking their application while also ensuring new users do not subscribe to the deprecated plan.
{% endhint %}

<figure><img src="../../.gitbook/assets/Screenshot 2023-03-21 at 3.44.11 PM.png" alt=""><figcaption><p>Stages of a plan in the UI</p></figcaption></figure>

Publishing a plan is as simple as clicking the **Publish Plan** button, confirming your desire to publish the plan with the modal that appears on your screen, and deploying your API again to synchronize the change.

{% @arcade/embed flowId="vOBfQE9VInuyA1g7b4kF" url="https://app.arcade.software/share/vOBfQE9VInuyA1g7b4kF" %}

A published plan can either be deprecated or closed. Neither operation can be undone.

## Plan selection

APIM automatically routes each API request to the correct plan. The plan selection workflow parses all the published plans in the following order: JWT, OAuth2, API Key, Keyless. Each plan type has the following rules:

{% hint style="warning" %}
This workflow only applies to [v4 APIs and v2 APIs in emulation mode.](../../overview/gravitee-api-definitions-and-execution-engines/#plan-selection)
{% endhint %}

* JWT
  * Retrieve JWT from `Authorization` Header or query parameters
  * Ignore empty `Authorization` Header or any type other than Bearer
  * An empty Bearer token is considered invalid
* OAuth2
  * Retrieve OAuth2 from `Authorization` Header or query parameters
  * Ignore empty `Authorization` Header or any type other than Bearer
  * An empty Bearer token is considered invalid
* API Key
  * Retrieve the API key from the request header or query parameters (default header: `X-Gravitee-Api-Key` and default query parameter: `api-key`)
  * An empty Bearer token is considered invalid
* Keyless
  * Will ignore any type of security (API key, Bearer token, etc.)
  * **If another plan has detected a security token, valid or invalid, all flows assigned to the Keyless plan will be ignored.** Therefore, if an API has multiple plans of different types and the incoming request contains a token or an API key that does not match any of the existing plans, then the Keyless plan will not be activated and the user will receive a generic `401` response without any details.

The parsed plan is selected for execution if all the following conditions are met:

* The request contains a token corresponding to the plan type (e.g., `X-Gravitee-Api-Key` header for API Key plans).
* The plan condition rule is valid or not set.
* There is an active subscription matching the incoming request.
  * During the OAuth2 plan selection, a token introspection is completed to retrieve the `client_id` which allows searching for a subscription. If there are performance concerns, a cache system is available to avoid completing the same token introspection multiple times. Where possible, it is recommended to use selection rules if there are multiple OAuth2 plans to avoid any unnecessary token introspection.
