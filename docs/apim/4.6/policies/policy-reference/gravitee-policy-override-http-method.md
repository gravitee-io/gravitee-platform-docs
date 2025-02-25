= Override HTTP method policy

ifdef::env-github[]
image:https://img.shields.io/static/v1?label=Available%20at&message=Gravitee.io&color=1EC9D2["Gravitee.io", link="https://download.gravitee.io/#graviteeio-apim/plugins/policies/gravitee-policy-override-http-method/"]
image:https://img.shields.io/badge/License-Apache%202.0-blue.svg["License", link="https://github.com/gravitee-io/gravitee-policy-override-http-method/blob/master/LICENSE.txt"]
image:https://img.shields.io/badge/semantic--release-conventional%20commits-e10079?logo=semantic-release["Releases", link="https://github.com/gravitee-io/gravitee-policy-override-http-method/releases"]
image:https://circleci.com/gh/gravitee-io/gravitee-policy-override-http-method.svg?style=svg["CircleCI", link="https://circleci.com/gh/gravitee-io/gravitee-policy-override-http-method"]
endif::[]

== Phase

=== V3 engine

[cols="2*", options="header"]
|===
^|onRequest
^|onResponse

^.^| X
^.^|

|===

=== V4 engine

[cols="4*", options="header"]
|===
^|onRequest
^|onResponse
^|onMessageRequest
^|onMessageResponse

^.^| X
^.^|
^.^|
^.^|
|===

== Description

You can use the `override-http-method` policy to override the HTTP method provided by the initial consumer with a new
configured value when the inbound request is sent to the backend API.

== Compatibility with APIM

|===
|Plugin version | APIM version

| Up to 1.x                  | Up to 3.20
| Up to 2.1                  | 4.0 to latest
|===

== Configuration

|===
|Property |Required |Description |Type| Default

.^|method
^.^|X
|HTTP method sent to the backend API
^.^|HTTP method
^.^|GET

|===
