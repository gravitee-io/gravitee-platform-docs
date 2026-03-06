# AM 4.11

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:AM-6338 -->
#### **Magic Link Authentication**

* Enables passwordless login by sending users a time-limited authentication link via email, eliminating the need to enter passwords during sign-in.
* Users request a magic link from the login page, receive an email with a clickable authentication button, and are automatically authenticated when they click the link.
* Requires email service configuration with valid SMTP settings and `gravitee-node` version 7.23.0 or higher.
* Magic link tokens expire after a configurable duration (default: 15 minutes) and are single-use only.
* Magic link logins are tracked separately in analytics dashboards and audit logs under the `USER_MAGIC_LINK_LOGIN` authentication type.
<!-- /PIPELINE:AM-6338 -->

## Improvements

## Bug Fixes
