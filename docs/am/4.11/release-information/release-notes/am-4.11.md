# AM 4.11

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:AM-6338 -->
#### **Magic Link Authentication**

* Enables passwordless login by sending users a time-limited authentication link via email, eliminating the need to enter credentials.
* Users submit their email address on the login page, receive a magic link token (valid for 15 minutes by default), and are authenticated when they click the link.
* Requires email service configuration in `gravitee.yml` and must be enabled at the domain level via `loginSettings.magicLinkAuthEnabled`.
* Tokens are single-use and bound to the user's browser session via a `session_id` claim for security.
* Integrates with the standard OAuth 2.0 authorization code flow—no client-side configuration changes required beyond initiating the authorization flow.
<!-- /PIPELINE:AM-6338 -->

## Improvements

## Bug Fixes
