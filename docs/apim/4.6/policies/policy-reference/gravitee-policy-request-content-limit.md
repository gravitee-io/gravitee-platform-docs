= Request content limit policy

ifdef::env-github[]
image:https://img.shields.io/static/v1?label=Available%20at&message=Gravitee.io&color=1EC9D2["Gravitee.io", link="https://download.gravitee.io/#graviteeio-apim/plugins/policies/gravitee-policy-request-content-limit/"]
image:https://img.shields.io/badge/License-Apache%202.0-blue.svg["License", link="https://github.com/gravitee-io/gravitee-policy-request-content-limit/blob/master/LICENSE.txt"]
image:https://img.shields.io/badge/semantic--release-conventional%20commits-e10079?logo=semantic-release["Releases", link="https://github.com/gravitee-io/gravitee-policy-request-content-limit/releases"]
image:https://circleci.com/gh/gravitee-io/gravitee-policy-request-content-limit.svg?style=svg["CircleCI", link="https://circleci.com/gh/gravitee-io/gravitee-policy-request-content-limit"]
endif::[]

== Phase

|===
|onRequest |onResponse
|X|
|===

== Description

You can use the `request-content-limit` policy to specify a maximum request content length allowed.
This limit is compared to the content length header of the request.

== Compatibility with APIM

|===
| Plugin version | APIM version
| 1.x            | All supported versions
|===

== Configuration

You can configure the policy with the following options:

|===
|Property |Required |Description |Type

|limit
|true
|Maximum length of request content allowed
|int

|===


[source, json]
.Sample
----
"request-content-limit": {
  "limit": 1000
}
----

== Errors

=== Default errors
|===
|Code |Message

.^| ```400```
| The limit from the configuration is not correct.

.^| ```413```
| Incoming HTTP request payload exceed the size limit.

.^| ```411```
| The HTTP request is not chunked and does not specify the `Content-Length` header.

|===

=== Default response override

You can use the response template feature to override the default responses provided by the policy. These templates must be defined at the API level (see the API Console *Response Templates*
option in the API *Proxy* menu).

Some possible responses are:

|===
|Error |description
|400|Content-length is not a valid integer.
|411|The request did not specify the length of its content, which is required by the requested resource.
|413|The request is larger than the server is willing or able to process.
|===

=== Error keys

The error keys sent by this policy are as follows:

[cols="2*", options="header"]
|===
^|Key
^|Parameters

.^|REQUEST_CONTENT_LIMIT_TOO_LARGE
^.^|length - limit

.^|REQUEST_CONTENT_LIMIT_LENGTH_REQUIRED
^.^|limit

|===
