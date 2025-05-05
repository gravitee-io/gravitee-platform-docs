= JSON validation policy

ifdef::env-github[]
image:https://img.shields.io/static/v1?label=Available%20at&message=Gravitee.io&color=1EC9D2["Gravitee.io", link="https://download.gravitee.io/#graviteeio-apim/plugins/policies/gravitee-policy-json-validation/"]
image:https://img.shields.io/badge/License-Apache%202.0-blue.svg["License", link="https://github.com/gravitee-io/gravitee-policy-json-validation/blob/master/LICENSE.txt"]
image:https://img.shields.io/badge/semantic--release-conventional%20commits-e10079?logo=semantic-release["Releases", link="https://github.com/gravitee-io/gravitee-policy-json-validation/releases"]
image:https://circleci.com/gh/gravitee-io/gravitee-policy-json-validation.svg?style=svg["CircleCI", link="https://circleci.com/gh/gravitee-io/gravitee-policy-json-validation"]
endif::[]

== Phase

=== V3 engine

[cols="2*", options="header"]
|===
^|onRequestContent
^|onResponseContent

^.^| X
^.^| X
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

You can use the `json-validation` policy to validate JSON payloads. This policy uses https://github.com/java-json-tools/json-schema-validator[JSON Schema Validator^].
It returns 400 BAD REQUEST when request validation fails and 500 INTERNAL ERROR when response validation fails, with a custom error message body.
It can inject processing report messages into request metrics for analytics.

== Compatibility with APIM

|===
| Plugin version | APIM version
| 1.x            | 4.5 and lower
| 2.x            | 4.6 and greater
|===

== Configuration

|===
|Property |Required |Description |Type| Default

.^|scope
^.^|X
|Policy scope from where the policy is executed
^.^|Policy scope
|REQUEST_CONTENT

.^|errorMessage
^.^|X
|Custom error message in JSON format. Spel is allowed.
^.^|string
|{"error":"Bad request"}

.^|schema
^.^|X
|Json schema.
^.^|string
|

.^|deepCheck
^.^|
|Validate descendant even if JSON parent container is invalid
^.^|boolean
^.^|false

.^|validateUnchecked
^.^|
|Unchecked validation means that conditions which would normally cause the processing to stop with an exception are instead inserted into the resulting report. Warning: this means that anomalous events like an unresolvable JSON Reference, or an invalid schema, are masked!.
^.^|boolean
^.^|false

.^|straightRespondMode
^.^|
|Only for RESPONSE scope. Straight respond mode means that responses failed to validate still will be sent to user without replacement. Validation failures messages are still being written to the metrics for further inspection.
^.^|boolean
^.^|false

|===

== Errors

== HTTP status code

|===
|Code |Message

.^| `400`(Request scope)

`500`(Response scope)

| Sent in the following cases:

* Invalid payload

* Invalid JSON schema

* Invalid error message JSON format

|===

== Errors

You can use the response template feature to override the default response provided by the policy. These templates must be defined at the API level (see the API Console *Response Templates*
option in the API *Proxy* menu).

The policy sends the following error keys:

[cols="2*", options="header"]
|===
^|Key
^|Parameters

.^|JSON_INVALID_PAYLOAD
^.^|-

.^|JSON_INVALID_FORMAT
^.^|-

.^|JSON_INVALID_RESPONSE_PAYLOAD
^.^|-

.^|JSON_INVALID_RESPONSE_FORMAT
^.^|-

|===
