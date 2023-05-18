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

## Phases

Provide link to a conceptual overview of phases as well as an explanation of the difference between v4 and v3 execution engine

{% tabs %}
{% tab title="V4 engine" %}
<table><thead><tr><th data-type="checkbox">onRequest</th><th data-type="checkbox">onResponse</th><th data-type="checkbox">onMessageRequest</th><th data-type="checkbox">onMessageResponse</th></tr></thead><tbody><tr><td>true</td><td>true</td><td>true</td><td>true</td></tr></tbody></table>
{% endtab %}

{% tab title="V3 engine" %}
<table><thead><tr><th data-type="checkbox">onRequestContent</th><th data-type="checkbox">onResponseContent</th><th data-type="checkbox"></th></tr></thead><tbody><tr><td>true</td><td>true</td><td>false</td></tr></tbody></table>
{% endtab %}
{% endtabs %}

## Example use cases

Real-world use cases

## Compatibility matrix

| Plugin Version | Supported APIM versions | Included in APIM Versions      |
| -------------- | ----------------------- | ------------------------------ |
| 2.2            | >=3.20                  | >=3.21                         |
| 2.1            | ^3.0                    | <p></p><p>>=3.0 &#x3C;3.21</p> |

## Installation guide

{% tabs %}
{% tab title="Docker" %}

{% endtab %}

{% tab title="GKO" %}

{% endtab %}

{% tab title="ZIP" %}

{% endtab %}
{% endtabs %}

## Configuration

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

