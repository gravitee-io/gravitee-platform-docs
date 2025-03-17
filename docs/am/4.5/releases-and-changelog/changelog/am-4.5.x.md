---
description: >-
  This page contains the changelog entries for AM 4.5.x and any future minor or
  patch AM 4.5.x releases
---

{% hint style="info" %}
When managing deployments using Helm, please note that the default startup, liveness, and readiness probes now use the httpGet method by default to request the internal API on the `/_node/health` endpoint. As a result, the internal API listens on `0.0.0.0` to allow the kubelet to check the component's status. If you don't provide custom probe definitions and have explicitly defined either the `api.http.services.core.http.host` or the `gateway.http.services.core.http.host`, ensure the value is set to `0.0.0.0`; otherwise, the probes will fail.
{% endhint %}

# AM 4.5.x

## Gravitee Access Management 4.5.12 - March 17, 2025

<details>

<summary>Bug fixes</summary>

**Gateway**

* MFA Challenge policy doesn't work when multiple redirect_uri are declared [#10407](https://github.com/gravitee-io/issues/issues/10407)
* Authentication fails when MFA Challenge policy is used [#10421](https://github.com/gravitee-io/issues/issues/10421)







</details>


## Gravitee Access Management 4.5.11 - March 11, 2025

<details>

<summary>Bug fixes</summary>

**Gateway**

* RememberDevice issue with uBlock [#10388](https://github.com/gravitee-io/issues/issues/10388)
* Fix regression on redirect URL [#10404](https://github.com/gravitee-io/issues/issues/10404)







</details>


## Gravitee Access Management 4.5.10 - February 28, 2025

{% hint style="warning" %}
This version contains a regression introduced by [#10344](https://github.com/gravitee-io/issues/issues/10344).
Please do not install this version if you are using Access Management to authenticate users on mobile applications.
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
* [AM][4.4.11] French language in email not working  [#10349](https://github.com/gravitee-io/issues/issues/10349)
* Lors d'une redemande d'OPT, même OTP [#10374](https://github.com/gravitee-io/issues/issues/10374)

</details>


## Gravitee Access Management 4.5.9 - February 17, 2025

<details>

<summary>Bug fixes</summary>

**Gateway**

* Update AM documentation and OpenAPI spec [#10299](https://github.com/gravitee-io/issues/issues/10299)
* [CIBA] Http Authentication Device Notifier hide some scope [#10309](https://github.com/gravitee-io/issues/issues/10309)
* No logs from InvalidGrantException in the Audits in the UI [#10313](https://github.com/gravitee-io/issues/issues/10313)
* No logs from InvalidGrantException in the Audits in the UI [#10314](https://github.com/gravitee-io/issues/issues/10314)
* Error with MFA (Stuck in a Loop) [#10317](https://github.com/gravitee-io/issues/issues/10317)





**Other**

* Fetch-groups does not work. [#10331](https://github.com/gravitee-io/issues/issues/10331)

</details>


## Gravitee Access Management 4.5.8 - January 31, 2025

<details>

<summary>Bug fixes</summary>

**Gateway**

* GIS reference not removed from session with prompt=login [#10292](https://github.com/gravitee-io/issues/issues/10292)





**Other**

* Double quote prevent HTTP Provider to authenticate [#10277](https://github.com/gravitee-io/issues/issues/10277)

</details>


## Gravitee Access Management 4.5.7 - January 16, 2025

<details>

<summary>Bug fixes</summary>

**Gateway**

* Access token is generated from refresh token of deactivated user [#10258](https://github.com/gravitee-io/issues/issues/10258)



**Console**

* Bug Affichage : Administrative Roles box list illisible.  [#10256](https://github.com/gravitee-io/issues/issues/10256)
* Memory user provider in fresh install has no permissions/roles [#10257](https://github.com/gravitee-io/issues/issues/10257)
* Audit log details differ between roles [#10266](https://github.com/gravitee-io/issues/issues/10266)

**Other**

* Unable to update any reporters on domain and organisation level [#10259](https://github.com/gravitee-io/issues/issues/10259)

</details>


## Gravitee Access Management 4.5.6 - January 3, 2025

<details>

<summary>Bug fixes</summary>





**Console**

* Can't configure new SSO IDP or modify existing one [#10251](https://github.com/gravitee-io/issues/issues/10251)

**Other**

* Unable to get a token using LDAP IDP [#10250](https://github.com/gravitee-io/issues/issues/10250)

</details>


## Gravitee Access Management 4.5.5 - December 20, 2024

<details>

<summary>Bug fixes</summary>







**Other**

* Certificates description on the right of the page refers to identity providers [#10201](https://github.com/gravitee-io/issues/issues/10201)
* Resize the client field for OAut2 scope repository record [#10239](https://github.com/gravitee-io/issues/issues/10239)

</details>


## Gravitee Access Management 4.5.4 - December 12, 2024

<details>

<summary>Bug fixes</summary>

**Gateway**

* SMSFactorProvider - Invalid phone number [#10193](https://github.com/gravitee-io/issues/issues/10193)
* [4.5.1] Scope OpenID on client credential and JWT bearer [#10196](https://github.com/gravitee-io/issues/issues/10196)


**Console**

* Able to create Kafka reporter without Bootstrap server and Topic [#10156](https://github.com/gravitee-io/issues/issues/10156)

**Other**

* SlowQuery (asSorted) + Index non utilisé [#10194](https://github.com/gravitee-io/issues/issues/10194)

</details>


## Gravitee Access Management 4.5.3 - November 22, 2024

<details>

<summary>Bug fixes</summary>

**Gateway**

* Users are returned randomly via SCIM [#10147](https://github.com/gravitee-io/issues/issues/10147)





**Other**

* [Helm Chart] Upgrader job can't be deployed [#10154](https://github.com/gravitee-io/issues/issues/10154)
* Improve WebAuthn Credential search indexes [#10165](https://github.com/gravitee-io/issues/issues/10165)

</details>


## Gravitee Access Management 4.5.2 - November 8, 2024

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


## Gravitee Access Management 4.5.1 - October 25, 2024

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

## Gravitee Access Management 4.5 - October 10, 2024

{% hint style="warning" %}
AM 4.5.0 introduce some deprecations which may have an impact on your systems. Please refer to the "Deprecations" section here after for more details.
{% endhint %}

<details>

<summary>What's new</summary>

### Repositories

A new repository scope named `gateway` has been introduced in AM 4.5.0.

### Token generation

For all domains created from AM 4.5.0 the `sub` claim will not represent the user internalID as it was the case previously.

### AWS Certificate plugin

An AWS certificate plugin is now available as EE feature. Thanks to this plugin you can load certificate provided by AWS Secret Manager.

### Reporters

Reporters have been improved in this new version of Access Management:

* additional reporters can be configured as "global" in order to collect audits events coming from all the domains linked to this organization.
* Events for domain creation and domain deletion are now published in the organization reporters.
* The kafka reporter has been improved to manage Schema Registry

### OpenID

We improved the OAuth2 / OpenID specification more strictly regarding the usage of the response\_mode paramet

### Group mapper

Identity Providers now provide a [Group Mapper](../../guides/identity-providers/user-and-role-mapping.md) section.

### Cache Layer

A cache layer has been introduce to limit the Database access during the user authentication flow.

### Upgrader framework

AM now provide the same upgrader framework as APIM meaning that from 4.5.0, no manual scripts need to be executed before an upgrade.
When AM is deployed on kuberneetes using Helm, the value `api.upgrader` needs to be set to `true` so before starting the Management API or the Gateway the helm chart will deploy a job to execute the upgraders. 

</details>

<details>

<summary>Breaking Changes</summary>

### Redirect Uris

On application creation or update `redirect_uris` is now required for application with type WEB, NATIVE or SPA.

### Token generation

For all domains created from AM 4.5.0 the `sub` claim will not represent the user internalID as it was the case previously. The `sub` value is now an opaque value computed based on the user externalId and the identity provider identifier. Even if this value is opaque, it will remain the same for a given user across multiple token generations as per the requirement of the OIDC specification.

<mark style="color:red;">**NOTE:**</mark> For all domains created in previous version, the sub claim remains the user internalId.

### Repositories

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

### Audits

For kafka and File reporters, the `status` attribute has been deprecated for removal. The recommended way to get access to the status is now the `outcome` structure which contains the `status` and a `message` fields. If you are using one of these reporter, please update your consumer to rely on the outcome structure

</details>
