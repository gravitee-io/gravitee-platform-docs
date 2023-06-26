# Policy Design Studio

## Overview

The Gravitee Policy Design Studio allows you to design "flows," or policy enforcement sequences that protect, transform, or otherwise alter how APIs are consumed. Gravitee comes with many different baked-in policies, some that come with the Community Edition and some that are only available in Gravitee's Enterprise Edition. For more information on specific policies, please refer to the [Policy Reference documentation. ](../../reference/policy-reference/)

## API definitions and execution engines

A Gravitee API definition is a specification for your Gravitee API Management (APIM) Gateway. A Gravitee API definition is very similar to an API specification (OpenAPI, AsynAPI, etc.) except it is a specification _for your Gravitee Gateway_ It’s a JSON representation of everything that the APIM Gateway needs to know for it to proxy, apply policies to, create plans for, etc., your APIs and their traffic.&#x20;

To execute your Gateway APIs and policy flows, the Gateway needs a runtime environment or engine. This is generally referred to as the execution engine.&#x20;

Since APIM 4.0, there is support for both the v2 and v4 Gravitee API definitions and v3 and v4 Gateway execution engines. You can think of these in pairs: v2 API definitions run on the v3 execution engine and v4 API definitions run on the v4 execution engine.

{% hint style="warning" %}
You can also run v2 API definitions on the v4 execution engine by enabling jupiter mode. This is detailed in the v2 API Policy Design Studio documentation.&#x20;
{% endhint %}

The [Gateway Execution Engines Compared guide](gateway-execution-engines-compared.md) does a deep dive into the difference between the two engines. In short, the v4 execution engine enables an improved execution flow for synchronous APIs and supports event-driven policy execution for asynchronous APIs. This adds features such as native support for Pub/Sub (Publish-Subscribe) design and enabling policies at the message level.

APIM still fully supports both API definitions and execution engines. The v2 API Policy Design Studio creates v2 APIs that are compatible with the v3 execution engine by default and the v4 engine in jupiter mode. The v4 API Policy Design Studio creates v4 APIs that are only compatible with v4 execution engine. To better understand the differences, take a look at the following detailed guides:

<table data-view="cards"><thead><tr><th></th><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td></td><td>Gateway Execution Engines Compared</td><td></td><td><a href="gateway-execution-engines-compared.md">gateway-execution-engines-compared.md</a></td></tr><tr><td></td><td>V2 API Policy Design Studio</td><td></td><td><a href="v2-api-policy-design-studio.md">v2-api-policy-design-studio.md</a></td></tr><tr><td></td><td>V4 API Policy Design Studio</td><td></td><td><a href="v4-api-policy-design-studio.md">v4-api-policy-design-studio.md</a></td></tr></tbody></table>

## Flows

### v2

### v4
