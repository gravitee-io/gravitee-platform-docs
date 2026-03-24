# OAuth 2.0 Token Exchange Configuration Reference

## Enable Token Exchange

To enable Token Exchange for your environment:

1. **Domain level:** Navigate to **Settings > OAuth 2.0 > Token Exchange** and toggle **Enable Token Exchange** on. Configure impersonation and/or delegation as needed.
2. **Application level:** In the application's OAuth 2.0 settings, add `Token Exchange` as an allowed grant type.
3. **Client authentication:** The client must authenticate on the token endpoint (e.g., using HTTP Basic authentication with `client_id` and `client_secret`).

## Domain Configuration Reference

**Settings > OAuth 2.0 > Token Exchange > Settings** tab

| Setting | Description | Default |
|:--------|:------------|:--------|
| Enable Token Exchange | Master toggle for the Token Exchange grant | Off |
| Allowed Subject Token Types | Token types accepted as `subject_token` | Access Token, Refresh Token, ID Token, JWT |
| Allowed Requested Token Types | Token types that can be issued | Access Token, ID Token |
| Allow Impersonation | Enable exchange without `actor_token` | On (when Token Exchange is enabled) |
| Allow Delegation | Enable exchange with `actor_token`; issued tokens include an `act` claim | Off |
| Allowed Actor Token Types | Token types accepted as `actor_token` (delegation only) | Access Token, ID Token, JWT |
| Maximum Delegation Depth | Maximum nesting depth of `act` claims (1–100) | 25 |
| Scope Handling | Mode controlling what scopes can be granted based on the request | Downscoping |

{% hint style="info" %}
At least one of **Allow Impersonation** or **Allow Delegation** must be enabled when Token Exchange is active.
{% endhint %}

### Delegation Depth

The **Maximum Delegation Depth** setting limits how deep the `act` claim chain can grow. Depth is calculated from the subject token only:

* A token with no `act` claim has depth 0.
* A token with `act: { sub: "A" }` has depth 1.
* A token with `act: { sub: "B", act: { sub: "A" } }` has depth 2.
* Each delegation exchange increments the depth by 1. If the resulting depth would exceed the configured maximum, the request is rejected with `invalid_request`.

{% hint style="info" %}
Only the subject token's `act` chain is counted for depth enforcement. The actor token's own `act` claim (captured as `actor_act`) does not contribute to the depth calculation.
{% endhint %}

### Scope Handling

The **Scope Handling** setting identifies the default mode for scope narrowing when processing Token Exchange requests within a domain.

* **Downscoping** is the default and recommended mode. Scopes granted in the response are restricted to those present in the `subject_token` (and `actor_token` if provided). Requests for additional scopes are denied. If no scopes are provided in the `scope` parameter, granted scopes are the default scopes configured for the OAuth client (Application or MCP Server) intersected with those of the `subject_token` (and `actor_token` if provided).
* **Permissive** can be used to exchange tokens with less restriction. Scopes of the `subject_token` (or `actor_token`) are not taken into account during an exchange. Requested scopes are only restricted to those defined for the OAuth client. If no scopes are provided in the `scope` parameter, granted scopes are the default scopes configured for the OAuth client.

**Permissive** mode is less secure but offers a solution for scenarios where `subject_token` or `actor_token` do not define any or sufficient scopes (for example, they are ID tokens and cannot bear scopes).

{% hint style="info" %}
The Scope Handling setting can be overridden for individual Applications or MCP Servers in the **OAuth 2.0 / OIDC** settings. By default, all instances inherit the Scope Handling setting from the domain settings.
{% endhint %}

## Trusted Issuer Configuration

Trusted issuers are configured per-domain in **Settings > OAuth 2.0 > Token Exchange > Trusted Issuer** tab.

There is a system-level cap on the number of entries, configurable in `gravitee.yaml` for the Management API:

```yaml
domain:
  tokenExchange:
    trustedIssuers:
      maxCount: 5   # default: 5
```

Each trusted issuer entry configures an external JWT issuer. Multiple issuers can be configured, but issuer URLs must be unique.

| Setting | Description | Required |
|:--------|:------------|:---------|
| Issuer URL | The exact string expected in the `iss` claim of the incoming JWT. Must be unique across the list. | Yes |
| Key Resolution Method | How to obtain the public key used to verify the JWT signature. `JWKS_URL` or `PEM`. | Yes |
| JWKS URL | URL of the issuer's JWKS endpoint (e.g. `https://idp.example.com/.well-known/jwks.json`). Only shown/required when method is `JWKS_URL`. | When method is `JWKS_URL` |
| PEM Certificate | PEM-encoded X.509 certificate whose public key is used for verification. Only shown/required when method is `PEM`. | When method is `PEM` |

### Scope Mappings

Scope Mappings can be configured using a 1-to-1 translation table from external scope name → domain scope name. External scopes that have no mapping entry are silently dropped (fail-closed).

### User Binding

When enabled, the gateway resolves the external JWT subject to exactly one existing domain user. The minted token carries that user's roles, groups, and full profile instead of a synthetic virtual user built from token claims only. If no domain user matches, or if more than one matches, the exchange is rejected (fail-closed).

**User Binding Criteria** can be defined as pairs of attributes and claims:

| Setting | Description | Examples |
|:--------|:------------|:---------|
| User Attribute | The domain user repository attribute to match against (must be a searchable field). | `userName`, `emails.value` |
| Claim / Expression | A claim name or an EL expression evaluated with the validated subject-token claims in context under the variable `token`. | `email`, `{#token['email']}` |

### Security Model

Trusted issuers follow a strict fail-closed design:

* Only explicitly listed issuers are accepted. An unrecognized `iss` value always results in `invalid_grant`.
* Only asymmetric signature algorithms are accepted (RS, PS, ES families). Symmetric/HMAC tokens from external parties are never trusted.
* Unmapped scopes are silently discarded, preventing privilege escalation through scope inflation.
* User binding requires exactly one matching domain user. Any ambiguity is treated as an error.
* The number of trusted issuers per domain is bounded (default: 5) to limit the attack surface.