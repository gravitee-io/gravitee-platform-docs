---
description: >-
  This page contains the changelog entries for AM 4.6.0 and any future minor or
  patch AM 4.6.x releases
---

# AM 4.7.x

## Gravitee Access Management 4.7.3 - May 6, 2025

<details>

<summary>Bug fixes</summary>

**Gateway**

* Filter audit type  [#10518](https://github.com/gravitee-io/issues/issues/10518)


**Other**

* Fail to enable the AM gateway service on SUSE [#10402](https://github.com/gravitee-io/issues/issues/10402)
* Use Gravitee GPG Key to sign RPM package [#10504](https://github.com/gravitee-io/issues/issues/10504)
* Fix authentication issue with Azure AD  [#10522](https://github.com/gravitee-io/issues/issues/10522)
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
* Error handling error=session_expired in Login Form [#10460](https://github.com/gravitee-io/issues/issues/10460)
* EL for language entries not resolving correctly [#10465](https://github.com/gravitee-io/issues/issues/10465)

**Management API**

* Prevent Ogranization IDP selection to send null [#10444](https://github.com/gravitee-io/issues/issues/10444)
* Fix audit log on user login failed [#10463](https://github.com/gravitee-io/issues/issues/10463)



**Other**

* Error in /ciba/authenticate/callback [#10412](https://github.com/gravitee-io/issues/issues/10412)
* [AM][4.5.11] Error when character "ë" in a token [#10418](https://github.com/gravitee-io/issues/issues/10418)
* Cant update SAML SP certifacte in UI application SAML tab  [#10442](https://github.com/gravitee-io/issues/issues/10442)
* Management API does not check if user exists on domain when added to a group on creation of the group [#10468](https://github.com/gravitee-io/issues/issues/10468)

</details>


## AM 4.7.x

### Gravitee Access Management 4.7 - March 31, 2025 <a href="#gravitee-access-management-4.5-october-10-2024" id="gravitee-access-management-4.5-october-10-2024"></a>

<details>

<summary>What's new</summary>

## User management improvement

On the console interface, an administrator can now see if the password set during user creation or password reset complies with the password policy rules.&#x20;

## Generic OpenID provider improvement

The Generic OpenID Identity Provider is able to support the `response_type` parameter. An administration can select `fragment` or `query` to match the supported `response_type` expected by the provider.

## CIBA Http Notifier

The HTTP Device Notifier plugin for [CIBA](../../guides/auth-protocols/ciba.md) has been updated to accept additional headers supporting Expression Language.

## Multi Data Plane architecture

Access Management evolves to improve the scalability and the resiliency of the solution.

This version introduces the ability to assign a domain to a Data Plane. The Management API can now access multiple Data Planes, with each Gateway linked to a single Data Plane. With this new functionality, it becomes possible to assign one database for the Control Plane data managed by the Management API service, and another for the Data Plane data managed by the Gateway.

</details>

<details>

<summary>Breaking Changes</summary>

## Domain Creation

To create a Security Domain via the Management REST API, the `dataPlaneId` attribute is mandatory. Even if multi-data plane capabilities are not being utilized, this attribute must still be specified with the value set to "default".

## Identity Provider

To update an IdentityProvider via the Management REST API, the `type` attribute is mandatory.&#x20;

## Extension Grant

To update an ExtensionGrant plugin via the Management REST API, the `type` attribute is mandatory.&#x20;

## AccountLinking Policy

The AccountLinking policy has been updated to version 2.0.0 to be compatible with AM 4.7.0.

{% hint style="danger" %}
versions 1.x of AccountLinking policy are not compatible with AM 4.7.0
{% endhint %}

## AWS CloudHSM Plugin

The AWS CloudHSM plugin has been updated to version 2.0.0 to be compatible with AM 4.7.0.

{% hint style="danger" %}
versions 1.x of AWS CloudHSM plugin are not compatible with AM 4.7.0
{% endhint %}



</details>

