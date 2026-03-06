### Session ID Handling

When a magic link request includes a `session_id` query parameter, the system embeds it as a JWT claim in the magic link token and removes it from the query string. This preserves session context across the email authentication flow. The `session_id` claim is accessible to downstream authentication handlers and can be used to resume interrupted flows or maintain session continuity after email verification.

### Analytics Integration

The management console displays a "Magic link Logins" pie chart in the analytics dashboard. This chart aggregates authentication events by the `magic_link` field type, providing visibility into magic link usage patterns.

### Audit System Integration

The audit system records magic link authentication events with the `USER_MAGIC_LINK_LOGIN` event type. This event type is logged alongside other authentication methods (`USER_LOGIN`, `USER_WEBAUTHN_LOGIN`, `USER_CBA_LOGIN`) for comprehensive audit trails.

### UI Changes

The login page includes a "Sign in with Magic Link" button when the feature is enabled. Context variables `allowMagicLink` and `magicLinkAction` control button visibility and form submission behavior.

### Database Schema Changes

MongoDB persists the `magicLinkAuthEnabled` flag in the `LoginSettings` collection. This flag determines whether magic link authentication is available for the domain.

### Email Template Internationalization

Email templates for magic link authentication support English and French localization. Customize the following keys to adjust messaging:

* `email.magic_link.button` — Button text
* `email.magic_link.expiration` — Expiration notice
* `email.magic_link.header.title` — Email subject and header title
* `email.magic_link.header.description.first.row` — Greeting text
* `email.magic_link.header.description.second.row` — Authentication request description
* `email.magic_link.raw.link` — Fallback link instructions

### Asynchronous Email Sending

The system sends magic link emails asynchronously using a cached thread pool. High-volume deployments should monitor thread pool behavior to ensure adequate resource allocation.

### Restrictions

* Magic link tokens are single-use and expire after the configured duration (default: 15 minutes).
* Email service must be enabled and properly configured before activating magic link authentication.
* The `MAGIC_LINK_LOGIN` form and `MAGIC_LINK` email template are available only when `magicLinkAuthEnabled` is true.
* Users must have a valid email address in their profile to receive magic links.
* The authenticator plugin (`gravitee-am-authenticator-magiclink` version 1.0.0) is currently commented out in the distribution and not included in production builds.

