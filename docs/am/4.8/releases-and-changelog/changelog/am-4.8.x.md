---
description: >-
  This page contains the changelog entries for AM 4.8.0 and any future minor or
  patch AM 4.8.x releases
---

# AM 4.8.x

## Gravitee Access Management 4.8.9 - October 13, 2025

{% hint style="danger" %}
Version 4.8.9 is unstable. We recommend not installing this version.
{% endhint %}

<details>

<summary>Bug fixes</summary>

**Management API**

* Regression in the way DataPlanes are loaded in the MAPI [#10883](https://github.com/gravitee-io/issues/issues/10883)

**Other**

* Make datasource configurable using helm values [#10884](https://github.com/gravitee-io/issues/issues/10884)

</details>

## Gravitee Access Management 4.8.8 - October 10, 2025

{% hint style="danger" %}
Version 4.8.8 is unstable. We recommend not installing this version.
{% endhint %}

<details>

<summary>Bug fixes</summary>

**Gateway**

* France Connect V2 - Review wording of error message [#10738](https://github.com/gravitee-io/issues/issues/10738)

**Management API**

* Sanitize the redirect\_uri to avoid empty segment when cockpit try to connect on the console [#10805](https://github.com/gravitee-io/issues/issues/10805)
* Secrets for old applications can't be renewed [#10871](https://github.com/gravitee-io/issues/issues/10871)

**Other**

* Introduce common connection pool for MongoIDP [#10719](https://github.com/gravitee-io/issues/issues/10719)
* AWS HSM Certificate Plugin logs remain at DEBUG level despite global INFO configuration, and Helm chart indentation/mapping issue for extraLoggers. [#10824](https://github.com/gravitee-io/issues/issues/10824)
* Limit the batchSize on Mongo Reporter request [#10846](https://github.com/gravitee-io/issues/issues/10846)
* Add helm.sh/chart to pod template annotations [#10849](https://github.com/gravitee-io/issues/issues/10849)
* User registration completion UI widget is broken [#10865](https://github.com/gravitee-io/issues/issues/10865)
* Conversion session.timeout for helm value incorrect [#10867](https://github.com/gravitee-io/issues/issues/10867)
* Improve logging in EnrichAuthFlowPolicy [#10875](https://github.com/gravitee-io/issues/issues/10875)

</details>

## Gravitee Access Management 4.8.7 - September 26, 2025

<details>

<summary>Bug fixes</summary>

**Gateway**

* Enhance idp plugin redeployment to avoid downtime [#10778](https://github.com/gravitee-io/issues/issues/10778)
* Am Is Creating Discrepancies With the Issuer Claim (`iss`) in Generated Access Tokens [#10779](https://github.com/gravitee-io/issues/issues/10779)

**Management API**

* AM Upgrader are failing with list of mongo servers [#10850](https://github.com/gravitee-io/issues/issues/10850)

</details>

## Gravitee Access Management 4.8.6 - September 18, 2025

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

## Gravitee Access Management 4.8.5 - August 29, 2025

<details>

<summary>Bug fixes</summary>

**Other**

* Can't get dynamic roles for the user [#10679](https://github.com/gravitee-io/issues/issues/10679)
* LDAP connection leak [#10736](https://github.com/gravitee-io/issues/issues/10736)
* Ciba notifier custom header config [#10739](https://github.com/gravitee-io/issues/issues/10739)
* Unable to configure IDP Http Body request [#10740](https://github.com/gravitee-io/issues/issues/10740)

</details>

## Gravitee Access Management 4.8.4 - August 15, 2025

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

## Gravitee Access Management 4.8.3 - August 1, 2025

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

</details>

## Gravitee Access Management 4.8.2 - July 18, 2025

<details>

<summary>Bug fixes</summary>

**Management API**

* GET /domain/users with parameter size=0 brings back all users [#10661](https://github.com/gravitee-io/issues/issues/10661)

**Other**

* Deadlock during accessing authorization code [#10614](https://github.com/gravitee-io/issues/issues/10614)
* Intermittent remote JWK set read time out [#10669](https://github.com/gravitee-io/issues/issues/10669)
* Allow AM to receive a JWT from an IDP rather than just JSON [#10673](https://github.com/gravitee-io/issues/issues/10673)

</details>

## Gravitee Access Management 4.8.1 - July 4, 2025

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

#### Gravitee Access Management 4.8 - June 20, 2025 <a href="#gravitee-access-management-4.8" id="gravitee-access-management-4.8"></a>

<details>

<summary>What's new</summary>

Client secret improvement

An application can now be configured to accept multiple client secrets. Each secret may have an associated expiration date, and a notification system has been implemented to alert the primary domain owner of any secrets nearing expiration. Refer to the [client-secrets.md](../../guides/applications/client-secrets.md "mention") documentation for additional details.

**FranceConnect**

The [FranceConnect Identity](../../guides/identity-providers/legal-identity-providers/franceconnect.md) provider is now able to support the version 2 of the FranceConnect API.

**Support for PBKDF2**

MongoDB and JDBC identity providers now support the PBKDF2 password encoder.

**Custom SCIM property**

The `forceResetPassword` attribute is managed as a custom property on the user profile. When this attribute is set to `true`, the user is required to update their password immediately after the login phase.

```
'urn:ietf:params:scim:schemas:extension:custom:2.0:User': {
  forceResetPassword: true
},
```

**Dynamic query parameter in redirect URI**

The Dynamic Redirect URI Parameters feature in the OAuth2 flow enhances flexibility and control over redirection behavior by letting you append dynamic parameters to the final `redirect_uri`. These parameters are resolved using [Gravitee Expression Language (EL)](https://app.gitbook.com/o/8qli0UVuPJ39JJdq9ebZ/s/ySqSVpDHfKA0fNml1fVO/), which lets you insert custom logic and data into the redirect URL Refer to the [dynamic-redirect-uri-parameters.md](../../guides/auth-protocols/oauth-2.0/dynamic-redirect-uri-parameters.md "mention") documentation for additional details.

</details>

[\
](https://documentation.gravitee.io/am/releases-and-changelog/changelog)
