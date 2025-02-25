= Dynamic routing policy

ifdef::env-github[]
image:https://img.shields.io/static/v1?label=Available%20at&message=Gravitee.io&color=1EC9D2["Gravitee.io", link="https://download.gravitee.io/#graviteeio-apim/plugins/policies/gravitee-policy-dynamic-routing/"]
image:https://img.shields.io/badge/License-Apache%202.0-blue.svg["License", link="https://github.com/gravitee-io/gravitee-policy-dynamic-routing/blob/master/LICENSE.txt"]
image:https://img.shields.io/badge/semantic--release-conventional%20commits-e10079?logo=semantic-release["Releases", link="https://github.com/gravitee-io/gravitee-policy-dynamic-routing/releases"]
image:https://circleci.com/gh/gravitee-io/gravitee-policy-dynamic-routing.svg?style=svg["CircleCI", link="https://circleci.com/gh/gravitee-io/gravitee-policy-dynamic-routing"]
image:https://f.hubspotusercontent40.net/hubfs/7600448/gravitee-github-button.jpg["Join the community forum", link="https://community.gravitee.io?utm_source=readme", height=20]
endif::[]


== Phase

[cols="2*", options="header"]
|===
^|onRequest
^|onResponse

^.^| X
^.^|

|===

== Compatibility with APIM

|===
| Plugin version | APIM version

| Up to 1.x                   | All
|===


== Description
The `dynamic-routing` policy is used to dispatch inbound calls to different targets / endpoints or to rewrite URIs.

This policy is particularly useful for creating API _Mashups_.

Another typical use case is defining this kind of routing:

* Requests from `http://gateway/apis/store/12/info` are redirected to `http://backend_store12/info`
* Requests from `http://gateway/apis/store/45/info` are redirected to `http://backend_store45/info`


== Attributes

|===
|Name |Description

.^|request.endpoint
|The endpoint URL invoked by the gateway after dynamic routing

|===


== Configuration
You can configure multiple rules and their respective redirections relative to the
initial request path.

WARNING: When you define rules, it is important to remember that the API `context-path` must not be part of the rule's path.
For example, if your `context-path` is `/myapi` and your call is `/myapi/123`, if you want to select `123` the regular expression is `/(.*)` (don't forget the `/`).

=== Regular expressions

Using regular expressions can be very useful when you want to capture some parts of the initial request path and reuse
them to define the redirection.

For example, to capture the end of a path after `/v1/stores/`, the rule path is `/v1/stores/(.*)`. You can then use it
in the `redirect to` property: `\http://store_backend/stores/{#group[[0]]}`

You can also use named groups instead of indexed groups:
`/api/(?<version>v[0-9]+)/stores.*` => `\http://host1/products/api/{#groupName['version']}`

== Examples

[source, json]
----
"dynamic-routing": {
    "rules": [
        {
            "pattern": "/v1/stores/(.*)",
            "url": "http://host2/stores/{#group[0]}"
        }
    ]
}
----

You can also select endpoints configured for your API by name using expression language:

[source, json]
----
"dynamic-routing": {
    "rules": [
        {
            "pattern": "/v1/stores/(.*)",
            "url": "{#endpoints['default']}/{#group[0]}"
        }
    ]
}
----

== Errors

=== HTTP status code
|===
|Code |Message

.^| ```400```
| When no rules match the inbound request

|===
