= Interrupt policy

ifdef::env-github[]
image:https://img.shields.io/static/v1?label=Available%20at&message=Gravitee.io&color=1EC9D2["Gravitee.io", link="https://download.gravitee.io/#graviteeio-apim/plugins/policies/gravitee-policy-interrupt/"]
image:https://img.shields.io/badge/License-Apache%202.0-blue.svg["License", link="https://github.com/gravitee-io/gravitee-policy-interrupt/blob/master/LICENSE.txt"]
image:https://img.shields.io/badge/semantic--release-conventional%20commits-e10079?logo=semantic-release["Releases", link="https://github.com/gravitee-io/gravitee-policy-interrupt/releases"]
image:https://circleci.com/gh/gravitee-io/gravitee-policy-interrupt.svg?style=svg["CircleCI", link="https://circleci.com/gh/gravitee-io/gravitee-policy-interrupt"]
endif::[]

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

`Interrupt` policy can be used to break the entire request processing in case of a condition (to define on the policy.
By default, if no policy condition is defined, the policy will always break request processing).

Breaking the request processing means that no more policy will be executed and no endpoint will be called by the gateway.

By default, the policy will return a response payload to the consumer which is containing the `message` (see the
configuration section).

If you want to override this standard response from the policy, you can define an `errorKey` which will be then be used to
define a Response Template.


== Compatibility with APIM

|===
|Plugin version | APIM version

|1.x and upper                  | 3.10.x to latest
|===

== Configuration

|===
|Property |Required |Description |Type |Default

.^|errorKey
^.^|X
|The error Key to use for defining a Response Template
^.^|string
^.^|-

.^|message
^.^|X
|Default response template
^.^|string
^.^|-

.^|variables
^.^|-
|The variables for Response Template purpose
^.^|List of variables
^.^|-

|===

== Examples

[source, json]
----
"policy-interrupt": {
    "errorKey": "MY_CUSTOM_KEY",
    "message": "You got a problem, sir !",
    "variables": [{
        "name": "custom-variable",
        "value": "{#request.headers['origin']}"
    }]
}
----

== Errors

=== Default error

|===
|Code |Message

.^| ```500```
| Request processing broken

|===