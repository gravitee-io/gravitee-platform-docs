= HTTP callout policy

ifdef::env-github[]
image:https://img.shields.io/static/v1?label=Available%20at&message=Gravitee.io&color=1EC9D2["Gravitee.io", link="https://download.gravitee.io/#graviteeio-apim/plugins/policies/gravitee-policy-callout-http/"]
image:https://img.shields.io/badge/License-Apache%202.0-blue.svg["License", link="https://github.com/gravitee-io/gravitee-policy-callout-http/blob/master/LICENSE.txt"]
image:https://img.shields.io/badge/semantic--release-conventional%20commits-e10079?logo=semantic-release["Releases", link="https://github.com/gravitee-io/gravitee-policy-callout-http/releases"]
image:https://circleci.com/gh/gravitee-io/gravitee-policy-callout-http.svg?style=svg["CircleCI", link="https://circleci.com/gh/gravitee-io/gravitee-policy-callout-http"]
endif::[]

== Phase

[cols="4*", options="header"]
|===
^|onRequest
^|onResponse
^|onRequestContent
^|onResponseContent

^.^| X
^.^| X
^.^| X
^.^| X

|===

== Description

You can use the `callout-http` policy to invoke an HTTP(S) URL and place a subset or all of the content in
one or more variables of the request execution context.

This can be useful if you need some data from an external service and want to inject it during request
processing.

The result of the callout is placed in a variable called `calloutResponse` and is only available during policy
execution. If no variable is configured the result of the callout is no longer available.

== Compatibility with APIM

|===
|Plugin version | APIM version

|4.x                            | 4.4.x to latest
|3.x                            | 4.0.x to 4.3.x
|2.x                            | 3.18.x to 3.20.x
|1.15.x and upper               | 3.15.x to 3.17.x
|1.13.x to 1.14.x               | 3.10.x to 3.14.x
|Up to 1.12.x                   | Up to 3.9.x
|===

== Configuration

|===
|Property |Required |Description |Type |Default

.^|method
^.^|X
|HTTP Method used to invoke URL
^.^|HTTP method
^.^|GET

.^|useSystemProxy
^.^|X
|Use the system proxy configured by your administrator
^.^|boolean
^.^|false

.^|url
^.^|X
|URL invoked by the HTTP client (support EL)
^.^|URL
^.^|-

.^|headers
^.^|X
|List of HTTP headers used to invoke the URL (support EL)
^.^|HTTP Headers
^.^|-

.^|body
^.^|X
|The body content send when calling the URL (support EL)
^.^|string
^.^|-

.^|fireAndForget
^.^|X
|Make the http call without expecting any response. When activating this mode, context variables and exit on error are useless.
^.^|boolean
^.^|false

.^|variables
^.^|X
|The variables to set in the execution context when retrieving content of HTTP call (support EL)
^.^|List of variables
^.^|-

.^|exitOnError
^.^|X
|Terminate the request if the error condition is true
^.^|boolean
^.^|false

.^|errorCondition
^.^|X
|The condition which will be verified to end the request (support EL)
^.^|string
^.^|{#calloutResponse.status >= 400 and #calloutResponse.status <= 599}

.^|errorStatusCode
^.^|X
|HTTP Status Code sent to the consumer if the condition is true
^.^|int
^.^|500

.^|errorContent
^.^|X
|The body response of the error if the condition is true (support EL)
^.^|string
^.^|-

|===

== Examples

[source, json]
----
"policy-http-callout": {
    "method": "GET",
    "url": "https://api.gravitee.io/echo",
    "headers": [ {
        "name": "X-Gravitee-Request-Id",
        "value": "{#request.id}"
    }],
    "variables": [{
        "name": "my-server",
        "value": "{#jsonPath(#calloutResponse.content, '$.headers.X-Forwarded-Server')}"
    }]
}
----

== System proxy

If the option `useSystemProxy` is checked, proxy information will be read from `JVM_OPTS` or from the `gravitee.yml` file if `JVM_OPTS` is not set.
The system properties are as follows:

|===
|Property |Required |Description

.^|system.proxy.host
^.^|X
|Proxy Hostname or IP

.^|system.proxy.port
^.^|X
|The proxy port

.^|system.proxy.type
^.^|X
|The type of proxy (HTTP, SOCK4, SOCK5)

.^|system.proxy.username
^.^|
|Username for proxy authentication if any

.^|system.proxy.password
^.^|
|Password for proxy authentication if any

|===

=== HTTP client proxy options

[source, yaml]
----
# global configuration of the http client
system:
  proxy:
    type: HTTP
    host: localhost
    port: 3128
    username: user
    password: secret
----

== Errors

=== Default error

|===
|Code |Message

.^| ```500```
| An error occurred while invoking URL

|===

=== Override errors

You can override the default response provided by the policy with the response templates feature. These templates must be defined at the API level with the APIM Console *Proxy > Response Templates* function.

The error keys sent by this policy are as follows:

[cols="2*", options="header"]
|===
^|Key
^|Parameters

.^|CALLOUT_EXIT_ON_ERROR
^.^|-

.^|CALLOUT_HTTP_ERROR
^.^|-

|===
