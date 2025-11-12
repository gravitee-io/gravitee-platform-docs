---
description: >-
  This article covers the new features released in Gravitee Access Management
  4.1
---

# AM 4.1

## MFA Challenge policy

The MFA Challenge policy is an [Enterprise Edition](../../overview/open-source-vs-enterprise-am/) policy plugin. It allows a security domain or application owner to apply an MFA step to enforce security and ensure that the user account has not been compromised. The MFA Factor used for the challenge can be specified. For more information, see [this section](docs/am/4.1/guides/multi-factor-authentication/mfa-security.md#mfa-challenge-policy).

<figure><img src="../../.gitbook/assets/mfa challenge policy.png" alt=""><figcaption><p>Password reset triggers MFA Challenge</p></figcaption></figure>

## Twilio phone factor enhancement

The enrollment screen for a Twilio phone factor now offers an optional field in which to enter an extension. If an extension is present in the user's enrollment data, the MFA call utilizes Twilio's sendDigits function to direct the call to the extension before playing the audible message containing the MFA code.

## Account linking

The Account Linking feature automatically links user accounts from various identity providers to the primary account created during initial registration if the user attributes are identical. A user who is recognized and associated with an existing profile is allowed to authenticate from other accounts without having to re-enroll. For more information, see [this page](docs/am/4.1/guides/user-management/account-linking.md).

<figure><img src="../../.gitbook/assets/account linking_flows.png" alt=""><figcaption><p>Apply account linking at the security domain level</p></figcaption></figure>

## Session management

4.1 introduces a session cookie option that allows the end user to consent to a "remember me" feature. With this option selected, the user is not logged out of an application after a period of idling and the session expiration corresponds to what has been set at the security domain level. For more information, see [this section](docs/am/4.1/guides/session-management.md#session-cookie-option).
