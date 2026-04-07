---
description: >-
  This article covers the new features released in Gravitee Access Management
  4.11.
---

# AM 4.11

## Highlights

* Magic Link Authentication enables passwordless login by sending time-limited, JWT-based authentication links via email.
* Domain-level certificate fallback prevents authentication failures by automatically using a backup certificate when an application's configured certificate can't load.
* Protected Resources support full OAuth 2.0 client lifecycle management with multiple client secrets, certificate-based auth, and RFC 8693 token exchange audience resolution.
* OAuth 2.0 Token Exchange (RFC 8693) enables clients to exchange security tokens for impersonation and delegation scenarios with configurable scope handling and trusted external JWT issuers.
* JWKS Resolver can now use the httpClient configuration.
* JDBC and Mongo reporters now support audits retention.
* SAML identity provider plugin can not be configured using metadata

## New Features

#### **Magic Link Authentication**

* Enables passwordless login by sending users a time-limited authentication link via email, eliminating the need to enter passwords during sign-in.
* Users enter their email address at `/magic-link/login`, receive a JWT-based authentication link valid for 15 minutes (configurable), and are authenticated when they click the link.
* Requires email service configuration and must be enabled in domain or application login settings via the `magicLinkAuthEnabled` property.
* Generates `USER_MAGIC_LINK_LOGIN` audit events for successful authentications and supports analytics filtering via the `magic_link` field type.
* Token expiration time is configurable via `user.magic.link.login.time.value` and `user.magic.link.login.time.unit` gateway properties (defaults to 15 minutes).

#### **Domain-Level Certificate Fallback**

* Administrators can configure a fallback certificate at the domain-level to prevent authentication failures when a certificate that is explicitly configured for an application cannot be used.
* When an application's certificate fails to load (e.g., external provider unavailable), the system automatically uses the domain's fallback certificate to sign OAuth and ID tokens.
* Fallback certificates are configured using the Management API (`/domains/{domain}/certificate-settings`) and require `DOMAIN_SETTINGS[UPDATE]` permission.
* Certificates configured as domain fallback cannot be deleted until removed from the fallback configuration.

#### **Protected Resource OAuth 2.0 Client Management**

* Protected Resources now support full OAuth 2.0 client lifecycle management, including multiple client secrets with independent expiration dates and certificate-based authentication for JWT signature verification.
* Secret rotation is enabled through the Management API, with server-generated secrets returned only once during creation or renewal to ensure secure credential handling.
* Token introspection resolves audience claims against both Applications and Protected Resources, with automatic fallback to RFC 8707 resource identifiers for multi-audience JWTs.
* MCP Servers configured as Protected Resources are restricted to `client_credentials` and `urn:ietf:params:oauth:grant-type:token-exchange` grant types, with authentication methods limited to `client_secret_basic`, `client_secret_post`, and `client_secret_jwt`.
* Requires AM 4.11.0+ with OAuth 2.0 enabled at the domain level; token exchange flows require `tokenExchangeSettings.enabled = true` in domain configuration.



#### **OAuth 2.0 Token Exchange (RFC 8693)**

* Enables clients to exchange security tokens for new tokens, supporting impersonation (acting as another user) and delegation (acting on behalf of another user) scenarios.
* Supports access tokens, refresh tokens, and ID tokens as input and output, with configurable scope handling modes (downscoping or permissive) to control granted permissions.
* Allows administrators to configure trusted external JWT issuers with JWKS or PEM-based key resolution, scope mappings, and user binding rules via EL expressions.
* Impersonation is enabled by default; delegation requires explicit configuration via `allowDelegation` setting.

## Improvements

#### JWKS Resolver

The default JWKS Resolver is using a Java class HttpURLConnection to fetch a remote JWKS. This default implementation is not using the `httpClient` settings in the gravitee.yaml which may lead to extra configuration using JAVA\_OPTS to configure the proxy settings or the truststore.&#x20;

In 4.11, a new resolver implementation has been introduce to rely on the httpClient. To enable this configuration, you have to spcify `gravitee_jwt_jwks_retriever_type=WEBCLIENT` as environment variable or in the gravitee.yaml.

```yml
jwt:
  jwks:
    retriever:
     type: WEBCLIENT # default value JOSE
```

#### Audits Retention

To simplify operations, we are moving away from manual "Time to Live" (TTL) management by the Platform Team. A new Purge Service is now available via the Management API to automate the deletion of audit logs.

{% hint style="warning" %}
_This capability is currently optional and disabled by default in 4.11. It will be enabled by default starting with version 4.12._
{% endhint %}

#### SAML Identity provider

Metadata for a SAML 2.0 identity provider (IdP) can be provided in one of following ways:

* Metadata URL: The configuration is supplied by a remote SAML 2.0 metadata xml endpoint. This allows for the dynamic exchange of metadata while reducing the likelihood of configuration errors. Fetching and updating configuration of the IdP occurs at startup of the AM and its plugins.
* Metadata File: The metadata is imported from an XML file. This is an alternative approach to hosting the metadata where security and versioning can be strictly controlled by static files, without a network dependency on startup.
* Manual: The metadata values are supplied individually to AM
