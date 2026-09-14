# Demonstrating Proof of Possession (DPoP)

[Demonstrating Proof of Possession (DPoP)](https://datatracker.ietf.org/doc/html/rfc9449) binds an access token to a key pair that the client holds. A DPoP-bound token is useless on its own, because every request that presents the token must also carry a proof signed with the client's private key.

AM issues DPoP-bound access and refresh tokens and enforces the binding on its own protected endpoints. You can require DPoP for one application or for every application in a security domain.

{% hint style="info" %}
DPoP is available from AM 4.13.0. DPoP is opt-in for clients. A client that doesn't send a proof keeps receiving bearer tokens unless you require DPoP for its application or for its security domain.
{% endhint %}

## How it works

1. The client generates an asymmetric key pair and keeps the private key secret.
2. The client calls the token endpoint with a `DPoP` header. The header carries a proof, which is a JWT signed with the private key that carries the public key in its `jwk` header.
3. AM validates the proof and issues an access token whose `token_type` is `DPoP`. The access token carries the SHA-256 thumbprint of the public key in its `cnf.jkt` claim, and the refresh token is bound to the same key.
4. The client calls a protected endpoint, such as the UserInfo endpoint, with the `Authorization: DPoP <access_token>` header and a fresh proof in the `DPoP` header. This proof also carries the `ath` claim, which is the base64url-encoded SHA-256 hash of the access token.
5. AM verifies the proof against the thumbprint in the token before it serves the request.

## Proof requirements

AM checks every proof against the following rules, at the token endpoint and at protected endpoints alike.

| Proof element | What AM requires |
| --- | --- |
| `DPoP` header | Exactly one `DPoP` header that contains a signed JWT. |
| `typ` header | `dpop+jwt`. |
| `alg` header | `ES256`, `ES384`, `ES512`, `RS256`, `RS384`, or `RS512`. When the security domain restricts the signing algorithms, the algorithm must also be on that list. |
| `jwk` header | The public key that verifies the signature, without any private key material. |
| Signature | Valid for the embedded public key. |
| `htm` claim | The HTTP method of the request. |
| `htu` claim | The URL of the endpoint that receives the request. AM ignores the query string and the fragment. |
| `iat` claim | Not older than the validity window, which is 30 seconds by default, and not more than 3 seconds in the future. |
| `jti` claim | Present and not used before. AM keeps a replay cache of the proof identifiers it has accepted. |
| `ath` claim | On protected endpoints only. The base64url-encoded SHA-256 hash of the access token presented in the `Authorization` header. |

{% hint style="info" %}
Read the endpoint URLs from the security domain's OpenID discovery document and use them verbatim as the `htu` value. When the AM Gateway runs behind a reverse proxy, AM builds the expected URL from the `X-Forwarded-Proto` and `X-Forwarded-Host` headers, and prefixes the path with the `X-Forwarded-Prefix` header, when the proxy sends them.
{% endhint %}

The [AM Gateway configuration](../../../getting-started/configuration/configure-am-gateway/README.md#dpop-proof-validation) controls the validity window and the replay cache.

## Configure DPoP

You don't need to change any setting for a client to obtain DPoP-bound tokens. The settings in this section make the proof mandatory and restrict the signing algorithms.

### Require DPoP for an application

Turn on **DPoP-bound access tokens** to reject every token request from the application that doesn't carry a valid `DPoP` header.

To turn the setting on in AM Console:

1. Log in to AM Console.
2. Select your security domain.
3. Click **Applications**.
4. Select your application.
5. Click **Settings**.
6. Click **OAuth 2.0 / OIDC**.
7. On the **Grant Flows** tab, scroll to the **Demonstrating Proof-of-Possession (DPoP)** section.
8. Turn on **DPoP-bound access tokens**.
9. Click **SAVE**.

<figure><img src="../../../.gitbook/assets/am-application-dpop-bound-access-tokens.png" alt=""><figcaption><p>DPoP-bound access tokens setting on the application Grant Flows tab</p></figcaption></figure>

To turn the setting on with the AM Management API, patch the application:

```json
PATCH /organizations/{organizationId}/environments/{environmentId}/domains/{domain}/applications/{application}
Content-Type: application/json

{
  "settings": {
    "oauth": {
      "dpopBoundAccessTokens": true
    }
  }
}
```

A client that registers through [dynamic client registration](../openid-connect.md#dynamic-client-registration) sets the same behavior with the `dpop_bound_access_tokens` client metadata.

### Require DPoP for every application in a security domain

Turn on **Require DPoP for all clients** to reject every token request in the security domain that doesn't carry a valid `DPoP` header. The setting applies even to applications whose own **DPoP-bound access tokens** setting is off.

To turn the setting on in AM Console:

1. Log in to AM Console.
2. Select your security domain.
3. Click **Settings**.
4. In the **OAuth 2.0** section, click **DPoP**.
5. Turn on **Require DPoP for all clients**.
6. Click **SAVE**.

<figure><img src="../../../.gitbook/assets/am-domain-dpop-settings.png" alt=""><figcaption><p>DPoP settings of a security domain</p></figcaption></figure>

To turn the setting on with the AM Management API, patch the security domain:

```json
PATCH /organizations/{organizationId}/environments/{environmentId}/domains/{domain}
Content-Type: application/json

{
  "oidc": {
    "dpopSettings": {
      "requireDpopForAll": true
    }
  }
}
```

The requirement applies to the token endpoint. Tokens that AM issued without a proof before you turned the setting on keep working on protected endpoints until they expire.

### Restrict the proof signing algorithms

By default, AM accepts the six signing algorithms listed in the [proof requirements](#proof-requirements). To accept a subset, configure an allowlist for the security domain. AM then rejects a proof signed with any other algorithm and advertises the allowlist in the OpenID discovery document.

To configure the allowlist in AM Console:

1. Log in to AM Console.
2. Select your security domain.
3. Click **Settings**.
4. In the **OAuth 2.0** section, click **DPoP**.
5. In the **Allowed signing algorithms** section, select the algorithms in the **Allowed DPoP signing algorithms** list. Leave the list empty to accept all six algorithms.
6. Click **SAVE**.

To configure the allowlist with the AM Management API, patch the security domain. Set `dpopSigningAlgorithms` to `null` to accept all six algorithms. AM rejects an empty list with HTTP 400, and it rejects a list that contains a value outside the six supported algorithms with HTTP 400.

```json
PATCH /organizations/{organizationId}/environments/{environmentId}/domains/{domain}
Content-Type: application/json

{
  "oidc": {
    "dpopSettings": {
      "dpopSigningAlgorithms": ["ES256", "ES384"]
    }
  }
}
```

{% hint style="info" %}
The allowlist applies to the token endpoint and to the discovery document. Protected endpoints accept a proof signed with any of the six supported algorithms, and the `WWW-Authenticate` challenge they return always lists the six.
{% endhint %}

## Request a DPoP-bound token

This section describes what a client sends to the token endpoint and what it receives.

### Token endpoint

Send the proof in the `DPoP` header of the token request. AM binds tokens for every grant type, including [extension grants](extension-grants.md).

```bash
POST https://am-gateway/{domain}/oauth/token HTTP/1.1
Authorization: Basic czZCaGRSa3F0MzpnWDFmQmF0M2JW
DPoP: eyJ0eXAiOiJkcG9wK2p3dCIsImFsZyI6IkVTMjU2IiwiandrIjp7...
Content-Type: application/x-www-form-urlencoded

grant_type=client_credentials
```

The proof carries the following claims for this request:

```json
{
  "htm": "POST",
  "htu": "https://am-gateway/{domain}/oauth/token",
  "iat": 1757420000,
  "jti": "5e6c6f1a-2c7f-4b0e-9d3a-1f2e3d4c5b6a"
}
```

AM answers with the `DPoP` token type:

```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIsInR5...",
  "token_type": "DPoP",
  "expires_in": 7199,
  "scope": "read"
}
```

The access token carries the thumbprint of the proof key in its `cnf` claim:

```json
"cnf": {
  "jkt": "0ZcOCORZNYy-DWpqq30jZyJGHTN0d2HglBV3uiguA4I"
}
```

When the application or the security domain requires DPoP, a token request without a `DPoP` header is rejected with HTTP 400 and the `invalid_request` error. When neither requires DPoP, the same request receives a bearer token with `token_type` set to `bearer`.

### Refresh a DPoP-bound token

The refresh token that AM issues with a DPoP-bound access token is bound to the same key. Send a fresh proof signed with that key in the `DPoP` header of the `refresh_token` request. The new access token and the new refresh token stay bound to the original key.

* A refresh request without a `DPoP` header is rejected with HTTP 400 and the `invalid_request` error.
* A refresh request with a proof signed with a different key is rejected with HTTP 400 and the `invalid_dpop_proof` error.

A refresh token that was issued without a proof isn't bound. A `refresh_token` request that presents a proof for such a token receives DPoP-bound tokens, and a request without a proof receives bearer tokens.

### Bind the authorization code to the DPoP key

In the authorization code flow, the client can commit to its DPoP key before AM issues the code. Add the `dpop_jkt` parameter, whose value is the SHA-256 thumbprint of the client's public key, to the authorization request. AM reads the parameter from the query string, from a signed request object, or from a pushed authorization request.

{% code overflow="wrap" %}
```bash
GET https://am-gateway/{domain}/oauth/authorize?response_type=code&client_id=web-app&redirect_uri=https://web-app/callback&dpop_jkt=0ZcOCORZNYy-DWpqq30jZyJGHTN0d2HglBV3uiguA4I HTTP/1.1
```
{% endcode %}

When the client redeems the code at the token endpoint, the request must carry a proof signed with the committed key. AM validates `dpop_jkt` in addition to [PKCE](proof-key-for-code-exchange-pkce.md).

* A redemption without a `DPoP` header is rejected with HTTP 400 and the `invalid_dpop_proof` error.
* A redemption with a proof signed with a different key is rejected with HTTP 400 and the `invalid_dpop_proof` error.

A code that was requested without `dpop_jkt` keeps the default behavior: the redemption is bound to whichever key signs the proof, and it receives bearer tokens when it carries no proof.

## Use a DPoP-bound token with AM endpoints

AM enforces the binding on the endpoints of the AM Gateway that accept an access token:

* The UserInfo endpoint
* The dynamic client registration endpoints
* The UMA 2.0 protection API
* The SCIM 2.0 endpoints
* The user consent endpoints
* The self-service account management endpoints

Present the token with the `DPoP` scheme in the `Authorization` header, and send a fresh proof that carries the `ath` claim in the `DPoP` header:

```bash
GET https://am-gateway/{domain}/oidc/userinfo HTTP/1.1
Authorization: DPoP eyJhbGciOiJSUzI1NiIsInR5...
DPoP: eyJ0eXAiOiJkcG9wK2p3dCIsImFsZyI6IkVTMjU2IiwiandrIjp7...
```

A DPoP-bound token must be sent in the `Authorization` header. AM rejects a bound token that's passed as the `access_token` body parameter.

AM rejects a DPoP-bound token that's presented with the `Bearer` scheme, or with a missing or invalid proof, with HTTP 401 and a `DPoP` challenge:

```
WWW-Authenticate: DPoP error="invalid_token", algs="ES256 ES384 ES512 RS256 RS384 RS512"
```

Tokens issued without a proof aren't bound, and the endpoints keep accepting them with the `Bearer` scheme. A request without any token receives the `Bearer realm="gravitee-io"` challenge, whether or not the security domain requires DPoP.

## Discovery and introspection

The OpenID discovery document of the security domain, at `https://am-gateway/{domain}/oidc/.well-known/openid-configuration`, advertises the accepted proof signing algorithms in `dpop_signing_alg_values_supported`. The list reflects the domain allowlist, or all six algorithms when no allowlist is configured.

The [introspection endpoint](README.md#introspection-endpoint) returns the `cnf` claim with the `jkt` thumbprint for a DPoP-bound access token.

## Errors

The following table lists the responses to the requests that AM rejects because of DPoP.

| Endpoint | Condition | Response |
| --- | --- | --- |
| Token endpoint | The application or the security domain requires DPoP, and the request has no `DPoP` header. | HTTP 400, `invalid_request` |
| Token endpoint | The request has a `DPoP` header, and the proof fails one of the [proof requirements](#proof-requirements). | HTTP 400, `invalid_dpop_proof` |
| Token endpoint, `refresh_token` grant | The refresh token is bound, and the request has no `DPoP` header. | HTTP 400, `invalid_request` |
| Token endpoint, `refresh_token` grant | The refresh token is bound, and the proof is signed with a different key. | HTTP 400, `invalid_dpop_proof` |
| Token endpoint, `authorization_code` grant | The code carries `dpop_jkt`, and the request has no `DPoP` header. | HTTP 400, `invalid_dpop_proof` |
| Token endpoint, `authorization_code` grant | The code carries `dpop_jkt`, and the proof is signed with a different key. | HTTP 400, `invalid_dpop_proof` |
| Protected endpoints | A DPoP-bound token is presented with the `Bearer` scheme. | HTTP 401, `WWW-Authenticate: DPoP error="invalid_token"` |
| Protected endpoints | A DPoP-bound token is passed as the `access_token` body parameter. | HTTP 401, `WWW-Authenticate: DPoP error="invalid_token"` |
| Protected endpoints | A DPoP-bound token is presented with the `DPoP` scheme, and the request has no `DPoP` header. | HTTP 401, `WWW-Authenticate: DPoP error="invalid_token"` |
| Protected endpoints | A DPoP-bound token is presented with the `DPoP` scheme, and the proof fails one of the [proof requirements](#proof-requirements). | HTTP 401, `WWW-Authenticate: DPoP error="invalid_token"` |
| Protected endpoints | The `Authorization` header uses a scheme other than `Bearer` or `DPoP`. | HTTP 401 |
| AM Management API | The security domain is saved with an empty `dpopSigningAlgorithms` list. | HTTP 400, `DPoP signing algorithms allowlist must not be empty` |
| AM Management API | The `dpopSigningAlgorithms` list contains an unsupported algorithm. | HTTP 400, `DPoP signing algorithms allowlist must only contain supported algorithms` |

{% hint style="info" %}
When the application or the security domain requires DPoP, the `invalid_request` check runs first. A redemption of a `dpop_jkt`-bound code without a `DPoP` header is then rejected with `invalid_request` rather than `invalid_dpop_proof`.
{% endhint %}

## Audit events

AM records a `TOKEN_CREATED` audit event for each token it issues. For a DPoP-bound token, the event parameters include `DPOP_JKT` with the thumbprint of the bound key. See [Audit Trail](../../audit-trail.md).
