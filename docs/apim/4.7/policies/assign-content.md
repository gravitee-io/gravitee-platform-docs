---
description: An overview about ---.
hidden: true
---

# Assign Content

## Overview

You can use the `policy-assign-content` policy to change or transform the content of the request body or response body.

The `body` configuration value of this policy is compatible with plain text, Gravitee Expression Language, and the [Freemarker](https://freemarker.apache.org/) template engine, which allows you to apply complex transformations, such as transforming from XML to JSON and vice versa.

You can also access multiple objects from the template context, such as the request and response bodies, dictionaries, context attributes and more, as shown in the usage examples below.

## Basic Usage

A typical usage would be to simply overwrite the original request payload with something new:

```json
{
  "name": "Assign content",
  "enabled": true,
  "policy": "policy-assign-content",
  "configuration": {
    "scope": "REQUEST",
    "body": "Put your new content here, or use Freemarker!"
  }
}
```

<figure><img src="../.gitbook/assets/image (186) (1).png" alt="" width="375"><figcaption><p>Assign Content policy configuration UI</p></figcaption></figure>

### Replace original payload with dynamic values

You can use the Assign Content policy to inject a request header, context attribute, or a dictionary value into the request payload:

```ftl
{
  "A-New-Header-Value": "${request.headers['X-Header'][0]}",
  "application": "${context.attributes['application']}",
  "example": "${context.dictionaries['my-dictionary']['my-value']}"
}
```

{% hint style="info" %}
Notice the use of `${}` instead of `#{}`. This is needed for compatibility with the Freemarker template engine.
{% endhint %}

For v4 message APIs, you can use the Assign Content policy to inject the metadata into the message:

```ftl
{
  "metadata": "${message.attributes['metadata']}"
}
```

### Append to existing content

You can append new content to the existing payload using Freemaker.

In the following example, the original JSON payload (`request.content`) is injected into a new JSON attribute (`result`), as well as other new content (`requestId` and `requestCost`):

<table data-full-width="true"><thead><tr><th width="289.85546875">Original request payload</th><th width="275.41015625">Assign Content (Freemarker) configuration</th><th width="419.8828125">Final response payload</th></tr></thead><tbody><tr><td><pre class="language-json"><code class="lang-json">[
  {
    "runway": "E",
    "runwayName": "EAST",
    "runwayStatus": "OPEN",
    "runwayDirection": "26R",
    "visibilityCategory": "I",
    "lastChange": "2024-09-11T10:45:45Z"
  },
  {
    "runway": "S",
    "runwayName": "SOUTH",
    "runwayStatus": "CLOSED",
    "runwayDirection": "26L",
    "visibilityCategory": "I",
    "lastChange": "2024-07-08T09:00:00Z"
  },
  {
    "runway": "W",
    "runwayName": "WEST",
    "runwayStatus": "OPEN",
    "runwayDirection": "08L",
    "visibilityCategory": "Z",
    "lastChange": "2024-09-11T10:45:45Z"
  }
]
</code></pre></td><td><pre class="language-json"><code class="lang-json">{
  "requestId": "${response.headers['X-Gravitee-Request-Id'][0]}",
  "requestCost": "${context.attributes['monetization_cost']}",
  "result": ${request.content}
}
</code></pre></td><td><pre class="language-json"><code class="lang-json">{
"requestId": "123456",
"requestCost": "0.12",
"result": [
{
"runway": "E",
"runwayName": "EAST",
"runwayStatus": "OPEN",
"runwayDirection": "26R",
"visibilityCategory": "I",
"lastChange": "2024-09-11T10:45:45Z"
},
{
"runway": "S",
"runwayName": "SOUTH",
"runwayStatus": "CLOSED",
"runwayDirection": "26L",
"visibilityCategory": "I",
"lastChange": "2024-07-08T09:00:00Z"
},
{
"runway": "W",
"runwayName": "WEST",
"runwayStatus": "OPEN",
"runwayDirection": "08L",
"visibilityCategory": "Z",
"lastChange": "2024-09-11T10:45:45Z"
}
]
}
</code></pre></td></tr></tbody></table>

### Rewrite or transform the payload

You may want to return only selective data from the response, or rewrite the final response payload.

In this scenario, the response from the backend service includes a JSON array with multiple airport runways. Only runways that match `"runwayStatus": "OPEN"` should be returned.

{% code title="Response payload from backend service: " %}
```json
[
  {
    "runway": "E",
    "runwayName": "EAST",
    "runwayStatus": "OPEN",
    "runwayDirection": "26R",
    "visibilityCategory": "I",
    "lastChange": "2024-09-11T10:45:45Z"
  },
  {
    "runway": "S",
    "runwayName": "SOUTH",
    "runwayStatus": "CLOSED",
    "runwayDirection": "26L",
    "visibilityCategory": "I",
    "lastChange": "2024-07-08T09:00:00Z"
  },
  {
    "runway": "W",
    "runwayName": "WEST",
    "runwayStatus": "OPEN",
    "runwayDirection": "08L",
    "visibilityCategory": "Z",
    "lastChange": "2024-09-11T10:45:45Z"
  }
]
```
{% endcode %}

This content is transformed using [Freemarker](https://freemarker.apache.org/) code, as shown below:

{% code lineNumbers="true" %}
```ftl
<#assign body = response.content?eval_json >
<#list body as runwayItem>
  <#if runwayItem.runway == 'OPEN'>
    [
      {
        <#list runwayItem?keys as key>
          "${key}":"${runwayItem[key]}",
        </#list>
      }
    ]
  </#if>
</#list>
```
{% endcode %}

Let's walk through the above Freemarker code, line by line:

**Line 1:** Assign the `response.content` value to a variable called `body` , and evaluate it into a JSON object.

**Line 2:** Using the root (`body`) array, iterate through each item (`runwayItem`).

**Line 3:** Using a standard `if` statement, check if the `runway` attribute equals `OPEN`.

**Lines 4 and 5:** Start the final response with a JSON array (using square brackets for the array, and curly brackets for each array object).

**Line 6:** Get all items within this unique `runwayItem` object and loop through each of them, using `key` as the index/iterator.

**Line 7:** Output all key/value pairs to the final response.

<figure><img src="../.gitbook/assets/image (185) (1).png" alt=""><figcaption><p>Assign Content policy configuration UI</p></figcaption></figure>

{% code title="Final response payload (sent onto client):" %}
```json
[
  {
    "runway": "E",
    "runwayName": "EAST",
    "runwayStatus": "OPEN",
    "runwayDirection": "26R",
    "visibilityCategory": "I",
    "lastChange": "2024-09-11T10:45:45Z"
  },
  {
    "runway": "W",
    "runwayName": "WEST",
    "runwayStatus": "OPEN",
    "runwayDirection": "08L",
    "visibilityCategory": "Z",
    "lastChange": "2024-09-11T10:45:45Z"
  }
]
```
{% endcode %}

## Examples

{% hint style="warning" %}
This policy can be applied to v2 APIs, v4 HTTP proxy APIs, and v4 message APIs. It cannot be applied to v4 TCP proxy APIs.
{% endhint %}

{% tabs %}
{% tab title="v4 API definition" %}
This snippet of a v4 HTTP proxy API definition includes a flow that uses the `policy-assign-content` policy in the response phase to write a custom response back to the client:

<pre class="language-json"><code class="lang-json">{
  "api": {
    "definitionVersion": "V4",
    "type": "PROXY",
    "name": "Assign Content Example v4 API",
<strong>    "flows" : [ {
</strong>          "name" : "Assign Content",
          "enabled" : true,
          "selectors" : [ {
            "type" : "HTTP",
            "path" : "/",
            "pathOperator" : "STARTS_WITH"
          } ],
          "request" : [],
          "response" : [ {
            "name" : "Assign Content",
            "enabled" : true,
            "policy": "policy-assign-content",
            "configuration": {
              "scope": "RESPONSE",
              "body": "This is my custom response"
            }
          } ],
          "subscribe": [],
          "publish": []
  ...
  } ],
  ...
}
</code></pre>

This snippet of a v4 message API definition includes a flow that uses the `policy-assign-content` policy in the publish phase to simply rewrite the message that will be sent onto the backend event broker:

<pre class="language-json"><code class="lang-json">{
  "api": {
    "definitionVersion": "V4",
    "type": "MESSAGE",
    "name": "Assign Content Example v4-Message (Protocol Mediation)",
<strong>    "flows" : [ {
</strong>          "enabled": true,
          "selectors": [
            {
              "type": "CHANNEL",
              "channel": "/",
              "channelOperator": "STARTS_WITH"
            }
          ],
          "request" : [],
          "response" : [],
          "subscribe": [],
          "publish": [
            {
              "name": "Assign content",
              "enabled": true,
              "policy": "policy-assign-content",
              "configuration": {
                "scope": "PUBLISH",
                "body": "{\n    \"my_field1\": 123456,\n    \"my_field2\": \"Modified data\"\n}"
              }
            }
          ]
  ...
  } ],
  ...
}
</code></pre>
{% endtab %}

{% tab title="v4 API CRD" %}
Below is a snippet of a v4 API YAML manifest for the Gravitee Kubernetes Operator. It includes a flow that uses the `policy-assign-content` policy in the request phase to rewrite the incoming message.

```yaml
apiVersion: "gravitee.io/v1alpha1"
kind: "ApiV4Definition"
metadata:
  name: "assign-content-example-v4-gko-api"
spec:
  name: "Assign Content Example V4 GKO API"
  type: "PROXY"
  flows:
  - name: "Common Flow"
    enabled: true
    selectors:
    - type: "HTTP"
      path: "/"
      pathOperator: "STARTS_WITH"
    request:
    - name: "Assign Content"
      enabled: true
      policy: "policy-assign-content"
      configuration:
        scope: "REQUEST"
        body: "{\n    \"my_field1\": 123456,\n    \"my_field2\": \"This is a custom message\"\n}"      
    ...
```
{% endtab %}
{% endtabs %}

## Configuration

### Phases

The phases checked below are supported by the `policy-assign-content` policy:

<table data-full-width="false"><thead><tr><th width="202">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="198">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>false</td><td>onRequest</td><td>false</td></tr><tr><td>onResponse</td><td>false</td><td>onResponse</td><td>false</td></tr><tr><td>onRequestContent</td><td>true</td><td>onMessageRequest</td><td>true</td></tr><tr><td>onResponseContent</td><td>true</td><td>onMessageResponse</td><td>true</td></tr></tbody></table>

### Options

You can configure the `policy-assign-content` policy with the following options:

<table><thead><tr><th width="121">Property</th><th width="101" data-type="checkbox">Required</th><th width="202">Description</th><th width="87">Type</th><th>Default</th></tr></thead><tbody><tr><td>scope</td><td>true</td><td>The execution scope of the policy</td><td>scope</td><td><code>REQUEST</code></td></tr><tr><td>body</td><td>true</td><td>The data to push as request or response body content</td><td>string</td><td>-</td></tr></tbody></table>

## Compatibility matrix

The following is the compatibility matrix for APIM and the `policy-assign-content` policy:

<table data-full-width="false"><thead><tr><th>Plugin Version</th><th>Supported APIM versions</th></tr></thead><tbody><tr><td>Up to 1.6.x</td><td>Up to 3.9.x</td></tr><tr><td>1.7.x</td><td>3.10.x to 3.20.x</td></tr><tr><td>2.x</td><td>4.0+</td></tr></tbody></table>

## Errors

<table data-full-width="false"><thead><tr><th width="210">Phase</th><th width="171">HTTP status code</th><th width="387">Error template key</th></tr></thead><tbody><tr><td>onRequestContent</td><td><code>500</code></td><td>The body content cannot be transformed.</td></tr><tr><td>onResponseContent</td><td><code>500</code></td><td>The body content cannot be transformed.</td></tr><tr><td>onMessageRequest</td><td><code>400</code></td><td>The body content cannot be transformed.</td></tr><tr><td>onMessageResponse</td><td><code>500</code></td><td>The body content cannot be transformed.</td></tr></tbody></table>

## Changelogs

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-assign-content/blob/master/CHANGELOG.md" %}
