---
description: >-
  This page contains the changelog entries for AM 4.5.x and any future minor or
  patch AM 4.5.x releases
---


{% hint style="info" %}
When managing deployments using Helm, please note that the default startup, liveness, and readiness probes now use the httpGet method by default to request the internal API on the `/_node/health` endpoint. As a result, the internal API listens on `0.0.0.0` to allow the kubelet to check the component's status. If you don't provide custom probe definitions and have explicitly defined either the `api.http.services.core.http.host` or the `gateway.http.services.core.http.host`, ensure the value is set to `0.0.0.0`; otherwise, the probes will fail.
{% endhint %}

## AM 4.5.x

## Gravitee Access Management 4.5.28 - October 10, 2025

<details>

<summary>Bug fixes</summary>

**Gateway**

* France Connect V2 - Review wording of error message [#10738](https://github.com/gravitee-io/issues/issues/10738)





**Other**

* AWS HSM Certificate Plugin logs remain at DEBUG level despite global INFO configuration, and Helm chart indentation/mapping issue for extraLoggers. [#10824](https://github.com/gravitee-io/issues/issues/10824)
* Add helm.sh/chart to pod template annotations [#10849](https://github.com/gravitee-io/issues/issues/10849)
* User registration completion UI widget is broken [#10865](https://github.com/gravitee-io/issues/issues/10865)
* Conversion session.timeout for helm value incorrect [#10867](https://github.com/gravitee-io/issues/issues/10867)

</details>


### Gravitee Access Management 4.5.27 - September 26, 2025

<details>

<summary>Bug fixes</summary>

**Gateway**

* Enhance idp plugin redeployment to avoid downtime [#10778](https://github.com/gravitee-io/issues/issues/10778)




</details>

### Gravitee Access Management 4.5.26 - September 18, 2025

<details>

<summary>Bug fixes</summary>

**Other**

* IDP Domain whitelist [#10790](https://github.com/gravitee-io/issues/issues/10790)
* Deleting Organization User Fails on SQL Server Due to Invalid DELETE Syntax [#10838](https://github.com/gravitee-io/issues/issues/10838)
* Incorrect audit log file formatting [#10757](https://github.com/gravitee-io/issues/issues/10757)
* Closing LDAP connections properly [#10769](https://github.com/gravitee-io/issues/issues/10769)
* Error searching for users in the UI [#10808](https://github.com/gravitee-io/issues/issues/10808)
* Replace Bitnami Mongo [#10789](https://github.com/gravitee-io/issues/issues/10789)

</details>

### Gravitee Access Management 4.5.25 - August 29, 2025

<details>

<summary>Bug fixes</summary>

**Other**

* Can't get dynamic roles for the user [#10679](https://github.com/gravitee-io/issues/issues/10679)
* LDAP connection leak [#10736](https://github.com/gravitee-io/issues/issues/10736)
* Unable to configure IDP Http Body request [#10740](https://github.com/gravitee-io/issues/issues/10740)

</details>

### Gravitee Access Management 4.5.24 - August 15, 2025

<details>

<summary>Bug fixes</summary>

**Other**

* Can't request on values containing + char using filters for searching users [#10495](https://github.com/gravitee-io/issues/issues/10495)
* Group search base in LDAP Provider in UI does not reflect backend value [#10668](https://github.com/gravitee-io/issues/issues/10668)
* LDAP connection leak [#10736](https://github.com/gravitee-io/issues/issues/10736)

</details>

### Gravitee Access Management 4.5.23 - August 1, 2025

<details>

<summary>Bug fixes</summary>

**Gateway**

* Duplicate Key collection errors caused by the mongo Audit Reporter [#10670](https://github.com/gravitee-io/issues/issues/10670)

**Other**

* Missing indexes on Devices table [#10677](https://github.com/gravitee-io/issues/issues/10677)
* Can't get dynamic roles for the user [#10679](https://github.com/gravitee-io/issues/issues/10679)
* When an Access token is missing from the authorization endpoint and only an ID Token is returned, any token is stored in user profile [#10680](https://github.com/gravitee-io/issues/issues/10680)
* NoSuchMethodError after JwkSourceresolver update [#10696](https://github.com/gravitee-io/issues/issues/10696)
* France Connect V2 - Problem when disconnecting France Connect [#10697](https://github.com/gravitee-io/issues/issues/10697)
* access and refresh token purging schedule. [#10703](https://github.com/gravitee-io/issues/issues/10703)

</details>

### Gravitee Access Management 4.5.22 - July 18, 2025

<details>

<summary>Bug fixes</summary>

**Management API**

* GET /domain/users with parameter size=0 brings back all users [#10661](https://github.com/gravitee-io/issues/issues/10661)

**Other**

* Intermittent remote JWK set read time out [#10669](https://github.com/gravitee-io/issues/issues/10669)

</details>

### Gravitee Access Management 4.5.21 - July 4, 2025

<details>

<summary>Bug fixes</summary>

**Gateway**

* Manage Multiple AndroidKey Root CA [#10658](https://github.com/gravitee-io/issues/issues/10658)

</details>

### Gravitee Access Management 4.5.20 - July 1, 2025

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

**Other**

* add liquibase logger in INFO by default [#10567](https://github.com/gravitee-io/issues/issues/10567)
* Improve users search queries from database in am management UI/API. [#10573](https://github.com/gravitee-io/issues/issues/10573)
* \[FC] update the sandbox urls [#10636](https://github.com/gravitee-io/issues/issues/10636)

{% hint style="info" %}
In [#10573](https://github.com/gravitee-io/issues/issues/10573) a new configuration option is introduced to disable case-insensitive search in MongoDB. Starting from AM 4.9.0, searches will become case-sensitive by default. If you are currently experiencing search performance issues, you can disable case-insensitive search by setting the legacy.mongodb.regexCaseInsensitive property to false in the gravitee.yaml file, or by using the environment variable gravitee\_legacy\_mongodb\_regexCaseInsensitive=false
{% endhint %}

</details>

### Gravitee Access Management 4.5.19 - June 20, 2025

<details>

<summary>Bug fixes</summary>

**Gateway**

* Multiple OAuth parameters are added to URLs when multiple MFA challenges are sent [#10610](https://github.com/gravitee-io/issues/issues/10610)

**Management API**

* Users cannot view the accessPoint field in the domain audit logs if they do not have a domain role permission [#10602](https://github.com/gravitee-io/issues/issues/10602)

</details>

### Gravitee Access Management 4.5.18 - June 9, 2025

<details>

<summary>Bug fixes</summary>

**Gateway**

* Improve user login logs [#10588](https://github.com/gravitee-io/issues/issues/10588)

**Other**

* OpenAPI spec for listDomains is not correct [#10591](https://github.com/gravitee-io/issues/issues/10591)
* \[R2DBC] version 1.0.2 of SQLServer driver not working [#10565](https://github.com/gravitee-io/issues/issues/10565)

</details>

### Gravitee Access Management 4.5.17 - May 28, 2025

<details>

<summary>Bug fixes</summary>

**Gateway**

* URL coding of user name seems to be broken [#10469](https://github.com/gravitee-io/issues/issues/10469)
* When username contains space the token generation fails [#10569](https://github.com/gravitee-io/issues/issues/10569)
* PeerCertificate not interpreted properly when it provided by header [#10586](https://github.com/gravitee-io/issues/issues/10586)

**Other**

* Access Gateway - X-Request header usage [#10552](https://github.com/gravitee-io/issues/issues/10552)

</details>

### Gravitee Access Management 4.5.16 - May 13, 2025

<details>

<summary>Bug fixes</summary>

**Management API**

* Users and Groups metadata not displayed for /members endpoint [#10515](https://github.com/gravitee-io/issues/issues/10515)
* Email notification fails when user doesn't have firstName [#10536](https://github.com/gravitee-io/issues/issues/10536)

**Other**

* Reporter Upgrader is using a syntax not supported by DocumentDB [#10528](https://github.com/gravitee-io/issues/issues/10528)

</details>

### Gravitee Access Management 4.5.15 - May 6, 2025

<details>

<summary>Bug fixes</summary>

**Gateway**

* Filter audit type [#10518](https://github.com/gravitee-io/issues/issues/10518)

**Other**

* Fail to enable the AM gateway service on SUSE [#10402](https://github.com/gravitee-io/issues/issues/10402)
* Use Gravitee GPG Key to sign RPM package [#10504](https://github.com/gravitee-io/issues/issues/10504)
* Support of FranceConnect API V2

</details>

### Gravitee Access Management 4.5.14 - April 25, 2025

<details>

<summary>Bug fixes</summary>

**Gateway**

* MFA "Remember Device" error when using CAS IDP [#10493](https://github.com/gravitee-io/issues/issues/10493)

**Other**

* GIS claim can be overridden with custom claim [#10472](https://github.com/gravitee-io/issues/issues/10472)
* JDBC pool parameters are incorrectly indented in the Helm chart [#10482](https://github.com/gravitee-io/issues/issues/10482)

</details>

### Gravitee Access Management 4.5.13 - April 11, 2025

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

### Gravitee Access Management 4.5.12 - March 17, 2025

<details>

<summary>Bug fixes</summary>

**Gateway**

* MFA Challenge policy doesn't work when multiple redirect\_uri are declared [#10407](https://github.com/gravitee-io/issues/issues/10407)
* Authentication fails when MFA Challenge policy is used [#10421](https://github.com/gravitee-io/issues/issues/10421)

</details>

### Gravitee Access Management 4.5.11 - March 11, 2025

<details>

<summary>Bug fixes</summary>

**Gateway**

* RememberDevice issue with uBlock [#10388](https://github.com/gravitee-io/issues/issues/10388)
* Fix regression on redirect URL [#10404](https://github.com/gravitee-io/issues/issues/10404)

</details>

### Gravitee Access Management 4.5.10 - February 28, 2025

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

### Gravitee Access Management 4.5.9 - February 17, 2025

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

### Gravitee Access Management 4.5.8 - January 31, 2025

<details>

<summary>Bug fixes</summary>

**Gateway**

* GIS reference not removed from session with prompt=login [#10292](https://github.com/gravitee-io/issues/issues/10292)

**Other**

* Double quote prevent HTTP Provider to authenticate [#10277](https://github.com/gravitee-io/issues/issues/10277)

</details>

### Gravitee Access Management 4.5.7 - January 16, 2025

<details>

<summary>Bug fixes</summary>

**Gateway**

* Access token is generated from refresh token of deactivated user [#10258](https://github.com/gravitee-io/issues/issues/10258)

**Console**

* Bug Affichage : Administrative Roles box list illisible. [#10256](https://github.com/gravitee-io/issues/issues/10256)
* Memory user provider in fresh install has no permissions/roles [#10257](https://github.com/gravitee-io/issues/issues/10257)
* Audit log details differ between roles [#10266](https://github.com/gravitee-io/issues/issues/10266)

**Other**

* Unable to update any reporters on domain and organisation level [#10259](https://github.com/gravitee-io/issues/issues/10259)

</details>

### Gravitee Access Management 4.5.6 - January 3, 2025

<details>

<summary>Bug fixes</summary>

**Console**

* Can't configure new SSO IDP or modify existing one [#10251](https://github.com/gravitee-io/issues/issues/10251)

**Other**

* Unable to get a token using LDAP IDP [#10250](https://github.com/gravitee-io/issues/issues/10250)

</details>

### Gravitee Access Management 4.5.5 - December 20, 2024

<details>

<summary>Bug fixes</summary>

**Other**

* Certificates description on the right of the page refers to identity providers [#10201](https://github.com/gravitee-io/issues/issues/10201)
* Resize the client field for OAut2 scope repository record [#10239](https://github.com/gravitee-io/issues/issues/10239)

</details>

### Gravitee Access Management 4.5.4 - December 12, 2024

<details>

<summary>Bug fixes</summary>

**Gateway**

* SMSFactorProvider - Invalid phone number [#10193](https://github.com/gravitee-io/issues/issues/10193)
* \[4.5.1] Scope OpenID on client credential and JWT bearer [#10196](https://github.com/gravitee-io/issues/issues/10196)

**Console**

* Able to create Kafka reporter without Bootstrap server and Topic [#10156](https://github.com/gravitee-io/issues/issues/10156)

**Other**

* SlowQuery (asSorted) + Index non utilisé [#10194](https://github.com/gravitee-io/issues/issues/10194)

</details>

### Gravitee Access Management 4.5.3 - November 22, 2024

<details>

<summary>Bug fixes</summary>

**Gateway**

* Users are returned randomly via SCIM [#10147](https://github.com/gravitee-io/issues/issues/10147)

**Other**

* \[Helm Chart] Upgrader job can't be deployed [#10154](https://github.com/gravitee-io/issues/issues/10154)
* Improve WebAuthn Credential search indexes [#10165](https://github.com/gravitee-io/issues/issues/10165)

</details>

### Gravitee Access Management 4.5.2 - November 8, 2024

<details>

<summary>Bug fixes</summary>

**Management API**

* Target not displaying on audit log for delete events [#10069](https://github.com/gravitee-io/issues/issues/10069)
* Able to create a admin service user via the create domain user endpoint [#10127](https://github.com/gravitee-io/issues/issues/10127)
* System reporter can be deleted via API [#10155](https://github.com/gravitee-io/issues/issues/10155)

**Other**

* JDBC - Device identifier errors - management, gateway and UI [#10139](https://github.com/gravitee-io/issues/issues/10139)
* BadSqlGrammarException after 4.5.0 Upgrade [#10148](https://github.com/gravitee-io/issues/issues/10148)

</details>

### Gravitee Access Management 4.5.1 - October 25, 2024

<details>

<summary>Bug fixes</summary>

**Gateway**

* AM Refresh token active set to false [#10065](https://github.com/gravitee-io/issues/issues/10065)
* The "path" parameter for SCIM patch requests does not function as expected [#10073](https://github.com/gravitee-io/issues/issues/10073)
* why does "Skip MFA enrollment" also skips MFA validation on login [#10086](https://github.com/gravitee-io/issues/issues/10086)
* Password rules not displayed in the registration confirmation webpage [#10089](https://github.com/gravitee-io/issues/issues/10089)

**Other**

* /sendChallenge returns status code 0 [#10097](https://github.com/gravitee-io/issues/issues/10097)
* Original access token out of an OpenID federation is not able to be used for the mapping into the ID token going back to the application [#10104](https://github.com/gravitee-io/issues/issues/10104)
* Gravitee AM SAML not working [#10106](https://github.com/gravitee-io/issues/issues/10106)
* Error message on IP filtering policy always returns remote address [#10108](https://github.com/gravitee-io/issues/issues/10108)

</details>

### Gravitee Access Management 4.5 - October 10, 2024

{% hint style="warning" %}
AM 4.5.0 introduce some deprecations which may have an impact on your systems. Please refer to the "Deprecations" section here after for more details.
{% endhint %}

<details>

<summary>What's new</summary>

#### Repositories

A new repository scope named `gateway` has been introduced in AM 4.5.0.

#### Token generation

For all domains created from AM 4.5.0 the `sub` claim will not represent the user internalID as it was the case previously.

#### AWS Certificate plugin

An AWS certificate plugin is now available as EE feature. Thanks to this plugin you can load certificate provided by AWS Secret Manager.

#### Reporters

Reporters have been improved in this new version of Access Management:

* additional reporters can be configured as "global" in order to collect audits events coming from all the domains linked to this organization.
* Events for domain creation and domain deletion are now published in the organization reporters.
* The kafka reporter has been improved to manage Schema Registry

#### OpenID

We improved the OAuth2 / OpenID specification more strictly regarding the usage of the response\_mode paramet

#### Group mapper

Identity Providers now provide a [Group Mapper](docs/am/4.5/guides/identity-providers/user-and-role-mapping.md) section.

#### Cache Layer

A cache layer has been introduce to limit the Database access during the user authentication flow.

#### Upgrader framework

AM now provide the same upgrader framework as APIM meaning that from 4.5.0, no manual scripts need to be executed before an upgrade. When AM is deployed on kuberneetes using Helm, the value `api.upgrader` needs to be set to `true` so before starting the Management API or the Gateway the helm chart will deploy a job to execute the upgraders.

</details>

<details>

<summary>Breaking Changes</summary>

#### Redirect Uris

On application creation or update `redirect_uris` is now required for application with type WEB, NATIVE or SPA.

#### Token generation

For all domains created from AM 4.5.0 the `sub` claim will not represent the user internalID as it was the case previously. The `sub` value is now an opaque value computed based on the user externalId and the identity provider identifier. Even if this value is opaque, it will remain the same for a given user across multiple token generations as per the requirement of the OIDC specification.

<mark style="color:red;">**NOTE:**</mark> For all domains created in previous version, the sub claim remains the user internalId.

#### Repositories

A new repository scope named `gateway` has been introduced in AM 4.5.0.

The new gateway scope will manage entities which was previously managed by the `oauth2` scope and the `management` scope:

* ScopeApproval
* AuthenticationFlowContext
* LoginAttempts
* RateLimit
* VerifyAttempt

If you managed to define two different databases for the `management` and the `oauth2` scopes, please configure the `gateway` scope to target the same database as the `oauth2` scope as ScopeApproval are now managed by the `gateway` scope. If you want to dedicate a database for the gateway scope you will have to migrate the scope\_approvals collection to the new database.

Previously, all the settings related to the repositories where define at the root level of the `gravitee.yaml` with the scope name as section name

{% code lineNumbers="true" %}
```yaml
management:
  type: mongodb
  mongodb: 
    uri: ...
    
oauth2:
  type: mongodb
  mongodb: 
    uri: ...
```
{% endcode %}

Starting from 4.5.0, a `repositories` section has been introduce to easily identify the settings related to the repository layer.

<pre class="language-yaml" data-line-numbers><code class="lang-yaml"><strong>repositories:
</strong><strong>  management:
</strong><strong>    type: mongodb
</strong>    mongodb: 
      uri: ...
    
  oauth2:
    type: mongodb
    mongodb: 
      uri: ...
  
  gateway:
    type: mongodb
    mongodb: 
      uri: ...
</code></pre>

If you were using environment variable to provide database settings remember to:

* adapt the variable name to include the "repositories" keyword, for example:\
  `GRAVITEE_MANAGEMENT_TYPE=... => GRAVITEE_REPOSITORIES_MANAGEMENT_TYPE=...`
* add the settings for the gateway scope\
  `GRAVITEE_GATEWAY_TYPE=... => GRAVITEE_REPOSITORIES_GATEWAY_TYPE=...`

</details>

<details>

<summary>Deprecations</summary>

#### Audits

For kafka and File reporters, the `status` attribute has been deprecated for removal. The recommended way to get access to the status is now the `outcome` structure which contains the `status` and a `message` fields. If you are using one of these reporter, please update your consumer to rely on the outcome structure

</details>
