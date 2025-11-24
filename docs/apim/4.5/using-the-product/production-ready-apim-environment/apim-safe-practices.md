---
description: An overview about api management safe practices overview.
---

# API Management Safe Practices overview

## Overview

This page discusses API Management safe practices as they relate to:

* [Roles, permissions, and groups](apim-safe-practices.md#roles-permissions-and-groups)
* [API review & quality](apim-safe-practices.md#api-review-and-quality)
* [API design](apim-safe-practices.md#api-design)

## Roles, permissions, and groups

Gravitee offers the ability to fine-tune a permissions list and the concept of roles, which can be used to **restrict user access to only what is required**.

Some good practices to establish:

* Use groups and permissions to restrict a given user's access to only a necessary subset of APIs.
* Ensure each user only has the necessary permissions (e.g., assign the API\_PUBLISHER role instead of ADMIN).
* Assign permissions to a group instead of each user individually.
* Automatically associate a group with each new API or application to facilitate permission management.

You can find detail on roles, groups, and permissions in the [Gravitee documentation](https://documentation.gravitee.io/apim/guides/administration/user-management-and-permissions).

## API review & quality

You can **enable API review and quality** to avoid public exposure to the Developer Portal that is unexpected and lacks strong security requirements, or if you want a member of a Quality team to review API designs prior to deploying the API and making it accessible to API consumers. This can seamlessly establish a robust API strategy.

You can find more information about API review and quality in the [Gravitee documentation](https://documentation.gravitee.io/apim/guides/api-measurement-tracking-and-analytics/using-the-api-quality-feature).

## API design

There is no "rule of thumb" when it comes to designing and exposing your APIs, as this always depends on the business requirements. However, consider the following to avoid mistakes and open unexpected security breaches:

* Enable and configure CORS at the API level. This ensures the best level of security when APIs are consumed by browser-based applications. See [details here](https://documentation.gravitee.io/apim/guides/api-configuration/v2-api-configuration/configure-cors#configure-cors).
* Avoid exposing an API without security (i.e., using a keyless plan) when possible. Always prefer stronger security solutions such as JWT or OAuth2.
* Disable auto-validation of API subscriptions. Instead, manually validate each subscription to ensure that you are familiar with your API consumers.
* Require the API consumer to enter a comment when subscribing to an API. This is a simple way to understand the motivation for a subscription and helps detect malicious attempts to access an API.
* Regularly review subscriptions and revoke those that are no longer used.

More information on how to manage API subscriptions is detailed in the [Gravitee documentation](https://documentation.gravitee.io/apim/guides/api-exposure-plans-applications-and-subscriptions/subscriptions).
