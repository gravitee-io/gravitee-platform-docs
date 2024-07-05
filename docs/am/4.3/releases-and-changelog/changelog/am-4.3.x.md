---
description: >-
  This page contains the changelog entries for AM 4.3.x and any future minor or
  patch AM 4.3.x releases
---

# AM 4.3.x

## Gravitee Access Management 4.3.7 - June 21, 2024

<details>

<summary>Bug fixes</summary>

**Gateway**

* Heml duplication of configuration [#9778](https://github.com/gravitee-io/issues/issues/9778)
* AM Gateway pod is not starting due to StackOverflowError [#9794](https://github.com/gravitee-io/issues/issues/9794)





**Other**

* Improve the ingress configuration to redirect HTTPS [#9712](https://github.com/gravitee-io/issues/issues/9712)

</details>


## Gravitee Access Management 4.3.6 - June 6, 2024

<details>

<summary>Bug fixes</summary>

**Gateway**

* [AM] [3.21.18] User don't receive the email to recover his password with an uppercase email [#9624](https://github.com/gravitee-io/issues/issues/9624)
* Exception on start-up in Spring Boot applications after upgrade to AM 4.3.1 [#9667](https://github.com/gravitee-io/issues/issues/9667)
* Error Azure SCIM user update  [#9674](https://github.com/gravitee-io/issues/issues/9674)
* DCR new client using Template doesn't copy all parameters [#9691](https://github.com/gravitee-io/issues/issues/9691)
* Brute Force Detection not working to IDPs with Account Linking Policy [#9713](https://github.com/gravitee-io/issues/issues/9713)
* Source IP and user agent missing from FORGOT_PASSWORD_REQUESTED audit log [#9724](https://github.com/gravitee-io/issues/issues/9724)
* Domain not available into the ExpresionLanguage context [#9745](https://github.com/gravitee-io/issues/issues/9745)

**Management API**

* Not able to configure email notifier using Gravitee [#9581](https://github.com/gravitee-io/issues/issues/9581)



**Other**

* Editing HTTP Provider selects wrong password encoder [#9627](https://github.com/gravitee-io/issues/issues/9627)

</details>


## Gravitee Access Management 4.3.5 - May 24, 2024

<details>

<summary>Bug fixes</summary>

**Gateway**

* Gravitee 4.3 Remember-Device Regression [#9734](https://github.com/gravitee-io/issues/issues/9734)
* Error with MFA Challenge policy in Reset Password Flow [#9735](https://github.com/gravitee-io/issues/issues/9735)

**Other**

* Unable to remove a FORM at organization level [#9124](https://github.com/gravitee-io/issues/issues/9124)
* Application - Forms - Page not found error when enabling custom form again after being 'cleared' [#9492](https://github.com/gravitee-io/issues/issues/9492)
* \[DCR] improve client sanitizeTemplate method [#9687](https://github.com/gravitee-io/issues/issues/9687)
* Password Policy Blank value in dropbox when selecting value Unlimited

</details>

## Gravitee Access Management 4.3.4 - May 9, 2024

<details>

<summary>Bug fixes</summary>

**Other**

* There are no MFA logs [#9629](https://github.com/gravitee-io/issues/issues/9629)
* Enabling MFA in Gravitee AM Console Gives 500 error [#9685](https://github.com/gravitee-io/issues/issues/9685)
* \_node/health endpoint is not accessible [#9698](https://github.com/gravitee-io/issues/issues/9698)
* Plugin "Orange Contact Everyone" is not compatible with version 4.3.2 [#9704](https://github.com/gravitee-io/issues/issues/9704)

</details>

## Gravitee Access Management 4.3.3 - April 29, 2024

<details>

<summary>Bug fixes</summary>

**Gateway**

* Issue with MFA and silent refresh token [#9622](https://github.com/gravitee-io/issues/issues/9622)
* \[WebAuthn] Problèmatique Authenticator "SecurityError : The operation is insecure." [#9686](https://github.com/gravitee-io/issues/issues/9686)

**Management API**

* Not able to add new attribute to User’s profile through AM REST Api when using Google Identity provider [#8434](https://github.com/gravitee-io/issues/issues/8434)
* AM - Application Analytics Timeout [#9405](https://github.com/gravitee-io/issues/issues/9405)

**Other**

* La vérification a échoué + email pas envoyé automatiquement [#9659](https://github.com/gravitee-io/issues/issues/9659)

</details>

## Gravitee Access Management 4.3.2 - April 12, 2024

<details>

<summary>Bug fixes</summary>

**Console**

* Error when notifications are acknowledged [#9661](https://github.com/gravitee-io/issues/issues/9661)

**Other**

* Enrollment Flow Logic Bug [#9518](https://github.com/gravitee-io/issues/issues/9518)
* Improve CORS Domain settings and replace default values [#9531](https://github.com/gravitee-io/issues/issues/9531)
* Empty rectangle displayed with fresh install of AM [#9649](https://github.com/gravitee-io/issues/issues/9649)

</details>

## Gravitee Access Management 4.3.1 - April 5, 2024

<details>

<summary>Bug fixes</summary>

**Gateway**

* Disable Application [#9584](https://github.com/gravitee-io/issues/issues/9584)

**Other**

* Expired records present in table ciba\_auth\_requests. Cron is not taken into account. [#9499](https://github.com/gravitee-io/issues/issues/9499)
* Logs too verbose in AM when GeoIP plugin is not available [#9633](https://github.com/gravitee-io/issues/issues/9633)
* Support SAML mixing response binding protocol [#9648](https://github.com/gravitee-io/issues/issues/9648)

</details>

## Gravitee Access Management 4.3 - March 29, 2024

For more in-depth information on what's new, please refer to the [Gravitee AM 4.3 release notes](../release-notes/am-4.3.md).

<details>

<summary>What's new</summary>

**Audit logs**

Gravitee 4.3 now captures audit logs for client authentications and MFA events so that an AM admin can understand where an authentication flow fails. Audit entries are written for each occurrence of the events listed below.

</details>

<details>

<summary>Breaking changes</summary>

The `openid` scope is now forbidden for client_credentials flow as this not related to user authentication. 

</details>
