---
description: >-
  This page contains the changelog entries for AM 4.8.0 and any future minor or
  patch AM 4.8.x releases
---

# AM 4.8.x

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
If the page templates have been customized, it is necessary to include the JavaScript scripts related to this new plugin.
For login, reset_password, registration and registration_confirmation, please add:

```
<script th:if="${rememberDeviceIsActive && deviceIdentifierProvider == 'CookieDeviceIdentifier'}" th:src="@{assets/js/device-type-v1.js}"></script>
<script th:if="${rememberDeviceIsActive && deviceIdentifierProvider == 'CookieDeviceIdentifier'}" th:attr="nonce=${script_inline_nonce}">
    const deviceId = "[[${cookieDeviceIdentifier}]]" ;

    $(document).ready(function () {
        $("#form").append('<input type="hidden" name="deviceId" value="' + deviceId + '"/>')
        $("#form").append('<input type="hidden" name="deviceType" value="' + retrievePlatform(window.navigator) + '"/>');
    });
</script>
````

For webauthn_login, please add :
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

* Add token sub claim from JWT token in the TOKEN_CREATED event [#10638](https://github.com/gravitee-io/issues/issues/10638)
* Manage Multiple AndroidKey Root CA [#10658](https://github.com/gravitee-io/issues/issues/10658)

**Management API**

* DomainOwner cannot access domain settings [#10624](https://github.com/gravitee-io/issues/issues/10624)



**Other**

* add liquibase logger in INFO by default [#10567](https://github.com/gravitee-io/issues/issues/10567)
* Improve users search queries from database in am management UI/API. [#10573](https://github.com/gravitee-io/issues/issues/10573)
* [FC] update the sandbox urls [#10636](https://github.com/gravitee-io/issues/issues/10636)

</details>


#### Gravitee Access Management 4.8 - June 20, 2025 <a href="#gravitee-access-management-4.8" id="gravitee-access-management-4.8"></a>

<details>

<summary>What's new</summary>

Client secret improvement

An application can now be configured to accept multiple client secrets. Each secret may have an associated expiration date, and a notification system has been implemented to alert the primary domain owner of any secrets nearing expiration. Refer to the [client-secrets.md](../../guides/applications/client-secrets.md "mention") documentation for additional details.

#### FranceConnect

The [FranceConnect Identity](../../guides/identity-providers/legal-identity-providers/franceconnect.md) provider is now able to support the version 2 of the FranceConnect API.

#### Support for PBKDF2

MongoDB and JDBC identity providers now support the PBKDF2 password encoder.

#### Custom SCIM property

The `forceResetPassword` attribute is managed as a custom property on the user profile. When this attribute is set to `true`, the user is required to update their password immediately after the login phase.

```
'urn:ietf:params:scim:schemas:extension:custom:2.0:User': {
  forceResetPassword: true
},
```

#### Dynamic query parameter in redirect URI

The Dynamic Redirect URI Parameters feature in the OAuth2 flow enhances flexibility and control over redirection behavior by letting you append dynamic parameters to the final `redirect_uri`. These parameters are resolved using [Gravitee Expression Language (EL)](https://app.gitbook.com/s/ySqSVpDHfKA0fNml1fVO/), which lets you insert custom logic and data into the redirect URL Refer to the [dynamic-redirect-uri-parameters.md](../../guides/auth-protocols/oauth-2.0/dynamic-redirect-uri-parameters.md "mention") documentation for additional details.

</details>

[\
](https://documentation.gravitee.io/am/releases-and-changelog/changelog)
