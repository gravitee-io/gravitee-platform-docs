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

* Password - Password salt format option
* Flows - add new TOKEN flow
* MFA - initiating MFA Enrollment via OpenID Connect 1.0
* Send email verification link
* \[Admin] Be able to re-trigger verification email
* Passwordless - Name passwordless device

**Gateway**

* **\[gateway]\[audit]:** It is impossible to see the user that consented the user consent in the audit log https://github.com/gravitee-io/issues/issues/9049\[#9049]
* **\[gateway]\[mfa]:** Allow OTP factor to handle clock drift issues https://github.com/gravitee-io/issues/issues/9074\[#9074]

**Management API**

* Create account with uppercase username https://github.com/gravitee-io/issues/issues/8966\[#8966]

**Other**

* Index name too long https://github.com/gravitee-io/issues/issues/8814\[#8814]
* \[policies] allow Enrich User Profile policy to accept objects as new claims
* WebAuthn post login flow does not contain webAuthnCredentialId
* Column messages in i18n\_dictionary\_entries  table has too little characters

</details>

<details>

<summary>Breaking Changes</summary>

**General**

* :page-sidebar: am\_3\_x\_sidebar
* :page-permalink: am/current/am\_breaking\_changes\_4.0.html
* :page-folder: am/installation-guide
* :page-layout: am

**NOTE:** To take advantage of these new features and incorporate these breaking changes, use the migration guide.

**MongoDB index names**

Starting from AM 4.0, the MongoDB indices are now named using the first letters of the fields that compose the index. This change will allow the automatic management of index creation on DocumentDB. This change requires the execution of a MongoDB script to delete and then recreate AM indices. See the migration guide.

**Enterprise Edition plugins**

As mentioned in the [changelog](am-4.x.x-2023-07-26.md), some plugins are now available for Enterprise Edition only and to use them requires a license.

</details>
