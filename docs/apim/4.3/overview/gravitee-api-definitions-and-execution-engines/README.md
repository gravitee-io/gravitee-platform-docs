---
layout:
  title:
    visible: true
  description:
    visible: false
  tableOfContents:
    visible: true
  outline:
    visible: true
  pagination:
    visible: true
---

# Gravitee API Definitions and Execution Engines

## Overview

A Gravitee API definition is a JSON representation of everything that the APIM Gateway needs to know for it to proxy, apply policies to, create plans for, etc., your APIs and their traffic. To execute Gateway APIs and policy flows, the Gateway relies on a runtime environment referred to as the execution engine.

{% hint style="info" %}
* The [v2 API Creation Wizard ](docs/apim/4.3/guides/create-apis/the-api-creation-wizard/v2-api-creation-wizard.md)creates APIs compatible with the legacy execution engine. These can be augmented with flows designed in the [v2 Policy Studio](docs/apim/4.3/guides/policy-studio/v2-api-policy-studio.md).
* The [v4 API Creation Wizard](docs/apim/4.3/guides/create-apis/the-api-creation-wizard/v4-api-creation-wizard.md) creates v4 APIs compatible with the reactive execution engine. These can be augmented with flows designed in the [v4 Policy Studio](docs/apim/4.3/guides/policy-studio/v4-api-policy-studio.md).
{% endhint %}

{% hint style="warning" %}
v2 Gateway APIs can run in [emulation mode](reactive-execution-engine.md#v2-gateway-api-emulation-mode) to take advantage of certain execution flow improvements of the reactive engine.&#x20;
{% endhint %}

The following sections summarize differences between the reactive and legacy execution engines and provides guidance for managing changes in system behavior when switching to the reactive engine or enabling compatibility mode with a v2 API.

<table data-view="cards"><thead><tr><th></th><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td></td><td>Reactive execution engine</td><td></td><td><a href="reactive-execution-engine.md">reactive-execution-engine.md</a></td></tr><tr><td></td><td>Engine comparisons</td><td></td><td><a href="engine-comparisons.md">engine-comparisons.md</a></td></tr></tbody></table>
