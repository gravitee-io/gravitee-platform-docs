= RateLimit policy

ifdef::env-github[]
image:https://img.shields.io/badge/License-Apache%202.0-blue.svg["License", link="https://github.com/gravitee-io/gravitee-policy-ratelimit/blob/master/LICENSE.txt"]
image:https://img.shields.io/badge/semantic--release-conventional%20commits-e10079?logo=semantic-release["Releases", link="https://github.com/gravitee-io/gravitee-policy-ratelimit/releases"]
image:https://circleci.com/gh/gravitee-io/gravitee-policy-ratelimit.svg?style=svg["CircleCI", link="https://circleci.com/gh/gravitee-io/gravitee-policy-ratelimit"]
endif::[]

== Phase

|===
|onRequest |onResponse

| X
|

|===

== Description

There are three `rate-limit` policies:

* Quota: configures the number of requests allowed over a period of time (hours, days, weeks, months)
image:https://img.shields.io/static/v1?label=Available%20at&message=Gravitee.io&color=1EC9D2["Gravitee.io", link="https://download.gravitee.io/#graviteeio-apim/plugins/policies/gravitee-policy-quota/"]

* Rate-Limit: configures the number of requests allowed over a limited period of time (seconds, minutes)
image:https://img.shields.io/static/v1?label=Available%20at&message=Gravitee.io&color=1EC9D2["Gravitee.io", link="https://download.gravitee.io/#graviteeio-apim/plugins/policies/gravitee-policy-ratelimit/"]

* Spike-Arrest: throttles the number of requests processed and sends them to the backend to avoid a spike
image:https://img.shields.io/static/v1?label=Available%20at&message=Gravitee.io&color=1EC9D2["Gravitee.io", link="https://download.gravitee.io/#graviteeio-apim/plugins/policies/gravitee-policy-spikearrest/"]

== Compatibility with APIM

|===
|Plugin version | APIM version

| 1.x                  | Up to 3.19
| 2.x                  | 3.20 to 4.5
| 3.x                  | 4.6 to latest
|===

== Configuration

You can configure the policies with the following options:

=== Quota

The Quota policy configures the number of requests allowed over a large period of time (from hours to months).
This policy does not prevent request spikes.

|===
|Property |Required |Description |Type |Default

|key
|No
|Key to identify a consumer to apply the quota against. Leave it empty to apply the default behavior (plan/subscription pair). Supports Expression Language.
|String
|null

|limit
|No
|Static limit on the number of requests that can be sent (this limit is used if the value > 0).
|integer
|0

|dynamicLimit
|No
|Dynamic limit on the number of requests that can be sent (this limit is used if static limit = 0). The dynamic value is based on Expression Language expressions.
|string
|null

|periodTime
|Yes
|Time duration
|Integer
|1

|periodTimeUnit
|Yes
|Time unit (`HOURS`, `DAYS`, `WEEKS`, `MONTHS`)
|String
|MONTHS

|===

==== Configuration example

[source, json]
----
  "quota": {
    "limit": "1000",
    "periodTime": 1,
    "periodTimeUnit": "MONTHS"
  }
----

=== Rate-Limit

The Rate-Limit policy configures the number of requests allow over a limited period of time (from seconds to minutes).
This policy does not prevent request spikes.

|===
|Property |Required |Description |Type |Default

|key
|No
|Key to identify a consumer to apply rate-limiting against. Leave it empty to use the default behavior (plan/subscription pair). Supports Expression Language.
|String
|null

|limit
|No
|Static limit on the number of requests that can be sent (this limit is used if the value > 0).
|integer
|0

|dynamicLimit
|No
|Dynamic limit on the number of requests that can be sent (this limit is used if static limit = 0). The dynamic value is based on Expression Language expressions.
|string
|null

|periodTime
|Yes
|Time duration
|Integer
|1

|periodTimeUnit
|Yes
|Time unit ("SECONDS", "MINUTES" )
|String
|SECONDS

|===

==== Configuration example

[source, json]
----
  "rate": {
    "limit": "10",
    "periodTime": 10,
    "periodTimeUnit": "MINUTES"
  }
----

=== Spike Arrest

The Spike-Arrest policy configures the number of requests allow over a limited period of time (from seconds to minutes).
This policy prevents request spikes by throttling incoming requests.
For example, a SpikeArrest policy configured to 2000 requests/second will limit the execution of simultaneous requests to 200 requests per 100ms.

By default, the SpikeArrest policy is applied to a plan, not a consumer. To apply a spike arrest to a consumer, you need to use the `key` attribute, which supports Expression Language.

|===
|Property |Required |Description |Type |Default

|key
|No
|Key to identify a consumer to apply spike arresting against. Leave it empty to use the default behavior. Supports Expression Language (example: `{#request.headers['x-consumer-id']}`).
|String
|null

|limit
|No
|Static limit on the number of requests that can be sent (this limit is used if the value > 0).
|integer
|0

|dynamicLimit
|No
|Dynamic limit on the number of requests that can be sent (this limit is used if static limit = 0). The dynamic value is based on Expression Language expressions.
|string
|null

|periodTime
|Yes
|Time duration
|Integer
|1

|periodTimeUnit
|Yes
|Time unit (`SECONDS`, `MINUTES`)
|String
|SECONDS

|===

==== Configuration example

[source, json]
----
  "spike": {
    "limit": "10",
    "periodTime": 10,
    "periodTimeUnit": "MINUTES"
  }
----

== Errors

=== Default response override

You can use the response template feature to override the default response provided by the policies. These templates must be defined at the API level (see the API Console *Response Templates*
option in the API *Proxy* menu).

=== Error keys

The error keys sent by these policies are as follows:

[cols="2*", options="header"]
|===
^|Key
^|Parameters

.^|RATE_LIMIT_TOO_MANY_REQUESTS
^.^|limit - period_time - period_unit

.^|QUOTA_TOO_MANY_REQUESTS
^.^|limit - period_time - period_unit

.^|SPIKE_ARREST_TOO_MANY_REQUESTS
^.^|limit - period_time - period_unit - slice_limit - slice_period_time - slice_limit_period_unit

|===
