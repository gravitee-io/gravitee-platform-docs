---
description: >-
  This article covers the new features released in Gravitee Access Management
  4.8.
---

# AM 4.8

## Client secret improvement <a href="#user-management-improvement" id="user-management-improvement"></a>

An application can now be configured to accept multiple client secrets. Each secret may have an associated expiration date, and a notification system has been implemented to alert the primary domain owner of any secrets nearing expiration. Refer to the [client-secrets.md](../../guides/applications/client-secrets.md "mention") documentation for additional details.

{% hint style="info" %}
By default, an application can accept up to 10 client secrets. This limit is configurable via the `gravitee.yaml` configuration file.
{% endhint %}

## FranceConnect v2

The [FranceConnect Identity](../../guides/identity-providers/legal-identity-providers/franceconnect.md) provider is now able to support the version 2 of the FranceConnect API.

{% include "../../.gitbook/includes/franceconnect-warning.md" %}

{% include "../../.gitbook/includes/franceconnect-required-parameter-note.md" %}

## Support for PBKDF2

MongoDB and JDBC identity providers now support the PBKDF2 password encoder.

## Custom SCIM property

The `forceResetPassword` attribute is managed as a custom property on the user profile. When this attribute is set to `true`, the user is required to update their password immediately after the login phase.

```
'urn:ietf:params:scim:schemas:extension:custom:2.0:User': {
  forceResetPassword: true
},
```

## Dynamic query parameter in redirect URI

The Dynamic Redirect URI Parameters feature in the OAuth2 flow enhances flexibility and control over redirection behavior by letting you append dynamic parameters to the final `redirect_uri`. These parameters are resolved using [Gravitee Expression Language (EL)](https://app.gitbook.com/o/8qli0UVuPJ39JJdq9ebZ/s/ySqSVpDHfKA0fNml1fVO/), which lets you insert custom logic and data into the redirect URL Refer to the [dynamic-redirect-uri-parameters.md](../../guides/auth-protocols/oauth-2.0/dynamic-redirect-uri-parameters.md "mention") documentation for additional details.
