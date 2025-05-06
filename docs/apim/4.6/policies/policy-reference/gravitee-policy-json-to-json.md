= JSON to JSON transformation policy

ifdef::env-github[]
image:https://img.shields.io/static/v1?label=Available%20at&message=Gravitee.io&color=1EC9D2["Gravitee.io", link="https://download.gravitee.io/#graviteeio-apim/plugins/policies/gravitee-policy-json-to-json/"]
image:https://img.shields.io/badge/License-Apache%202.0-blue.svg["License", link="https://github.com/gravitee-io/gravitee-policy-json-to-json/blob/master/LICENSE.txt"]
image:https://img.shields.io/badge/semantic--release-conventional%20commits-e10079?logo=semantic-release["Releases", link="https://github.com/gravitee-io/gravitee-policy-json-to-json/releases"]
image:https://circleci.com/gh/gravitee-io/gravitee-policy-json-to-json.svg?style=svg["CircleCI", link="https://circleci.com/gh/gravitee-io/gravitee-policy-json-to-json"]
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

You can use the `json-to-json` policy to apply a transformation (or mapping) on the request and/or response and/or
message content.

This policy is based on the https://github.com/bazaarvoice/jolt[JOLT^] library.

In APIM, you need to provide the JOLT specification in the policy configuration.

NOTE: You can use APIM EL in the JOLT specification.

At request/response level, the policy will do nothing if the processed request/response does not contain JSON. This
policy checks the `Content-Type` header before applying any transformation.

At message level, the policy will do nothing if the processed message has no content. It means that the message will be
re-emitted as is.


== Compatibility with APIM

|===
| Plugin version | APIM version
| 1.x            | Up to 3.19.x
| 2.x            | 3.20.x
| 3.x            | 4.x to latest

|===

== Configuration

You can configure the policy with the following options:

[cols="5*", options=header]
|===
^| Property
^| Required
^| Description
^| Type
^| Default

.^|scope
^.^| only for v3 engine
.^|The execution scope (`request` or `response`)
^.^|string
^.^|`REQUEST`

.^|specification
^.^|X
.^|The http://jolt-demo.appspot.com/[JOLT^] specification to apply on a given content.

Can contains EL.
^.^|string
|

.^|overrideContentType
^.^|
.^|Override the Content-Type to `application/json`.
^.^|string
^.^|`true`

|===

Example configuration:

[source, json]
----
{
    "json-to-json": {
        "scope": "REQUEST",
        "specification": "[{ \"operation\": \"shift\", \"spec\": { \"_id\": \"id\", \"*\": { \"$\": \"&1\" } } }, { \"operation\": \"remove\", \"spec\": { \"__v\": \"\" } }]"
    }
}
----

== Examples

For this input:

[source, json]
.Input
----
{
    "_id": "57762dc6ab7d620000000001",
    "name": "name",
    "__v": 0
}
----

And this JOLT specification:

[source, json]
----
[
  {
    "operation": "shift",
    "spec": {
      "_id": "id",
      "*": {
        "$": "&1"
      }
    }
  },
  {
    "operation": "remove",
    "spec": {
      "__v": ""
    }
  }
]
----

The output is as follows:

[source, json]
----
{
    "id": "57762dc6ab7d620000000001",
    "name": "name"
}
----

== Errors

=== V3 engine

|===
|Code |Message

.^| ```500```
.^| Bad specification file or transformation cannot be executed properly

|===

=== V4 engine

|===
|Phase | Code | Error template key | Description

.^| *
.^| ```500```
.^| INVALID_JSON_TRANSFORMATION
.^| Unable to apply JOLT transformation to payload

|===
