---
hidden: false
noIndex: false
---

# Secure your API proxy
<!-- GAP-STRUCTURAL: Missing procedural content source -->

After creating an API proxy, attach one or more security plans to control how consumers authenticate. Plans define the authentication mechanism the API Gateway enforces at runtime — every incoming request is evaluated against the active plans before it reaches your backend.

## Plan types

The Gamma console supports five plan types. You can attach multiple plans to a single API proxy; the Gateway evaluates them in order and uses the first plan that matches the consumer's credentials.

### Keyless

No authentication required. Any consumer can call the API without credentials.

{% hint style="warning" %}
Keyless plans provide no consumer identification. You cannot track usage per consumer, revoke individual access, or enforce per-consumer rate limits. Use keyless only for internal testing, health checks, or truly public endpoints.
{% endhint %}

### API Key

Consumers include an API key in the request header or query parameter. The Gateway validates the key against issued keys and identifies the consuming application.

**When to use:** Simple consumer tracking, rate limiting per key, onboarding flows where OAuth complexity isn't justified.

### JWT

Consumers present a signed JSON Web Token (JWT). The Gateway verifies the signature using a configured JWKS endpoint or certificate, then extracts claims for downstream use.

**Configuration fields:**

| Field                   | Description                                                          |
| ----------------------- | -------------------------------------------------------------------- |
| **Signature algorithm** | The algorithm used to verify JWT signatures.                         |
| **JWKS resolver**       | How the Gateway resolves the public keys for signature verification. |
| **Resolver parameter**  | The JWKS URL or certificate.                                         |

**When to use:** Integration with external identity providers, fine-grained claims-based access control, enterprise SSO.

### OAuth2

Consumers present an OAuth 2.0 access token. The Gateway validates the token against a configured OAuth2 resource using token introspection.

**Configuration fields:**

| Field               | Description                                                                                        |
| ------------------- | -------------------------------------------------------------------------------------------------- |
| **OAuth2 resource** | The OAuth2 resource configured in the Gamma console that the Gateway uses for token introspection. |

**When to use:** Delegated authorization, enterprise identity providers, scenarios requiring scope-based access control.

### mTLS

Consumers present a client TLS certificate during the TLS handshake. The Gateway validates the certificate against trusted certificate authorities.

**When to use:** Machine-to-machine communication, zero-trust network environments, internal service mesh.

## Add a plan to an existing API proxy

<figure><img src="https://3745118555-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fa6QVD3iIxTvnV5eQ8OH1%2Fuploads%2Fgit-blob-b86bcd2b3acadc6112d18f8ea50420e0d7e63a68%2Fgamma-api-plans.png?alt=media" alt="Plans management page with lifecycle cards"><figcaption><p>The Plans page shows plan lifecycle cards (Staging, Published, Deprecated, Closed) and a table listing each plan's name, security type, status, and validation mode.</p></figcaption></figure>

Plans are managed from the **Consumer Access → Plans** tab in the API detail sidebar.

1. Navigate to the API detail page for your API proxy.
2. In the sidebar, open **Consumer Access → Plans**.
3. Select **Create plan** and choose a plan type from the dropdown:

| Plan type   | Available for API proxies | Available for API products |
| ----------- | :-----------------------: | :------------------------: |
| **API Key** |             ✓             |              ✓             |
| **JWT**     |             ✓             |              ✓             |
| **OAuth2**  |             ✓             |              —             |
| **mTLS**    |             ✓             |              ✓             |
| **Keyless** |             ✓             |              —             |

4. Complete the plan creation wizard. The wizard steps vary depending on the plan type and context:

| Context                                   | Plan type   | Wizard steps                                  |
| ----------------------------------------- | ----------- | --------------------------------------------- |
| API proxy + API Key, JWT, OAuth2, or mTLS | non-Keyless | **General** → **Security** → **Restrictions** |
| API proxy + Keyless                       | Keyless     | **General** → **Restrictions**                |
| API product + API Key, JWT, or mTLS       | non-Keyless | **General** → **Security**                    |
| API product + Keyless                     | Keyless     | **General** only                              |

### Step 1: General

Configure the plan's metadata and access control settings.

| Field                       | Description                                                                                                                      | Default    |
| --------------------------- | -------------------------------------------------------------------------------------------------------------------------------- | ---------- |
| **Name**                    | Human-readable plan name.                                                                                                        | (required) |
| **Description**             | Freeform description of the plan's purpose.                                                                                      | (empty)    |
| **Characteristics**         | Tags describing the plan.                                                                                                        | (empty)    |
| **General conditions**      | Terms of service or usage conditions.                                                                                            | (empty)    |
| **Subscription validation** | **Auto** (subscriptions are approved immediately) or **Manual** (API owner must approve each subscription).                      | Manual     |
| **Comment required**        | Require consumers to describe their use case when subscribing. When enabled, a custom message field appears (max 64 characters). | Off        |
| **Sharding tags**           | Restrict the plan to gateways with matching sharding tags. Only appears if organization-level tags are configured.               | None       |
| **Groups excluded**         | Consumer groups that cannot subscribe to this plan. Only appears for API proxy plans (not API products).                         | None       |

### Step 2: Security (skipped for Keyless)

Configure authentication settings specific to the selected plan type.

**API Key plans:**

| Field                                 | Description                                                                          | Default                         |
| ------------------------------------- | ------------------------------------------------------------------------------------ | ------------------------------- |
| **Propagate API Key to upstream API** | Forward the API Key header to the backend service after gateway validation.          | Off                             |
| **Custom API Key header**             | Override the default API Key header name.                                            | Off (uses `X-Gravitee-Api-Key`) |
| **API Key header name**               | The header name used to pass the API key (only shown when custom header is enabled). | `X-Gravitee-Api-Key`            |

**JWT plans:**

Configure JWT signature verification. The Gateway validates the token signature and extracts claims for policy evaluation.

**OAuth2 plans:**

Select an OAuth2 resource for token introspection. The Gateway forwards the access token to the configured resource for validation.

**mTLS plans:**

No additional configuration required. Consumers are identified by the X.509 certificate presented during the TLS handshake.

**Additional selection rule (all non-Keyless types):**

For APIs with multiple plans of the same security type, define an additional selection rule using an Expression Language (EL) expression. For example:

```
{#context.attributes['jwt'].claims['iss'] == 'my-issuer'}
```

### Step 3: Restrictions (API proxy plans only)

Configure rate limits, quotas, and resource access rules for the plan.

**Rate Limiting:**

Limit the number of HTTP requests an application can make per second or minute.

| Field              | Default               |
| ------------------ | --------------------- |
| **Max requests**   | 10                    |
| **Period**         | 1                     |
| **Unit**           | Seconds               |
| **Error strategy** | Fallback pass-through |

**Quota:**

Limit the number of HTTP requests an application can make per hour, day, week, or month.

| Field                      | Default |
| -------------------------- | ------- |
| **Max requests**           | 100     |
| **Period**                 | 1       |
| **Unit**                   | Hours   |
| **Add rate limit headers** | On      |

**Resource Filtering:**

Restrict access to specific API paths using whitelist and/or blacklist rules. Each rule specifies a URL pattern and the HTTP methods it applies to. Supported HTTP methods: `GET`, `POST`, `PUT`, `PATCH`, `DELETE`, `OPTIONS`, `HEAD`, `TRACE`, `CONNECT`.

When resource filtering is enabled, additional path normalization options appear:

* **Normalize request path** — Normalize the incoming request path before matching rules.
* **Decode encoded slash** — Decode `%2F` in the request path (only available when normalization is enabled).

5. Select **Create plan** to save. The plan is created in **Staging** status.

## Plan lifecycle

Each plan moves through a defined lifecycle:

| Status         | Description                                                                                                                                             |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Staging**    | Initial status after creation. The plan is not available for subscriptions. Use staging to configure and review plans before opening them to consumers. |
| **Published**  | The plan is active and available for consumer subscriptions.                                                                                            |
| **Deprecated** | The plan no longer accepts new subscriptions, but existing subscriptions remain active.                                                                 |
| **Closed**     | The plan is deactivated. All subscriptions are terminated.                                                                                              |

## Plan evaluation order

When multiple plans are attached to an API proxy, the Gateway evaluates them in the order determined by the plan's `order` field. The first plan whose authentication mechanism matches the incoming request is used. If no plan matches, the request is rejected.

{% hint style="info" %}
The Gamma console does not currently expose a plan reordering mechanism. Plan evaluation order is determined by the internal `order` field set at creation time.
{% endhint %}

## Next steps

* [Establish consumer access](configure-your-api-proxy/establish-consumer-access.md) — Create applications, manage subscriptions, and issue API keys for your plans.
* [Apply security policies](configure-your-api-proxy/apply-security-policies.md) — Add fine-grained authorization and request/response policies on top of your security plans.
