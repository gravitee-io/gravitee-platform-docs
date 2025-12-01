---
description: >-
  This article covers the new features released in Gravitee Access Management
  4.9.
---

# AM 4.9

## OpenID provider improvement

The [OpenID identity provider ](../../guides/identity-providers/social-identity-providers/openid-connect.md)has been updated to support the `application/jwt` content type at the [UserInfo Endpoint](https://openid.net/specs/openid-connect-core-1_0.html#UserInfoResponse).&#x20;

The system accepts only signed JWT tokens. Signature validation is handled by the [Public Key Resolver](../../guides/identity-providers/social-identity-providers/openid-connect.md#public-key-resolver) defined in the provider's configuration.

## Support schema with PostgreSQL backend

You can now specify the [schema](https://www.postgresql.org/docs/current/ddl-schemas.html) when Access Management is configured with a PostgreSQL backend. For more information, see the [repositories](../../getting-started/configuration/configure-repositories.md#jdbc) section.

## Rate Limit policy

Access Management now offers a Rate Limit policy that is functionally equivalent to the API Management Rate Limit policy. You can use Gravitee Expression Language to enforce a limit per client ID.

## Audit logs

A new audit log is generated for multi-factor authentication (MFA). When a user selects the "remember device" option during the MFA challenge phase, an MFA\_REMEMBER\_DEVICE audit [event](../../guides/audit-trail.md#event-types) is created.

The improved MongoDB audit log implementation uses secondary nodes for search requests. This behavior is [configurable](../../getting-started/configuration/configure-reporters.md#mongodb-reporter) in the `gravitee.yaml` of the Management API.

## Extension Grant improvement

The [Extension Grant](../../guides/auth-protocols/oauth-2.0/extension-grants.md) plugin now supports using a JWKS\_URL to retrieve the public key that processes the `assertion` parameter.

## Events Retention

The update requests received by the Management API are communicated to the Gateways through database records called "events." These events are used solely for Gateway synchronization.

If a Gateway restarts, it reads its configuration directly from the database, and then queries the events table for any changes that occurred. With this architecture, events records don't need to be retained indefinitely.

Access Management version 4.9 implements a 90-day retention policy on the events table. To achieve this, a TTL (Time-to-Live) index is created for installations that use a MongoDB backend. For installations that use an RDBMS backend, a purge service runs daily, at 11:00 PM by default.&#x20;

{% hint style="info" %}
The MongoDB index is created automatically on the Management API, at Gateway startup.
{% endhint %}

## Prompt password changed when password is expired

A new option is available to require users to reset their passwords after a configurable time period has elapsed since their last reset. Upon successful login, if the password has expired, users are immediately prompted to set a new password before continuing the login flow. See the [force reset password page](../../guides/login/force-reset-password-on-expiration.md) for more details.
