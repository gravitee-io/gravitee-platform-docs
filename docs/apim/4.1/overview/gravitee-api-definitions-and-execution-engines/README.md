---
description: An overview about Gravitee API Definitions and Execution Engines.
---

# Gravitee API Definitions and Execution Engines

## Overview

A Gravitee API definition is very similar to an API specification (e.g., OpenAPI, AsyncAPI) except it is a specification for your Gravitee API Management (APIM) Gateway\_.\_ It’s a JSON representation of everything that the APIM Gateway needs to know for it to proxy, apply policies to, create plans for, etc., your APIs and their traffic.

To execute your Gateway APIs and policy flows, the Gateway needs a runtime environment, or engine. This is generally referred to as the execution engine. As of APIM 4.0, there is support for both the v2 and v4 Gravitee API definitions, where v2 API definitions run on the legacy execution engine and v4 API definitions run on the reactive execution engine.

{% hint style="warning" %}
You can run v2 Gateway APIs in [emulation mode](reactive-execution-engine.md#v2-gateway-api-emulation-mode), which emulates some of the execution flow improvements of the reactive execution engine.
{% endhint %}

The [v2 API Creation Wizard ](../../guides/create-apis/how-to/v2-api-creation-wizard.md)creates v2 Gateway APIs compatible with the legacy execution engine that can be augmented with flows designed in the [v2 Policy Studio](../../guides/policy-design/v2-api-policy-design-studio.md). The [v4 API Creation Wizard](../../guides/create-apis/how-to/v4-api-creation-wizard.md) creates v4 APIs compatible with the reactive execution engine that can be augmented with flows designed in the [v4 Policy Studio](../../guides/policy-design/v4-api-policy-design-studio.md).

This guide is a deep dive into the differences between the new reactive execution engine and the existing legacy execution engine. Additionally, guidance is provided on managing changes in system behavior when switching to the reactive policy execution engine or enabling compatibility mode with a v2 API. The information is grouped by functional area.
