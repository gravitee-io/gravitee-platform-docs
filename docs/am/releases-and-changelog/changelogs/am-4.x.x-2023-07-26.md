---
description: >-
  This page contains the changelog entries for AM 4.0 and any future minor or
  patch AM 4.x.x releases
---

# AM 4.x.x (2023-07-26)

## Gravitee Access Management 4.0 - July 20, 2023

For more in-depth information on what's new, please refer to the [Gravitee AM 4.0 release notes](../release-notes.md).

<details>

<summary>What's new</summary>

**Enterprise Edition**

Some plugins are now part of the Enterprise Edition:

* idp-saml2
* idp-ldap
* idp-azure-ad
* idp-franceconnect
* idp-salesforce
* factor-call
* factor-sms&#x20;
* factor-fido2
* factor-http
* factor-recovery-code
* factor-otp-sender
* resource-twilio

**Community Edition**

If you use the Community Edition, for each enterprise feature you will have a dedicated pop-up to suggest the enterprise version.

* Password: Password salt format option
* Flows: Add new TOKEN flow
* MFA: Initiate MFA Enrollment via OpenID Connect 1.0
* Send email verification link
* Ability to re-trigger verification email
* Passwordless: Name passwordless device

**Gateway**

* It is impossible to see the user that consented the user consent in the audit log: [#9049](https://github.com/gravitee-io/issues/issues/9049)
* Allow OTP factor to handle clock drift issues: [#9074](https://github.com/gravitee-io/issues/issues/9074)

**Management API**

* Create account with uppercase username: [#8966](https://github.com/gravitee-io/issues/issues/8966)

**Other**

* Index name is too long: [#8814](https://github.com/gravitee-io/issues/issues/8814)
* Allow Enrich User Profile policy to accept objects as new claims
* WebAuthn post login flow does not contain webAuthnCredentialId
* Column messages in `i18n_dictionary_entries` table has too few characters

</details>

<details>

<summary>Breaking Changes</summary>

**NOTE:** To take advantage of these new features and incorporate these breaking changes, use the [migration guide](../../getting-started/install-and-upgrade-guides/upgrade-guide.md).

**MongoDB index names**

Starting from AM 4.0, the MongoDB indices are now named using the first letters of the fields that compose the index. This change will allow the automatic management of index creation on DocumentDB. This change requires the execution of a MongoDB script to delete and then recreate AM indices. See the [migration guide](../../getting-started/install-and-upgrade-guides/upgrade-guide.md).

**Enterprise Edition plugins**

As mentioned in the [changelog](am-4.x.x-2023-07-26.md), some plugins are now available for Enterprise Edition only and to use them requires a license.

</details>
