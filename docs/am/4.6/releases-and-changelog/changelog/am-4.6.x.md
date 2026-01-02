---
description: >-
  This page contains the changelog entries for AM 4.6.0 and any future minor or
  patch AM 4.6.x releases
---

# AM 4.6.x

## Gravitee Access Management 4.6.30 - January 2, 2026

<details>

<summary>Bug fixes</summary>







**Other**

* AuthenticationFlow: missing transactionId [#11033](https://github.com/gravitee-io/issues/issues/11033)
* Unable to add multiple virtual hosts in Gravitee AM [#11048](https://github.com/gravitee-io/issues/issues/11048)

</details>


## Gravitee Access Management 4.6.29 - December 19, 2025

<details>

<summary>Bug fixes</summary>







**Other**

* Apply jemalloc to dockerfile for Gateway/MAPI (4.7+) [#10991](https://github.com/gravitee-io/issues/issues/10991)
* Introduce setting to avoid fallback on HMAC [#11018](https://github.com/gravitee-io/issues/issues/11018)
* Enhance logging in gateway consent failure handler [#11025](https://github.com/gravitee-io/issues/issues/11025)
* MFA challenge is always presented when session is expired and Remember Me cookie bypasses login [#11029](https://github.com/gravitee-io/issues/issues/11029)

</details>


## Gravitee Access Management 4.6.28 - December 5, 2025

<details>

<summary>Bug fixes</summary>



**Management API**

* WebAuthn - credentials are not removed when a user is deleted [#10990](https://github.com/gravitee-io/issues/issues/10990)



**Other**

* Allow implicit authentication on CloudHSM plugin [#10996](https://github.com/gravitee-io/issues/issues/10996)

</details>


## Gravitee Access Management 4.6.27 - November 21, 2025

<details>

<summary>Bug fixes</summary>

**Gateway**

* JSON Logging for AM Token Endpoint [#10943](https://github.com/gravitee-io/issues/issues/10943)
* Filter CLIENT_AUTHENTICATION success audit logs [#10954](https://github.com/gravitee-io/issues/issues/10954)
* translate email from name [#10958](https://github.com/gravitee-io/issues/issues/10958)

**Management API**

* Error creating identities in 4.7.X [#10940](https://github.com/gravitee-io/issues/issues/10940)



**Other**

* STS Client is not closed in HSM implementation [#10977](https://github.com/gravitee-io/issues/issues/10977)

</details>


## Gravitee Access Management 4.6.26 - November 7, 2025

<details>

<summary>Bug fixes</summary>

**Gateway**

* Improve Thread Management for RDBMS backend [#10938](https://github.com/gravitee-io/issues/issues/10938)





**Other**

* Reduce log verbosity on MFA validation failure [#10903](https://github.com/gravitee-io/issues/issues/10903)

</details>

## Gravitee Access Management 4.6.25 - October 30, 2025

<details>

<summary>Bug fixes</summary>

**Gateway**

* StackOverflowError when logging out [#10928](https://github.com/gravitee-io/issues/issues/10928)

</details>

## Gravitee Access Management 4.6.24 - October 24, 2025

<details>

<summary>Bug fixes</summary>

**Gateway**

* Account's password is expired error when using account linking [#10851](https://github.com/gravitee-io/issues/issues/10851)
* Password policy apply to LDAP idp [#10874](https://github.com/gravitee-io/issues/issues/10874)

**Management API**

* Domain deletion does not remove all entities [#10899](https://github.com/gravitee-io/issues/issues/10899)

**Other**

* Make datasource configurable using helm values [#10884](https://github.com/gravitee-io/issues/issues/10884)

</details>

## Gravitee Access Management 4.6.23 - October 10, 2025

<details>

<summary>Bug fixes</summary>

**Gateway**

* France Connect V2 - Review wording of error message [#10738](https://github.com/gravitee-io/issues/issues/10738)

**Management API**

* Sanitize the redirect\_uri to avoid empty segment when cockpit try to connect on the console [#10805](https://github.com/gravitee-io/issues/issues/10805)

**Other**

* Introduce common connection pool for MongoIDP [#10719](https://github.com/gravitee-io/issues/issues/10719)
* AWS HSM Certificate Plugin logs remain at DEBUG level despite global INFO configuration, and Helm chart indentation/mapping issue for extraLoggers. [#10824](https://github.com/gravitee-io/issues/issues/10824)
* Limit the batchSize on Mongo Reporter request [#10846](https://github.com/gravitee-io/issues/issues/10846)
* Add helm.sh/chart to pod template annotations [#10849](https://github.com/gravitee-io/issues/issues/10849)
* User registration completion UI widget is broken [#10865](https://github.com/gravitee-io/issues/issues/10865)
* Conversion session.timeout for helm value incorrect [#10867](https://github.com/gravitee-io/issues/issues/10867)
* Improve logging in EnrichAuthFlowPolicy [#10875](https://github.com/gravitee-io/issues/issues/10875)

</details>

## Gravitee Access Management 4.6.22 - September 26, 2025

<details>

<summary>Bug fixes</summary>

**Gateway**

* Enhance idp plugin redeployment to avoid downtime [#10778](https://github.com/gravitee-io/issues/issues/10778)
* Am Is Creating Discrepancies With the Issuer Claim (`iss`) in Generated Access Tokens [#10779](https://github.com/gravitee-io/issues/issues/10779)

</details>

## Gravitee Access Management 4.6.21 - September 18, 2025

<details>

<summary>Bug fixes</summary>

**Other**

* IDP Domain whitelist [#10790](https://github.com/gravitee-io/issues/issues/10790)
* When a kafka reporter is inherited from the organization, each domain has it own producer [#10576](https://github.com/gravitee-io/issues/issues/10576)
* Reduce the number of threads with MongoDB Backend [#10713](https://github.com/gravitee-io/issues/issues/10713)
* Deleting Organization User Fails on SQL Server Due to Invalid DELETE Syntax [#10838](https://github.com/gravitee-io/issues/issues/10838)
* Incorrect audit log file formatting [#10757](https://github.com/gravitee-io/issues/issues/10757)
* NullPointerException upon first login with password expiration [#10780](https://github.com/gravitee-io/issues/issues/10780)
* Error searching for users in the UI [#10808](https://github.com/gravitee-io/issues/issues/10808)
* Replace Bitnami Mongo [#10789](https://github.com/gravitee-io/issues/issues/10789)

</details>

## Gravitee Access Management 4.6.20 - September 1, 2025

<details>

<summary>Bug fixes</summary>

**Other**

* Closing LDAP connections properly [#10769](https://github.com/gravitee-io/issues/issues/10769)

</details>

## Gravitee Access Management 4.6.19 - August 29, 2025

<details>

<summary>Bug fixes</summary>

**Other**

* Can't get dynamic roles for the user [#10679](https://github.com/gravitee-io/issues/issues/10679)
* LDAP connection leak [#10736](https://github.com/gravitee-io/issues/issues/10736)
* Unable to configure IDP Http Body request [#10740](https://github.com/gravitee-io/issues/issues/10740)

</details>

## Gravitee Access Management 4.6.18 - August 15, 2025

<details>

<summary>Bug fixes</summary>

**Other**

* Can't request on values containing + char using filters for searching users [#10495](https://github.com/gravitee-io/issues/issues/10495)
* Missing MAPI audits in Global kafka reporter [#10609](https://github.com/gravitee-io/issues/issues/10609)
* Group search base in LDAP Provider in UI does not reflect backend value [#10668](https://github.com/gravitee-io/issues/issues/10668)
* LDAP connection leak [#10736](https://github.com/gravitee-io/issues/issues/10736)

</details>

## Gravitee Access Management 4.6.17 - August 1, 2025

<details>

<summary>Bug fixes</summary>

**Other**

* Missing indexes on Devices table [#10677](https://github.com/gravitee-io/issues/issues/10677)
* Can't get dynamic roles for the user [#10679](https://github.com/gravitee-io/issues/issues/10679)
* When an Access token is missing from the authorization endpoint and only an ID Token is returned, any token is stored in user profile [#10680](https://github.com/gravitee-io/issues/issues/10680)
* NoSuchMethodError after JwkSourceresolver update [#10696](https://github.com/gravitee-io/issues/issues/10696)
* France Connect V2 - Problem when disconnecting France Connect [#10697](https://github.com/gravitee-io/issues/issues/10697)
* access and refresh token purging schedule. [#10703](https://github.com/gravitee-io/issues/issues/10703)

</details>

## Gravitee Access Management 4.6.16 - July 18, 2025

<details>

<summary>Bug fixes</summary>

**Management API**

* GET /domain/users with parameter size=0 brings back all users [#10661](https://github.com/gravitee-io/issues/issues/10661)

**Other**

* Deadlock during accessing authorization code [#10614](https://github.com/gravitee-io/issues/issues/10614)
* Intermittent remote JWK set read time out [#10669](https://github.com/gravitee-io/issues/issues/10669)

</details>

## Gravitee Access Management 4.6.15 - July 4, 2025

<details>

<summary>What's new !</summary>

**What's new!**

* Cookie Based remember device: it is now possible to use a new DeviceIdentifier plugin based on cookie instead of fingerprint.

{% hint style="info" %}
If the page templates have been customized, it is necessary to include the JavaScript scripts related to this new plugin. For login, reset\_password, registration and registration\_confirmation, please add:

```
<script th:if="${rememberDeviceIsActive && deviceIdentifierProvider == 'CookieDeviceIdentifier'}" th:src="@{assets/js/device-type-v1.js}"></script>
<script th:if="${rememberDeviceIsActive && deviceIdentifierProvider == 'CookieDeviceIdentifier'}" th:attr="nonce=${script_inline_nonce}">
    const deviceId = "[[${cookieDeviceIdentifier}]]" ;

    $(document).ready(function () {
        $("#form").append('<input type="hidden" name="deviceId" value="' + deviceId + '"/>')
        $("#form").append('<input type="hidden" name="deviceType" value="' + retrievePlatform(window.navigator) + '"/>');
    });
</script>
```

For webauthn\_login, please add :

```
<script th:if="${rememberDeviceIsActive && deviceIdentifierProvider == 'CookieDeviceIdentifier'}" th:src="@{../assets/js/device-type-v1.js}"></script>
<script th:if="${rememberDeviceIsActive && deviceIdentifierProvider == 'CookieDeviceIdentifier'}" th:attr="nonce=${script_inline_nonce}">
    const deviceId = "[[${cookieDeviceIdentifier}]]" ;

    $(document).ready(function () {
        $("#login").append('<input type="hidden" name="deviceId" value="' + deviceId + '"/>')
        $("#login").append('<input type="hidden" name="deviceType" value="' + retrievePlatform(window.navigator) + '"/>');
    });
</script>
```

If FingerprintJS Community edition is currently used, you can use the cookie management for this plugin by enabling the new configuration option.
{% endhint %}

</details>

<details>

<summary>Bug fixes</summary>

**Gateway**

* Manage Multiple AndroidKey Root CA [#10658](https://github.com/gravitee-io/issues/issues/10658)

</details>

## Gravitee Access Management 4.6.14 - June 25, 2025

<details>

<summary>Bug fixes</summary>

**Gateway**

* Add token sub claim from JWT token in the TOKEN\_CREATED event [#10638](https://github.com/gravitee-io/issues/issues/10638)

**Other**

* \[FC] update the sandbox urls [#10636](https://github.com/gravitee-io/issues/issues/10636)

</details>

## Gravitee Access Management 4.6.13 - June 20, 2025

<details>

<summary>Bug fixes</summary>

**Gateway**

* Multiple OAuth parameters are added to URLs when multiple MFA challenges are sent [#10610](https://github.com/gravitee-io/issues/issues/10610)
* Certificate implementation for AWS CloudHSM doesn't scale [#10615](https://github.com/gravitee-io/issues/issues/10615)

**Management API**

* Users cannot view the accessPoint field in the domain audit logs if they do not have a domain role permission [#10602](https://github.com/gravitee-io/issues/issues/10602)

**Console**

* Policies not saving and being applied [#10633](https://github.com/gravitee-io/issues/issues/10633)

</details>

## Gravitee Access Management 4.6.12 - June 9, 2025

<details>

<summary>Bug fixes</summary>

**Gateway**

* Improve user login logs [#10588](https://github.com/gravitee-io/issues/issues/10588)

**Console**

* HTTP Callout policy has misaligned text boxes [#10551](https://github.com/gravitee-io/issues/issues/10551)

**Other**

* OpenAPI spec for listDomains is not correct [#10591](https://github.com/gravitee-io/issues/issues/10591)
* \[R2DBC] version 1.0.2 of SQLServer driver not working [#10565](https://github.com/gravitee-io/issues/issues/10565)

</details>

## Gravitee Access Management 4.6.11 - May 28, 2025

<details>

<summary>Bug fixes</summary>

**Gateway**

* URL coding of user name seems to be broken [#10469](https://github.com/gravitee-io/issues/issues/10469)
* When username contains space the token generation fails [#10569](https://github.com/gravitee-io/issues/issues/10569)
* PeerCertificate not interpreted properly when it provided by header [#10586](https://github.com/gravitee-io/issues/issues/10586)

**Other**

* Access Gateway - X-Request header usage [#10552](https://github.com/gravitee-io/issues/issues/10552)

</details>

## Gravitee Access Management 4.6.10 - May 13, 2025

<details>

<summary>Bug fixes</summary>

**Management API**

* Users and Groups metadata not displayed for /members endpoint [#10515](https://github.com/gravitee-io/issues/issues/10515)
* Email notification fails when user doesn't have firstName [#10536](https://github.com/gravitee-io/issues/issues/10536)

**Other**

* Reporter Upgrader is using a syntax not supported by DocumentDB [#10528](https://github.com/gravitee-io/issues/issues/10528)

</details>

## Gravitee Access Management 4.6.9 - May 6, 2025

<details>

<summary>Bug fixes</summary>

**Gateway**

* Filter audit type [#10518](https://github.com/gravitee-io/issues/issues/10518)

**Other**

* Fail to enable the AM gateway service on SUSE [#10402](https://github.com/gravitee-io/issues/issues/10402)
* Support of FranceConnect API V2

</details>

## Gravitee Access Management 4.6.8 - April 28, 2025

<details>

<summary>Bug fixes</summary>

**Other**

* GIS claim can be overridden with custom claim [#10472](https://github.com/gravitee-io/issues/issues/10472)

</details>

## Gravitee Access Management 4.6.7 - April 15, 2025

<details>

<summary>Bug fixes</summary>

**Management API**

* MFA "Remember Device" error when using CAS IDP [#10493](https://github.com/gravitee-io/issues/issues/10493)

**Other**

* JDBC pool parameters are incorrectly indented in the Helm chart [#10482](https://github.com/gravitee-io/issues/issues/10482)

</details>

## Gravitee Access Management 4.6.6 - April 11, 2025

<details>

<summary>Bug fixes</summary>

**Gateway**

* Problem with API management console application creation/update and DCR [#10232](https://github.com/gravitee-io/issues/issues/10232)
* Login button remains disabled when using a password manager [#10411](https://github.com/gravitee-io/issues/issues/10411)
* Setting max consecutive letters to 0 in password policies using mapi displays unnecessary password requirement [#10416](https://github.com/gravitee-io/issues/issues/10416)
* Unable to use id\_token when configuring Azure though OpenId form [#10453](https://github.com/gravitee-io/issues/issues/10453)
* Using of Redis on Production and Crash situation [#10454](https://github.com/gravitee-io/issues/issues/10454)
* Error handling error=session\_expired in Login Form [#10460](https://github.com/gravitee-io/issues/issues/10460)
* EL for language entries not resolving correctly [#10465](https://github.com/gravitee-io/issues/issues/10465)
* Resilient mode is failing [#10474](https://github.com/gravitee-io/issues/issues/10474)

**Management API**

* Prevent Ogranization IDP selection to send null [#10444](https://github.com/gravitee-io/issues/issues/10444)
* Fix audit log on user login failed [#10463](https://github.com/gravitee-io/issues/issues/10463)

**Other**

* Unable to save Group Mapper for Social IDP at organization level in AM UI [#10403](https://github.com/gravitee-io/issues/issues/10403)
* Error in /ciba/authenticate/callback [#10412](https://github.com/gravitee-io/issues/issues/10412)
* MinLength value can be greater than maxLength value in a password policy when using the mapi [#10417](https://github.com/gravitee-io/issues/issues/10417)
* \[AM]\[4.5.11] Error when character "ë" in a token [#10418](https://github.com/gravitee-io/issues/issues/10418)
* Can't update SAML SP certificate in UI application SAML tab [#10442](https://github.com/gravitee-io/issues/issues/10442)
* Group Mapper not apply with JDBC [#10445](https://github.com/gravitee-io/issues/issues/10445)
* Management API does not check if user exists on domain when added to a group on creation of the group [#10468](https://github.com/gravitee-io/issues/issues/10468)

</details>

## Gravitee Access Management 4.6.5 - March 17, 2025

<details>

<summary>Bug fixes</summary>

**Gateway**

* MFA Challenge policy doesn't work when multiple redirect\_uri are declared [#10407](https://github.com/gravitee-io/issues/issues/10407)
* Authentication fails when MFA Challenge policy is used [#10421](https://github.com/gravitee-io/issues/issues/10421)

</details>

## Gravitee Access Management 4.6.4 - March 11, 2025

<details>

<summary>Bug fixes</summary>

**Gateway**

* RememberDevice issue with uBlock [#10388](https://github.com/gravitee-io/issues/issues/10388)
* Fix regression on redirect URL [#10404](https://github.com/gravitee-io/issues/issues/10404)

**Other**

* Improve how MongoDB connections are manage [#10381](https://github.com/gravitee-io/issues/issues/10381)

</details>

## Gravitee Access Management 4.6.3 - February 28, 2025

{% hint style="warning" %}
This version contains a regression introduced by [#10344](https://github.com/gravitee-io/issues/issues/10344). Please do not install this version if you are using Access Management to authenticate users on mobile applications.
{% endhint %}

<details>

<summary>Bug fixes</summary>

**Gateway**

* Redirect URL not whitelisted [#10344](https://github.com/gravitee-io/issues/issues/10344)
* Improve memory usage of Gateway [#10366](https://github.com/gravitee-io/issues/issues/10366)
* Close all LifeCycleService when domain is undeployed [#10367](https://github.com/gravitee-io/issues/issues/10367)

**Management API**

* Remove default baseURL for loadPreAuthUserResource in HttpIdentityProvider [#10361](https://github.com/gravitee-io/issues/issues/10361)

**Other**

* Error with MFA (/resetPassword page) [#10341](https://github.com/gravitee-io/issues/issues/10341)
* \[AM]\[4.4.11] French language in email not working [#10349](https://github.com/gravitee-io/issues/issues/10349)
* Lors d'une redemande d'OPT, même OTP [#10374](https://github.com/gravitee-io/issues/issues/10374)

</details>

{% hint style="info" %}
When managing deployments using Helm, please note that the default startup, liveness, and readiness probes now use the httpGet method by default to request the internal API on the `/_node/health` endpoint. As a result, the internal API listens on `0.0.0.0` to allow the kubelet to check the component's status. If you don't provide custom probe definitions and have explicitly defined either the `api.http.services.core.http.host` or the `gateway.http.services.core.http.host`, ensure the value is set to `0.0.0.0`; otherwise, the probes will fail.
{% endhint %}

## AM 4.6.x

### Gravitee Access Management 4.6.2 - February 17, 2025

<details>

<summary>Bug fixes</summary>

**Gateway**

* Update AM documentation and OpenAPI spec [#10299](https://github.com/gravitee-io/issues/issues/10299)
* \[CIBA] Http Authentication Device Notifier hide some scope [#10309](https://github.com/gravitee-io/issues/issues/10309)
* No logs from InvalidGrantException in the Audits in the UI [#10313](https://github.com/gravitee-io/issues/issues/10313)
* No logs from InvalidGrantException in the Audits in the UI [#10314](https://github.com/gravitee-io/issues/issues/10314)
* Error with MFA (Stuck in a Loop) [#10317](https://github.com/gravitee-io/issues/issues/10317)

**Other**

* Fetch-groups does not work. [#10331](https://github.com/gravitee-io/issues/issues/10331)

</details>

### Gravitee Access Management 4.6.1 - January 31, 2025

<details>

<summary>Bug fixes</summary>

**Gateway**

* GIS reference not removed from session with prompt=login [#10292](https://github.com/gravitee-io/issues/issues/10292)

**Other**

* Double quote prevent HTTP Provider to authenticate [#10277](https://github.com/gravitee-io/issues/issues/10277)

</details>

### Gravitee Access Management 4.6 - January 20, 2025 <a href="#gravitee-access-management-4.5-october-10-2024" id="gravitee-access-management-4.5-october-10-2024"></a>

<details>

<summary>What's new</summary>

#### Twilio Resource

The new version of the Twilio resource for SMS or Call factors allows you to specify the templateSid as configuration option.

#### LDAP Identity Provider

The new version of the LDAP identity provider grant you access to the Operational Attributes linked to the user profile coming from the LDAP server. (**NOTE:** If this option is enable, Opertational Attributes will be accessible using the User Mapper.)

#### User Migration

For users migrations from an alternative OIDC provider to Access Management, you now have the capability to define the `lastPasswordReset` attribute so a password policy with password expiry will request a password reset according to the value provided during the migration. This attribute is accepted only during user creation through the SCIM protocol or the Management API.

#### Audit Logs

Additional audit logs have been added on SCIM endpoint to track failing user creations or updates due to an invalid password. In additiopn, a distinction is made between user login with password against using passwordless in a way that the dashboard now expose these information.

#### Bulk action for user provisioning

User provisioning is now possible using Bulk actions to create, update or delete users. A dedicated endpoint has been added on the Management API and the SCIM protocol exposed by the Gateway implement the Bulk endpoint (only for the users, groups are currently not managed)

#### New Certificate plugin

A key pair registered in AWS Cloud HSM can be used to sign an tokens generated by Access Management by using the new "AWS Cloud HSM" certificate plugin.

</details>

<details>

<summary>Breaking Changes</summary>

**SCIM pagination**

In previous versions, the `startIndex` parameter used by SCIM paginiation was representing the page number. According to the [specification](https://datatracker.ietf.org/doc/html/rfc7644#section-3.4.2) the `startIndex` represent `the index of the first search result desired by the search client` . In order to be align with the specification, the SCIM endpoints of AM Gateway are managing the startIndex as specified by the RFC.

</details>

\\
