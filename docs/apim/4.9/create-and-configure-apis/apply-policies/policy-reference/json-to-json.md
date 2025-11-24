---
description: An overview about json to json.
---

# JSON to JSON

## Overview

You can use the `json-to-json` policy to apply a transformation (or mapping) on the request, response, and/or message content.

This policy is based on the [JOLT](https://github.com/bazaarvoice/jolt) library. In APIM, you need to provide the JOLT specification in the policy configuration.

{% hint style="info" %}
You can use the Gravitee Expression Language (EL) in the JOLT specification.
{% endhint %}

At the request/response level, the policy does nothing if the processed request/response does not contain JSON. This policy checks the `Content-Type` header before applying any transformation.

At message level, the policy does nothing if the processed message has no content. This means that the message will be sent again as is.

## Basic Usage

### Append a new attribute to existing content

If you want to append a new attribute and value to the existing content, use the JOLT operation `default`, as shown below:

<table data-full-width="false"><thead><tr><th width="217.8359375">Starting Content</th><th width="213.203125">Desired Content</th><th>JOLT Specification</th></tr></thead><tbody><tr><td><pre class="language-json"><code class="lang-json">{
  "_id": "57762",
  "name": "name
}
</code></pre></td><td><pre class="language-json"><code class="lang-json">{
  "_id": "57762",
  "name": "name",
  "UUID": 123456
}
</code></pre></td><td><pre class="language-json"><code class="lang-json">[
  {
    "operation": "shift",
    "spec": {
      "*": "&#x26;"
    }
  },
  {
    "operation": "default",
    "spec": {
      "UUID": 123456
    }
  }
]
</code></pre></td></tr></tbody></table>

Gravitee Expression Language is also supported, so you can dynamically inject values (such as a `X-myHeader` header value), as shown below:

<table data-full-width="false"><thead><tr><th width="217.8359375">Starting Content</th><th width="213.203125">Desired Content</th><th>JOLT Specification</th></tr></thead><tbody><tr><td><pre class="language-json"><code class="lang-json">{
  "_id": "57762",
  "name": "name
}
</code></pre></td><td><pre class="language-json"><code class="lang-json">{
  "_id": "57762",
  "name": "name",
  "UUID": 123456
}
</code></pre></td><td><pre class="language-json"><code class="lang-json">[
  {
    "operation": "shift",
    "spec": {
      "*": "&#x26;"
    }
  },
  {
    "operation": "default",
    "spec": {
      "UUID": {#request.headers['X-myHeader'][0]}
    }
  }
]
</code></pre></td></tr></tbody></table>

### Rename a specific attribute

If you want to rename an existing attribute, use the JOLT operation `shift`, as shown below:

<table data-full-width="false"><thead><tr><th width="217.8359375">Starting Content</th><th width="213.203125">Desired Content</th><th>JOLT Specification</th></tr></thead><tbody><tr><td><pre class="language-json"><code class="lang-json">{
  "_id": "57762",
  "name": "name"
}
</code></pre></td><td><pre class="language-json"><code class="lang-json">{
  "userId": "57762",
  "name": "name"
}
</code></pre></td><td><pre class="language-json"><code class="lang-json">[
  {
    "operation": "shift",
    "spec": {
      "_id": "userId",
      "*": {
        "$": "&#x26;1"
      }
    }
  }
]
</code></pre></td></tr></tbody></table>

### Remove an attribute, and rename another attribute

If you want to remove one attribute and rename another, use the `shift` and `remove` JOLT operations together, as shown below:

<table data-full-width="false"><thead><tr><th width="217.8359375">Starting Content</th><th width="213.203125">Desired Content</th><th>JOLT Specification</th></tr></thead><tbody><tr><td><pre class="language-json"><code class="lang-json">{
  "_id": "57762",
  "name": "name",
  "__v": 0
}
</code></pre></td><td><pre class="language-json"><code class="lang-json">{
  "userId": "57762",
  "name": "name"
}
</code></pre></td><td><pre class="language-json"><code class="lang-json">[
  {
    "operation": "shift",
    "spec": {
      "_id": "userId",
      "*": {
        "$": "&#x26;1"
      }
    }
  },
  {
    "operation": "remove",
    "spec": {
      "__v": ""
    }
  }
]
</code></pre></td></tr></tbody></table>

## Transformation

As a more complex use case, you may want to trim down the response payload by only including certain fields. In this scenario, you can rewrite the response using the JOLT operation `shift`, as shown below.

* `name` needs to change to `accountHolder`
* Each account should include only the `id`, `name`, and `metadata` fields
* `metadata` needs to remain unchanged

<table data-full-width="true"><thead><tr><th width="289.85546875">Starting Content</th><th width="275.41015625">Desired Content</th><th width="419.8828125">JOLT Specification</th></tr></thead><tbody><tr><td><pre class="language-json"><code class="lang-json">{
  "item": {
    "id": "1230120207321556",
    "name": "Donald Duck",
    "accountDetails": {
      "updatedAt": "2025-03-24T08:10:35+01:00",
      "items": [
        {
          "balance": 1234.56,
          "account": {
            "id": 2073214,
            "name": "Current Account 1",
            "lastUpdated": "2025-03-24T08:09:12+01:00"
          }
        },
        {
          "balance": 246810.57,
          "account": {
            "id": 3073214,
            "name": "Checking Account 2",
            "lastUpdated": "2024-12-19T17:12:13+01:00",
            "metadata": {
              "id": 20,
              "name": "CheckBook 1",
              "otherDetails": {
                "friendlyName": "Checking",
                "currency": "GBP"
              }
            }
          }
        },
        {
          "balance": 36912.58,
          "account": {
            "id": 4073214,
            "name": "Savings Account 3",
            "lastUpdated": "2024-12-19T15:59:52+01:00",
            "unUsed": false,
            "expired": false,
            "metadata": {
              "id": 22,
              "name": "Savings 3",
              "otherDetails": {
                "friendlyName": "Savings",
                "currency": "GBP"
              }
            }
          }
        }
      ]
    }
  }
}
</code></pre></td><td><pre class="language-json"><code class="lang-json">{
  "accountHolder" : "Donald Duck",
  "accountDetails" : [ {
    "balance" : 1234.56,
    "account" : {
      "id" : 2073214,
      "name" : "Current Account 1"
    }
  }, {
    "balance" : 246810.57,
    "account" : {
      "id" : 3073214,
      "name" : "Checking Account 2",
      "metadata" : {
        "id" : 20,
        "name" : "CheckBook 1",
        "otherDetails" : {
          "friendlyName" : "Checking",
          "currency" : "GBP"
        }
      }
    }
  }, {
    "balance" : 36912.58,
    "account" : {
      "id" : 4073214,
      "name" : "Savings Account 3",
      "metadata" : {
        "id" : 22,
        "name" : "Savings 3",
        "otherDetails" : {
          "friendlyName" : "Savings",
          "currency" : "GBP"
        }
      }
    }
  } ]
}
</code></pre></td><td><pre class="language-json"><code class="lang-json">[
{
"operation": "shift",
"spec": {
"item": {
"name": "accountHolder",
"accountDetails": {
"items": {
"*": {
"balance": "accountDetails[&#x26;1].balance",
"account": {
"id": "accountDetails[&#x26;2].account.id",
"name": "accountDetails[&#x26;2].account.name",
"metadata": "accountDetails[&#x26;2].account.metadata"
}
}
}
}
}
}
}
]
</code></pre></td></tr></tbody></table>

## Examples

{% hint style="warning" %}
This policy can be applied to v2 APIs, v4 HTTP proxy APIs, and v4 Message APIs. It cannot be applied to v4 TCP proxy APIs.
{% endhint %}

{% tabs %}
{% tab title="v4 API definition" %}
This snippet of a v4 API definition includes a flow that uses the `json-to-json` policy in the response phase to rename the `_id` key to `userId` and remove the `__v` field.

<pre class="language-json"><code class="lang-json">{
  "api": {
    "definitionVersion": "V4",
    "type": "PROXY",
    "name": "JSON Transformation Example v4 API",
<strong>    "flows" : [ {
</strong>          "name" : "JSON Transformation",
          "enabled" : true,
          "selectors" : [ {
            "type" : "HTTP",
            "path" : "/",
            "pathOperator" : "STARTS_WITH"
          } ],
          "request" : [],
          "response" : [ {
            "name" : "JSON to JSON Transformation",
            "description": "Rename '_id' to 'userId', and remove '__v' field.",
            "enabled" : true,
            "policy" : "json-to-json",
            "configuration" : {
                "overrideContentType": true,
                "scope": "REQUEST",
                "specification": "[\n  {\n    \"operation\": \"shift\",\n    \"spec\": {\n      \"_id\": \"userId\",\n      \"*\": {\n        \"$\": \"&#x26;1\"\n      }\n    }\n  },\n  {\n    \"operation\": \"remove\",\n    \"spec\": {\n      \"__v\": \"\"\n    }\n  }\n]"
            }
          } ],
          "subscribe": [],
          "publish": []
  ...
  } ],
  ...
}
</code></pre>
{% endtab %}

{% tab title="v4 API CRD" %}
Below is a snippet of a v4 API YAML manifest for the Gravitee Kubernetes Operator. It includes a flow that uses the `json-to-json` policy in the response phase to rename the `_id` key to `userId` and remove the `__v` field.

```yaml
apiVersion: "gravitee.io/v1alpha1"
kind: "ApiV4Definition"
metadata:
  name: "json-transformation-example-v4-gko-api"
spec:
  name: "JSON Transformation Example V4 GKO API"
  flows:
    name: "Common Flow"
    enabled: true
    selectors:
    - type: "HTTP"
      path: "/"
      pathOperator: "STARTS_WITH"
    response:
    - name: "JSON to JSON Transformation"
      enabled: true
      policy: "json-to-json"
      configuration:
        overrideContentType: true
        specification: "[\n  {\n    \"operation\": \"shift\",\n    \"spec\": {\n      \"_id\": \"userId\",\n      \"*\": {\n        \"$\": \"&1\"\n      }\n    }\n  },\n  {\n    \"operation\": \"remove\",\n    \"spec\": {\n      \"__v\": \"\"\n    }\n  }\n]"      
    ...
```
{% endtab %}
{% endtabs %}

## Configuration

A sample policy configuration is shown below:

{% code title="Sample Configuration" %}
```json
{
    "json-to-json": {
        "scope": "REQUEST",
        "specification": "[{ \"operation\": \"shift\", \"spec\": { \"_id\": \"id\", \"*\": { \"$\": \"&1\" } } }, { \"operation\": \"remove\", \"spec\": { \"__v\": \"\" } }]"
    }
}
```
{% endcode %}

### Phases

The phases checked below are supported by the `json-to-json` policy:

<table data-full-width="false"><thead><tr><th width="209">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="199.41136671177264">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>true</td><td>onRequest</td><td>true</td></tr><tr><td>onResponse</td><td>true</td><td>onResponse</td><td>true</td></tr><tr><td>onRequestContent</td><td>true</td><td>onMessageRequest</td><td>true</td></tr><tr><td>onResponseContent</td><td>true</td><td>onMessageResponse</td><td>true</td></tr></tbody></table>

### Options

The `json-to-json` policy can be configured with the following options:

<table><thead><tr><th width="210">Property</th><th width="165">Required</th><th width="238">Description</th><th width="83">Type</th><th>Default</th></tr></thead><tbody><tr><td>scope</td><td>(only needed for legacy execution engine)</td><td>The execution scope (<code>request</code> or <code>response</code>)</td><td>string</td><td><code>REQUEST</code></td></tr><tr><td>specification</td><td>X</td><td><p>The <a href="http://jolt-demo.appspot.com/">JOLT</a> specification to apply on a given content.</p><p>Can contain EL.</p></td><td>string</td><td></td></tr><tr><td>overrideContentType</td><td></td><td>Override the Content-Type to <code>application/json</code></td><td>string</td><td><code>true</code></td></tr></tbody></table>

## Compatibility matrix

The following is the compatibility matrix for APIM and the `json-to-json` policy:

<table data-full-width="false"><thead><tr><th>Plugin Version</th><th>Supported APIM versions</th></tr></thead><tbody><tr><td>1.x</td><td>Up to 3.19.x</td></tr><tr><td>2.x</td><td>3.20.x</td></tr><tr><td>3.x</td><td>4.0+</td></tr></tbody></table>

## Errors

{% hint style="info" %}
You can use the Response Template feature to override the default responses provided by the policy. These templates must be defined at the API level. They can be configured in the APIM Console by selecting **Entrypoints** from the API menu and clicking the **Response Templates** tab.
{% endhint %}

Errors generated by the reactive execution engine:

<table data-full-width="false"><thead><tr><th width="98.5">Code</th><th width="302">Error template key</th><th>Description</th></tr></thead><tbody><tr><td><code>500</code></td><td>INVALID_JSON_TRANSFORMATION</td><td>Unable to apply JOLT transformation to payload</td></tr></tbody></table>

Errors generated by the legacy execution engine:

<table data-full-width="false"><thead><tr><th width="171">Code</th><th width="387">Message</th></tr></thead><tbody><tr><td><code>500</code></td><td>Bad specification file or transformation cannot be executed properly</td></tr></tbody></table>

## Changelogs

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-json-xml/blob/master/CHANGELOG.md" %}
