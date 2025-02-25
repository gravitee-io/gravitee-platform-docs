= Transform headers policy

ifdef::env-github[]
image:https://img.shields.io/static/v1?label=Available%20at&message=Gravitee.io&color=1EC9D2["Gravitee.io", link="https://download.gravitee.io/#graviteeio-apim/plugins/policies/gravitee-policy-transformheaders/"]
image:https://img.shields.io/badge/License-Apache%202.0-blue.svg["License", link="https://github.com/gravitee-io/gravitee-policy-transformheaders/blob/master/LICENSE.txt"]
image:https://img.shields.io/badge/semantic--release-conventional%20commits-e10079?logo=semantic-release["Releases", link="https://github.com/gravitee-io/gravitee-policy-transformheaders/releases"]
image:https://circleci.com/gh/gravitee-io/gravitee-policy-transformheaders.svg?style=svg["CircleCI", link="https://circleci.com/gh/gravitee-io/gravitee-policy-transformheaders"]
endif::[]

== Compatibility matrix

|===
|Plugin version | APIM version

|1.x            | 3.x
|3.x            | 4.0 to latest

|===

== Phase

[cols="4*", options="header"]
|===
^|onRequest
^|onResponse
^|onRequestContent
^|onResponseContent

^.^| X
^.^| X
^.^| X
^.^| X

|===

== Description

You can use the `transformheaders` policy to override HTTP headers in incoming requests or outbound responses.
You can override the HTTP headers by:

* Adding to or updating the list of headers
* Removing headers individually
* Defining a whitelist

== Example

[source, json]
----
"transform-headers": {
    "addHeaders": [
        {
            "name": "X-Gravitee-Request-Id",
            "value": "{#request.id}"
        }
    ],
    "removeHeaders": [
        "X-Gravitee-TransactionId"
    ],
    "whitelistHeaders": [
        "Content-Type",
        "Content-Length"
    ],
    "scope": "REQUEST"
}
----

Add a header from the request's payload:

[source, json]
----
"transform-headers": {
    "addHeaders": [
        {
            "name": "X-Product-Id",
            "value": "{#jsonPath(#request.content, '$.product.id')}"
        }
    ]
    "scope": "REQUEST_CONTENT"
}
----
