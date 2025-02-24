= Resource filtering policy

ifdef::env-github[]
image:https://img.shields.io/static/v1?label=Available%20at&message=Gravitee.io&color=1EC9D2["Gravitee.io", link="https://download.gravitee.io/#graviteeio-apim/plugins/policies/gravitee-policy-resource-filtering/"]
image:https://img.shields.io/badge/License-Apache%202.0-blue.svg["License", link="https://github.com/gravitee-io/gravitee-policy-resource-filtering/blob/master/LICENSE.txt"]
image:https://img.shields.io/badge/semantic--release-conventional%20commits-e10079?logo=semantic-release["Releases", link="https://github.com/gravitee-io/gravitee-policy-resource-filtering/releases"]
image:https://circleci.com/gh/gravitee-io/gravitee-policy-resource-filtering.svg?style=svg["CircleCI", link="https://circleci.com/gh/gravitee-io/gravitee-policy-resource-filtering"]
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

You can use the `resource-filtering` policy to filter REST resources. By applying this filter, you can restrict or allow access to
 a specific resource determined by a path and a method (or an array of methods).

This policy is mainly used in plan configuration, to limit subscriber access to specific resources only.

A typical usage would be to allow access to all paths (`/**`) but in read-only mode (GET method).

WARNING: You can't apply whitelisting and blacklisting to the same resource. Whitelisting takes precedence over blacklisting.

== Compatibility with APIM

|===
| Plugin version | APIM version
| 1.x            | All supported versions
|===

== Configuration

|===
|Property |Required |Description |Type| Default

.^|whitelist
^.^|-
|List of allowed resources
^.^|array of <<gravitee-policy-resource-filtering-resource, `resources`>>
^.^|-

.^|blacklist
^.^|-
|List of restricted resources
^.^|array of <<gravitee-policy-resource-filtering-resource, `resources`>>
^.^|-

|===

[[gravitee-policy-resource-filtering-resource]]
A resource is defined as follows:
|===
|Property |Required |Description |Type| Default

.^|pattern
^.^|X
|An <<gravitee-policy-resource-filtering-ant, Ant-style path patterns>> (http://ant.apache.org/[Apache Ant]).
^.^|string
^.^|-

.^|methods
^.^|-
|List of HTTP methods for which filter is applied.
^.^|array of HTTP methods
^.^|All HTTP methods

|===

=== Configuration example

[source, json]
"resource-filtering" : {
    "whitelist":[
        {
            "pattern":"/**",
            "methods": ["GET"]
        }
    ]
}

[[gravitee-policy-resource-filtering-ant]]
==== Ant style path pattern
URL mapping matches URLs using the following rules:

* `?` matches one character
* `*` matches zero or more characters
* `**` matches zero or more directories in a path

== Errors

=== HTTP status codes

|===
|Code |Message

.^| ```403```
| Access to the resource is forbidden according to resource-filtering rules

.^| ```405```
| Method not allowed while accessing this resource

|===

=== Default response override

You can use the response template feature to override the default responses provided by the policy. These templates must be defined at the API level (see the API Console *Response Templates*
option in the API *Proxy* menu).

=== Error keys

The error keys sent by this policy are as follows:

[cols="2*", options="header"]
|===
^|Key
^|Parameters

.^|RESOURCE_FILTERING_FORBIDDEN
^.^|path - method

.^|RESOURCE_FILTERING_METHOD_NOT_ALLOWED
^.^|path - method
|===
