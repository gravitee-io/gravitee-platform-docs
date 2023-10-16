---
description: >-
  This page contains the changelog entries for AM 4.0 and any future minor or
  patch AM 4.0.x releases
---

# AM 4.0.x

## Gravitee Access Management 4.0.3 - October 16, 2023



<details>
<summary>Bug fixes</summary>
**Gateway**

* Align XSRF token ttl to the user session ttl https://github.com/gravitee-io/issues/issues/9282[#9282]

**Management API**

* Wrong values returned by Gravitee AM management API https://github.com/gravitee-io/issues/issues/9141[#9141]
* AM Management API should start even with missing or unknown Identity Provider plugins https://github.com/gravitee-io/issues/issues/9230[#9230]



**Other**

* MS SqlServer 10.2 onwards driver support https://github.com/gravitee-io/issues/issues/9178[#9178]
* Upgrade script of the 3.21.6 does not work as expected https://github.com/gravitee-io/issues/issues/9288[#9288]
* Update mongo script to create indexes https://github.com/gravitee-io/issues/issues/9291[#9291]
</details>


## Gravitee Access Management 4.0.2 - September 29, 2023

<details>

<summary>Bug fixes</summary>

**Gateway**

* AM allows invalid emails during MFA enrollment which prevents future logins and presents an attack vector [#8887](https://github.com/gravitee-io/issues/issues/8887)
* Gravitee AM: Search users using SCIM query [#9109](https://github.com/gravitee-io/issues/issues/9109)
* 500 internal server error due to invalid HTML template in enroll, login , challenge form [#9111](https://github.com/gravitee-io/issues/issues/9111)
* AM: Invalid encoding value after multiple redirects [#9154](https://github.com/gravitee-io/issues/issues/9154)
* Filter is not implemented in SCIM group endpoint [#9183](https://github.com/gravitee-io/issues/issues/9183)
* Key usage is always "enc" [#9236](https://github.com/gravitee-io/issues/issues/9236)

**Management API**

* Multiple concurrent requests create users with duplicated usernames [#9117](https://github.com/gravitee-io/issues/issues/9117)

**Console**

* After a migration, the IDP checkbox `Allow CRUD operation` is not shown as enabled in the UI but is enabled in the backend [#9123](https://github.com/gravitee-io/issues/issues/9123)

**Other**

* When the pre-registration option is set, we are not able to finish the registration properly [#9221](https://github.com/gravitee-io/issues/issues/9221)
* Allow the bypass of MongoDB indices creation [#9232](https://github.com/gravitee-io/issues/issues/9232)
* Map of claims unusable in EL [#9240](https://github.com/gravitee-io/issues/issues/9240)
* Alerts Dashboard is not retaining the alert channel selection/deselection [#9253](https://github.com/gravitee-io/issues/issues/9253)

</details>

## Gravitee Access Management 4.0 - July 20, 2023

For more in-depth information on what's new, please refer to the [Gravitee AM 4.0 release notes](../release-notes/).

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
* factor-sms
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

As mentioned in the [changelog](am-4.0.x-changelog.md), some plugins are now only available to Enterprise Edition and to use them requires a license.

</details>
