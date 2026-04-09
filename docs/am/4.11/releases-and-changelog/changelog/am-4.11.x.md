---
description: >-
  This page contains the changelog entries for AM 4.11.0 and any future minor or
  patch AM 4.11.x releases.
---

# AM 4.11.x

#### Gravitee Access Management 4.11 - April 3, 2026 <a href="#gravitee-access-management-4.8" id="gravitee-access-management-4.8"></a>

<details>

<summary><strong>What's new</strong></summary>

**Magic Link Authentication**

Magic Link Authentication enables passwordless login by sending time-limited, JWT-based authentication links via email.

**Certificate fallback**

Domain-level certificate fallback prevents authentication failures by automatically using a backup certificate when an application's configured certificate can't load.

**SAML IdentityProvider plugin**

SAML 2.0 identity provider can be initialized by providing metadata in one of following ways:\
Metadata URL, Metadata File.

**Protected Resources improvements**

Protected Resources support full OAuth 2.0 client lifecycle management with multiple client secrets, certificate-based auth, and RFC 8693 token exchange audience resolution.

**OAuth 2.0 Token Exchange (RFC 8693)**

OAuth 2.0 Token Exchange (RFC 8693) enables clients to exchange security tokens for impersonation and delegation scenarios with configurable scope handling and trusted external JWT issuers.

**JWKS Resolver**

A new JWKS resolver implementation has been introduce to rely on the httpClient settings defined in the gravitee.yaml.&#x20;

**Audits Retention**

To simplify operations, we are moving away from manual "Time to Live" (TTL) management by the Platform Team. A new Purge Service is now available via the Management API to automate the deletion of audit logs.

{% hint style="warning" %}
_This capability is currently optional and disabled by default in 4.11. It will be enabled by default starting with version 4.12._
{% endhint %}

</details>

<details>

<summary><strong>Deprecation Notice</strong></summary>

AM 4.12 will be the last release to support application-level password policies. This feature, deprecated since v4.4.0, will be strictly removed in upcoming versions. Please ensure your security settings are migrated to the supported policy levels.

AM 4.12 will be the last release to support the `openid` scope client\_credentials flow. This is effectively the case since AM 4.3.0 but a setting has been introduced to keep this behavior for backward compatibility. This settings will be removed.

</details>

<details>

<summary><strong>Breaking Changes</strong></summary>

When an application sign a token, HMAC signature is not used as fallback mechanism anymore if the application certificate is not available. &#x20;

</details>

## Gravitee Access Management 4.11.1 - April 9, 2026

<details>

<summary>Bug fixes</summary>

**Gateway**

* EnrichAuthContext ignored when session is active [#11301](https://github.com/gravitee-io/issues/issues/11301)

**Management API**

* Improve list domain response time [#11315](https://github.com/gravitee-io/issues/issues/11315)

**Console**

* User History - event names are truncated [#11290](https://github.com/gravitee-io/issues/issues/11290)
* Re: Audit Logs - Column "Target" is truncated [#11291](https://github.com/gravitee-io/issues/issues/11291)

**Other**

* Force reset password not prompting user to reset password during login [#11298](https://github.com/gravitee-io/issues/issues/11298)
* Force ordering for application search [#11309](https://github.com/gravitee-io/issues/issues/11309)

</details>


