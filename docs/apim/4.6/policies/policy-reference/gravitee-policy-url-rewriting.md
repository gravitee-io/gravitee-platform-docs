= URL rewriting policy

ifdef::env-github[]
image:https://img.shields.io/static/v1?label=Available%20at&message=Gravitee.io&color=1EC9D2["Gravitee.io", link="https://download.gravitee.io/#graviteeio-apim/plugins/policies/gravitee-policy-url-rewriting/"]
image:https://img.shields.io/badge/License-Apache%202.0-blue.svg["License", link="https://github.com/gravitee-io/gravitee-policy-url-rewriting/blob/master/LICENSE.txt"]
image:https://img.shields.io/badge/semantic--release-conventional%20commits-e10079?logo=semantic-release["Releases", link="https://github.com/gravitee-io/gravitee-policy-url-rewriting/releases"]
image:https://circleci.com/gh/gravitee-io/gravitee-policy-url-rewriting.svg?style=svg["CircleCI", link="https://circleci.com/gh/gravitee-io/gravitee-policy-url-rewriting"]
endif::[]

== Phase

[cols="^2,^2,^2,^2",options="header"]
|===
|onRequest|onResponse|onRequestContent|onResponseContent

|-
|X
|-
|X

|===

== Description

You can use the `url-rewriting` policy to rewrite URLs from an HTTP response header or response body.

== Compatibility with APIM

|===
| Plugin version | APIM version
| 1.x            | All supported versions
|===


== Configuration

|===
|Property |Required |Description |Type |Default

.^|rewriteResponseHeaders
^.^|X
|Rewrite the value of HTTP response headers
^.^|boolean
^.^|true

.^|rewriteResponseBody
^.^|X
|Rewrite the HTTP response body
^.^|boolean
^.^|true

.^|fromRegex
^.^|X
|The regex pattern for matching URLs
^.^|string (regex)
^.^|true

.^|toReplacement
^.^|X
|The value used to replace matching URLs (supports Expression Language)
^.^|string
^.^|true

|===

== Example

[source, json]
----
"url-rewriting": {
    "rewriteResponseHeaders": true,
    "rewriteResponseBody": true,
    "fromRegex": "https?://[^\/]*\/((?>\w|\d|\-|\/|\?|\=|\&)*)",
    "toReplacement": "https://apis.gravitee.io/{#group[0]}"
}
----
