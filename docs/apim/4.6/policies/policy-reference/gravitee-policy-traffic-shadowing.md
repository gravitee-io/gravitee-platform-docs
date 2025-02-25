= Traffic Shadowing

ifdef::env-github[]
image:https://img.shields.io/static/v1?label=Available%20at&message=Gravitee.io&color=1EC9D2["Gravitee.io", link="https://download.gravitee.io/#graviteeio-apim/plugins/policies/gravitee-policy-traffic-shadowing/"]
image:https://img.shields.io/badge/License-Apache%202.0-blue.svg["License", link="https://github.com/gravitee-io/gravitee-policy-traffic-shadowing/blob/master/LICENSE.txt"]
image:https://img.shields.io/badge/semantic--release-conventional%20commits-e10079?logo=semantic-release["Releases", link="https://github.com/gravitee-io/gravitee-policy-traffic-shadowing/releases"]
image:https://circleci.com/gh/gravitee-io/gravitee-policy-traffic-shadowing.svg?style=svg["CircleCI", link="https://circleci.com/gh/gravitee-io/gravitee-policy-traffic-shadowing"]
endif::[]

== Phase

=== V3 engine

[cols="4*", options="header"]
|===
^|onRequest
^|onResponse
^|onRequestContent
^|onResponseContent

^.^| X
^.^| -
^.^| -
^.^| -

|===

=== V4 engine

[cols="4*", options="header"]
|===
^|onRequest
^|onResponse
^|onMessageRequest
^|onMessageResponse

^.^| X
^.^| -
^.^| -
^.^| -

|===



== Description

Traffic shadowing allows to asynchronously copy the traffic to another service. By using this policy, the requests are duplicated and sent to the target. The target is an endpoint defined at the API level. The request can be enriched with additional headers.

== Compatibility with APIM

|===
| Plugin version | APIM version
| 2.x            | 4.0 to 4.5
| 3.x            | 4.6 and upper
|===

== Configuration

|===
|Property |Required |Description |Default |Example

.^|target
^.^|X
|The target endpoint (supports EL).
^.^| -
^.^| {#endpoints['my-endpoint']}

.^|headers
^.^|-
|A list of HTTP headers.
^.^| -
^.^| -

|===


[source, json]
.Traffic Shadowing Policy example:
----
{
  "traffic-shadowing": {
    "target": "{#endpoints['target-endpoint']}",
    "headers": [
        {
            "name": "X-Gravitee-Request-Id",
            "value": "{#request.id}"
        }
    ]
  }
}
----
