= Latency policy

ifdef::env-github[]
image:https://img.shields.io/static/v1?label=Available%20at&message=Gravitee.io&color=1EC9D2["Gravitee.io", link="https://download.gravitee.io/#graviteeio-apim/plugins/policies/gravitee-policy-latency/"]
image:https://img.shields.io/badge/License-Apache%202.0-blue.svg["License", link="https://github.com/gravitee-io/gravitee-policy-latency/blob/master/LICENSE.txt"]
image:https://img.shields.io/badge/semantic--release-conventional%20commits-e10079?logo=semantic-release["Releases", link="https://github.com/gravitee-io/gravitee-policy-latency/releases"]
image:https://circleci.com/gh/gravitee-io/gravitee-policy-latency.svg?style=svg["CircleCI", link="https://circleci.com/gh/gravitee-io/gravitee-policy-latency"]
endif::[]

== Compatibility with APIM

|===
|Plugin version | APIM version

| Up to 1.3.x   | Up to 3.9.x
| 1.4.x         | Up to 3.20
| 2.x           | 4.x to latest
|===

=== V3 engine

[cols="4*", options="header"]
|===
^|onRequest
^|onResponse
^|onRequestContent
^|onResponseContent

^.^| X
^.^|
^.^|
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
^.^| X
^.^| X
|===

== Description

You can use the latency policy to add latency to either the request or the response. So for example, if you configure the policy on the request with a latency of 100ms, the gateway waits 100ms before routing the request to the backend service.

This policy is particularly useful in two scenarios:

* Testing: adding latency allows you to test client applications when APIs are slow to respond.
* Monetization: a longer latency can be added to free plans to encourage clients to move to a better (or paid) plan.

|===

== Configuration

You can configure the policy with the following options:

|===
|Property |Required |Description |Type| Default

.^|time
^.^|
|Time to wait (`ms`)
^.^|integer
^.^|`100`

.^|timeUnit
^.^|
|Time unit ( `"MILLISECONDS"` or `"SECONDS"`) 
^.^|string
^.^|`"MILLISECONDS"`

|===

== Errors

== HTTP status code

|===
|Code |Message

.^| ```500```
| Server error

|===
