---
description: >-
  This page contains the changelog entries for AM 4.0.x and any future minor or
  patch AM 4.0.x releases
---

# AM 4.0.x

## Gravitee Access Management 4.0.23 - July 19, 2024

<details>

<summary>Bug fixes</summary>

**Gateway**

* Propagate Message from Error Condition of HTTP IdP to Audit log. [#9841](https://github.com/gravitee-io/issues/issues/9841)

**Management API**

*  Redirect to login when device credentials are deleted [#9859](https://github.com/gravitee-io/issues/issues/9859)

**Console**

* A switch has an incorrect state when revisiting page - Application Settings [#9433](https://github.com/gravitee-io/issues/issues/9433)

**Other**

* Switching between environments is broken when multiple environments linked in cockpit [#9844](https://github.com/gravitee-io/issues/issues/9844)

</details>


## Gravitee Access Management 4.0.22 - July 5, 2024

<details>

<summary>Bug fixes</summary>

**Gateway**

* OTPFactorProvider - An error occurs while validating 2FA code [#9725](https://github.com/gravitee-io/issues/issues/9725)
* null-1 entry in auth_flow_ctx table should not be stored in database [#9803](https://github.com/gravitee-io/issues/issues/9803)





**Other**

* When creating user with preregistratoin, the password creation steps are skipped [#9839](https://github.com/gravitee-io/issues/issues/9839)

</details>


## Gravitee Access Management 4.0.21 - June 21, 2024

<details>

<summary>Bug fixes</summary>

**Gateway**

* Heml duplication of configuration [#9778](https://github.com/gravitee-io/issues/issues/9778)





**Other**

* Improve the ingress configuration to redirect HTTPS [#9712](https://github.com/gravitee-io/issues/issues/9712)

</details>


## Gravitee Access Management 4.0.20 - June 6, 2024

<details>

<summary>Bug fixes</summary>

**Gateway**

* [AM] [3.21.18] User don't receive the email to recover his password with an uppercase email [#9624](https://github.com/gravitee-io/issues/issues/9624)
* Exception on start-up in Spring Boot applications after upgrade to AM 4.3.1 [#9667](https://github.com/gravitee-io/issues/issues/9667)
* Error Azure SCIM user update  [#9674](https://github.com/gravitee-io/issues/issues/9674)
* DCR new client using Template doesn't copy all parameters [#9691](https://github.com/gravitee-io/issues/issues/9691)
* Source IP and user agent missing from FORGOT_PASSWORD_REQUESTED audit log [#9724](https://github.com/gravitee-io/issues/issues/9724)
* Domain not available into the ExpresionLanguage context [#9745](https://github.com/gravitee-io/issues/issues/9745)

**Management API**

* Not able to configure email notifier using Gravitee [#9581](https://github.com/gravitee-io/issues/issues/9581)

**Console**

* AM - Change error message when admin user tries to remove certificate tied to an application [#8952](https://github.com/gravitee-io/issues/issues/8952)

**Other**

* Editing HTTP Provider selects wrong password encoder [#9627](https://github.com/gravitee-io/issues/issues/9627)
* Email from [%s] is invalid - SMTP Resource [#9749](https://github.com/gravitee-io/issues/issues/9749)

</details>


## Gravitee Access Management 4.0.19 - May 24, 2024

<details>

<summary>Bug fixes</summary>

**Other**

* Unable to remove a FORM at organization level [#9124](https://github.com/gravitee-io/issues/issues/9124)
* Application - Forms - Page not found error when enabling custom form again after being 'cleared' [#9492](https://github.com/gravitee-io/issues/issues/9492)
* Password Policy Blank value in dropbox when selecting value Unlimited

</details>

## Gravitee Access Management 4.0.18 - May 9, 2024

<details>

<summary>Bug fixes</summary>

**Other**

* There are no MFA logs [#9629](https://github.com/gravitee-io/issues/issues/9629)
* \_node/health endpoint is not accessible [#9698](https://github.com/gravitee-io/issues/issues/9698)

</details>

## Gravitee Access Management 4.0.17 - April 29, 2024

<details>

<summary>Bug fixes</summary>

**Gateway**

* Issue with MFA and silent refresh token [#9622](https://github.com/gravitee-io/issues/issues/9622)
* \[WebAuthn] Problèmatique Authenticator "SecurityError : The operation is insecure." [#9686](https://github.com/gravitee-io/issues/issues/9686)

**Management API**

* Not able to add new attribute to User’s profile through AM REST Api when using Google Identity provider [#8434](https://github.com/gravitee-io/issues/issues/8434)
* AM - Application Analytics Timeout [#9405](https://github.com/gravitee-io/issues/issues/9405)

</details>

## Gravitee Access Management 4.0.16 - April 12, 2024

<details>

<summary>Bug fixes</summary>

**Console**

* Error when notifications are acknowledged [#9661](https://github.com/gravitee-io/issues/issues/9661)

**Other**

* Enrollment Flow Logic Bug [#9518](https://github.com/gravitee-io/issues/issues/9518)
* Improve CORS Domain settings and replace default values [#9531](https://github.com/gravitee-io/issues/issues/9531)

</details>

## Gravitee Access Management 4.0.15 - April 5, 2024

<details>

<summary>Bug fixes</summary>

**Gateway**

* Disable Application [#9584](https://github.com/gravitee-io/issues/issues/9584)

**Other**

* Expired records present in table ciba\_auth\_requests. Cron is not taken into account. [#9499](https://github.com/gravitee-io/issues/issues/9499)
* Logs too verbose in AM when GeoIP plugin is not available [#9633](https://github.com/gravitee-io/issues/issues/9633)
* Support SAML mixing response binding protocol [#9648](https://github.com/gravitee-io/issues/issues/9648)

</details>

## Gravitee Access Management 4.0.14 - March 28, 2024

<details>

<summary>Bug fixes</summary>

**Gateway**

* Login - MFA challenge should be prompted when prompt=login is used [#9497](https://github.com/gravitee-io/issues/issues/9497)
* Revert: Passwordless authentication doesn't take the IDP status into account (#9494) [#9615](https://github.com/gravitee-io/issues/issues/9615)
* Addition of WebAuthn Credentials info into the context [#9620](https://github.com/gravitee-io/issues/issues/9620)

**Console**

* No space between source IP and user agent in audit logs [#9458](https://github.com/gravitee-io/issues/issues/9458)
* User agent showing 'undefined' in audit logs [#9459](https://github.com/gravitee-io/issues/issues/9459)
* Fetch user group doesn't persist [#9609](https://github.com/gravitee-io/issues/issues/9609)

</details>

## Gravitee Access Management 4.0.13 - March 15, 2024

<details>

<summary>Bug fixes</summary>

**Gateway**

* Redirect executed with jwt-bearer grant\_type [#9505](https://github.com/gravitee-io/issues/issues/9505)
* Invalid Phone Number [#9519](https://github.com/gravitee-io/issues/issues/9519)

</details>

## Gravitee Access Management 4.0.12 - February 29, 2024

<details>

<summary>Bug fixes</summary>

**Gateway**

* Passwordless authentication doesn't take the IDP status into account [#9494](https://github.com/gravitee-io/issues/issues/9494)
* State parameter encoded twice with response\_mode set to form\_post [#9528](https://github.com/gravitee-io/issues/issues/9528)
* Passwordless registration appearing for users who have already authenticated with step up [#9568](https://github.com/gravitee-io/issues/issues/9568)

</details>

## Gravitee Access Management 4.0.11 - February 19, 2024

<details>

<summary>Bug fixes</summary>

**Gateway**

* Unable to finalize SAML authentication using HTTP-POST binding [#9485](https://github.com/gravitee-io/issues/issues/9485)
* Security Domain may not be loaded on Gateway startup [#9496](https://github.com/gravitee-io/issues/issues/9496)
* Custom email not being sent when resending account registered verification email [#9500](https://github.com/gravitee-io/issues/issues/9500)
* Do not log stack trace when user has to provide password after webauthn authentication [#9503](https://github.com/gravitee-io/issues/issues/9503)

**Console**

* Missing read password policy role [#8924](https://github.com/gravitee-io/issues/issues/8924)

**Other**

* SAML 2.0 Identity Provider requires AM dependency update [#9515](https://github.com/gravitee-io/issues/issues/9515)

</details>

## Gravitee Access Management 4.0.10 - February 9, 2024

<details>

<summary>Bug fixes</summary>

**Gateway**

* Invalid form parameter when ResponseMode is set to form\_post [#9179](https://github.com/gravitee-io/issues/issues/9179)
* SCIM search operator PR doesn't work as expected [#9265](https://github.com/gravitee-io/issues/issues/9265)
* Authentication flow rejected due to redirect\_uri when PAR is used [#9478](https://github.com/gravitee-io/issues/issues/9478)
* WebAuthn: "Force authenticator integrity" - LastCheckedAt systematically updated at each webauthn login [#9327](https://github.com/gravitee-io/issues/issues/9327)

</details>

## Gravitee Access Management 4.0.9 - January 24, 2024

<details>

<summary>Bug fixes</summary>

**Gateway**

* Passwordless not working for iOS v17.2.1 [#9470](https://github.com/gravitee-io/issues/issues/9470)

</details>

## Gravitee Access Management 4.0.8 - January 19, 2024

<details>

<summary>Bug fixes</summary>

**Gateway**

* Avoid BodyHandler processing for GET request [#9352](https://github.com/gravitee-io/issues/issues/9352)
* WebAuthnCredentialId is null into the EL context [#9455](https://github.com/gravitee-io/issues/issues/9455)

</details>

## Gravitee Access Management 4.0.7 - December 22, 2023

<details>

<summary>Bug fixes</summary>

**Gateway**

* Session expired problem - X-XRF-TOKEN [#9398](https://github.com/gravitee-io/issues/issues/9398)
* 500 response received on creating user with /scim endpoint with duplicate externalId [#9421](https://github.com/gravitee-io/issues/issues/9421)
* Exclude null value from SCIM UserMapper [#9427](https://github.com/gravitee-io/issues/issues/9427)

**Management API**

* Unable to list users [#9125](https://github.com/gravitee-io/issues/issues/9125)

</details>

## Gravitee Access Management 4.0.6 - December 11, 2023

<details>

<summary>Bug fixes</summary>

**Gateway**

* Excessive number of ExpiredJWTException errors in Gravitee logs [#9261](https://github.com/gravitee-io/issues/issues/9261)
* Original Parameters lost during redirect using SAML Handler [#9393](https://github.com/gravitee-io/issues/issues/9393)
* Avoid logging GeoIP error stackstrace [#9401](https://github.com/gravitee-io/issues/issues/9401)

**Other**

* Invalid value in Issuer for Response [#9409](https://github.com/gravitee-io/issues/issues/9409)
* MessageDigest Encoder is not ThreadSafe [#9413](https://github.com/gravitee-io/issues/issues/9413)
* Configuration files are being overwritten during YUM update [#9368](https://github.com/gravitee-io/issues/issues/9368)

</details>

## Gravitee Access Management 4.0.5 - November 10, 2023

<details>

<summary>Bug fixes</summary>

**Gateway**

* Deadlock during generate AccessToken [#9238](https://github.com/gravitee-io/issues/issues/9238)

**Other**

* Upgrade Groovy policy [#9229](https://github.com/gravitee-io/issues/issues/9229)
* EnrollmentMFA policy doesn't manage the useVariableFactorSecurity setting [#9365](https://github.com/gravitee-io/issues/issues/9365)

</details>

## Gravitee Access Management 4.0.4 - October 27, 2023

<details>

<summary>Bug fixes</summary>

**Gateway**

* Application error when using an undefined translation [#9237](https://github.com/gravitee-io/issues/issues/9237)
* Registration confirmation Javascript error (anti-XSRF token) [#9276](https://github.com/gravitee-io/issues/issues/9276)
* Quotes are lost in Gravitee AM forms [#9326](https://github.com/gravitee-io/issues/issues/9326)
* When a resource plugin has been removed from the installation, other resources may not be loaded [#9344](https://github.com/gravitee-io/issues/issues/9344)

**Management API**

* Management API hangs completely [#9339](https://github.com/gravitee-io/issues/issues/9339)

**Other**

* EnrichProfile reset factor defined by EnrollMFA policy [#9161](https://github.com/gravitee-io/issues/issues/9161)

</details>

## Gravitee Access Management 4.0.3 - October 16, 2023

<details>

<summary>Bug fixes</summary>

**Gateway**

* Align XSRF token TTL to the user session TTL [#9282](https://github.com/gravitee-io/issues/issues/9282)

**Management API**

* Wrong values returned by Gravitee AM Management API [#9141](https://github.com/gravitee-io/issues/issues/9141)
* AM Management API should start even with missing or unknown Identity Provider plugins [#9230](https://github.com/gravitee-io/issues/issues/9230)

**Other**

* MS SqlServer 10.2 onwards driver support [#9178](https://github.com/gravitee-io/issues/issues/9178)
* Upgrade script for 3.21.6 does not work as expected [#9288](https://github.com/gravitee-io/issues/issues/9288)
* Update Mongo script to create indices [#9291](https://github.com/gravitee-io/issues/issues/9291)

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

## Gravitee Access Management 4.0.0 - July 20, 2023

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

**NOTE:** To take advantage of these new features and incorporate these breaking changes, use the [migration guide](docs/am/4.0/getting-started/install-and-upgrade-guides/upgrade-guide.md).

**MongoDB index names**

Starting from AM 4.0, the MongoDB indices are now named using the first letters of the fields that compose the index. This change will allow the automatic management of index creation on DocumentDB. This change requires the execution of a MongoDB script to delete and then recreate AM indices. See the [migration guide](docs/am/4.0/getting-started/install-and-upgrade-guides/upgrade-guide.md).

**Enterprise Edition plugins**

As mentioned in the [changelog](am-4.0.x.md), some plugins are now only available to Enterprise Edition and to use them requires a license.

</details>
