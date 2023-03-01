---
title: V4 policy execution engine (V4 BETA)
tags:
  - Event-native API Management
  - New V4 BETA Policy Execution Engine
  - Introduced in version 3.19.0
  - BETA release
---

# V4 policy execution engine (V4 BETA)

Introduced in release 3.19.0 of the Gravitee API Management platform, there is a beta version of a new policy execution engine that enables an improved execution flow for synchronous APIs and supports event-driven policy execution for asynchronous APIs. It is based on a modern and fully reactive architecture designed to address a number of challenges Gravitee users have been facing with the existing policy execution engine, available with the Gravitee’s V2 API definition specification used in versions prior to APIM 3.19.x.

The new policy execution engine builds on the new V4 BETA API definition of Gravitee’s event-native platform. This adds features such as native support for Pub/Sub (Publish-Subscribe) design and enabling policies at message level. The new V4 BETA event-native API definition makes it possible for the Gateway to handle asynchronous API use cases.

The new engine provides the following capabilities:

- The ability to execute policies in the exact order in which they have been placed in Design Studio (see [Create and configure an API flow](../user-guide/published/design-studio/design-studio-create.md#/#create-and-configure-an-api-flow) and [Configure plan flows and policies](../user-guide/publisher/plans/plan-policies.md) This addresses some issues experienced by users related to the order in which policies are executed by the V3 engine where policies interacting with the Head part of the request are always executed first, even when placed in a different order in the Design Studio during the design phase. With the new execution engine, it is possible to apply logic on a head policy based on the payload of the request - for example, to apply dynamic routing based on the request payload.
- Proper isolation between platform-level policies and API-level policies during policy execution. This ensures that platform-level policies are always executed prior to any API-level policies during the request stage, and after any API-level policies during the response stage.
- Removal of the need to define a scope for policies (`onRequest`, `onRequestContent`, `onResponse`, `onResponseContent`).
- The introduction of new API types to better differentiate REST APIs from Async APIs (Websocket, SSE, Webhook), as a foundation to fully support the execution of Async APIs.

This BETA release does not provide GUI support for these capabilities. You can check out the new engine behaviour with the [V4 BETA event-native API Management example use cases](v4-beta-event-native-apim-example-use-cases.md).

This new policy execution engine has been released as a BETA version: it should not be used in production. The production-ready GA release, due in 2023, will come with additional features - [contact us](https://www.gravitee.io/contact-us) if you want to know more about it and what new capabilities and improvements we are bringing to event-native API Management regarding synchronous and asynchronous APIs.

## How to enable and disable the new engine

To enable the new V4 BETA policy execution engine, create a new environment variable called `gravitee_api_jupiterMode_enabled` and set it to `true` on the Management API and the API Gateway.

To disable the new engine and revert to using the V3 engine mode, set this environment variable to `false`.

See [Environment variables](../installation-guide/configuration/rest-apis/installation-guide-rest-apis-configuration.md#environment-variables) on the Management API and [Environment variables](../installation-guide/configuration/gateway/installation-guide-gateway-configuration.md#environment-variables) on the API Gateway for more
detail about setting environment variables.
