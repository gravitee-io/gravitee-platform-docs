# Overview 

OAuth 2.0 Token Exchange [RFC-8693](https://datatracker.ietf.org/doc/html/rfc8693) allows a client to request a new security token by presenting an existing one. This enables scenarios where one service needs to act as, or on behalf of, a user or another service, without requiring the user to re-authenticate.

Gravitee Access Management supports the following Token Exchange paradigms:

* **Impersonation:** The issued token represents the subject directly. The requesting client acts as the subject. There is no indication in the token that a different party initiated the exchange.
* **Delegation:** The issued token represents the subject but includes an act (actor) claim identifying the party that is acting on the subject's behalf. The actor's identity is preserved in the token.

Here are the key behaviours for OAuth 2.0 token exchange:
* No refresh tokens are issued during token exchange.
* The issued token's expiration is bounded by the subject token's remaining lifetime.
* The `client_id` claim in the issued token identifies the requesting client.
* When an ID token is requested, it is returned in the `access_token` response field with the token_type set to `N_A`.

## Enable Token Exhange 
To enable token exchange, complete the following steps:
1. [Enable the Token Exchange setting](#enable-the-token-exchange-setting)
2. [Add Token Exchange as an allowed grant type in your application](#add-token-exchange-as-an-allowed-grant-type-in-your-application)

### Enable the Token Exchange setting
1. From the dashboard, click **Settings**.
2. In the **Settings** menu, navigate to the **OAuth 2.0** section, and then click **Token Exchange**.
3. Turn on the **Enable Token Exchange** toggle.

### Add Token Exchange as an allowed grant type in your application
1. Click **Applications**. 
2. Select the application that you want to add Token Exchange to.
3. In the application's menu, click **Settings**. 
4. Navigate to **Grant flows**, and then select **Token Exchange**.

## Client authentication
* The client must authenticate the on the token endpoint. For example, use a HTTP basic authentication with `client_id` and `client_secret`.

## Domain Token Exchange Settings

{% hint style="info" %}
When Token Exchange is active, you must enable either `Allow Impersonation` or `Allow Delegation`.
{% endhint %}

Configure token exchange at the security domain level. To confiuge the token exchange, complete the following steps:
1. Click **Settings**. 
2. In the **Settings** menu, navigate to the **OAuth 2.0**, and then click **Token Exchange**. 

Here is a reference for the token exchange settings:


| Setting                       | Description                                                              | Default                                    |
| ----------------------------- | ------------------------------------------------------------------------ | ------------------------------------------ |
| Enable Token Exchange         | Master toggle for the Token Exchange grant                               | Off                                        |
| Allowed Subject Token Types   | Token types accepted as `subject_token`                                  | Access Token, Refresh Token, ID Token, JWT |
| Allowed Requested Token Types | Token types that can be issued                                           | Access Token, ID Token                     |
| Allow Impersonation           | Enable exchange without `actor_token`                                    | On (when Token Exchange is enabled)        |
| Allow Delegation              | Enable exchange with `actor_token`; issued tokens include an `act` claim | Off                                        |
| Allowed Actor Token Types     | Token types accepted as `actor_token` (delegation only)                  | Access Token, ID Token, JWT                |
| Maximum Delegation Depth      | Maximum nesting depth of `act` claims (1-100)                            | 25                                         |
| Scope Handling                | Mode controlling what scopes can be granted based on the request         | Downscoping                                |

### Delegation Depth
{% hint style="info" %}
The Scope Handling setting can be overridden for individual Applications or MCP Servers in the **OAuth 2.0 / OIDC settings**. By Default, all instances inherit the Scope Handling setting from the domain settings.
{% endhint %}

The Maximum Delegation Depth setting limits how deep the act claim chain grows. Depth is calculated from the subject token only:
* A token with no `act` claim has depth 0.
* A token with act: `{ sub: "A" }`  has depth 1.
* A token with act: `{ sub: "B", act: { sub: "A" } }`  has depth 2.
* Each delegation exchange increments the depth by 1. If the resulting depth would exceed the configured maximum, the request is rejected with `invalid_request`.

### Scope Handling 
{% hint style="info" %}
Only the subject token's act chain is counted for depth enforcement. The actor token's own act claim (captured as actor_act) does not contribute to the depth calculation.
{% endhint %}

The Scope Handling setting identifies the default mode for scope narrowing when processing Token Exchange requests within a domain.
* **Downscoping** is the default mode. Scopes granted in the response are restricted to those present in the subject_token and, if provided `actor_token`. Requests for additional scopes are denied. If no scopes are provided in the scope parameter, granted scopes are the default scopes configured for the OAuth client (Application or MCP Server) intersected with those of the subject_token and, if provided, th actor_token if provided).
* **Permissive** can be used to exchange tokens with less restriction. Scopes of the subject_token (or actor_token) are not taken into account during an exchange. Requested scopes are only restricted to those defined for the OAuth client. If no scopes are provided in the scope parameter, granted scopes are the default scopes configured for the OAuth client.
Permissive mode is less secure but offers a solution for scenarios where subject_token or actor_token do not define any or sufficient scopes (for example, they are ID tokens and cannot bear scopes).

### Trusted Issuer Configuration

Navigate to **Settings > OAuth 2.0 > Token Exchange > Trusted Issuers** to add external identity providers whose tokens can be exchanged.

| Property | Description | Example |
|:---------|:------------|:--------|
| `issuer` | Issuer URL (must match JWT `iss` claim) | `https://accounts.google.com` |
| `keyResolutionMethod` | How to resolve signing keys | `JWKS_URL` or `PEM` |
| `jwksUri` | JWKS endpoint URL (when method is `JWKS_URL`) | `https://accounts.google.com/.well-known/jwks.json` |
| `certificate` | PEM-encoded certificate (when method is `PEM`) | `-----BEGIN CERTIFICATE-----...` |
| `scopeMappings` | Map external scopes to domain scopes | `{"https://www.googleapis.com/auth/userinfo.email": "email"}` |
| `userBindingEnabled` | Enable user binding via EL expressions | `true` |
| `userBindingCriteria` | EL expressions to resolve external subject to domain user | See below |

#### User Binding Criteria

| Property | Description | Example |
|:---------|:------------|:--------|
| `attribute` | User attribute to match | `email`, `username` |
| `expression` | EL expression evaluated against token claims | `{#token['email']}` |

User binding resolves external token subjects to domain users. If zero users match the criteria, the request fails with "No user found matching binding criteria". If multiple users match, the request fails with "Multiple users found matching binding criteria". If `userBindingEnabled=false` or no criteria are configured, a virtual user is created from token claims.

