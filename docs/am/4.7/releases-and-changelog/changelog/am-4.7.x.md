---
description: >-
  This page contains the changelog entries for AM 4.7.0 and any future minor or
  patch AM 4.7.x releases
---

# AM 4.7.x

## Gravitee Access Management 4.7.20 - November 7, 2025

<details>

<summary>Bug fixes</summary>

**Gateway**

* VertX Thread Blocked when JWKS is loaded [#10932](https://github.com/gravitee-io/issues/issues/10932)
* Upgrade Spring Data R2DBC [#10936](https://github.com/gravitee-io/issues/issues/10936)
* Improve Thread Management for RDBMS backend [#10938](https://github.com/gravitee-io/issues/issues/10938)

**Other**

* Reduce log verbosity on MFA validation failure [#10903](https://github.com/gravitee-io/issues/issues/10903)

</details>

## Gravitee Access Management 4.7.19 - October 30, 2025

<details>

<summary>Bug fixes</summary>

**Gateway**

* StackOverflowError when logging out [#10928](https://github.com/gravitee-io/issues/issues/10928)

**Console**

* Unable to delete a user when the IDP has been removed [#10915](https://github.com/gravitee-io/issues/issues/10915)

</details>

## Gravitee Access Management 4.7.18 - October 24, 2025

<details>

<summary>Bug fixes</summary>

**Gateway**

* Account's password is expired error when using account linking [#10851](https://github.com/gravitee-io/issues/issues/10851)
* Password policy apply to LDAP idp [#10874](https://github.com/gravitee-io/issues/issues/10874)

**Management API**

* Domain deletion does not remove all entities [#10899](https://github.com/gravitee-io/issues/issues/10899)

</details>

## Gravitee Access Management 4.7.17 - October 13, 2025

<details>

<summary>Bug fixes</summary>

**Management API**

* Regression in the way DataPlanes are loaded in the MAPI [#10883](https://github.com/gravitee-io/issues/issues/10883)

**Other**

* Make datasource configurable using helm values [#10884](https://github.com/gravitee-io/issues/issues/10884)

</details>

## Gravitee Access Management 4.7.16 - October 10, 2025

{% hint style="warning" %}
Version 4.7.16 is unstable. We recommend not installing this version.
{% endhint %}

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

## Gravitee Access Management 4.7.15 - September 26, 2025

<details>

<summary>Bug fixes</summary>

**Gateway**

* Enhance idp plugin redeployment to avoid downtime [#10778](https://github.com/gravitee-io/issues/issues/10778)
* Am Is Creating Discrepancies With the Issuer Claim (`iss`) in Generated Access Tokens [#10779](https://github.com/gravitee-io/issues/issues/10779)

**Management API**

* AM Upgrader are failing with list of mongo servers [#10850](https://github.com/gravitee-io/issues/issues/10850)

</details>

## Gravitee Access Management 4.7.14 - September 18, 2025

<details>

<summary>Bug fixes</summary>

**Other**

* IDP Domain whitelist [#10790](https://github.com/gravitee-io/issues/issues/10790)
* When a kafka reporter is inherited from the organization, each domain has it own producer [#10576](https://github.com/gravitee-io/issues/issues/10576)
* Reduce the number of threads with MongoDB Backend [#10713](https://github.com/gravitee-io/issues/issues/10713)
* Deleting Organization User Fails on SQL Server Due to Invalid DELETE Syntax [#10838](https://github.com/gravitee-io/issues/issues/10838)
* Incorrect audit log file formatting [#10757](https://github.com/gravitee-io/issues/issues/10757)
* Closing LDAP connections properly [#10769](https://github.com/gravitee-io/issues/issues/10769)
* NullPointerException upon first login with password expiration [#10780](https://github.com/gravitee-io/issues/issues/10780)
* Error searching for users in the UI [#10808](https://github.com/gravitee-io/issues/issues/10808)
* Replace Bitnami Mongo [#10789](https://github.com/gravitee-io/issues/issues/10789)
* Issue AM update [#10801](https://github.com/gravitee-io/issues/issues/10801)

</details>

## Gravitee Access Management 4.7.13 - August 29, 2025

<details>

<summary>Bug fixes</summary>

**Other**

* Can't get dynamic roles for the user [#10679](https://github.com/gravitee-io/issues/issues/10679)
* LDAP connection leak [#10736](https://github.com/gravitee-io/issues/issues/10736)

</details>

## Gravitee Access Management 4.7.12 - August 26, 2025

<details>

<summary>Bug fixes</summary>

**Other**

* Ciba notifier custom header config [#10739](https://github.com/gravitee-io/issues/issues/10739)
* Unable to configure IDP Http Body request [#10740](https://github.com/gravitee-io/issues/issues/10740)

</details>

## Gravitee Access Management 4.7.11 - August 15, 2025

<details>

<summary>Bug fixes</summary>

**Other**

* Can't request on values containing + char using filters for searching users [#10495](https://github.com/gravitee-io/issues/issues/10495)
* Missing MAPI audits in Global kafka reporter [#10609](https://github.com/gravitee-io/issues/issues/10609)
* Group search base in LDAP Provider in UI does not reflect backend value [#10668](https://github.com/gravitee-io/issues/issues/10668)
* FreeMarker template error [#10722](https://github.com/gravitee-io/issues/issues/10722)
* Limit concurrent HSM action at gateway level [#10731](https://github.com/gravitee-io/issues/issues/10731)
* LDAP connection leak [#10736](https://github.com/gravitee-io/issues/issues/10736)

</details>

## Gravitee Access Management 4.7.10 - August 1, 2025

<details>

<summary>Bug fixes</summary>

**Other**

* Missing indexes on Devices table [#10677](https://github.com/gravitee-io/issues/issues/10677)
* Can't get dynamic roles for the user [#10679](https://github.com/gravitee-io/issues/issues/10679)
* When an Access token is missing from the authorization endpoint and only an ID Token is returned, any token is stored in user profile [#10680](https://github.com/gravitee-io/issues/issues/10680)
* NoSuchMethodError after JwkSourceresolver update [#10696](https://github.com/gravitee-io/issues/issues/10696)
* France Connect V2 - Problem when disconnecting France Connect [#10697](https://github.com/gravitee-io/issues/issues/10697)

</details>

## Gravitee Access Management 4.7.9 - July 18, 2025

<details>

<summary>Bug fixes</summary>

**Management API**

* GET /domain/users with parameter size=0 brings back all users [#10661](https://github.com/gravitee-io/issues/issues/10661)

**Other**

* Deadlock during accessing authorization code [#10614](https://github.com/gravitee-io/issues/issues/10614)
* Intermittent remote JWK set read time out [#10669](https://github.com/gravitee-io/issues/issues/10669)

</details>

## Gravitee Access Management 4.7.8 - July 4, 2025

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

* Add token sub claim from JWT token in the TOKEN\_CREATED event [#10638](https://github.com/gravitee-io/issues/issues/10638)
* Manage Multiple AndroidKey Root CA [#10658](https://github.com/gravitee-io/issues/issues/10658)

**Management API**

* DomainOwner cannot access domain settings [#10624](https://github.com/gravitee-io/issues/issues/10624)

**Other**

* add liquibase logger in INFO by default [#10567](https://github.com/gravitee-io/issues/issues/10567)
* Improve users search queries from database in am management UI/API. [#10573](https://github.com/gravitee-io/issues/issues/10573)
* \[FC] update the sandbox urls [#10636](https://github.com/gravitee-io/issues/issues/10636)

</details>

## Gravitee Access Management 4.7.7 - June 20, 2025

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

## Gravitee Access Management 4.7.6 - June 9, 2025

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

## Gravitee Access Management 4.7.5 - May 28, 2025

<details>

<summary>Bug fixes</summary>

**Gateway**

* URL coding of user name seems to be broken [#10469](https://github.com/gravitee-io/issues/issues/10469)
* When username contains space the token generation fails [#10569](https://github.com/gravitee-io/issues/issues/10569)
* PeerCertificate not interpreted properly when it provided by header [#10586](https://github.com/gravitee-io/issues/issues/10586)

**Other**

* Access Gateway - X-Request header usage [#10552](https://github.com/gravitee-io/issues/issues/10552)

</details>

## Gravitee Access Management 4.7.4 - May 13, 2025

<details>

<summary>Bug fixes</summary>

**Management API**

* Email notification fails when user doesn't have firstName [#10536](https://github.com/gravitee-io/issues/issues/10536)

**Other**

* Reporter Upgrader is using a syntax not supported by DocumentDB [#10528](https://github.com/gravitee-io/issues/issues/10528)

</details>

## Gravitee Access Management 4.7.3 - May 6, 2025

<details>

<summary>Bug fixes</summary>

**Gateway**

* Filter audit type [#10518](https://github.com/gravitee-io/issues/issues/10518)

**Other**

* Fail to enable the AM gateway service on SUSE [#10402](https://github.com/gravitee-io/issues/issues/10402)
* Use Gravitee GPG Key to sign RPM package [#10504](https://github.com/gravitee-io/issues/issues/10504)
* Fix authentication issue with Azure AD [#10522](https://github.com/gravitee-io/issues/issues/10522)
* Support of FranceConnect API V2

</details>

## Gravitee Access Management 4.7.2 - April 25, 2025

<details>

<summary>Bug fixes</summary>

**Gateway**

* MFA "Remember Device" error when using CAS IDP [#10493](https://github.com/gravitee-io/issues/issues/10493)

**Other**

* GIS claim can be overridden with custom claim [#10472](https://github.com/gravitee-io/issues/issues/10472)

</details>

## Gravitee Access Management 4.7.1 - April 11, 2025

<details>

<summary>Bug fixes</summary>

**Gateway**

* Problem with API management console application creation/update and DCR [#10232](https://github.com/gravitee-io/issues/issues/10232)
* Login button remains disabled when using a password manager [#10411](https://github.com/gravitee-io/issues/issues/10411)
* Setting max consecutive letters to 0 in password policies using mapi displays unnecessary password requirement [#10416](https://github.com/gravitee-io/issues/issues/10416)
* Using of Redis on Production and Crash situation [#10454](https://github.com/gravitee-io/issues/issues/10454)
* Error handling error=session\_expired in Login Form [#10460](https://github.com/gravitee-io/issues/issues/10460)
* EL for language entries not resolving correctly [#10465](https://github.com/gravitee-io/issues/issues/10465)

**Management API**

* Prevent Ogranization IDP selection to send null [#10444](https://github.com/gravitee-io/issues/issues/10444)
* Fix audit log on user login failed [#10463](https://github.com/gravitee-io/issues/issues/10463)

**Other**

* Error in /ciba/authenticate/callback [#10412](https://github.com/gravitee-io/issues/issues/10412)
* \[AM]\[4.5.11] Error when character "ë" in a token [#10418](https://github.com/gravitee-io/issues/issues/10418)
* Can't update SAML SP certificate in UI application SAML tab [#10442](https://github.com/gravitee-io/issues/issues/10442)
* Management API does not check if user exists on domain when added to a group on creation of the group [#10468](https://github.com/gravitee-io/issues/issues/10468)

</details>

## AM 4.7.x

### Gravitee Access Management 4.7 - March 31, 2025 <a href="#gravitee-access-management-4.5-october-10-2024" id="gravitee-access-management-4.5-october-10-2024"></a>

<details>

<summary>What's new</summary>

#### User management improvement

On the console interface, an administrator can now see if the password set during user creation or password reset complies with the password policy rules.

#### Generic OpenID provider improvement

The Generic OpenID Identity Provider is able to support the `response_type` parameter. An administration can select `fragment` or `query` to match the supported `response_type` expected by the provider.

#### CIBA Http Notifier

The HTTP Device Notifier plugin for [CIBA](../../guides/auth-protocols/ciba.md) has been updated to accept additional headers supporting Expression Language.

#### Multi Data Plane architecture

Access Management evolves to improve the scalability and the resiliency of the solution.

This version introduces the ability to assign a domain to a Data Plane. The Management API can now access multiple Data Planes, with each Gateway linked to a single Data Plane. With this new functionality, it becomes possible to assign one database for the Control Plane data managed by the Management API service, and another for the Data Plane data managed by the Gateway.

</details>

<details>

<summary>Breaking Changes</summary>

#### Domain Creation

To create a Security Domain via the Management REST API, the `dataPlaneId` attribute is mandatory. Even if multi-data plane capabilities are not being utilized, this attribute must still be specified with the value set to "default".

#### Identity Provider

To update an IdentityProvider via the Management REST API, the `type` attribute is mandatory.

#### Extension Grant

To update an ExtensionGrant plugin via the Management REST API, the `type` attribute is mandatory.

#### AccountLinking Policy

The AccountLinking policy has been updated to version 2.0.0 to be compatible with AM 4.7.0.

{% hint style="danger" %}
versions 1.x of AccountLinking policy are not compatible with AM 4.7.0
{% endhint %}

#### AWS CloudHSM Plugin

The AWS CloudHSM plugin has been updated to version 2.0.0 to be compatible with AM 4.7.0.

{% hint style="danger" %}
versions 1.x of AWS CloudHSM plugin are not compatible with AM 4.7.0
{% endhint %}

</details>
