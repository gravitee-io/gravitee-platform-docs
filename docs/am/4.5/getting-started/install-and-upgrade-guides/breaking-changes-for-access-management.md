---
description: >-
  This page describes the breaking changes that may occur when upgrading
  Gravitee Access Management
---

# Breaking changes for Access Management

## Breaking changes from 4.X

Here are the breaking changes from versions 4.X of Gravitee.

### 4.5.0

**Redirect Uris**

When you create or update an application, `redirect_uris` is required with the following types:&#x20;

* WEB
* NATIVE
* SPA

**Token generation**

Before this update, the `sub` claim represented the user internalID.

With this update, the `sub` value is an opaque value, which is based on the user externalId and the identity provider identifier. As per the requirement of the OIDC specification, even if this value is opaque, it remains the same for a user across multiple token generations.&#x20;

{% hint style="info" %}
For all domains that you created in previous versions, the `sub` claim remains the user internalId.
{% endhint %}

**Repositories**

Before this update, the following entities were managed by the `oauth2` scope and the `management` scope:

* ScopeApproval&#x20;
* AuthenticationFlowContext
* LoginAttempts
* RateLimit
* VerifyAttempt

Also, you defined the settings related to the repositories at the root level of the `gravitee.yaml` with the scope name as the section name:

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

With this update, there is a new repository scope named `gateway`, which manages these entities instead of the `oauth2` scope and the `management` scope. As the `gateway` scope manages the ScopeApproval, if you defined two different databases for the `management` and the `oauth2` scope, configure the `gateway` to target the same database as `oauth2`.&#x20;

Also, a `repositories` section has been introduced to identify the settings related to the repository layer:

{% code lineNumbers="true" %}
```yaml
repositories:
  management:
    type: mongodb
    mongodb: 
      uri: ...
    
  oauth2:
    type: mongodb
    mongodb: 
      uri: ...
  
  gateway:
    type: mongodb
    mongodb: 
      uri: ...
```
{% endcode %}

{% hint style="info" %}
If you use the environment variable to provide database settings, complete the following actions:

* adapt the variable name to include the "repositories" keyword, for example:\
  `GRAVITEE_MANAGEMENT_TYPE=... => GRAVITEE_REPOSITORIES_MANAGEMENT_TYPE=...`
* add the settings for the gateway scope\
  `GRAVITEE_GATEWAY_TYPE=... => GRAVITEE_REPOSITORIES_GATEWAY_TYPE=...`


{% endhint %}

### 4.0.0

**MongoDB index names**

The MongoDB indices are named using the first letters of the fields that compose the index. This change allows the automatic management of index creation on DocumentDB. This change requires the execution of a MongoDB script to delete, and then recreate AM indices. For more information about this change, see the [migration guide](https://documentation.gravitee.io/am/4.0/getting-started/install-and-upgrade-guides/upgrade-guide).

**Enterprise Edition plugins**

Some plugins are available to only Enterprise Edition and requires a license to use them. For more information about the Enterprise Edition plugins, see the [changelog](https://documentation.gravitee.io/am/4.0/releases-and-changelog/changelog/am-4.0.x)

## Breaking changes from 3.X

Here are the breaking changes from versions 3.X of Gravitee.

### 3.21.6, 3.20.11, and 3.19.17

**Rename or Remove users with duplicate user name**

&#x20;In the **users** collection/table in AM version 3.21.6 / 3.20.11 / 3.19.17, there is a unique constraint on the `username` field. This constraint fixes the [AM-680](https://github.com/gravitee-io/issues/issues/9117) bug to avoid users with the same user name within an identity provider (IDP). Users with same user name are not active users, and it is not possible to log in using these user’s details. As a result, you may experience issues while upgrading Access Management (AM) from any previous version to 3.21.6 in case the **users** collection/table already has more than one user with the same user name in the `username` field. For the relational database, there could be a unique constraint error in the management API log and for the MongoDB ,the application may not start as MongoDB  does not apply the unique constraint due to duplicate data. To start the application, you need to rename or delete the duplicate users from both the **users** collection/table and the corresponding identity provider collection/table.

To delete the duplicate users, complete the following steps :

1. Run a query to find all the users with the duplicate user name from the **users** collection/table.
2. Rename or Delete these users from the corresponding identity provider collection/table.
3. Rename or Delete these users from the users collection/table.

**MongoDB**

{% hint style="danger" %}
Complete these steps in a test environment first.
{% endhint %}

To view a migration script that can help you, go to [GitHub](https://github.com/gravitee-io/gravitee-access-management/blob/master/docs/upgrades/username\_uniqueness/username\_uniqueness.js). This script identifies duplicates and renames some of them according to the connection metadata for each profile. The mostly used profile is considered as the reference and other will be renamed with a "\_TO\_RENAME\_OR\_DELETE" suffix.

For safety, this script define at the beginning a boolean **dryRun** set to **true** to only display the script output and see the action that is applied in case of duplicate. To effectively process the changes, you have to define this variable to **false**.

We strongly recommend executing this script in a test environment first. Backup the database before executing in the production environment.

{% hint style="info" %}
Whatever the dryRun value is, this script generates a summary in JSON format about actions that have been applied. If there are some errors entries, you have to check into the database and manually manage these cases.
{% endhint %}

```bash
 $>mongosh mongohostname:27017/gravitee-am /tmp/username_uniqueness.js | tee /tmp/script.out
```

**Relational Database**

{% hint style="danger" %}
Complete these steps in a test environment first.
{% endhint %}

To help you, A liquibase script is executed. This script identifies duplicates and rename some of them according to the connection metadata for each profile. The mostly used profile is considered as the reference and other is renamed with a "\_TO\_RENAME\_OR\_DELETE" suffix.

We strongly recommend executing upgrade in a test environment first. Backup the database before executing in the production environment.

If the Management API startup fails, check the logs and see if some duplicates are on error. If there aere errors, for these specific usernames, you will to manually rename them.

If a username cannot be duplicate, there is an error into the logs referencing the username and the identity provider.

{% hint style="info" %}
* In case of liquibase script error, the management API may fail to start and the **databasechangeloglock** has the `locked` column set to true. Once the duplicate is managed manually, the `locked` columns have to be updated to false to make the liquibase execution possible. You can update the lock using this query : `UPDATE DATABASECHANGELOGLOCK SET LOCKED=0`
* After the migration, make sure that the **idp\_users\_xxx** tables contains a unique index in the username column. If there is no index, create this index.


{% endhint %}

Here are two types of User entry errors:

```bash
Username 'duplicateuser' can't be processed due to unknown identity provider with id 'idpinternal'
Duplicate user detected in IdentityProvider different from the default one for username 'duplicateuser' and idp 'idpinternal'
```

Organization User entry example:

```bash
Organization Username 'duplicateuser' migration only manages gravitee & cockpit identity providers
```

Run the following **select** statement to identify all data with duplicate user name before the upgrade.

```bash
-- on USERS table
select id, u.username, u.source
from users u,
(select username, source
from (select username, source, count(username) as count
from users
group by source, username) as multiEntries
where multiEntries.count > 1) aa
where u.username = aa.username
and u.source = aa.source

-- on ORGANIZATION_USERS table
select id, u.username, u.source
from organization_users u,
(select username, source
from (select username, source, count(username) as count
from organization_users
group by source, username) as multiEntries
where multiEntries.count > 1) aa
where u.username = aa.username
and u.source = aa.source
```

**Manual actions in case of errors**

_Rename duplicate for users table_

1. Select the username on error.

```bash
select id, external_id, username, source, logins_count, logget_at, created_at from users where username = 'duplicateuser' and source = 'idpinternal';
"id"	"external_id"  "username"  "source"  "logins_count"  "logget_at"  "created_at"
"xxxxxxxx-eeee-aaaa-bc0b-7bef9bec6af4" "xxxxxxxx-ef9b-4c6a-bc0b-7bef9bec6af4"	"duplicateuser"  "idpinternal" '1' '2023-10-11 13:18:21.555' '2023-10-11 13:18:20.555'
"yyyyyyyy-bbbb-cccc-bc0b-7bef9bec6af4" "yyyyyyyy-ef9b-4c6a-bc0b-7bef9bec6af4"	"duplicateuser"  "idpinternal" '0' '2023-10-11 13:18:20.555' '2023-10-11 13:18:20.555'
```

2. Second search for the identity provider linked to the user.

```bash
select id, type, name, configuration from identities where id = 'idpinternal';
```

3. Based on the identity provider type, the action maybe different. In this procedure, we are considering an JDBC IDP. Check the configuration field's connection settings to the IDP database, the table, and the table column containing the entry id, external ID of the user table, and the table column containing the username.

```bash
select id, username from idp_table where username = 'duplicateuser';
"id"	"username"
"xxxxxxxx-ef9b-4c6a-bc0b-7bef9bec6af4"	"duplicateuser"
"yyyyyyyy-ef9b-4c6a-bc0b-7bef9bec6af4"	"duplicateuser"
```

4. Based on the users table query output, choose the one that you want to preserve, and then rename to order into the the users table and into the idp table. Ensure that the user you are updating the exrernal\_id in the users table matching the user id into the idp table.

**Rename duplicate from Organization users Table**

The procedure is the same as the one for the **users** table but need to be applied on the **organization\_users** table.

### 3.21

**Docker Images**

To be compliant with [CIS\_Docker\_v1.3.1\_L1](https://www.tenable.com/audits/items/CIS\_Docker\_v1.3.1\_L1\_Docker\_Linux.audit:bdcea17ac365110218526796ae3095b1) ,the docker images  use the `graviteeio` user. This change means that if you use the official images and deploy them on your k8s installation, nothing changes. If you build your own Dockerfile from Gravitee images, you must provide the correct rights according to your modifications. If you deploy on `openshift`, you have to add the following configuration:

```bash
securityContext:
    runAsGroup: 1000
```

**RxJava 3 and Plugins**

The introduction of RxJava3 lead to upgrades on plugins that were both dependent on this library directly or through Access Management libraries:

* [gravitee-am-factor-otp-sender - 2.0.0](https://download.gravitee.io/#pre-releases/graviteeio-ee/am/plugins/factors/gravitee-am-factor-otp-sender/)
* [gravitee-am-factor-fido2 - 2.0.0](https://download.gravitee.io/#pre-releases/graviteeio-ee/am/plugins/factors/gravitee-am-factor-fido2/)
* [gravitee-am-factor-http - 2.0.0](https://download.gravitee.io/#pre-releases/graviteeio-ee/am/plugins/factors/gravitee-am-factor-http/)
* [gravitee-am-identityprovider-kerberos - 2.0.0](https://download.gravitee.io/#pre-releases/graviteeio-ee/am/plugins/idps/gravitee-am-identityprovider-kerberos/)
* [gravitee-am-identityprovider-cas - 2.0.0](https://download.gravitee.io/#pre-releases/graviteeio-ee/am/plugins/idps/gravitee-am-identityprovider-cas/)
* [gravitee-am-identityprovider-http-flow - 2.0.0](https://download.gravitee.io/#pre-releases/graviteeio-ee/am/plugins/idps/gravitee-am-identityprovider-http-flow/)
* [gravitee-am-identityprovider-saml - 2.0.0](https://download.gravitee.io/#pre-releases/graviteeio-ee/am/plugins/idps/gravitee-am-identityprovider-saml2-generic/)
* [gravitee-am-gateway-handler-saml2-idp - 2.0.0](https://download.gravitee.io/#pre-releases/graviteeio-ee/am/plugins/gateway/handlers/gravitee-am-gateway-handler-saml2-idp/)
* [gravitee-service-geoip - 2.0.0](https://download.gravitee.io/#plugins/services/gravitee-service-geoip/)
* [gravitee-risk-assessment - 2.0.0](https://download.gravitee.io/#graviteeio-ee/plugins/services/risk-assessment/gravitee-risk-assessment-core/)

Some of the plugins are still in alpha. They will soon be released after Access Management 3.21.x.

### 3.20

**Improved security on default installations of Access Management**

With this update, the following are enabled to improve security:

* CSP directives
* &#x20;X-XSS-Protection header
* X-Frame-Options header&#x20;

&#x20;Analyze your deployment needs to adapt the default values that we put in place.

### 3.19

**Theme and Branding**

With this update, there is a  [**theme builder**](https://docs.gravitee.io/am/current/am\_userguide\_branding\_theme\_builder.html)**,** which enables Access Management (AM) users to create unique AM templates. The theme builder has new assets that are  used by the default forms and emails of AM. All the assets provided before AM 3.19 are still served by the Gateway to render the old form templates. Those assets are deprecated and will be removed in a future version. Here is a list of deprecated assets:

* css/access\_confirmation.css
* css/forgot\_password.css
* css/login.css
* css/mfa\_challenge\_alternatives.css
* css/mfa\_challenge.css
* css/mfa\_enroll.css
* css/mfa\_recover\_code.css
* css/password\_validation.css
* css/register.css
* css/registration\_confirmation.css
* css/reset\_password.css
* css/webauthn\_login.css
* css/webauthn\_register.css
* js/password-validation.js

**Mitigate Cross Site Scripting (XSS) and Cross Site Framing**

{% hint style="danger" %}
By default in AM 3.20, to improve security on default installations of AccessManagement, CSP directives, X-XSS-Protection header, and X-Frame-Options header are enabled. Analyze your deployment needs to adapt the default values that we put in place.
{% endhint %}

Gateway CSP:

```
csp:
    script-inline-nonce: true
    directives:
      - "default-src 'self';"
      - "script-src 'self' https://cdn.jsdelivr.net/npm/@fingerprintjs/fingerprintjs@3/dist/fp.min.js https://cdn.jsdelivr.net/npm/@fingerprintjs/fingerprintjs-pro@3/dist/fp.min.js *.gstatic.com *.google.com;"
      - "img-src 'self' data: 'unsafe-inline';"
      - "style-src 'self' 'unsafe-inline';"
      - "frame-ancestors 'none';"
      - "frame-src 'self' https://www.google.com;"
```

Gateway XSS-Protection:

```
 xss:
    action: 1; mode=block
```

Gateway X-Frame-Option:

```
 xframe:
    action: DENY
```

### 3.18

**Bundle Community Edition and Enterprise Edition**

{% hint style="warning" %}
Access Management versions from 3.17.2 to 3.17.4 haven been impacted by a regression introduced in the 3.17.2 version of AM. We strongly advise you to upgrade directly to the 3.17.5 or 3.18.4 minimum. For more details about this change, see [Upgrade to 3.18](https://docs.gravitee.io/am/current/am\_installguide\_migration.html#upgrade\_to\_3\_17\_2\_3\_17\_3\_3\_17\_4\_3\_18\_0\_3\_18\_1\_3\_18\_2\_3\_18\_3).
{% endhint %}

With this update, Gravitee provides a single bundle for the Access Management (AM) Community Edition (CE) and Enterprise Edition (EE). By default, this bundle or docker image provide CE features and they do not contain EE plugins. If you want to start AM EE with plugins that you paid for, you have to deploy the license key and EE plugin that you need.

_Start AM EE with Docker_

If you use docker to start AM, after a docker-compose, you find a snippet that mounts two volumes to complete the following actions:

* To deploy enterprise plugins in an additional plugin directory.
* To deploy the license file.

```
management:
    image: graviteeio/am-management-api:3.18.0
    container_name: gio_am_management
    volumes:
      - /path/to/plugins-dir:/opt/graviteeio-am-management-api/plugins-ee
      - /path/to/license-dir/license.key:/opt/graviteeio-am-management-api/license/license.key
    environment:
      - GRAVITEE_PLUGINS_PATH_0=/opt/graviteeio-am-management-api/plugins
      - GRAVITEE_PLUGINS_PATH_1=/opt/graviteeio-am-management-api/plugins-ee

  gateway:
    image: graviteeio/am-gateway:3.18.0
    container_name: gio_am_gateway
    restart: always
    volumes:
      - /path/to/plugins-dir:/opt/graviteeio-am-gateway/plugins-ee
      - /path/to/license/license.key:/opt/graviteeio-am-gateway/license/license.key
    environment:
      - GRAVITEE_PLUGINS_PATH_0=/opt/graviteeio-am-gateway/plugins
      - GRAVITEE_PLUGINS_PATH_1=/opt/graviteeio-am-gateway/plugins-ee
```

_Deploy AM EE with Helm_

If you use helm, you have to mount the license file using a secret, and then in the `additionalPlugins` section for the gateway and the api, specify which EE plugin to download.

```
gateway:
  additionalPlugins:
  - https://download.gravitee.io/graviteeio-ee/am/plugins/idps/gravitee-am-identityprovider-saml2-generic/gravitee-am-identityprovider-saml2-generic-<version>.zip
  extraVolumeMounts: |
    - name: graviteeio-license
      mountPath: /opt/graviteeio-am-gateway/license
      readOnly: true
  extraVolumes: |
    - name: graviteeio-license
      secret:
        secretName: graviteeio-license

api:
  additionalPlugins:
  - https://download.gravitee.io/graviteeio-ee/am/plugins/idps/gravitee-am-identityprovider-saml2-generic/gravitee-am-identityprovider-saml2-generic-<version>.zip
  extraVolumeMounts: |
    - name: graviteeio-license
      mountPath: /opt/graviteeio-am-management-api/license
      readOnly: true
  extraVolumes: |
    - name: graviteeio-license
      secret:
        secretName: graviteeio-license
```

**WebAuthn (passwordless) V2 JavaScript files**

To better match the recommendation asked by Apple to use biometric devices for WebAuthn (passwordless) feature, backend APIs and JavaScript scripts have been updated to reflect that change.

If you use webauthn JavaScript scripts in your custom HTML templates, we strongly advise you to use the v2 version started from the 3.18.0 version.

For more information about the recommendation from Apple, go to [WebKit Bugzilla](https://bugs.webkit.org/show\_bug.cgi?id=213595).

```bash
WebAuthn Register

--- <script th:src="@{../assets/js/webauthn.auth.js"></script>
--- <script th:src="@{../assets/js/webauthn-register.js}"></script>

+++ <script th:src="@{../assets/js/webauthn.auth-v2.js"></script>
+++ <script th:src="@{../assets/js/webauthn-register-v2.js}"></script>
```

```bash
WebAuthn Login

--- <script th:src="@{../assets/js/webauthn.auth.js"></script>
--- <script th:src="@{../assets/js/webauthn-login.js}"></script>

+++ <script th:src="@{../assets/js/webauthn.auth-v2.js"></script>
+++ <script th:src="@{../assets/js/webauthn-login-v2.js}"></script>
```

**IP, User Agent, and User consent**

The User IP and User-Agent used for audit logs require the user to consent to exploit the information.

* `uc_geoip` : consent for IP and geolocation
* `uc_ua` : consent for User Agent

You can use the following code:&#x20;

```bash
 <input class="mdl-checkbox__input" type="checkbox" th:checked="${uc_geoip}" id="uc_geoip" name="uc_geoip">
    <input class="mdl-checkbox__input" type="checkbox" th:checked="${uc_ua}" id="uc_ua" name="uc_ua">
```

If the use have consented to these, you can simply add those inputs as `hidden` form fields. Here is an example:&#x20;

```bash
 <input class="mdl-checkbox__input" type="hidden" th:value="on"  id="uc_geoip" name="uc_geoip">
    <input class="mdl-checkbox__input" type="hidden" th:value="on"  id="uc_ua" name="uc_ua">
```

For more information about this change, see [Risk-based MFA](https://docs.gravitee.io/am/current/am\_userguide\_mfa\_risk\_based.html#user\_activity\_and\_consent).

{% hint style="info" %}
From **3.18.6**, you can implicit user consent in **gravitee.yml** file on the gateway side. In the **consent** section of the yml file, variable **ip** and **user-agent** is introduced for collecting user consent implicitly.
{% endhint %}

### 3.17.2

{% hint style="warning" %}
Access Management versions from 3.17.2 to 3.17.4 haven been impacted by a regression introduced in the 3.17.2 version of AM. We strongly advise you to upgrade directly to the 3.17.5 or 3.18.4 minimum. For more details about this change, see [Upgrade to 3.18](https://docs.gravitee.io/am/current/am\_installguide\_migration.html#upgrade\_to\_3\_17\_2\_3\_17\_3\_3\_17\_4\_3\_18\_0\_3\_18\_1\_3\_18\_2\_3\_18\_3).
{% endhint %}

**Automatic redirection to External IDP**

Access Management 3.17.0 introduced the selection rules on application identity providers. These rules are used in accordance with the identifier-first login feature to redirect to the identity provider based on the defined rule and the user input.&#x20;

With this update, the rules on external identity providers are evaluated also during the get login page to redirect quickly to the relevant provider and save a user interaction.

### 3.17

**Allowed domain lists**

Due to the selection rule feature added in application identity providers, domain whitelists now operate after login and not after identifier-first login. For more information about this change, see[Identifier-first Login Flow](https://docs.gravitee.io/am/current/am\_userguide\_login\_identifier\_first\_login\_flow.html)

**Application Identity Providers**

At application level, identity providers support the following actions:

* Priority: When the end user tries to log in, the application will first try to log in with the highest priority identity provider.
* Selection rule: When the end user tries to log in, the application will try to log in with the identity provider that matches the rule.

For more information about this change, see [Application Identity Providers](https://docs.gravitee.io/am/current/am\_userguide\_client\_identity\_providers.html).

Also, at management-api level, the schema changes to save the new application configuration:

* Prior to this update:

```
{
    ...
    "identities": [
      "idp-id-1", "idp-id-2", "idp-id-3"
    ],
    ...
}
```

* After this update:

```
{
    ...
    "identityProviders":[
      { "identity" : "idp-id-1", "selectionRule" : "", "priority": 0 },
      { "identity" : "idp-id-2", "selectionRule": "{#request.params['username'] matches '.+gravitee.+'}", "priority":1 },
      { "identity" : "idp-id-3", "selectionRule": "", "priority":2 }
  ],
    ...
}
```

Finally, you can check the API reference. To check the APU reference, go to [Management API reference](https://docs.gravitee.io/am/current/am\_devguide\_management\_api\_documentation.html).

### 3.15

**OAuth2/OpenID**

Prior to this update, If a user consented to the `openid` scope and no requested claim was provided, the `full_profile` scope was implicit. Otherwise only the requested claims were provided

With this update, you have to explicitly request the `full_profile` scope claim to get the entire user profile information.

**Identity Provider / RoleMappers**

RoleMappers attached to an identity provider allow the attribution of a role dynamically based on a matching rule.&#x20;

Prior to this update, these dynamic roles were stored in the same location as the manually assigned roles, and we could not determine whether a Role was attributed using RoleMapper or manually using the portal.

With this update, we introduced `dynamic roles`, which are separated from the manually assigned roles.

{% hint style="warning" %}
As we cannot differentiate between the two types of roles before 3.15 and how those roles were assigned, we cannot automate the migration of roles.
{% endhint %}

### 3.12

**Management REST API: Application Scopes**

Pior to this update, the application OAuth settings contained multiple collections about scopes. Here are the collections about scopes:

* scopes: A list with all scopes authorized for the application.
* defaultScopes: A list of scopes added as default if the authorized request doesn’t specify a list of scopes.
* scopeApprovals: A map to specify the amount of time (in seconds) that a scope is considered acceptable by the end user.

```bash
{
  "settings": {
    "oauth": {
      "scopes": [ "scope1", "openid"],
      "defaultScopes": [ "openid"],
      "scopeApprovals": { "opendid" : 3600}
    }
  }
}
```

More settings are related to a scope, the OAuth settings for an application have to be refactored to provide a single list — `scopeSettings` — containing objects with scope settings. **This object has the following attributes**:

* **scope**: the scope name.
* **defautlScope**: boolean to defined this scope as a default one if the authorize request doesn’t specify a list of scopes.
* **scopeApproval**: the amount of time (in seconds) that a scope is considered as accepted per the end user.

### 3.10.6

**Extension Grants**

Before v3.10.6, claims mapping for the extension grant worked only if you had user existence checks off. Starting from v3.10.6, this behavior has changed. If you use the extension grant with claims mapping and user existence enabled, you need to validate the content of generated tokens.

### 3.10.4

**JWK**

The `use` attribute is defined for JWK exposed through the `jwks_uri` endpoint. For more information, go to the [Datatracker](https://datatracker.ietf.org/doc/html/rfc7517#section-4.2)

You can define this value when you configure the domain certificates ( **Settings > domains > mydomain > certiciates**.).

{% hint style="warning" %}
if the `use` attribute isn’t defined, `sig` is used as default. If one of your certificate is currently used to decrypt/encrypt a JWT, update your certificates configurations .
{% endhint %}
