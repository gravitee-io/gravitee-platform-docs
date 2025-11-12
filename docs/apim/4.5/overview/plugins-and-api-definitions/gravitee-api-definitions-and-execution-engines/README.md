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

# API Definitions and Execution Engines

## Overview

A Gravitee API definition is a JSON representation of everything that the APIM gateway needs to know for it to proxy, apply policies to, and create plans for your APIs and their traffic. To execute APIs and policy flows, the gateway relies on a runtime environment referred to as the **execution** **engine**.

As Gravitee's gateway has evolved, a new execution engine version has been introduced focused on providing the runtime necessary to combine sync and async APIs in one platform. The new engine leverages a reactive execution methodology, which introduces some incompatibilities with the execution mode in older versions of Gravitee's gateway

Some important initial differences are as follows:

{% hint style="info" %}
* The [v2 API Creation Wizard ](docs/apim/4.5/using-the-product/managing-your-apis/create-apis/the-api-creation-wizard/v2-api-creation-wizard.md)creates APIs compatible with the legacy execution engine. These can be augmented with flows designed in the [v2 Policy Studio](docs/apim/4.5/using-the-product/managing-your-apis/policy-studio/v2-api-policy-studio.md).
* The [v4 API Creation Wizard](docs/apim/4.5/using-the-product/managing-your-apis/create-apis/the-api-creation-wizard/v4-api-creation-wizard.md) creates v4 APIs compatible with the reactive execution engine. These can be augmented with flows designed in the [v4 Policy Studio](docs/apim/4.5/using-the-product/managing-your-apis/policy-studio/v4-api-policy-studio.md).
* v2 Gateway APIs can run in [emulation mode](reactive-execution-engine.md#v2-gateway-api-emulation-mode) to take advantage of certain execution flow improvements of the reactive engine.&#x20;
{% endhint %}

The following sections summarize differences between the reactive and legacy execution engines and provides guidance for managing changes in system behavior when switching to the reactive engine or enabling compatibility mode with a v2 API.

<table data-view="cards"><thead><tr><th></th><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td></td><td><a href="reactive-execution-engine.md">Reactive execution engine</a></td><td></td><td><a href="reactive-execution-engine.md">reactive-execution-engine.md</a></td></tr><tr><td><a href="engine-comparisons.md">Execution engine comparisons</a></td><td></td><td></td><td></td></tr></tbody></table>
