= Groovy policy

ifdef::env-github[]
image:https://img.shields.io/static/v1?label=Available%20at&message=Gravitee.io&color=1EC9D2["Gravitee.io", link="https://download.gravitee.io/#graviteeio-apim/plugins/policies/gravitee-policy-groovy/"]
image:https://img.shields.io/badge/License-Apache%202.0-blue.svg["License", link="https://github.com/gravitee-io/gravitee-policy-groovy/blob/master/LICENSE.txt"]
image:https://img.shields.io/badge/semantic--release-conventional%20commits-e10079?logo=semantic-release["Releases", link="https://github.com/gravitee-io/gravitee-policy-groovy/releases"]
image:https://circleci.com/gh/gravitee-io/gravitee-policy-groovy.svg?style=svg["CircleCI", link="https://circleci.com/gh/gravitee-io/gravitee-policy-groovy"]
image:https://f.hubspotusercontent40.net/hubfs/7600448/gravitee-github-button.jpg["Join the community forum", link="https://community.gravitee.io?utm_source=readme", height=20]
endif::[]

== Phase

=== V3 engine

[cols="^2,^2,^2,^2",options="header"]
|===
|onRequest|onResponse|onRequestContent|onResponseContent

|X
|X
|X
|X
|===

=== V4 engine

[cols="4*", options="header"]
|===
^|onRequest
^|onResponse
^|onMessageRequest
^|onMessageResponse

^.^| X
^.^| X
^.^| X
^.^| X
|===

== Description

You can use the http://www.groovy-lang.org/[Groovy^] policy to run Groovy scripts at any stage of request processing through the gateway.

The following example Groovy script is executed during the OnResponse phase to change HTTP headers:

[source, groovy]
----
response.headers.remove 'X-Powered-By'
response.headers.'X-Gravitee-Gateway-Version' = '0.14.0'
----


== Compatibility with APIM

|===
|Plugin version | APIM version

|2.x            | All supported versions
|===

== Configuration

[source, json]
"groovy": {
    "onRequestScript": "request.headers.'X-Gravitee-Gateway' = '0.14.0'",
    "onResponseScript": "response.headers.remove 'X-Powered-By'",
    "onRequestContentScript": "" // Not executed if empty
    "onResponseContentScript": "" // Not executed if empty
}

== Usage and examples

=== onRequest / onResponse

Some variables are automatically bound to the Groovy script to allow users to use them and define the policy behavior.

[width="100%",cols="2,10",options="header"]
.List of groovy script variables
|===
| Name | Description

| `request` | Inbound HTTP request
| `response` | Outbound HTTP response
| `context` | `PolicyContext` used to access external components such as services and resources
| `result` | Groovy script result

|===

Request or response processing can be interrupted by setting the result state to `FAILURE`.
By default, it will throw a `500 - internal server error` but you can override this behavior with the following properties:
- `code`: An HTTP status code
- `error`: The error message
- `key`: The key of a response template

[source, groovy]
----
import io.gravitee.policy.groovy.PolicyResult.State

if (request.headers.containsKey('X-Gravitee-Break')) {
    result.key = 'RESPONSE_TEMPLATE_KEY';
    result.state = State.FAILURE;
    result.code = 500
    result.error = 'Stop request processing due to X-Gravitee-Break header'
} else {
    request.headers.'X-Groovy-Policy' = 'ok'
}
----

To customize the error sent by the policy:

[source, groovy]
----
import io.gravitee.policy.groovy.PolicyResult.State
result.key = 'RESPONSE_TEMPLATE_KEY';
result.state = State.FAILURE;
result.code = 400
result.error = '{"error":"My specific error message","code":"MY_ERROR_CODE"}'
result.contentType = 'application/json'
----

=== OnRequestContent / OnResponseContent

You can also transform request or response body content by applying a Groovy script on
the `OnRequestContent` phase or the `OnResponseContent` phase.

Please note that if you are using the V4 engine, a single script is defined. To override
the content of the request or response, `overrideContent`must be enabled in your configuration.

The following example shows you how to use the Groovy policy to transform JSON content:

==== Input body content
[source, json]
----
[
    {
        "age": 32,
        "firstname": "John",
        "lastname": "Doe"
    }
]
----

==== Groovy script
[source, groovy]
----
import groovy.json.JsonSlurper
import groovy.json.JsonOutput

def jsonSlurper = new JsonSlurper()
def content = jsonSlurper.parseText(response.content)
content[0].firstname = 'Hacked ' + content[0].firstname
content[0].country = 'US'
return JsonOutput.toJson(content)
----

==== Output body content
[source, json]
----
[
    {
        "age": 32,
        "firstname": "Hacked John",
        "lastname": "Doe",
        "country": "US"
    }
]
----

=== Overriding the content of a message

The content of a message can be accessed using the `message.content` property from your Groovy script.

==== Input message content
[source, json]
----
{
    "greeting": "Hello World !"
}
----

==== Groovy script
[source, groovy]
----
import groovy.json.JsonSlurper
import groovy.json.JsonOutput

def jsonSlurper = new JsonSlurper()
def content = jsonSlurper.parseText(message.content)
content.greeting = 'Hello Universe!'
return JsonOutput.toJson(content)
----

The content of a message can also be accessed directly:

 - as a base64 string with `message.contentAsBase64`
 - as an array of bytes with `message.contentAsByteArray`

== Errors

=== Sandbox

Groovy policy comes with a native sandbox feature allowing to safely run Groovy scripts. The sandbox is based on a
predefined list of allowed methods, fields, constructors, and annotations.

The complete whitelist can be found here : https://raw.githubusercontent.com/gravitee-io/gravitee-policy-groovy/master/src/main/resources/groovy-whitelist[gravitee groovy whitelist]

This whitelist should be enough for almost all possible use cases. If you have specific needs which are not allowed by the built-in whitelist, you can extend (or even replace) the list with your own declarations.
For that, you can configure the gravitee.yml by specifying:

 * `groovy.whitelist.mode`: `append` or `replace`. This allows you to just append some new whitelisted definitions to the built-in list or completely replace it. We recommend you to always choose `append` unless you absolutely know what you are doing.
 * `groovy.whitelist.list`: allows declaring other methods, constructors, fields or annotations to the whitelist.
 ** start with `method` to allow a specific method (complete signature).
 ** start with `class` to allow a complete class. All methods, constructors and fields of the class will then be accessible.
 ** start with `new` to allow a specific constructor (complete signature).
 ** start with `field` to allow access to a specific field of a class.
 ** start with `annotation` to allow use of a specific annotation.

Example:
[source, yaml]
groovy:
  whitelist:
    mode: append
    list:
        - method java.time.format.DateTimeFormatter ofLocalizedDate java.time.format.FormatStyle
        - class java.time.format.DateTimeFormatter

*Note*: the `DateTimeFormatter` class is already part of the build-in whitelist.

*WARNING*: be care when you allow use of classes or methods. In some cases, giving access to all methods of a classes may allow access by transitivity to unwanted methods and may open security breaches.

=== Policy configuration

=== V3 engine

[cols="^2,^2,^2,^2",options="header"]
|===
|onRequestScript|onResponseScript|onRequestContentScript|onResponseContentScript

|This script will be executed during the `onRequest` phase.
|This script will be executed during the `onResponse` phase.
|This script will be executed during the `onRequestContent` phase, meaning that you can access the content of the request.
|This script will be executed during the `onRequestContent` phase, meaning that you can access the content of the response.
|===

=== V4 engine

[cols="^2,^2", options="header"]
|===
^|script
^|overrideContent

^.^|This script will be executed regardless of the phase.
^.^|If set to true, the content of the request, response, or message will be overridden by the result of the script.
|===

=== HTTP status code

|===
|Code |Message

| ```500```
| The Groovy script cannot be parsed/compiled or executed (mainly due to a syntax error)

|===
