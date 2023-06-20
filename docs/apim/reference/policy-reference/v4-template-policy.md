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

## Overview

The `json-xml` policy transforms JSON payloads to XML before either sending the payload to the backend system or returning it to the client.

{% hint style="warning" %}
For transforming XML content to JSON, please see the `xml-json` policy.
{% endhint %}

### Proxy API example

For Proxy APIs, the JSON-to-XML policy is most commonly used for transforming JSON data before returning it to the client in the `response` phase.

For example, the Gravitee echo API returns a JSON response when a `GET` request is sent to [https://api.gravitee.io/echo](https://api.gravitee.io/echo). The response is formatted like so:

{% code title="Default response" %}
```json
{
    "bodySize": 0,
    "headers": {
        "Accept": "*/*",
        "Host": "api.gravitee.io",
        "User-Agent": "{{user-agent-info}}",
        "X-Gravitee-Request-Id": "{{generated-request-id}}",
        "X-Gravitee-Transaction-Id": "{{generated-trx-id}}",
        "accept-encoding": "deflate, gzip"
    },
    "query_params": {}
}
```
{% endcode %}

Adding a JSON-to-XML policy on the `response` phase for a Proxy API will transform the response output to:

{% code title="Transformed response" %}
```xml
<root>
  <headers>
    <Accept>*/*</Accept>
    <Host>api.gravitee.io</Host>
    <User-Agent>{{user-agent-info}}</User-Agent>
    <X-Gravitee-Request-Id>{{generated-request-id}}</X-Gravitee-Request-Id>
    <X-Gravitee-Transaction-Id>{{generated-trx-id}}</X-Gravitee-Transaction-Id>
    <accept-encoding>deflate, gzip</accept-encoding>
  </headers>
  <query_params/>
  <bodySize>0</bodySize>
</root>
```
{% endcode %}

### Message API example

For message APIs, the JSON-to-XML policy is used to transform the message `content` in either the `publish` or `subscribe` phase.

For example, you can create a message API with an HTTP GET entrypoint and a mock endpoint. Suppose the endpoint is configured to return the message content as follows:

{% code title="Default message" %}
```json
{ \"id\": \"1\", \"name\": \"bob\", \"v\": 2 }
```
{% endcode %}

Then adding a JSON-to-XML policy on the subscribe phase will return the payload to the client via the HTTP GET entrypoint like so (the number of messages returned will vary by the number of messages specified in the Mock endpoint):

{% code title="Transformed messages" %}
```xml
{
    "items": [
        {
            "content": "<root><id>1</id><name>bob</name><v>2</v></root>",
            "id": "0"
        },
        {
            "content": "<root><id>1</id><name>bob</name><v>2</v></root>",
            "id": "1"
        },
        {
            "content": "<root><id>1</id><name>bob</name><v>2</v></root>",
            "id": "2"
        },
        {
            "content": "<root><id>1</id><name>bob</name><v>2</v></root>",
            "id": "3"
        }
    ],
    "pagination": {
        "nextCursor": "3"
    }
}
```
{% endcode %}

The output is the typical return structure for the HTTP GET entrypoint with each message `content` field being transformed from JSON to XML.

{% hint style="info" %}
For the HTTP GET entrypoint specifically, the entire payload can be returned as XML by adding the `"Accept": "application/json"` header to the GET request. In this case, the message content is transformed into [CDATA](https://www.w3.org/TR/REC-xml/#sec-cdata-sect) and is therefore not treated as marked-up content for the purpose of the entrypoint using the `Accept` header. &#x20;
{% endhint %}

## Configuration

Policies can be added to flows that are assigned to an API or to a plan. Gravitee supports configuring policies through the policy design studio in the management UI, interacting directly with the management API, or using the Gravitee Kubernetes Operator (GKO) in a Kubernetes deployment.

{% tabs %}
{% tab title="Management UI" %}
<mark style="color:yellow;">We should wait to make these once the v4 policy design studio is finalized</mark>

{% @arcade/embed flowId="w2EIKB74a9xXG3sXcQVI" url="https://app.arcade.software/share/w2EIKB74a9xXG3sXcQVI" %}
{% endtab %}

{% tab title="Managment API" %}
When using the management API, policies are added as flows either directly to an API or to a  plan. To learn more about the structure of the management API, check out the reference documentation here.

{% code title="Sample Configuration" %}
```json
{
  "name": "Custom name",
  "description": "Converts data from JSON to XML",
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

### Reference

<table data-full-width="false"><thead><tr><th>Property</th><th data-type="checkbox">Required</th><th>Description</th><th data-type="select">Type</th><th>Options</th><th>Default</th></tr></thead><tbody><tr><td>name</td><td>false</td><td>Provide a descriptive name for your policy</td><td></td><td>N/a</td><td>N/a</td></tr><tr><td>description</td><td>false</td><td>Provide a description for your policy</td><td></td><td>N/a</td><td>N/a</td></tr><tr><td>rootElement</td><td>true</td><td>XML root element name that encloses content.</td><td></td><td>N/a</td><td>root</td></tr><tr><td>scope</td><td>true</td><td>The execution scope</td><td></td><td>REQUEST, RESPONSE</td><td>REQUEST</td></tr></tbody></table>

### Phases

Provide link to a conceptual overview of phases as well as an explanation of the difference between v4 and v2 API definitions

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

In the [changelog for each version of APIM](../../releases-and-changelog/changelog/), we provide a list of policies included in the default distribution. The chart below summarizes this information in relation to the `json-xml` policy.

<table data-full-width="false"><thead><tr><th>Plugin Version</th><th>Supported APIM versions</th><th>Included in APIM default distribution</th></tr></thead><tbody><tr><td>2.2</td><td>>=3.20</td><td>>=3.21</td></tr><tr><td>2.1</td><td>^3.0</td><td><p></p><p>>=3.0 &#x3C;3.21</p></td></tr><tr><td>2.0</td><td>^3.0</td><td>N/a</td></tr></tbody></table>

## Installation and deployment

Each version of APIM includes a number of policies by default. If the policy is not included in the default distribution or you would like to use a different version of the policy, you can modify the plugin.

{% hint style="warning" %}
Please ensure the policy version you select is compatible with your version of APIM.
{% endhint %}

To do so, follow these steps:

1. Download the plugin archive (a `.zip` file) from [the plugins download page](https://download.gravitee.io/#graviteeio-apim/plugins/)
2. Add the file into the `plugins` folder for both the gateway and management API

{% hint style="info" %}
**Location of `plugins` folder**

The location of the `plugins` folder varies depending on your installation. By default, it is in ${GRAVITEE\_HOME/plugins}. This can be modified in [the `gravitee.yaml` file.](../../getting-started/configuration/the-gravitee-api-gateway/environment-variables-system-properties-and-the-gravitee.yaml-file.md#configure-the-plugins-repository)

Most installations will contain the `plugins` folder in`/gravitee/apim-gateway/plugins` for the gateway and `/gravitee/apim-management-api/plugins` for the management API.
{% endhint %}

3. Remove any existing plugins of the same name.&#x20;
4. Restart your APIM nodes

## Errors

### Overview

<table data-full-width="false"><thead><tr><th>Phase</th><th>HTTP status code</th><th>Error template key</th><th>Description</th></tr></thead><tbody><tr><td>onRequest</td><td><code>400</code></td><td>JSON_INVALID_PAYLOAD</td><td>Request payload cannot be transformed properly to XML</td></tr><tr><td>onResponse</td><td><code>500</code></td><td>JSON_INVALID_PAYLOAD</td><td>Response payload cannot be transformed properly to XML</td></tr><tr><td>onMessageRequest</td><td><code>400</code></td><td>JSON_INVALID_MESSAGE_PAYLOAD</td><td>Incoming message cannot be transformed properly to XML</td></tr><tr><td>onMessageResponse</td><td><code>500</code></td><td>JSON_INVALID_MESSAGE_PAYLOAD</td><td>Outgoing message cannot be transformed properly to XML</td></tr></tbody></table>

### Nested objects

To limit the processing time in the case of a nested object, the default max depth of a nested object has been set to 1000. This default value can be overridden using the environment variable `gravitee_policy_jsonxml_maxdepth`.

## Changelog

### 2.2

#### What's New?

* Blazingly fast
* Full chatgpt and neuralink integration for quick API mastery

#### Bug fixes

* Fix crashes related to nested objects

#### Breaking Changes

* Only supports APIM versions >4.0

### 2.1

#### What's New?

* Blazingly fast
* Full chatgpt and neuralink integration for quick API mastery

#### Bug fixes

* Fix crashes related to nested objects

#### Breaking Changes

* Only supports APIM versions >4.0

