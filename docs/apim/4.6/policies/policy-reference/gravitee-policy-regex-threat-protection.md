= Regex threat protection policy

ifdef::env-github[]
image:https://img.shields.io/static/v1?label=Available%20at&message=Gravitee.io&color=1EC9D2["Gravitee.io", link="https://download.gravitee.io/#graviteeio-apim/plugins/policies/gravitee-policy-regex-threat-protection/"]
image:https://img.shields.io/badge/License-Apache%202.0-blue.svg["License", link="https://github.com/gravitee-io/gravitee-policy-regex-threat-protection/blob/master/LICENSE.txt"]
image:https://img.shields.io/badge/semantic--release-conventional%20commits-e10079?logo=semantic-release["Releases", link="https://github.com/gravitee-io/gravitee-policy-regex-threat-protection/releases"]
image:https://circleci.com/gh/gravitee-io/gravitee-policy-regex-threat-protection.svg?style=svg["CircleCI", link="https://circleci.com/gh/gravitee-io/gravitee-policy-regex-threat-protection"]
endif::[]

== Phase

[cols="2*", options="header"]
|===
^|onRequest
^|onRequestContent
^.^| X
^.^| X

|===

== Description

You can use the `regex-threat-protection` to extract information from a request (headers, path, query parameters, body payload) and evaluate that content against pre-defined regular expressions.
If any content matches the specified regular expression, the request is considered a threat and rejected with a 400 BAD REQUEST.
The policy injects processing report messages into request metrics for analytics.

== Compatibility with APIM

|===
| Plugin version | APIM version
| 1.x            | All supported versions
|===

== Configuration

|===
|Property |Required |Description |Type| Default

.^|regex
^.^|X
|Regex used to detect malicious injections. You can enable this regular expression on headers, path and body or add multiple Regex threat protection policies with different regex, depending on your needs.
^.^|string
|

.^|caseSensitive
^.^|
|Perform case-sensitive matching. *WARNING*: Use with caution. Enabling case sensitive matching may miss some risky patterns such as ```DrOp TaBlE```.
^.^|boolean
^.^|false

.^|checkHeaders
^.^|
|Evaluate regex on request headers
^.^|boolean
^.^|true

.^|checkPath
^.^|
|Evaluate regex on request path and query parameters
^.^|boolean
^.^|true

.^|checkBody
^.^|
|Evaluate regex on request body content
^.^|boolean
^.^|true

|===

== Errors

=== HTTP status code

|===
|Code |Message

.^| ```400```

a| Applies to:

* Matching request headers
* Matching request path or query parameters
* Matching request body

|===

=== Default response override

You can use the response template feature to override the default response provided by the policy. These templates must be defined at the API level (see the API Console *Response Templates*
option in the API *Proxy* menu).

=== Error keys

The error keys sent by this policy are as follows:

[cols="2*", options="header"]
|===
^|Key
^|Parameters

.^|HEADER_THREAT_DETECTED
^.^|-

.^|PATH_THREAT_DETECTED
^.^|-

.^|BODY_THREAT_DETECTED
^.^|-

|===
