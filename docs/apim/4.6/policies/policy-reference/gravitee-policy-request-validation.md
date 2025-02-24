= Request validation policy

ifdef::env-github[]
image:https://img.shields.io/static/v1?label=Available%20at&message=Gravitee.io&color=1EC9D2["Gravitee.io", link="https://download.gravitee.io/#graviteeio-apim/plugins/policies/gravitee-policy-request-validation/"]
image:https://img.shields.io/badge/License-Apache%202.0-blue.svg["License", link="https://github.com/gravitee-io/gravitee-policy-request-validation/blob/master/LICENSE.txt"]
image:https://img.shields.io/badge/semantic--release-conventional%20commits-e10079?logo=semantic-release["Releases", link="https://github.com/gravitee-io/gravitee-policy-request-validation/releases"]
image:https://circleci.com/gh/gravitee-io/gravitee-policy-request-validation.svg?style=svg["CircleCI", link="https://circleci.com/gh/gravitee-io/gravitee-policy-request-validation"]
endif::[]

== Phase

[cols="4*", options="header"]
|===
^|onRequest
^|onResponse
^|onRequestContent
^|onResponseContent

^.^| X
^.^|
^.^| X
^.^|

|===

== Description

You can use the `request-validation` policy to validate an incoming HTTP request according to defined rules.
A rule is defined for an input value. This input value supports Expression Language expressions and is validated against constraint
rules.

Constraint rules can be:

* `NOT_NULL` -- Input value is required
* `MIN` -- Input value is a number and its value is greater than or equal to a given parameter
* `MAX` -- Input value is a number and its value is lower than or equal to a given parameter
* `MAIL` -- Input value is valid according to the mail pattern
* `DATE` -- Input value is valid according to the date format pattern given as a parameter
* `PATTERN` -- Input value is valid according to the pattern given as a parameter
* `SIZE` -- Input value length is between two given parameters
* `ENUM` -- Field value included in ENUM

By default, if none of the rules can be validated, the policy returns a `400` status code.

== Compatibility with APIM

|===
| Plugin version | APIM version
| 1.x            | All supported versions
|===

== Configuration

|===
|Property |Required |Description |Type |Default

.^|scope
^.^|X
|Phase when the policy is executed
^.^|Policy scope
^.^|ON_REQUEST

.^|status
^.^|X
|HTTP status code send to the consumer in case of validation issues
^.^|HTTP status code
^.^|400

.^|rules
^.^|X
|Rules to apply to incoming request
^.^|List of rules
^.^|-

|===

=== Example configuration

[source, json]
----
"policy-request-validation": {
    "rules": [
        {
            "constraint": {
                "parameters": [
                    ".*\\\\.(txt)$"
                ],
                "type": "PATTERN"
            },
            "input": "{#request.pathInfos[2]}"
        }
    ],
    "status": "400"
}
----

== Errors

=== HTTP status code
|===
|Code |Message

.^| ```400```
| Incoming HTTP request can not be validated.

|===

=== Default response override

You can use the response template feature to override the default response provided by the policy. These templates must be defined at the API level (see the API Console *Response Templates*
option in the API *Proxy* menu).

=== Error keys

The error keys sent by this policy are as follows:

[cols="2*", options="header"]
|===
^|Key
^|Parameters

.^|REQUEST_VALIDATION_INVALID
^.^|violations

|===
