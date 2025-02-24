= Retry policy

ifdef::env-github[]
image:https://img.shields.io/static/v1?label=Available%20at&message=Gravitee.io&color=1EC9D2["Gravitee.io", link="https://download.gravitee.io/#graviteeio-apim/plugins/policies/gravitee-policy-retry/"]
image:https://img.shields.io/badge/License-Apache%202.0-blue.svg["License", link="https://github.com/gravitee-io/gravitee-policy-retry/blob/master/LICENSE.txt"]
image:https://img.shields.io/badge/semantic--release-conventional%20commits-e10079?logo=semantic-release["Releases", link="https://github.com/gravitee-io/gravitee-policy-retry/releases"]
image:https://circleci.com/gh/gravitee-io/gravitee-policy-retry.svg?style=svg["CircleCI", link="https://circleci.com/gh/gravitee-io/gravitee-policy-retry"]
endif::[]

== Phase

[cols="2*", options="header"]
|===
^|onRequest
^|onResponse

^.^| X
^.^| -

|===

== Description

You can use the `retry` policy to replay requests when experiencing backend connection issues or if the response meets a given _condition_.

If the retry takes too long, relative to the `timeout` value, the request stops and returns status code `502`.

NOTE: To replay a request with a payload, the gateway stores it in memory. We recommend you avoid applying it to requests with a large payload.

== Compatibility with APIM

|===
|Plugin version | APIM version
| 2.x           | All supported versions
|===

=== Policy identifier

You can enable or disable the policy with policy identifier `retry`.

== Configuration

|===
|Property |Required |Description |Default |Example

.^|condition
^.^|X
|Condition to test to determine whether or not to retry the request (supports Expression Language)
^.^| -
^.^| {#response.status > 500}

.^|maxRetries
^.^|X
|Number of retries before failing (502 - Bad Gateway)
^.^| 1
^.^| -

.^|delay
^.^| -
|Time between each attempt
^.^| 0
^.^| -

.^|timeout
^.^|X
|Time after which an operation is considered a failure
^.^| 1000
^.^| -

.^|lastResponse
^.^|-
|Returns the last attempt response, even if it failed regarding the configured condition. In timeout case, `502` is returned.
^.^| false
^.^| -

|===


[source, json]
.Retry Policy example:
----
{
  "retry": {
    "condition": "{#response.status > 500}",
    "maxRetries": 3,
    "timeout": 1000
  }
}
----

== Errors

=== HTTP status code

|===
|Code |Reason

.^| ```502```
a|

Received in the following cases:

* No response satisfies the condition after `maxRetries`
* Technical errors when calling the backend (for example, connection refused, timeout)

|===
