---
description: >-
  This article covers the new features released in Gravitee Access Management
  4.0
---

# AM 4.0

## Support for password salt formats

AM 4.0 supports the `PREPENDING`, `APPENDING`, and `DIGEST` password salt formats:

* A user can sign in to AM via the identity provider `"separate salt" + PREPENDING mode`.
* If an identity provider (either `"separate salt" + APPENDING mode` or `"separate salt" + DIGEST mode`) user with multiple passwordless roaming authenticator credentials signs in to AM, AM will display the list of credential names.

<figure><img src="../../.gitbook/assets/password salt.png" alt=""><figcaption></figcaption></figure>

## Passwordless device management

A user with a roaming authenticator or cross-platform authenticator can now name their security key to identify it when using it on other devices:

*   If a user signs in to AM and **Enable passwordless** is activated on the security domain, the user can assign a device name during configuration.&#x20;

    <figure><img src="../../.gitbook/assets/passwordless device naming management.png" alt=""><figcaption></figcaption></figure>

    <figure><img src="../../.gitbook/assets/passwordless device naming gateway.png" alt=""><figcaption></figcaption></figure>
* If a user who signs in with AM has multiple passwordless roaming authenticator credentials, AM will display the list of credential names.

## Configure token steps in flows

A Gravitee security domain or application owner can configure policies to add business logic to the PRE and POST creation of access tokens. This functionality allows the user to enhance tokens for OAuth 2.0 (e.g., resource owner, refresh token, or client credentials), validate context before generating access tokens, etc.

## Initiate MFA enrollment via OpenID Connect 1.0

A Gravitee security domain or application owner can leverage an extension to the OpenID Connect Authentication Framework to let users directly access the MFA enrollment page (without having to go through the AM login flow). When an end user who wants to enroll a new MFA factor calls the OAuth 2.0 Authorization Endpoint with the `prompt=mfa_enroll` parameter during an active session, the login page is bypassed and the enroll page is displayed.

## Trigger an email verification link

An admin can require users to verify their email as part of the registration flow by enabling **Account verification via email** in the **User Accounts** section of the Access Management Console.

<figure><img src="../../.gitbook/assets/email verification.png" alt=""><figcaption></figcaption></figure>

After a user submits the AM registration form, they will receive an email with a link to confirm their account. If an unverified user does not validate their account, an admin can manually trigger a resend of the email verification link via the user's **Profile** in the **Users** section of the AM Console.

<figure><img src="../../.gitbook/assets/resend email verification.png" alt=""><figcaption></figcaption></figure>
