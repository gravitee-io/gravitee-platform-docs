---
description: Sample structure for policy documentation
---

# Template Policy

***

***

publisher: GraviteeSource

product: API Management

type: Kafka

category: Identity Provider

license type: Enterprise

\---

<details>

<summary>Enterprise Feature</summary>

This plugin requires an enterprise license or trial which you can learn more about here.

</details>

## Description

High-level details on functionality

## Example use cases

Real-world use cases

{% tabs %}
{% tab title="Management UI" %}
Arcade policy design studio
{% endtab %}

{% tab title="Managment API" %}
Link to API definition explained



Sample flow JSON specific to policy; maybe openapi spec
{% endtab %}

{% tab title="GKO" %}
Link to description of overall API definition in yaml format



subsection of yaml file

```yaml
// Some code
```
{% endtab %}
{% endtabs %}

## Phases

Provide link to a conceptual overview of phases as well as an explanation of the difference between v4 and v3 execution engine

{% tabs %}
{% tab title="V4 API definition" %}
<table data-full-width="false"><thead><tr><th data-type="checkbox">onRequest</th><th data-type="checkbox">onResponse</th><th data-type="checkbox">onMessageRequest</th><th data-type="checkbox">onMessageResponse</th></tr></thead><tbody><tr><td>true</td><td>true</td><td>true</td><td>true</td></tr></tbody></table>
{% endtab %}

{% tab title="V2 API definition" %}
<table><thead><tr><th data-type="checkbox">onRequestContent</th><th data-type="checkbox">onResponseContent</th><th data-type="checkbox"></th></tr></thead><tbody><tr><td>true</td><td>true</td><td>false</td></tr></tbody></table>
{% endtab %}
{% endtabs %}

## Compatibility matrix

<table data-full-width="true"><thead><tr><th>Plugin Version</th><th>Supported APIM versions</th><th>Included in APIM Versions</th></tr></thead><tbody><tr><td>2.2</td><td>>=3.20</td><td>>=3.21</td></tr><tr><td>2.1</td><td>^3.0</td><td><p></p><p>>=3.0 &#x3C;3.21</p></td></tr></tbody></table>

## Installation guide

Only for policies not included in default bundle. Link to section of installation guides that cover plugins

## Configuration

Need to understand convention for UI label vs API definition name

<table><thead><tr><th>Property</th><th data-type="checkbox">Required</th><th>Description</th><th>Type</th><th>Default</th></tr></thead><tbody><tr><td></td><td>true</td><td></td><td></td><td></td></tr><tr><td></td><td>false</td><td></td><td></td><td></td></tr><tr><td></td><td>true</td><td></td><td></td><td></td></tr></tbody></table>

## Errors

| Phase | HTTP status code | Error template key | Description |
| ----- | ---------------- | ------------------ | ----------- |
|       |                  |                    |             |
|       |                  |                    |             |
|       |                  |                    |             |

## Changelog

### 2.2

#### What's New?

* Blazingly fast
* Full chatgpt and neuralink integration for quick API mastery

#### Breaking Changes

* Potentially your mind

### 2.1

#### What's New?

* Blazingly fast
* Full chatgpt and neuralink integration for quick API mastery

#### Breaking Changes

* Potentially your mind

