= Mock policy

ifdef::env-github[]
image:https://img.shields.io/static/v1?label=Available%20at&message=Gravitee.io&color=1EC9D2["Gravitee.io", link="https://download.gravitee.io/#graviteeio-apim/plugins/policies/gravitee-policy-mock/"]
image:https://img.shields.io/badge/License-Apache%202.0-blue.svg["License", link="https://github.com/gravitee-io/gravitee-policy-mock/blob/master/LICENSE.txt"]
image:https://img.shields.io/badge/semantic--release-conventional%20commits-e10079?logo=semantic-release["Releases", link="https://github.com/gravitee-io/gravitee-policy-mock/releases"]
image:https://circleci.com/gh/gravitee-io/gravitee-policy-mock.svg?style=svg["CircleCI", link="https://circleci.com/gh/gravitee-io/gravitee-policy-mock"]
endif::[]

== Phase

|===
|onRequest|onResponse

|X
|

|===

== Description

You can use the `mock` policy to create mock responses when a consumer calls one of your services.
This means you do not have to provide a functional backend as soon as you create your API, giving you more time to think about your API contract.

You can think of the policy as a contract-first approach -- you are able to create a fully-functional API without needing to write a single line of code to handle consumer calls.

Internally, this policy replaces the default HTTP invoker with a mock invoker. There are no more HTTP calls between
the gateway and a remote service or backend.

NOTE: The Mock policy will *not* cause the other policies to be skipped, regardless of its location in the flow.

When defining the response body content, you can use Expression Language to provide a dynamic mock response.

== Compatibility with APIM

|===
| Plugin version | APIM version
| Up to 1.13.5      | All
| From 1.14.0      | 4.1.24+
|===


== Examples

Note that you don't need to provide the `Content-Type` header, since the Mock policy can automatically detect the
content type.

=== Body content example (XML)

[source, xml]
----
<user id="{#request.paths[3]}">
    <firstname>{#properties['firstname_' + #request.paths[3]]}</firstname>
	<lastname>{#properties['lastname_' + #request.paths[3]]}</lastname>
	<age>{(T(java.lang.Math).random() * 60).intValue()}</age>
	<createdAt>{(new java.util.Date()).getTime()}</createdAt>
</user>
----

=== Body content example (JSON)

[source, json]
----
{
    "id": "{#request.paths[3]}",
    "firstname": "{#properties['firstname_' + #request.paths[3]]}",
    "lastname": "{#properties['lastname_' + #request.paths[3]]}",
    "age": {(T(java.lang.Math).random() * 60).intValue()},
    "createdAt": {(new java.util.Date()).getTime()}
}
----

== Configuration

You can configure the policy with the following options:

|===
|Property |Required |Description |Type |Default

|status|X|HTTP Status Code|integer|
|headers|X|HTTP Headers|Array of HTTP headers|
|content|X|HTTP Body content|string|

|===

=== Configuration example

[source, json]
----
"mock": {
    "status": "200",
    "headers": [
        {
            "name": "Content-Type",
            "value": "application/json"
        }, {
            "name": "Server",
            "value": "Gravitee.io"
        }
    ],
    "content": "<user id=\"{#request.paths[3]}\">\n\t<firstname>{#properties['firstname_' + #request.paths[3]]}</firstname>\n\t<lastname>{#properties['lastname_' + #request.paths[3]]}</lastname>\n\t<age>{(T(java.lang.Math).random() * 60).intValue()}</age>\n\t<createdAt>{(new java.util.Date()).getTime()}</createdAt>\n</user>"
}
----
