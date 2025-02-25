= Assign metrics policy

ifdef::env-github[]
image:https://img.shields.io/static/v1?label=available%20at&message=Gravitee.io&color=1EC9D2["Gravitee.io", link="https://download.gravitee.io/#graviteeio-apim/plugins/policies/gravitee-policy-assign-metrics/"]
image:https://circleci.com/gh/gravitee-io/gravitee-policy-assign-metrics.svg?style=shield&circle-token=62b071200b50818be6c423c654940a385b735068["CircleCI", link="https://circleci.com/gh/gravitee-io/gravitee-policy-assign-metrics"]
image:https://img.shields.io/badge/semantic--release-conventional%20commits-e10079?logo=semantic-release["Releases", link="https://github.com/gravitee-io/gravitee-policy-assign-metrics/releases"]
endif::[]

[label label-enterprise]#Enterprise feature#

== Phases

=== V3 engine

[cols="^2,^2,^2,^2",options="header"]
|===
|onRequest|onResponse|onRequestContent|onResponseContent

|X
|X
|X
|X
|===

=== V4 engine

[cols="4*", options="header"]
|===
^|onRequest
^|onResponse
^|onMessageRequest
^|onMessageResponse

^.^| X
^.^| X
^.^| X
^.^| X
|===

== Description

You can use the `assign-metrics` policy to push extra metrics in addition to the natively provided request metrics.

These metrics can then be used from analytics dashboards to create custom widgets and, optionally, apply aggregations based on their value.

|===
|Plugin version | APIM version

|1.x            | Up to 3.17
|2.x            | 3.18 to 3.20
|3.x            | 4.0 to latest
|===

=== Policy identifier

You can enable or disable the policy with policy identifier `policy-assign-metrics`.

== Example

=== On a Request header

To display your request distribution based on a particular HTTP header in your dashboards, create the custom metric shown below.

```
"assign-metrics": {
    "metrics": [
        {
            "name": "myCustomHeader,
            "value": "{#request.headers['X-MyCustomHeader'] != null ? #request.headers['X-MyCustomHeader'][0] : null}"
        }
    ]
}
```
