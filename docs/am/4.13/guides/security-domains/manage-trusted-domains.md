---
description: Trusted domains declare which outside authorities an Access Management 4.13 security domain trusts for token exchange, Cross App Access and SPIFFE. Learn how to configure them.
---

# Manage Trusted Domains

## Overview

A trusted domain is an outside authority that a security domain trusts. Trusted domains are the only place where a security domain declares that trust. One trusted domain can serve several usages from the same key material:

| Usage | What AM does with the trusted domain |
|:------|:-------------------------------------|
| **Token exchange** | Validates external subject and actor tokens during an [RFC 8693 token exchange](../oauth-2.0-token-exchange-concepts/README.md). The token's `iss` claim must match the trusted domain's issuer. |
| **Cross App Access** | Mints an ID-JAG towards the resource servers the authority exposes. The issuer is used as the `aud` of the ID-JAG. |
| **SPIFFE** | Validates JWT-SVIDs presented by workloads as client assertions with the `spiffe_jwt` authentication method. The SVID `sub` must belong to the trusted domain's SPIFFE trust domain. |

Trusted domains are scoped to a security domain. Creating, updating or deleting a trusted domain is picked up by the gateway without restarting the security domain.

## Create a trusted domain

1. Navigate to **Settings > Security > Trusted Domains** in the domain sidebar.
2. On the **Domains** tab, click the **+** button.
3. In the **Trusted domain** section, enter a **Name** and an optional **Description**. The name is a label shown in the Console and must be unique within the security domain. On creation, the name is derived from the issuer URL until you edit it.
4. In the **Usage** section, select one or more usages:
   * **Token exchange** and **Cross App Access** require an **Issuer URL**: the issuer identifier of the authority's authorization server. It must be unique within the security domain, and an absolute URI when Cross App Access is selected.
   * **SPIFFE** requires a **SPIFFE trust domain**, without the `spiffe://` scheme (for example `prod.example`). Only lowercase letters, digits, `.` and `-` are allowed. It must be unique within the security domain.
5. In the **Key material** section, select the **Key source** of the authority's signing keys. Key material is not needed when Cross App Access is the only usage.
   * **JWKS URL**: the endpoint serving the JWK set, and the **Refresh interval (seconds)** at which AM polls it (default `300`).
   * **JWK Set**: an inline JWK set, for example `{ "keys": [ ... ] }`.
   * **PEM Certificate**: a PEM-encoded X.509 certificate holding the signing key.
6. Configure the sections of the selected usages, as described below.
7. Click **Create**.

To edit or delete a trusted domain, open it from the **Domains** tab. Deleting a trusted domain stops every usage it serves.

### Token exchange settings

| Setting | Description |
|:--------|:------------|
| **Scope mappings** | Maps external scopes from this issuer to domain scopes. Once at least one mapping exists, unmapped external scopes are dropped. Without mappings, external scopes are kept as they are. |
| **Enable User Binding** | Resolves the external token's subject to exactly one existing domain user. The minted token carries that user's roles, groups and profile instead of a synthetic user. If no user or several users match, the exchange is rejected. |
| **User binding mappings** | Pairs of **User Attribute** (a searchable user field, for example `userName` or `emails.value`) and **Claim / Expression** (a claim name such as `email`, or an EL expression such as `{#token['email']}`). All pairs must match. At least one pair is required when user binding is enabled. |

An external token is only accepted when it is presented with the token type `urn:ietf:params:oauth:token-type:jwt`, is signed with an RS, PS or ES algorithm, and its `iss` claim exactly matches the issuer URL.

### Cross App Access settings

| Setting | Description |
|:--------|:------------|
| **Resource servers** | The protected resources behind the authority's authorization server, which AM may mint an ID-JAG towards. Each entry has a **Name** and a **Resource URI**, an absolute URI carried by the `resource` claim. Resource URIs must be unique within the trusted domain. At least one resource server is required. |
| **aud\_sub expression** | EL expression that produces the `aud_sub` claim for every resource server of this authority, with the user profile at `context.attributes['user']` (for example `{#context.attributes['user'].email}`). The claim is omitted when the expression yields nothing; issuance is refused when the expression fails. |
| **Scope mappings** | Maps domain scopes to the names the authority knows them by. A requested domain scope with no mapping is refused. |

Unselecting **Cross App Access** disables it but keeps its settings, so they come back when you select it again.

### SPIFFE settings

| Setting | Description |
|:--------|:------------|
| **Signing algorithms** | Algorithms accepted for JWT-SVIDs signed by this trust domain. Leave empty to inherit the domain default from **Workload Identity > SPIFFE Settings**. `none` and HMAC algorithms are always rejected. |

SPIFFE authentication must also be enabled on the security domain. See [Configure SPIFFE and CIMD Settings](configure-spiffe-and-cimd-settings.md).

## Key retrieval

The **Key retrieval** tab of **Settings > Security > Trusted Domains** sets how AM fetches and caches keys from JWKS URLs. These limits apply to every trusted domain of the security domain, whichever usage it serves. They are checked both when a trusted domain is saved and when the gateway fetches keys.

| Setting | Field | Default |
|:--------|:------|:--------|
| **Allow unsecured HTTP JWKS URLs** | `allowUnsecuredHttpUri` | `false` |
| **Allow JWKS URLs resolving to private IP addresses** | `allowPrivateIpAddress` | `false` |
| **Fetch timeout (ms)** | `fetchTimeoutMs` | `5000` |
| **Max JWKS response size (KB)** | `maxResponseSizeKb` | `32` |
| **Cache TTL (seconds)** | `cacheTtlSeconds` | `300` |
| **Cache max entries** | `cacheMaxEntries` | `50` |

A cached JWK set is refreshed after the trusted domain's refresh interval or the cache TTL, whichever is shorter. A token signed with an unknown `kid` triggers a new fetch. If a refresh fails, the previously fetched keys are kept.

These settings are stored on the domain under `keyRetrievalSettings`:

```
PATCH /organizations/{organizationId}/environments/{environmentId}/domains/{domain}
Content-Type: application/json

{
  "keyRetrievalSettings": {
    "allowUnsecuredHttpUri": false,
    "allowPrivateIpAddress": false,
    "fetchTimeoutMs": 5000,
    "maxResponseSizeKb": 32,
    "cacheTtlSeconds": 300,
    "cacheMaxEntries": 50
  }
}
```

{% hint style="info" %}
The same fields under `oidc.workloadIdentitySettings` are deprecated. They are still accepted and applied to `keyRetrievalSettings`.
{% endhint %}

## Management API

Trusted domains are managed with the `/trusted-domains` endpoints. They require the `DOMAIN_TRUST_DOMAIN` permission.

| Method | Path |
|:-------|:-----|
| `GET` | `/organizations/{organizationId}/environments/{environmentId}/domains/{domain}/trusted-domains` |
| `POST` | `/organizations/{organizationId}/environments/{environmentId}/domains/{domain}/trusted-domains` |
| `GET` | `/organizations/{organizationId}/environments/{environmentId}/domains/{domain}/trusted-domains/{trustedDomainId}` |
| `PUT` | `/organizations/{organizationId}/environments/{environmentId}/domains/{domain}/trusted-domains/{trustedDomainId}` |
| `DELETE` | `/organizations/{organizationId}/environments/{environmentId}/domains/{domain}/trusted-domains/{trustedDomainId}` |

The following example creates a trusted domain that serves both token exchange and SPIFFE from the same JWKS URL:

```
POST /organizations/{organizationId}/environments/{environmentId}/domains/{domain}/trusted-domains
Content-Type: application/json

{
  "name": "acme",
  "description": "Acme Corp",
  "domainIdentifier": "https://sso.acme.com",
  "keyMaterial": {
    "source": "JWKS_URL",
    "jwksUrl": "https://sso.acme.com/.well-known/jwks.json",
    "refreshIntervalSeconds": 300
  },
  "spiffe": {
    "spiffeTrustDomain": "prod.acme.com",
    "allowedAlgorithms": ["RS256", "ES256"]
  },
  "tokenExchange": {
    "enabled": true,
    "scopeMappings": { "acme:read": "read" },
    "userBindingEnabled": true,
    "userBindingCriteria": [
      { "attribute": "emails.value", "expression": "{#token['email']}" }
    ]
  }
}
```

| Field | Description |
|:------|:------------|
| `name` | Label of the trusted domain. Required, unique within the security domain. |
| `description` | Optional description. |
| `domainIdentifier` | Issuer URL. Required for token exchange and Cross App Access, unique within the security domain. |
| `keyMaterial.source` | `JWKS_URL`, `JWK_SET` or `PEM`. |
| `keyMaterial.jwksUrl` | JWKS endpoint, when `source` is `JWKS_URL`. |
| `keyMaterial.refreshIntervalSeconds` | Refresh interval of the JWKS endpoint. Default `300`. |
| `keyMaterial.jwkSet` | Inline JWK set, when `source` is `JWK_SET`. |
| `keyMaterial.certificate` | PEM-encoded X.509 certificate, when `source` is `PEM`. |
| `spiffe.spiffeTrustDomain` | SPIFFE trust domain, without the `spiffe://` scheme. Lowercased on save. |
| `spiffe.allowedAlgorithms` | Signing algorithms accepted for JWT-SVIDs. Empty to inherit the domain default. |
| `tokenExchange.enabled` | Enables the token exchange usage. |
| `tokenExchange.scopeMappings` | External scope to domain scope. |
| `tokenExchange.userBindingEnabled` | Enables user binding. |
| `tokenExchange.userBindingCriteria` | List of `attribute` and `expression` pairs. |
| `crossAppAccess.enabled` | Enables the Cross App Access usage. |
| `crossAppAccess.resourceServers` | List of `name` and `resource` pairs. AM generates an `id` for each resource server; send it back on update to keep it. |
| `crossAppAccess.audSubMapping` | EL expression producing the `aud_sub` claim. |
| `crossAppAccess.scopeMappings` | Domain scope to external scope. |

A trusted domain must declare at least one usage: `spiffe`, `tokenExchange` or `crossAppAccess`.

On `PUT`, `name`, `domainIdentifier` and each of `keyMaterial`, `spiffe`, `tokenExchange` and `crossAppAccess` are kept when absent from the request, and replaced as a whole when present. `description` is always replaced. To stop accepting tokens from an issuer for token exchange, send `"tokenExchange": { "enabled": false }`.

## Deprecated APIs

The following APIs are deprecated and will be removed in a later version:

* The `/trust-domains` endpoints from AM 4.12 still work, with their 4.12 request body. A trusted domain created through them serves the SPIFFE usage, with its name as SPIFFE trust domain. Use `/trusted-domains` instead.
* The `tokenExchangeSettings.trustedIssuers` list in the domain settings is kept in sync with the trusted domains that serve token exchange. Writing it creates, updates or removes those trusted domains. Use `/trusted-domains` instead.
