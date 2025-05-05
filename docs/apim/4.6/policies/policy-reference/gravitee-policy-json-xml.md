= JSON to XML transformation policy

ifdef::env-github[]
image:https://img.shields.io/static/v1?label=Available%20at&message=Gravitee.io&color=1EC9D2["Gravitee.io", link="https://download.gravitee.io/#graviteeio-apim/plugins/policies/gravitee-policy-json-xml/"]
image:https://img.shields.io/badge/License-Apache%202.0-blue.svg["License", link="https://github.com/gravitee-io/gravitee-policy-json-xml/blob/master/LICENSE.txt"]
image:https://img.shields.io/badge/semantic--release-conventional%20commits-e10079?logo=semantic-release["Releases", link="https://github.com/gravitee-io/gravitee-policy-json-xml/releases"]
image:https://circleci.com/gh/gravitee-io/gravitee-policy-json-xml.svg?style=svg["CircleCI", link="https://circleci.com/gh/gravitee-io/gravitee-policy-json-xml"]
image:https://f.hubspotusercontent40.net/hubfs/7600448/gravitee-github-button.jpg["Join the community forum", link="https://community.gravitee.io?utm_source=readme", height=20]
endif::[]

== Phases

=== V3 engine

[cols="2*", options="header"]
|===
^|onRequestContent
^|onResponseContent

^.^| X
^.^| X

|===

=== Jupiter engine

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

== Compatibility with APIM

|===
| Plugin version | APIM version
| 1.x            | 3.x
| 3.x            | 4.x to latest

|===

== Description

You can use the `json-xml` policy to transform JSON content to XML content.

== Configuration

You can configure the policy with the following options:

|===
|Property |Required |Description |Type |Default

.^|scope _(deprecated, v3 only)_
^.^|X
|The execution scope (`request` or `response`).
^.^|string
^.^|`REQUEST`
.^|rootElement
^.^|X
|Root element name that's enclose content.
^.^|string
^.^|`root`

|===

== Example

[source, json]
----
"json-xml": {
    "scope": "RESPONSE",
    "rootElement": "root"
}
----

== Errors

=== V3 engine

|===
|Code | Description

.^| ```500```
| The transformation cannot be executed properly

|===

=== Jupiter engine

|===
|Phase | Code | Error template key | Description

.^| onRequest
| ```400```
| JSON_INVALID_PAYLOAD
| Request payload cannot be transformed properly to XML
.^| onResponse
| ```500```
| JSON_INVALID_PAYLOAD
| Response payload cannot be transformed properly to XML
.^| onMessageRequest
| ```400```
| JSON_INVALID_MESSAGE_PAYLOAD
| Incoming message cannot be transformed properly to XML
.^| onMessageResponse
| ```500```
| JSON_INVALID_MESSAGE_PAYLOAD
| Outgoing message cannot be transformed properly to XML

|===

=== Nested objects

To limit the processing time in case of nested object, a default max depth of nested object has been defined to 100. This default value can be overriden using the environment variable `gravitee_policy_jsonxml_maxdepth`.
