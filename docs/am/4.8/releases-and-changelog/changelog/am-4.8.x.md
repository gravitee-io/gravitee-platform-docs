---
description: >-
  This page contains the changelog entries for AM 4.8.0 and any future minor or
  patch AM 4.8.x releases
---

# AM 4.8.x

## AM 4.8.x

#### Gravitee Access Management 4.8 - June 30, 2025 <a href="#gravitee-access-management-4.5-october-10-2024" id="gravitee-access-management-4.5-october-10-2024"></a>

<details>

<summary>What's new</summary>

Client secret improvement

An application can now be configured to accept multiple client secrets. Each secret may have an associated expiration date, and a notification system has been implemented to alert the primary domain owner of any secrets nearing expiration. Refer to the [client-secrets.md](../../guides/applications/client-secrets.md "mention") documentation for additional details.

#### FranceConnect

The [FranceConnect Identity](../../guides/identity-providers/legal-identity-providers/franceconnect.md) provider is now able to support the version 2 of the FranceConnect API.

#### Support for PBKDF2

MongoDB and JDBC identity providers now support the PBKDF2 password encoder.

#### Custom SCIM property

The `forceResetPassword` attribute is managed as a custom property on the user profile. When this attribute is set to `true`, the user is required to update their password immediately after the login phase.

```
'urn:ietf:params:scim:schemas:extension:custom:2.0:User': {
  forceResetPassword: true
},
```

#### Dynamic query parameter in redirect URI

The Dynamic Redirect URI Parameters feature in the OAuth2 flow enhances flexibility and control over redirection behavior by letting you append dynamic parameters to the final `redirect_uri`. These parameters are resolved using [Gravitee Expression Language (EL)](https://app.gitbook.com/s/ySqSVpDHfKA0fNml1fVO/), which lets you insert custom logic and data into the redirect URL Refer to the [dynamic-redirect-uri-parameters.md](../../guides/auth-protocols/oauth-2.0/dynamic-redirect-uri-parameters.md "mention") documentation for additional details.

</details>

[\
](https://documentation.gravitee.io/am/releases-and-changelog/changelog)
