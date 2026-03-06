### Overview

Magic Link Authentication enables passwordless login by sending users a time-limited authentication link via email. When enabled, users can request a magic link on the login page, click the link in their email, and authenticate without entering a password.

### Key Concepts

#### Magic Link Token

A time-limited JWT token embedded in an email link that authenticates a user when clicked. The token includes a `session_id` claim if the authentication request originated from an existing session. Tokens expire after a configurable duration (default: 15 minutes) and are single-use.

#### Email Template Flow

The system sends two types of emails:

* **Magic link email** — Uses the `MAGIC_LINK` template and contains a clickable button and a fallback raw URL
* **Login form confirmation** — Uses the `MAGIC_LINK_LOGIN` template

Both templates support internationalization in English and French.

#### Analytics and Auditing

Magic link logins are tracked as a distinct authentication type (`USER_MAGIC_LINK_LOGIN`) in analytics dashboards and audit logs. The system aggregates magic link login events separately from standard password logins, WebAuthn, and certificate-based authentication.

### Prerequisites

Before enabling Magic Link Authentication, ensure the following requirements are met:

* Email service must be configured and enabled
* SMTP settings must be valid and tested
* Domain must be configured for email sender address
* Users must have valid email addresses in their profiles
* `gravitee-node` version 7.23.0 or higher

### Enable Magic Link Authentication

1. Navigate to **Settings > Login**.
2. Toggle **Magic Link Authentication** to enable the feature.
3. Configure the token expiration time if needed.
4. Click **Save**.
