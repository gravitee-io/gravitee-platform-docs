---
hidden: true
---

# HTTP Callout

## Overview

You can use the `callout-http` policy to invoke an HTTP(S) URL and place a subset or all of the content in one or more variables of the request execution context.

This can be useful if you need some data from an external service and want to inject it during request processing.

The result of the callout is placed in a variable called `calloutResponse` and is only available during policy execution. If no variable is configured, the result of the callout is no longer available.

## Examples

{% hint style="warning" %}
This policy can be applied to v2 APIs and v4 HTTP proxy APIs. It cannot be applied to v4 message APIs or v4 TCP proxy APIs.
{% endhint %}

{% tabs %}
{% tab title="V4 API Definition" %}
This flow demonstrates the use of the HTTP Callout policy to make an external callout to the JsonPlaceholder API, retrieve key elements that are inserted in Context Variables, and chained with an Assign Content policy that maps the response to the consumer.

````json
```
"flows" : [ {
      "id" : "0e919364-f985-4d4b-9193-64f9857d4b9b",
      "path-operator" : {
        "path" : "/",
        "operator" : "STARTS_WITH"
      },
      "condition" : "",
      "consumers" : [ ],
      "methods" : [ ],
      "pre" : [ {
        "name" : "HTTP Callout",
        "description" : "",
        "enabled" : true,
        "policy" : "policy-http-callout",
        "configuration" : {"variables":[{"name":"name","value":"{#jsonPath(#calloutResponse.content, '$.name')}"},{"value":"true","name":"idtest"}],"method":"GET","fireAndForget":false,"scope":"REQUEST","errorStatusCode":"500","errorCondition":"{#calloutResponse.status >= 400 and #calloutResponse.status <= 599}","url":"https://jsonplaceholder.typicode.com/users/{#request.headers['userId'][0]}/","exitOnError":false}
      }, {
        "name" : "HTTP Callout",
        "description" : "",
        "enabled" : true,
        "policy" : "policy-http-callout",
        "condition" : "{#context.attributes['idtest'] = true}",
        "configuration" : {"variables":[{"name":"posts","value":"{#calloutResponse.content}"}],"method":"GET","fireAndForget":false,"scope":"REQUEST","errorStatusCode":"500","errorCondition":"{#calloutResponse.status >= 400 and #calloutResponse.status <= 599}","url":"https://jsonplaceholder.typicode.com/users/{#request.headers['userId'][0]}/posts","exitOnError":false}
      } ],
      "post" : [ {
        "name" : "Assign content",
        "description" : "",
        "enabled" : true,
        "policy" : "policy-assign-content",
        "condition" : "{#context.attributes['posts'] != null}",
        "configuration" : {"scope":"RESPONSE","body":"{\n\"userId\": ${request.headers['userId'][0]},\n\"name\": ${context.attributes['name']},\n\"posts\": ${context.attributes['posts']}\n}"}
      } ],
      "enabled" : true
    } ]
  } ],
```
````

\{% endtab %\}

\{% tab title="V4 API CRD" %\} This flow demonstrates the use of the HTTP Callout policy to make an external callout to the JsonPlaceholder API, retrieve key elements that are inserted in Context Variables, and chained with an Assign Content policy that maps the response to the consumer.

\`

\`\`yaml flows: - id: "0e919364-f985-4d4b-9193-64f9857d4b9b" path-operator: path: "/" operator: "STARTS\_WITH" condition: "" consumers: \[] methods: \[] pre: - name: "HTTP Callout" description: "" enabled: true policy: "policy-http-callout" configuration: variables: - name: "name" value: "{#jsonPath(#calloutResponse.content, '$.name')}" - value: "true" name: "idtest" method: "GET" fireAndForget: false scope: "REQUEST" errorStatusCode: "500" errorCondition: "{#calloutResponse.status >= 400 and #calloutResponse.status\
\ <= 599}" url: "https://jsonplaceholder.typicode.com/users/{#request.headers\['userId']\[0]}/" exitOnError: false - name: "HTTP Callout" description: "" enabled: true policy: "policy-http-callout" condition: "{#context.attributes\['idtest'] = true}" configuration: variables: - name: "posts" value: "{#calloutResponse.content}" method: "GET" fireAndForget: false scope: "REQUEST" errorStatusCode: "500" errorCondition: "{#calloutResponse.status >= 400 and #calloutResponse.status\
\ <= 599}" url: "https://jsonplaceholder.typicode.com/users/{#request.headers\['userId']\[0]}/posts" exitOnError: false post: - name: "Assign content" description: "" enabled: true policy: "policy-assign-content" condition: "{#context.attributes\['posts'] != null}" configuration: scope: "RESPONSE" body: "{\n"userId": ${request.headers\['userId']\[0]},\n"name": ${context.attributes\['name']},\n\
"posts": ${context.attributes\['posts']}\n}" enabled: true

```

</div>

</div>

## Configuration

### Phases

The phases checked below are supported by the `callout-http` policy:

<table data-full-width="false"><thead><tr><th width="202">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="198">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>true</td><td>onRequest</td><td>true</td></tr><tr><td>onResponse</td><td>true</td><td>onResponse</td><td>true</td></tr><tr><td>onRequestContent</td><td>true</td><td>onMessageRequest</td><td>false</td></tr><tr><td>onResponseContent</td><td>true</td><td>onMessageResponse</td><td>false</td></tr></tbody></table>

### Options

The `callout-http` policy can be configured with the following options:

<table><thead><tr><th width="193">Property</th><th width="106" data-type="checkbox">Required</th><th width="192">Description</th><th>Type</th><th>Default</th></tr></thead><tbody><tr><td>method</td><td>true</td><td>HTTP Method used to invoke URL</td><td>HTTP method</td><td>GET</td></tr><tr><td>useSystemProxy</td><td>true</td><td>Use the system proxy configured by your administrator</td><td>boolean</td><td>false</td></tr><tr><td>url</td><td>true</td><td>URL invoked by the HTTP client (support EL)</td><td>URL</td><td>-</td></tr><tr><td>headers</td><td>true</td><td>List of HTTP headers used to invoke the URL (support EL)</td><td>HTTP Headers</td><td>-</td></tr><tr><td>body</td><td>true</td><td>The body content send when calling the URL (support EL)</td><td>string</td><td>-</td></tr><tr><td>fireAndForget</td><td>true</td><td>Make the http call without expecting any response. When activating this mode, context variables and exit on error are useless.</td><td>boolean</td><td>false</td></tr><tr><td>variables</td><td>true</td><td>The variables to set in the execution context when retrieving content of HTTP call (support EL)</td><td>List of variables</td><td>-</td></tr><tr><td>exitOnError</td><td>true</td><td>Terminate the request if the error condition is true</td><td>boolean</td><td>false</td></tr><tr><td>errorCondition</td><td>true</td><td>The condition which will be verified to end the request (support EL)</td><td>string</td><td>{#calloutResponse.status >= 400 and #calloutResponse.status ⇐ 599}</td></tr><tr><td>errorStatusCode</td><td>true</td><td>HTTP Status Code sent to the consumer if the condition is true</td><td>int</td><td>500</td></tr><tr><td>errorContent</td><td>true</td><td>The body response of the error if the condition is true (support EL)</td><td>string</td><td></td></tr></tbody></table>

### System Proxy

If the option `useSystemProxy` is checked, proxy information will be read from `JVM_OPTS` or from the `gravitee.yml` file if `JVM_OPTS` is not set. The system properties are as follows:

<table><thead><tr><th>Property</th><th width="132.66666666666666" data-type="checkbox">Required</th><th>Description</th></tr></thead><tbody><tr><td>system.proxy.host</td><td>true</td><td>Proxy Hostname or IP</td></tr><tr><td>system.proxy.port</td><td>true</td><td>The proxy port</td></tr><tr><td>system.proxy.type</td><td>true</td><td>The type of proxy (HTTP, SOCK4, SOCK5)</td></tr><tr><td>system.proxy.username</td><td>false</td><td>Username for proxy authentication if any</td></tr><tr><td>system.proxy.password</td><td>false</td><td>Password for proxy authentication if any</td></tr></tbody></table>

#### HTTP client proxy options

```

## global configuration of the http client

system: proxy: type: HTTP host: localhost port: 3128 username: user password: secret

```

## Compatibility matrix

The following is the compatibility matrix for APIM and the `callout-http` policy:

<table data-full-width="false"><thead><tr><th>Plugin Version</th><th>Supported APIM versions</th></tr></thead><tbody><tr><td>2.x+</td><td>3.18+</td></tr><tr><td>1.15.x+</td><td>3.15.x to 3.17.x</td></tr><tr><td>1.13.x to 1.14.x</td><td>3.10.x to 3.14.x</td></tr><tr><td>Up to 1.12.x</td><td>Up to 3.9.x</td></tr></tbody></table>

## Errors

<table data-full-width="false"><thead><tr><th width="171">HTTP status code</th><th width="387">Error template key</th></tr></thead><tbody><tr><td><code>500</code></td><td>An error occurred while invoking URL</td></tr></tbody></table>

You can override the default response provided by the policy with the response templates feature. These templates must be defined at the API level with the APIM Console **Proxy > Response Templates** function.

The error keys sent by this policy are as follows:

<table data-full-width="false"><thead><tr><th>Key</th><th>Parameters</th></tr></thead><tbody><tr><td>CALLOUT_EXIT_ON_ERROR</td><td>-</td></tr><tr><td>CALLOUT_HTTP_ERROR</td><td>-</td></tr></tbody></table>

## Changelogs

<div data-gb-custom-block data-tag="@github-files/github-code-block" data-url='https://github.com/gravitee-io/gravitee-policy-callout-http/blob/master/CHANGELOG.md'></div>
```
{% endtab %}
{% endtabs %}
