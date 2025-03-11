---
description: >-
  This page contains the changelog entries for AM 4.6.0 and any future minor or
  patch AM 4.6.x releases
---

# AM 4.6.x

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

### Twilio Resource

The new version of the Twilio resource for SMS or Call factors allows you to specify the templateSid as configuration option.

### LDAP Identity Provider

The new version of the LDAP identity provider grant you access to the Operational Attributes linked to the user profile coming from the LDAP server. (**NOTE:** If this option is enable, Opertational Attributes will be accessible using the User Mapper.)

### User Migration

For users migrations from an alternative OIDC provider to Access Management, you now have the capability to define the `lastPasswordReset` attribute so a password policy with password expiry will request a password reset according to the value provided during the migration. This attribute is accepted only during user creation through the SCIM protocol or the Management API.

### Audit Logs

Additional audit logs have been added on SCIM endpoint to track failing user creations or updates due to an invalid password. In additiopn, a distinction is made between user login with password against using passwordless in a way that the dashboard now expose these information.

### Bulk action for user provisioning

User provisioning is now possible using Bulk actions to create, update or delete users. A dedicated endpoint has been added on the Management API and the SCIM protocol exposed by the Gateway implement the Bulk endpoint (only for the users, groups are currently not managed)

### New Certificate plugin

A key pair registered in AWS Cloud HSM can be used to sign an tokens generated by Access Management by using the new "AWS Cloud HSM" certificate plugin.

</details>

<details>

<summary>Breaking Changes</summary>

#### SCIM pagination

In previous versions, the `startIndex` parameter used by SCIM paginiation was representing the page number. According to the [specification](https://datatracker.ietf.org/doc/html/rfc7644#section-3.4.2) the `startIndex` represent `the index of the first search result desired by the search client` . In order to be align with the specification, the SCIM endpoints of AM Gateway are managing the startIndex as specified by the RFC.

</details>

\\
