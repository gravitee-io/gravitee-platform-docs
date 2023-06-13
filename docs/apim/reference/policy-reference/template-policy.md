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

You can use the `json-xml` policy to transform JSON content to XML content.

{% hint style="warning" %}
For transforming XML content to JSON, please see the `xml-json` policy.
{% endhint %}

## Configuration options

<table data-full-width="true"><thead><tr><th>Property</th><th data-type="checkbox">Required</th><th>Description</th><th data-type="select">Type</th><th>Options</th><th>Default</th></tr></thead><tbody><tr><td>name</td><td>false</td><td>Provide a descriptive name for your policy</td><td></td><td>N/a</td><td>N/a</td></tr><tr><td>description</td><td>false</td><td>Provide a description for your policy</td><td></td><td>N/a</td><td>N/a</td></tr><tr><td>rootElement</td><td>true</td><td>XML root element name that encloses content.</td><td></td><td>N/a</td><td>root</td></tr><tr><td>scope</td><td>true</td><td>The execution scope</td><td></td><td>REQUEST, RESPONSE</td><td>REQUEST</td></tr></tbody></table>

## Example use cases

Policies can be added to flows assigned to an API or to a plan. Gravitee supports configuring policies through the policy design studio in the management UI, interacting directly with the management API, or using the Gravitee Kubernetes Operator (GKO) in a Kubernetes deployment.

{% tabs %}
{% tab title="Management UI" %}
<mark style="color:yellow;">We should wait to make these once the v4 policy design studio is finalized</mark>


{% endtab %}

{% tab title="Managment API" %}
When using the management API, policies are added as flows either directly to an API or to a  plan. To learn more about the structure of the management API, check out the reference documentation here.

{% code title="Sample Configuration" %}
```json
{
  "name": "Custom name",
  "description": "Custom description",
  "policy": "json-xml",
  "configuration": {
    "scope": "RESPONSE",
    "rootElement": "root"
  }
}
```
{% endcode %}
{% endtab %}

{% tab title="GKO" %}
The Gravitee Kubernetes Operator (GKO) allows you to manage your APIs as custom resources. The `APIDefinition` custom resource represents the configuration for a single proxied API and its versions. It is similar to a YAML representation of an API Definition in JSON format.

The example below shows a simple `ApiDefinition` custom resource definition using the `json-xml`  policy:

{% code title="Sample Configuration" %}
```yaml
apiVersion: gravitee.io/v1alpha1
kind: ApiDefinition
metadata:
  name: json-xml example
spec:
  name: "GKO Basic"
  version: "1.1"
  description: "Basic api managed by Gravitee Kubernetes Operator"
  proxy:
    virtual_hosts:
      - path: "/k8s-basic"
    groups:
      - endpoints:
          - name: "Default"
            target: "https://api.gravitee.io/echo"
```
{% endcode %}
{% endtab %}
{% endtabs %}

## Phases

Provide link to a conceptual overview of phases as well as an explanation of the difference between v4 and v3 execution engine

{% tabs %}
{% tab title="V4 API definition" %}
Link explaining difference

<table data-full-width="false"><thead><tr><th data-type="checkbox">onRequest</th><th data-type="checkbox">onResponse</th><th data-type="checkbox">onMessageRequest</th><th data-type="checkbox">onMessageResponse</th></tr></thead><tbody><tr><td>true</td><td>true</td><td>true</td><td>true</td></tr></tbody></table>
{% endtab %}

{% tab title="V2 API definition" %}
Link explaining difference

<table><thead><tr><th data-type="checkbox">onRequest</th><th data-type="checkbox">on </th><th width="197" data-type="checkbox">onRequestContent</th><th data-type="checkbox">onResponseContent</th></tr></thead><tbody><tr><td>false</td><td>false</td><td>true</td><td>true</td></tr></tbody></table>
{% endtab %}
{% endtabs %}

## Compatibility matrix

<table data-full-width="true"><thead><tr><th>Plugin Version</th><th>Supported APIM versions</th><th>Included in APIM Versions</th></tr></thead><tbody><tr><td>2.2</td><td>>=3.20</td><td>>=3.21</td></tr><tr><td>2.1</td><td>^3.0</td><td><p></p><p>>=3.0 &#x3C;3.21</p></td></tr></tbody></table>

## Installation

Only for policies not included in default bundle. Link to section of installation guides that cover plugins

## Errors

### Overview

<table data-full-width="true"><thead><tr><th>Phase</th><th>HTTP status code</th><th>Error template key</th><th>Description</th></tr></thead><tbody><tr><td>onRequest</td><td><code>400</code></td><td>JSON_INVALID_PAYLOAD</td><td>Request payload cannot be transformed properly to XML</td></tr><tr><td>onResponse</td><td><code>500</code></td><td>JSON_INVALID_PAYLOAD</td><td>Response payload cannot be transformed properly to XML</td></tr><tr><td>onMessageRequest</td><td><code>400</code></td><td>JSON_INVALID_MESSAGE_PAYLOAD</td><td>Incoming message cannot be transformed properly to XML</td></tr><tr><td>onMessageResponse</td><td><code>500</code></td><td>JSON_INVALID_MESSAGE_PAYLOAD</td><td>Outgoing message cannot be transformed properly to XML</td></tr></tbody></table>

### Nested objects

To limit the processing time in the case of a nested object, the default max depth of a nested object has been set to 1000. This default value can be overridden using the environment variable `gravitee_policy_jsonxml_maxdepth`.

## Changelog

### 2.2

#### What's New?

* Blazingly fast
* Full chatgpt and neuralink integration for quick API mastery

#### Fixes

* Fix crashes related to nested objects

#### Breaking Changes

* Only supports APIM versions >4.0

### 2.1

#### What's New?

* Blazingly fast
* Full chatgpt and neuralink integration for quick API mastery

#### Fixes

* Fix crashes related to nested objects

#### Breaking Changes

* Only supports APIM versions >4.0

