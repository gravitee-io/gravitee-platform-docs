= Assign attributes policy

ifdef::env-github[]
image:https://img.shields.io/static/v1?label=Available%20at&message=Gravitee.io&color=1EC9D2["Gravitee.io", link="https://download.gravitee.io/#graviteeio-apim/plugins/policies/gravitee-policy-assign-attributes/"]
image:https://img.shields.io/badge/License-Apache%202.0-blue.svg["License", link="https://github.com/gravitee-io/gravitee-policy-assign-attributes/blob/master/LICENSE.txt"]
image:https://img.shields.io/badge/semantic--release-conventional%20commits-e10079?logo=semantic-release["Releases", link="https://github.com/gravitee-io/gravitee-policy-assign-attributes/releases"]
image:https://circleci.com/gh/gravitee-io/gravitee-policy-assign-attributes.svg?style=svg["CircleCI", link="https://circleci.com/gh/gravitee-io/gravitee-policy-assign-attributes"]
endif::[]

== Phases

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

You can use the `assign-attributes` policy to set variables such as request attributes, message attributes and other execution context attributes.

#When you are using this policy on the message request or response, the attribute will be available in the message attribute list and not on the context one.#

You can use it to retrieve initial request attributes after `Transform headers` or `Transform query parameters` policies and reuse them in other policies (`Dynamic routing`, for example).

== Compatibility with APIM

|===
| Plugin version | APIM version

| Up to 1.x                   | All
| From 2.x                   | 4.0+
|===

== Configuration

You can configure the policy with the following options:

.Configuration
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

.^|attributes
^.^|X
.^|List of attributes
^.^|See <<attribute-table>>
|

|===

[#attribute-table]
.Attribute
[cols="5*", options=header]
|===
^| Property
^| Required
^| Description
^| Type
^| Default

|name
^.^|X
|attribute name
|string
|

|value
^.^|X
|attribute value (can be EL)
|string
|

|===


== Examples

=== Request header

Let's say we want to inject request attributes into the context attributes.


[source]
----
"assign-attributes": {
    "attributes": [
        {
            "name": "initialContentTypeHeader,
            "value": "{#request.headers['Content-Type']}"
        },
        {
            "name": "initialFooParamHeader,
            "value": "{#request.params['foo']}"
        }
    ]
}
----

To extract the request attributes you can use the following syntax:

Get the content-type header:

----
{#context.attributes['initialContentTypeHeader']}
----

Get the foo query param:

----
{#context.attributes['initialFooParamHeader']}
----

=== Request objects

You can also be more general and put complex objects into the context attributes:

[source]
----
"assign-attributes": {
    "attributes": [
        {
            "name": "initialRequest,
            "value": "{#request}"
        }
    ]
}
----

To extract the request attributes you can use the following syntax:

Get the content-type header:

----
{#context.attributes['initialRequest'].headers['content-type']}
----

Get the foo query param:

----
{#context.attributes['initialRequest'].params['foo']}
----

=== Message

You can use for example the content of a message:

[source]
----
"assign-attributes": {
    "attributes": [
        {
            "name": "messageContent,
            "value": "{#message.content}"
        }
    ]
}
----



== Errors

=== HTTP status code

|===
|Code |Message

.^| ```500```
| An error occurred while setting request attributes in the execution context

|===
