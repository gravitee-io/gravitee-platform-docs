= XML to JSON transformation policy

ifdef::env-github[]
image:https://img.shields.io/static/v1?label=Available%20at&message=Gravitee.io&color=1EC9D2["Gravitee.io",link="https://download.gravitee.io/#graviteeio-apim/plugins/policies/gravitee-policy-xml-json/"]
image:https://img.shields.io/badge/License-Apache%202.0-blue.svg["License",link="https://github.com/gravitee-io/gravitee-policy-xml-json/blob/master/LICENSE.txt"]
image:https://img.shields.io/badge/semantic--release-conventional%20commits-e10079?logo=semantic-release["Releases",link="https://github.com/gravitee-io/gravitee-policy-xml-json/releases"]
image:https://circleci.com/gh/gravitee-io/gravitee-policy-xml-json.svg?style=svg["CircleCI",link="https://circleci.com/gh/gravitee-io/gravitee-policy-xml-json"]
endif::[]

== Compatibility matrix

|===
|Plugin version | APIM version

|1.x            | 3.x
|2.x            | 4.0 to latest
|===

== Phase

[cols="2*",options="header"]
|===
^|onRequestContent
^|onResponseContent

^.^| X
^.^| X

|===

== Description

You can use the `xml-json` policy to transform XML content to JSON content.

== Configuration

You can configure the policy with the following options:

|===
|Property |Required |Description |Type |Default

.^|scope
^.^|X
|The execution scope (`request` or `response`).
^.^|string
^.^|`RESPONSE`

|===

== Example

[source,json]
----
"xml-json": {
    "scope": "RESPONSE"
}
----

== Errors

=== HTTP status code

|===
|Code |Message

.^| ```500```
| The transformation cannot be executed properly

|===

=== Nested objects

To limit the processing time and memory consumption in case of nested object, a default max depth of nested object has been defined to 100. This default value can be overridden using the environment variable `gravitee_policy_xmljson_maxdepth`.