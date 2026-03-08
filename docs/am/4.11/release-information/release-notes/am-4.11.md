# AM 4.11

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:AM-6338 -->
#### **Magic Link Authentication**

* Enables passwordless login by sending users a time-limited authentication link via email, eliminating the need to enter passwords during sign-in.
* Users enter their email address at `/magic-link/login`, receive a JWT-based authentication link valid for 15 minutes (configurable), and are authenticated when they click the link.
* Requires email service configuration and must be enabled in domain or application login settings via the `magicLinkAuthEnabled` property.
* Generates `USER_MAGIC_LINK_LOGIN` audit events for successful authentications and supports analytics filtering via the `magic_link` field type.
* Token expiration time is configurable via `user.magic.link.login.time.value` and `user.magic.link.login.time.unit` gateway properties (defaults to 15 minutes).
<!-- /PIPELINE:AM-6338 -->

## Improvements

## Bug Fixes
