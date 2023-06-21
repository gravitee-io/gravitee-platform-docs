# Policy Design Studio

## Overview

The Gravitee Policy Design Studio allows you to design "flows," or policy enforcement sequences that protect, transform, or otherwise alter how APIs are consumed. Gravitee comes with many different baked-in policies, some that come with the Community Edition and some that are only available in Gravitee's Enterprise Edition. For more information on specific policies, please refer to the [Policy Reference documentation. ](../../reference/policy-reference/)

## API definitions and execution engines

A Gravitee API definition is a specification for your Gravitee API Management (APIM) Gateway. A Gravitee API definition is very similar to an API specification (OpenAPI, AsynAPI, etc.) except it is a specification _for your Gravitee Gateway_ It’s a JSON representation of everything that the APIM Gateway needs to know for it to proxy, apply policies to, create plans for, etc., your APIs and their traffic.&#x20;

To execute your gateway APIs and policy flows, the Gateway needs a runtime environment or engine. This is generally referred to as the execution engine.&#x20;

APIM 4.0 and later supports v2 and v4 Gravitee API definitions and v3 and v4 Gateway execution engines. You can think of these in pairs: v2 API definitions run on the v3 execution engine and v4 API definitions run on the v4 execution engine.

{% hint style="info" %}
The v4 execution engine can also run v2 API definitions in compatibility mode. This is detailed in the v4 API Policy Design Studio documentation.&#x20;
{% endhint %}

The Policy Execution Engines Compared guide does a deep dive into the difference in the two engines. In short, the v4 execution engine enables an improved execution flow for synchronous APIs and supports event-driven policy execution for asynchronous APIs. This adds features such as native support for Pub/Sub (Publish-Subscribe) design and enabling policies at the message level.

This is why APIM has both the v2 API Policy Design Studio and the v4 API Policy Design Studio.&#x20;

###

## Flows

### v2

### v4
