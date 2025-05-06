= Circuit Breaker policy

ifdef::env-github[]
image:https://img.shields.io/static/v1?label=Available%20at&message=Gravitee.io&color=1EC9D2["Gravitee.io", link="https://download.gravitee.io/#graviteeio-apim/plugins/policies/gravitee-policy-circuit-breaker/"]
image:https://img.shields.io/badge/License-Apache%202.0-blue.svg["License", link="https://github.com/gravitee-io/gravitee-policy-circuit-breaker /blob/master/LICENSE.txt"]
image:https://img.shields.io/badge/semantic--release-conventional%20commits-e10079?logo=semantic-release["Releases", link="https://github.com/gravitee-io/gravitee-policy-circuit-breaker/releases"]
image:https://circleci.com/gh/gravitee-io/gravitee-policy-circuit-breaker.svg?style=svg["CircleCI", link="https://circleci.com/gh/gravitee-io/gravitee-policy-circuit-breaker"]
endif::[]

== Phase

|===
|onRequest |onResponse
| X
|
|===

== Description

This policy allows to switch to another backend or making the call fails with a `503 Service Unavailable` in case of errors or latency. It is possible to configure errors and latency threshold rate to open the circuit breaker.

Implementation is based on Resilience4j, you can find more information on https://resilience4j.readme.io/docs/circuitbreaker[their documentation].

It guaranties high availability making your system resilient if your target is detected as failing.


== Compatibility with APIM

|===
|Plugin version | APIM version

| 1.x           | APIM 4.5 or earlier
| 2.x           | APIM 4.6 or later
|===


== Configuration

You can configure the policy with the following options:

|===
|Property |Required |Description |Type |Default

|failureRateThreshold|X|Failure rate threshold before the circuit breaker switches to open state. A failure represents a response's status code >= 500. The threshold is expressed as a percentage.|integer (min. 0, max.100)|50
|slowCallRateThreshold|X|Slow call rate threshold before the circuit breaker switches to open state. A slow call is represented by a response time greater than the configured `slowCallDurationThreshold`. The threshold is expressed as a percentage.|integer (min. 0, max.100)|50
|slowCallDurationThreshold|X|The duration threshold above which a call is considered as slow, increasing `slowCallRateThreshold`. The duration is expressed in milliseconds.|integer (min. 1)|1000
|windowSize|X|The size of the sliding window which is used to record the outcome of calls when the circuit is closed.|integer (min. 0)|100
|waitDurationInOpenState||The duration in millisecond before switching from open circuit to half-open.|integer (min. 1)|1000
|redirectToURL||Redirect the call to the given URL instead of returning '503 Service Unavailable' status (supports EL)|string|
|===
