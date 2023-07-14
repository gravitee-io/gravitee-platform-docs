---
description: Used to override the HTTP method provided by initial API consumer
---

# Override HTTP Method

<details>

<summary>Enterprise Feature</summary>

This plugin requires an enterprise license or trial which you can learn more about here.

</details>

## Overview

The `override-http-method` policy alters the HTTP method that the API consumer specifies when calling the API and uses a new method specified in the flow to make the call.

This policy does not act on messages and only applies to the request phase of API flows.

### Example

{% hint style="info" %}
This example will work for proxy APIs and message APIs, just acting on the initial connection request phase in both cases.
{% endhint %}

The Gravitee echo API returns a JSON response when a `GET` request is sent to [https://api.gravitee.io/echo](https://api.gravitee.io/echo). The response is formatted like so:

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

This API would typically be called with just a `GET` request, but if a client tries to run a `PUT` request, they will get a [405 Method Not Allowed](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/405) response. If the API publisher wants to ensure consistent behavior regardless of HTTP method called (in this case, returning the standard response), then adding an `override-http-method` policy to convert the request from any method (e.g. `PUT`, `POST`, etc) to a `GET` request will ensure that the expected response above is always returned.

## Configuration

Policies can be added to flows that are assigned to an API or to a plan. Gravitee supports configuring policies through the policy design studio in the management UI, interacting directly with the management API, or using the Gravitee Kubernetes Operator (GKO) in a Kubernetes deployment.

{% tabs %}
{% tab title="Management UI" %}
<mark style="color:yellow;">We should wait to make these once the v4 policy design studio is finalized</mark>
{% endtab %}

{% tab title="Management API" %}
When using the management API, policies are added as flows either directly to an API or to a  plan. To learn more about the structure of the management API, check out the reference documentation here.

{% code title="Sample Configuration" %}
```json
{
  "name": "Custom name",
  "description": "Overrides HTTP method",
  "policy": "policy-override-request-method",
  "configuration": {
    "method": "GET"
  }
}
```
{% endcode %}
{% endtab %}

{% tab title="Kubernetes Operator" %}

{% endtab %}
{% endtabs %}

### Reference

<table data-full-width="false"><thead><tr><th width="157">Property</th><th width="101" data-type="checkbox">Required</th><th width="155">Description</th><th width="100" data-type="select">Type</th><th>Options</th><th>Default</th></tr></thead><tbody><tr><td>name</td><td>false</td><td>Provide a descriptive name for your policy</td><td></td><td>N/a</td><td>N/a</td></tr><tr><td>method</td><td>true</td><td>HTTP method used regardless of method called</td><td></td><td>GET<br>POST<br>PUT<br>DELETE<br>PATCH<br>HEAD<br>CONNECT<br>OPTIONS<br>TRACE</td><td>GET</td></tr></tbody></table>

### Phases

Provide link to a conceptual overview of phases as well as an explanation of the difference between v4 and v2 API definitions.

{% tabs %}
{% tab title="V4 API definition" %}
Link explaining difference

<table data-full-width="false"><thead><tr><th width="138" data-type="checkbox">onRequest</th><th width="152" data-type="checkbox">onResponse</th><th data-type="checkbox">onMessageRequest</th><th data-type="checkbox">onMessageResponse</th></tr></thead><tbody><tr><td>true</td><td>false</td><td>false</td><td>false</td></tr></tbody></table>
{% endtab %}

{% tab title="V2 API definition" %}
Link explaining difference

<table><thead><tr><th data-type="checkbox">onRequest</th><th data-type="checkbox">on </th><th width="197" data-type="checkbox">onRequestContent</th><th data-type="checkbox">onResponseContent</th></tr></thead><tbody><tr><td>true</td><td>false</td><td>false</td><td>false</td></tr></tbody></table>
{% endtab %}
{% endtabs %}

## Compatibility matrix

In the [changelog for each version of APIM](../../../releases-and-changelog/changelog/), we provide a list of policies included in the default distribution. The chart below summarizes this information in relation to the `override-http-method` policy.

<table data-full-width="false"><thead><tr><th>Plugin Version</th><th width="233">Supported APIM versions</th><th>Included in APIM default distribution</th></tr></thead><tbody><tr><td>Up to 2.x</td><td>>=3.21</td><td>>= 3.21</td></tr><tr><td>Up to 1.x</td><td>All</td><td>&#x3C;= 3.20</td></tr></tbody></table>

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

The location of the `plugins` folder varies depending on your installation. By default, it is in ${GRAVITEE\_HOME/plugins}. This can be modified in [the `gravitee.yaml` file.](../../../getting-started/configuration/the-gravitee-api-gateway/environment-variables-system-properties-and-the-gravitee.yaml-file.md#configure-the-plugins-repository)

Most installations will contain the `plugins` folder in`/gravitee/apim-gateway/plugins` for the gateway and `/gravitee/apim-management-api/plugins` for the management API.
{% endhint %}

3. Remove any existing plugins of the same name.&#x20;
4. Restart your APIM nodes

## Errors

There are no out-of-the-box errors returned by this policy.

## Changelog

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-override-http-method/blob/master/CHANGELOG.md" %}

