## Overview

Magic Link Authentication enables passwordless login by sending users a time-limited authentication link via email. When users click the link, they are authenticated without entering a password. This feature is designed for API administrators configuring authentication flows and developers integrating passwordless login into applications.

## Key concepts

### Magic Link Token

A JWT token embedded in the authentication email link. The token includes standard claims (issuer, subject, audience, expiration, issued-at) and an optional `session_id` claim if present in the original request. Tokens expire after 15 minutes by default. The `session_id` query parameter is consumed during token generation and removed from subsequent redirect URLs.

### Email Template System

Magic Link authentication requires two templates: an email template (`MAGIC_LINK`) containing the authentication link, and a form template (`MAGIC_LINK_LOGIN`) where users enter their email address. Both templates are available only when Magic Link authentication is enabled in login settings.

### Audit Event Type

Successful Magic Link authentications generate a `USER_MAGIC_LINK_LOGIN` audit event. Analytics support includes a `magic_link` field type for reporting and filtering authentication events.

## Prerequisites

Before configuring Magic Link authentication, ensure the following requirements are met:

* Email service configured and operational
* User accounts with valid email addresses
* Domain or application login settings accessible for configuration

## Gateway configuration

### Email service properties

Configure the following properties to control Magic Link email behavior:

| Property | Description | Default |
|:---------|:------------|:--------|
| `user.magic.link.login.email.subject` | Subject line for magic link emails | `"Sign in"` |
| `user.magic.link.login.time.value` | Token expiration time value | `15` |
| `user.magic.link.login.time.unit` | Token expiration time unit | `MINUTES` |

### Login settings

| Property | Description | Default |
|:---------|:------------|:--------|
| `magicLinkAuthEnabled` | Enable or disable Magic Link authentication | `false` |

## Enabling Magic Link authentication

To enable Magic Link authentication:

1.  Navigate to login settings in the management console.
2. Enable the Magic Link authentication option.
3. Configure email service properties if defaults are insufficient.
4. Save settings.

When enabled, the `/magic-link/login` endpoint becomes available and email/form templates are activated. The system validates template availability based on the `magicLinkAuthEnabled` flag. If disabled, Magic Link templates are filtered from available forms. UI components filter Magic Link login forms based on the `allowMagicLink()` check, hiding the template when disabled.

## User authentication flow

Users authenticate via Magic Link using the following process:

1. Navigate to `/magic-link/login` and enter an email address in the form.
2. The system generates a JWT token with the user's email as subject, client ID as audience (if client exists), and optional `session_id` claim from query parameters. The `session_id` query parameter is consumed during token generation and removed from subsequent redirect URLs.
3. An email containing the authentication link (`{domain}/magic-link/auth?token={jwt_token}`) is sent asynchronously via cached thread pool. Delivery failures are logged but don't block the authentication request.
4. Click the link within the expiration window (default 15 minutes).
5. The gateway validates the token. On success, the user is authenticated and a `USER_MAGIC_LINK_LOGIN` audit event is logged. On failure, a generic error message ("Invalid user") is displayed to prevent user enumeration attacks.

## Restrictions

* Magic Link authenticator plugin (`gravitee-am-authenticator-magiclink`) is commented out in distribution artifacts and is not yet included in releases
* Token expiration is fixed at configuration time; runtime adjustment requires gateway restart
* Email sending uses asynchronous execution via cached thread pool; delivery failures are logged but don't block the authentication request
* Error messages are generic ("Invalid user") to prevent user enumeration attacks
* The `session_id` query parameter is consumed during token generation and isn't forwarded in redirect URLs
* The `MAGIC_LINK` and `MAGIC_LINK_LOGIN` templates are unavailable if `magicLinkAuthEnabled` is `false`

## Related changes

The Management API now includes authenticator plugin handler dependencies to support Magic Link configuration. Analytics dashboards support the `magic_link` field type for filtering authentication events. Localization files include English and French labels for Magic Link UI elements, error messages, and form instructions. The `gravitee-node` dependency was updated from 7.18.2 to 7.23.0 to support underlying framework requirements.
