---
description: Learn how to create your Gravitee APIs using the Gravitee API creation wizard
---

# The API Creation Wizard

## Introduction

The Gravitee API creation wizard provides an easy-to-use UI to create Gravitee Gateway APIs. There are two versions of the API creation wizard:

* v2 API creation wizard: creates APIs that use the Gravitee v2 API definition. This API definition supports:
  * HTTP 1 and 2 protocols
  * The legacy v2 Policy Studio
* v4 API creation wizard: creates APIs that use the Gravitee v4 API definition. This API definition supports:
  * AsyncAPI spec
  * Asynchronous APIs
  * Decoupled Gateway entrypoints and endpoints: this enables Gravitee's advanced protocol mediation
  * The new Policy Studio: this supports policy enforcement at both the request/response level and the message level
  * Event brokers as backend data sources

{% hint style="info" %}
**Current v4 API limitations**

It's important to note that v4 APIs do not support:

* Documentation upload during the API creation process
* Gravitee Debug mode
* Analytics or logs in the API Management UI
* Auditing functionality
* Messages and notifications&#x20;
{% endhint %}

Please see the documentation for:

* [v4 API Creation wizard](how-to/v4-api-creation-wizard.md)
* [v2 API creation wizard](how-to/v2-api-creation-wizard.md)
