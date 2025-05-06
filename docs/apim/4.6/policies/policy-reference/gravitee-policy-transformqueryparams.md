= Transform query parameters policy

ifdef::env-github[]
image:https://img.shields.io/static/v1?label=Available%20at&message=Gravitee.io&color=1EC9D2["Gravitee.io", link="https://download.gravitee.io/#graviteeio-apim/plugins/policies/gravitee-policy-transformqueryparams/"]
image:https://img.shields.io/badge/License-Apache%202.0-blue.svg["License", link="https://github.com/gravitee-io/gravitee-policy-transformqueryparams/blob/master/LICENSE.txt"]
image:https://img.shields.io/badge/semantic--release-conventional%20commits-e10079?logo=semantic-release["Releases", link="https://github.com/gravitee-io/gravitee-policy-transformqueryparams/releases"]
image:https://circleci.com/gh/gravitee-io/gravitee-policy-transformqueryparams.svg?style=svg["CircleCI", link="https://circleci.com/gh/gravitee-io/gravitee-policy-transformqueryparams"]
endif::[]

== Phase

[cols="2*", options="header"]
|===
^|onRequest
^|onResponse

^.^| X
^.^|

|===

== Description

You can use the `transformqueryparams` policy to override incoming HTTP request query parameters.
You can override the HTTP query parameters by:

* Clearing all existing query parameters
* Adding to or updating the list of query parameters
* Removing query parameters individually

You can also append a value to an existing query parameter.

The query parameter values of the incoming request are accessible via the `{#request.params['query_parameter_name']}` construct.

== Compatibility with APIM

|===
|Plugin version | APIM version

|Up to 1.6.x    | 3.x
|1.7.x          | 4.0 to latest
|===


== Examples
=== Add the ID of the incoming request to the outgoing request
[source,json]
----
"transform-queryparams": {
    "addQueryParameters": [
        {
            "name": "myParam",
            "value": "{#request.id}"
        }
    ]
}
----
`https://host:port/path?foo=bar` becomes `https://host:port/path?a=b&myParam=my-request-id`

=== Remove existing param and add a new one
[source, json]
----
"transform-queryparams": {
    "removeQueryParameters": [
        "foo"
    ],
    "addQueryParameters": [
        {
            "name": "myParam",
            "value": "myValue"
        }
    ]
}
----
`https://host:port/path?foo=bar&key=value` becomes `https://host:port/path?key=value&myParam=myValue`

=== Remove all existing params and add a new one
[source, json]
----
"transform-queryparams": {
    "clearAll": true,
    "addQueryParameters": [
        {
            "name": "myParam",
            "value": "myValue"
        }
    ]
}
----
`https://host:port/path?foo=bar&key=value` becomes `https://host:port/path?myParam=myValue`

=== Replace an existing param
[source, json]
----
"transform-queryparams": {
    "addQueryParameters": [
        {
            "name": "myParam",
            "value": "myNewValue"
        }
    ]
}
----
`https://host:port/path?myParam=myValue` becomes `https://host:port/path?myParam=myNewValue`

=== Append multiple values to an existing param
[source, json]
----
"transform-queryparams": {
    "addQueryParameters": [
        {
            "name": "foo",
            "value": "bar2",
            "appendToExistingArray": true
        },
        {
            "name": "foo",
            "value": "bar3",
            "appendToExistingArray": true
        }
    ]
}
----
`https://host:port/path?foo=bar` becomes `https://host:port/path?foo=bar&foo=bar2&foo=bar3`

=== Replace an existing param with an array
[source, json]
----
"transform-queryparams": {
    "addQueryParameters": [
        {
            "name": "foo",
            "value": "bar2",
            "appendToExistingArray": false
        },
        {
            "name": "foo",
            "value": "bar3",
            "appendToExistingArray": true
        }
    ]
}
----
`https://host:port/path?foo=bar` becomes `https://host:port/path?foo=bar2&foo=bar3`