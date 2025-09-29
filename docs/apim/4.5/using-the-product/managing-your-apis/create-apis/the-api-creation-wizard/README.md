---
description: Learn how to create your Gravitee APIs using the Gravitee API creation wizard
---

# Creating APIs with API Creation Wizard

{% hint style="warning" %}
When you create an API with a JSON payload that has duplicate keys, APIM keeps the last key.&#x20;

To avoid any errors because of duplicate keys, apply the JSON threat protection policy to the API. For more information about the JSON threat protection policy, see [json-threat-protection.md](../../policy-studio/policies-for-your-apis/i-k/json-threat-protection.md "mention").
{% endhint %}

The Gravitee API creation wizard provides an easy-to-use UI to create Gravitee Gateway APIs. There are two versions of the API creation wizard:

* v2: Creates APIs that use the Gravitee v2 API definition
* v4: Creates APIs that use the Gravitee v4 API definition

<table><thead><tr><th width="212">Version</th><th>Supports</th></tr></thead><tbody><tr><td><a href="v2-api-creation-wizard.md">v2 API creation wizard</a></td><td><ul><li>HTTP 1 and 2 protocols</li><li>The legacy v2 Policy Studio</li></ul></td></tr><tr><td><a href="v4-api-creation-wizard.md">v4 API creation wizard</a></td><td><ul><li>AsyncAPI spec</li><li>Asynchronous APIs</li><li>Decoupled Gateway entrypoints and endpoints to enable Gravitee's advanced protocol mediation</li><li>Policy enforcement at both the request/response and message levels</li><li>Event brokers as backend data sources</li></ul></td></tr></tbody></table>

{% hint style="info" %}
**Limitations**

v4 APIs do not support Gravitee Debug mode
{% endhint %}
