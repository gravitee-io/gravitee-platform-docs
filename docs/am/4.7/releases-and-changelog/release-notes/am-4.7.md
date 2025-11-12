---
description: >-
  This article covers the new features released in Gravitee Access Management
  4.7.
---

# AM 4.7

## Java Upgrade

Gravitee Access Management requires Java 21. If you are deploying Access Management with RPM or using the distribution bundle, please ensure to upgrade your java version.

## User management improvement

On the console interface, an administrator can now see if the password set during user creation or password reset complies with the password policy rules.&#x20;

## Generic OpenID provider improvement

The Generic OpenID Identity Provider is able to support the `response_type` parameter. An administration can select `fragment` or `query` to match the supported `response_type` expected by the provider.

## CIBA Http Notifier

The HTTP Device Notifier plugin for [CIBA](docs/am/4.7/guides/auth-protocols/ciba.md) has been updated to accept additional headers supporting Expression Language.

## Multi Data Plane architecture

Access Management evolves to improve the scalability and the resiliency of the solution.

Prior to version 4.7, the data managed by Gravitee Access Management was not effectively distributed between the [Data Plane and the Control Plane](docs/am/4.7/overview/am-architecture/control-plane-and-data-plane.md). Specifically, user profiles associated with a domain, along with other entities, were managed in the Control Plane. As a result, if the Control Plane became inaccessible, users were unable to log in. To address this issue, version 4.7 introduces the ability to assign a domain to a Data Plane. The Management API can now access [multiple Data Planes](docs/am/4.7/getting-started/install-and-upgrade-guides/configure-multiple-data-planes.md), with each Gateway linked to a single Data Plane. With this new functionality, it becomes possible to assign one database for the Control Plane data managed by the Management API service, and another for the Data Plane data managed by the Gateway.

{% hint style="info" %}
Existing deployments with a single database remains possible.
{% endhint %}

{% hint style="warning" %}
If you are currently using dedicated databases for each repository scope, please make sure to read the [installation and upgrade guide](docs/am/4.7/getting-started/install-and-upgrade-guides/4.7-upgrade-guide.md) carefully, as data migration will be required.
{% endhint %}



