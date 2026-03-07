### Overview

Magic Link Authentication enables passwordless login by sending users a time-limited authentication link via email. When users click the link, they are authenticated and redirected to the application without entering credentials. This feature is designed for API administrators configuring domain-level authentication options and developers integrating passwordless flows.

### Key Concepts

#### Magic Link Token

A JWT-based token embedded in the authentication email URL. The token includes a `session_id` claim to bind the authentication attempt to the user's browser session and expires after a configurable time window (default: 15 minutes). Tokens are single-use and can't be reused after successful authentication.

#### Email-Based Authentication Flow

Users initiate login by submitting their email address. The system generates a magic link token, sends it via email, and validates the token when the user clicks the link. On successful validation, the user is redirected to the authorization endpoint with an authorization code, completing the OAuth 2.0 flow.

#### Template Integration

Magic link authentication uses two HTML templates: `magic_link_login` (the email submission form at `/magic-link/login`) and `magic_link` (the token validation handler at `/magic-link/auth`). Templates receive context variables including `allowMagicLink`, `magicLinkAction` (the form submission URL), and email-specific variables (`client.name`, `url`, `expireAfterSeconds`).

### Prerequisites

Before enabling magic link authentication, ensure the following requirements are met:

* Email service must be configured and operational
* Domain must have login settings enabled
* Users must have valid email addresses registered in the identity provider
* Email templates (`magic_link_login.html` and `magic_link.html`) must be available

### Gateway Configuration

#### Email Service Settings

Configure magic link email behavior in `gravitee.yml`:

| Property | Description | Default |
|:---------|:------------|:--------|
| `user.magic.link.login.email.subject` | Subject line for authentication emails | `"Sign in"` |
| `user.magic.link.login.time.value` | Token expiration time value | `15` |
| `user.magic.link.login.time.unit` | Token expiration time unit | `MINUTES` |

{% code title="gravitee.yml" %}
```yaml
user:
  magic:
    link:
      login:
        email:
          subject: Sign in
        time:
          unit: MINUTES
          value: 15
```
{% endcode %}

#### Domain Login Settings

Enable magic link authentication at the domain level by setting the `magicLinkAuthEnabled` property:

| Property | Description | Default |
|:---------|:------------|:--------|
| `loginSettings.magicLinkAuthEnabled` | Enable/disable magic link authentication | `false` |

Example domain patch request:

```json
{
  "loginSettings": {
    "magicLinkAuthEnabled": true
  }
}
```

### Enabling Magic Link Authentication

Enable the feature by patching the domain's login settings with `magicLinkAuthEnabled: true`. Once enabled, the login page displays a "Sign in with Magic Link" button alongside other authentication methods. Users click the button, enter their email address (validated for correct format), and submit the form. The system sends an email containing the magic link URL with an embedded token. When the user clicks the link, the gateway validates the token and session ID, then redirects to the authorization endpoint with an authorization code if validation succeeds.

### Client Integration

Clients interact with magic link authentication through the standard OAuth 2.0 authorization code flow. After the user completes magic link authentication, the authorization endpoint returns a `code` parameter in the redirect URL. Clients exchange this code for access tokens using the token endpoint. No client-side configuration changes are required beyond initiating the authorization flow with the appropriate `client_id`.

### Restrictions

* Magic link tokens expire after the configured time window (default: 15 minutes) and can't be extended
* Tokens are single-use; clicking a magic link twice returns the error "Something went wrong, please try again"
* Invalid email formats return HTTP 302 redirects with `error_description` = "Value [input] is not a valid email."
* Invalid or expired tokens return `error_description` = "An unexpected error has occurred"
* Email delivery depends on external email service availability; failed sends aren't retried automatically
* The `gravitee-am-authenticator-magiclink` plugin (version 1.0.0) isn't yet included in the distribution and must be manually installed
* Magic link authentication requires the `gravitee-am-plugins-handlers-authenticator` module

### Related Changes

The feature adds analytics support for magic link login events under the `USER_MAGIC_LINK_LOGIN` event type, grouped by `outcome.status` and displayed as "magic link login" in the analytics UI. Audit logs capture magic link authentication attempts using the `AuthenticationMagicLinkAuditBuilder`. UI labels are localized in English and French (`messages_en.properties` and `messages_fr.properties`), including button text ("Send e-mail with authentication link"), success messages ("Magic link has been sent."), and error descriptions.
