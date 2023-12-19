---
description: Learn how to create your Gravitee APIs using the Gravitee API creation wizard
---

# The API Creation Wizard

## Introduction

The Gravitee API creation wizard provides an easy-to-use UI to create Gravitee Gateway APIs.&#x20;

{% hint style="warning" %}
In Gravitee 4.2, the v4 API creation wizard does not include the option to create a TCP proxy API. To create TCP proxy APIs, you must use the Management API and curl commands.
{% endhint %}

There are two versions of the API creation wizard:

* [v2 API creation wizard:](v2-api-creation-wizard.md) Creates APIs that use the Gravitee v2 API definition. This API definition supports:
  * HTTP 1 and 2 protocols
  * The legacy v2 Policy Studio
* [v4 API creation wizard:](v4-api-creation-wizard.md) Creates APIs that use the Gravitee v4 API definition. This API definition supports:
  * AsyncAPI spec
  * Asynchronous APIs
  * Decoupled Gateway entrypoints and endpoints to enable Gravitee's advanced protocol mediation
  * The new Policy Studio to support policy enforcement at both the request/response and message levels
  * Event brokers as backend data sources

{% hint style="info" %}
**Current v4 API limitations**

It's important to note that v4 APIs do not support:

* Documentation upload during the API creation process
* Gravitee Debug mode
* Analytics or logs in the API Management Console
* Auditing functionality
* Messages and notifications
{% endhint %}
