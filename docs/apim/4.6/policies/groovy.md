---
description: This page provides the technical details of the Groovy policy
hidden: true
---

# Groovy

## Overview

You can use the `groovy` policy to run [Groovy](http://www.groovy-lang.org/) scripts at any stage of request processing through the Gateway.

Functional and implementation information for the `groovy` policy is organized into the following sections:

* [Examples](groovy.md#examples)
* [Configuration](groovy.md#configuration)
* [Compatibility Matrix](groovy.md#compatibility-matrix)
* [Errors](groovy.md#errors)
* [Changelogs](groovy.md#changelogs)

## Examples

{% hint style="warning" %}
This policy can be applied to v2 APIs, v4 HTTP proxy APIs, and v4 message APIs. It cannot be applied to v4 TCP proxy APIs.
{% endhint %}

{% tabs %}
{% tab title="HTTP proxy API example" %}
**Example 1: onRequest / onResponse**

The following example Groovy script is executed during the OnResponse phase to change HTTP headers:

```groovy
response.headers.remove 'X-Powered-By'
response.headers.'X-Gravitee-Gateway-Version' = '0.14.0'
```

**Example 2: OnRequestContent / OnResponseContent**

The following example shows you how to use the `groovy` policy to transform JSON content:

**Input body content**

```json
{
  "age": 32,
  "firstname": "John",
  "lastname": "Doe"
}
```

**Groovy script**

```groovy
import groovy.json.JsonSlurper
import groovy.json.JsonOutput

def jsonSlurper = new JsonSlurper()
def content = jsonSlurper.parseText(response.content)
content.firstname = 'Hacked ' + content.firstname
content.country = 'US'
return JsonOutput.toJson(content)
```

**Output body content**

```json
{
  "age": 32,
  "firstname": "Hacked John",
  "lastname": "Doe",
  "country": "US"
}
```
{% endtab %}

{% tab title="Message API example" %}
**OnMessageRequest / OnMessageResponse**

The following example shows you how to use the Groovy policy to override the content of a message to change the greeting:

**Input message content**

```json
{
    "greeting": "Hello World !"
}
```

**Groovy script**

```groovy
import groovy.json.JsonSlurper
import groovy.json.JsonOutput

def jsonSlurper = new JsonSlurper()
def content = jsonSlurper.parseText(message.content)
content.greeting = 'Hello Universe!'
return JsonOutput.toJson(content)
```
{% endtab %}
{% endtabs %}

## Configuration

Sample policy configuration:

{% code title="Sample Configuration" %}
```groovy
"groovy": {
    "onRequestScript": "request.headers.'X-Gravitee-Gateway' = '0.14.0'",
    "onResponseScript": "response.headers.remove 'X-Powered-By'",
    "onRequestContentScript": "" // Not executed if empty
    "onResponseContentScript": "" // Not executed if empty
}
```
{% endcode %}

### Phases

The phases checked below are supported by the `groovy` policy:

<table data-full-width="false"><thead><tr><th width="202">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="198">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>true</td><td>onRequest</td><td>true</td></tr><tr><td>onResponse</td><td>true</td><td>onResponse</td><td>true</td></tr><tr><td>onRequestContent</td><td>true</td><td>onMessageRequest</td><td>true</td></tr><tr><td>onResponseContent</td><td>true</td><td>onMessageResponse</td><td>true</td></tr></tbody></table>

### Implementation by phase

{% tabs %}
{% tab title="onRequest / onResponse" %}
Some variables are automatically bound to the Groovy script to allow users to use them and define the policy behavior:

<table><thead><tr><th width="164.5">Name</th><th>Description</th></tr></thead><tbody><tr><td><code>request</code></td><td>Inbound HTTP request</td></tr><tr><td><code>response</code></td><td>Outbound HTTP response</td></tr><tr><td><code>context</code></td><td><code>PolicyContext</code> used to access external components such as services and resources</td></tr><tr><td><code>result</code></td><td>Groovy script result</td></tr></tbody></table>

Request or response processing can be interrupted by setting the result state to `FAILURE`. By default, it will throw a `500 - internal server error`, but you can override this behavior with the following properties:

* `code`: An HTTP status code
* `error`: The error message
* `key`: The key of a response template

```groovy
import io.gravitee.policy.groovy.PolicyResult.State

if (request.headers.containsKey('X-Gravitee-Break')) {
    result.key = 'RESPONSE_TEMPLATE_KEY';
    result.state = State.FAILURE;
    result.code = 500
    result.error = 'Stop request processing due to X-Gravitee-Break header'
} else {
    request.headers.'X-Groovy-Policy' = 'ok'
}
```

To customize the error sent by the policy:

```groovy
import io.gravitee.policy.groovy.PolicyResult.State
result.key = 'RESPONSE_TEMPLATE_KEY';
result.state = State.FAILURE;
result.code = 400
result.error = '{"error":"My specific error message","code":"MY_ERROR_CODE"}'
result.contentType = 'application/json'
```
{% endtab %}

{% tab title="onRequestContent / onResponseContent" %}
You can also transform request or response body content by applying a Groovy script on the `OnRequestContent` phase or the `OnResponseContent` phase.

{% hint style="info" %}
If you are using the [reactive](../overview/gravitee-api-definitions-and-execution-engines/reactive-execution-engine.md) engine, a single script is defined. To override the content of the request or response, `overrideContent`must be enabled in your configuration.
{% endhint %}
{% endtab %}

{% tab title="onMessageRequest / onMessageResponse" %}
This policy allows you to override the content of a message. Message content can be accessed using the `message.content` property in your Groovy script.
{% endtab %}
{% endtabs %}

### Impact of execution engine

The number of scripts used for the `groovy` policy and their execution depend on which [execution engine](../overview/execution-engine.md#reactive-and-legacy-execution-engine-comparison) is running.

{% tabs %}
{% tab title="Legacy engine" %}
| onRequestScript                                            | onResponseScript                                            | onRequestContentScript                                                                                                    | onResponseContentScript                                                                                                    |
| ---------------------------------------------------------- | ----------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| This script will be executed during the `onRequest` phase. | This script will be executed during the `onResponse` phase. | This script will be executed during the `onRequestContent` phase, meaning that you can access the content of the request. | This script will be executed during the `onRequestContent` phase, meaning that you can access the content of the response. |
{% endtab %}

{% tab title="Reactive engine" %}
<table><thead><tr><th width="255.5">script</th><th>overrideContent</th></tr></thead><tbody><tr><td>This script will be executed regardless of the phase.</td><td>If set to true, the content of the request, response, or message will be overridden by the result of the script.</td></tr></tbody></table>
{% endtab %}
{% endtabs %}

### Whitelist sandbox

The `groovy` policy comes with a native sandbox feature, which allows you to safely run Groovy scripts. The sandbox is based on a predefined list of allowed methods, fields, constructors, and annotations.

The complete whitelist can be found here: [gravitee groovy whitelist](https://gh.gravitee.io/gravitee-io/gravitee-policy-groovy/master/src/main/resources/groovy-whitelist).

This whitelist should be enough for almost all possible use cases. If you have specific needs which are not allowed by the built-in whitelist, you can extend (or even replace) the list with your own declarations by configuring the `gravitee.yml` file to specify:

* `groovy.whitelist.mode`: `append` or `replace`. This allows you to append some new whitelisted definitions to the built-in list or completely replace it. We recommend you always choose `append` unless you absolutely know what you are doing.
* `groovy.whitelist.list`: Allows declaring other methods, constructors, fields or annotations to the whitelist
  * Start with `method` to allow a specific method (complete signature)
  * Start with `class` to allow a complete class. All methods, constructors and fields of the class will then be accessible.
  * Start with `new` to allow a specific constructor (complete signature)
  * Start with `field` to allow access to a specific field of a class
  * Start with `annotation` to allow use of a specific annotation

Example:

```groovy
groovy:
  whitelist:
    mode: append
    list:
        - method java.time.format.DateTimeFormatter ofLocalizedDate java.time.format.FormatStyle
        - class java.time.format.DateTimeFormatter
```

{% hint style="info" %}
**`DateTimeFormatter`**

The `DateTimeFormatter` class is already part of the built-in whitelist.
{% endhint %}

{% hint style="danger" %}
**Security implications**

Exercise care when using classes or methods. In some cases, giving access to all methods of a class may allow access by transitivity to unwanted methods and may open potential security breaches.
{% endhint %}

## Compatibility matrix

The following is the compatibility matrix for APIM and the `groovy` policy:

<table data-full-width="false"><thead><tr><th>Plugin Version</th><th>Supported APIM versions</th></tr></thead><tbody><tr><td>2.x</td><td>All</td></tr></tbody></table>

## Errors

<table data-full-width="false"><thead><tr><th width="171">HTTP status code</th><th width="387">Message</th></tr></thead><tbody><tr><td><code>500</code></td><td>The Groovy script cannot be parsed/compiled or executed (mainly due to a syntax error)</td></tr></tbody></table>

## Changelogs

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-groovy/blob/master/CHANGELOG.md" %}
