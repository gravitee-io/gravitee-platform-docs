---
description: >-
  This page contains the changelog entries for AM 4.6.0 and any future minor or
  patch AM 4.6.x releases
---

# AM 4.7.x

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

