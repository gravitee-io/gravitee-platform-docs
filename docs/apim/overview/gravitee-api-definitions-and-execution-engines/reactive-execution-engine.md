---
description: This page provides a high-level overview of the v4 engine
---

# Reactive execution engine

## Overview

The reactive execution engine is based on a modern and fully reactive architecture. It enables an improved execution flow for synchronous APIs and supports event-driven policy execution for asynchronous APIs. Added features include native support for pub/sub (publish-subscribe) design and the capability to enforce policies at the message level.&#x20;

## Key improvements

The new reactive engine is designed to address a number of challenges associated with the legacy execution engine used for v2 APIs.

<details>

<summary>Policy execution order</summary>

Policies can be executed in the exact order in which they have been placed in the Policy Studio. This addresses a limitation of the legacy engine where policies interacting with the Head part of the request are always executed first, regardless of how they are ordered during the design phase.&#x20;

With the new reactive execution engine, it is possible to apply logic on a Head policy based on the payload of the request, e.g., to apply dynamic routing based on the request payload.

v2 Gateway APIs have this capability when [emulation mode](reactive-execution-engine.md#v2-gateway-api-emulation-mode) is enabled.

</details>

<details>

<summary>Policy isolation</summary>

Proper isolation between platform-level policies and API-level policies is enforced during policy execution. This ensures that platform-level policies are executed before any API-level policies during the request stage and after any API-level policies during the response stage.

v2 Gateway APIs have this capability when [emulation mode](reactive-execution-engine.md#v2-gateway-api-emulation-mode) is enabled.

</details>

<details>

<summary>Simplified scopes</summary>

Scopes have been simplified for API publishers by merging `onRequest` and `onRequestContent` into `onRequest` and `onResponse` and `onResponseContent` into `onResponse`. This means API publishers no longer have to define a scope in the policy configuration for v4 APIs.

</details>

<details>

<summary>Async support</summary>

Message-based, asynchronous APIs such as Kafka, MQTT, WebSocket, SSE, and Webhook are supported.

</details>

## Policy support

With the legacy execution engine, all existing supported policies will continue to work as before without any changes.

All policies will also support the new reactive execution engine. However, only some policies are capable of being applied at the message level. This is detailed for each policy in the [Policy Reference](../../reference/policy-reference/) Guide.

## v2 Gateway API emulation mode

{% hint style="info" %}
By default, emulation mode is not enabled for v2 APIs as it may cause unexpected changes in behavior. Please review this guide in its entirety before enabling emulation mode.
{% endhint %}

All v2 Gateway APIs can be used in emulation mode as shown in the image below:

<figure><img src="../../.gitbook/assets/Screenshot 2023-07-19 at 4.45.21 PM.png" alt=""><figcaption><p>v2 API emulation mode</p></figcaption></figure>

Enabling this option allows v2 Gateway APIs to easily access all the improvements of the reactive execution engine detailed in the following sections.

{% hint style="warning" %}
v4 Gateway APIs have some features that are dependent on the API definition itself instead of the execution engine. Therefore, v2 APIs in emulation mode will **not** have the following benefits:

* Event native API management: support for event brokers, multi-entry points, QOS, etc.
* Analytics improvements
  * Message-level analytics with sampling
  * Ability to disable analytics in the API definition
* Modified flow execution phases: request, response, subscribe, publish
* Flow required match option
* Generic flow selectors
{% endhint %}
