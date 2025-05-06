= Custom Query Parameters Parser policy

ifdef::env-github[]
image:https://img.shields.io/static/v1?label=Available%20at&message=Gravitee.io&color=1EC9D2["Gravitee.io", link="https://download.gravitee.io/#graviteeio-apim/plugins/policies/gravitee-policy-custom-query-parameters-parser/"]
image:https://img.shields.io/badge/License-Apache%202.0-blue.svg["License", link="https://github.com/gravitee-io/gravitee-policy-custom-query-parameters-parser/blob/master/LICENSE.txt"]
image:https://img.shields.io/badge/semantic--release-conventional%20commits-e10079?logo=semantic-release["Releases", link="https://github.com/gravitee-io/gravitee-policy-custom-query-parameters-parser/releases"]
endif::[]

== Phase

[cols="^2,^2,^2,^2",options="header"]
|===
|onRequest|onResponse|onRequestContent|onResponseContent

|X
|
|
|

|===

== Description

You can use the `custom-query-parameters-parser` policy to set variables such as request attributes and other execution context attributes.

You can use it to change the way query parameters are extracted.

Semicolon character (`;`) is not considered as a separator:

`http://host:port/my-api?filter=field1;field2` will be computed with this query param: `filter: ['field1;field']`

WARNING: Policies are executed after flow evaluation: for a condition on a flow using Expression Language to test query parameters, they will be extracted the regular way by the Gateway, with `;` as a separator.

== Compatibility with APIM

|===
| Plugin version | APIM version

| Up to 1.x         | 3.20.x
| 2.x               | 4.0.x to latest
|===

== Errors

=== HTTP status code

|===
|Code |Message

.^| ```500```
| An error occurred while extracting query parameters from request url.

|===
