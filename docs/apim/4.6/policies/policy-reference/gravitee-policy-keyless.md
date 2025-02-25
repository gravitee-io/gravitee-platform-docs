= Keyless policy

ifdef::env-github[]
image:https://img.shields.io/static/v1?label=Available%20at&message=Gravitee.io&color=1EC9D2["Gravitee.io", link="https://download.gravitee.io/#graviteeio-apim/plugins/policies/gravitee-policy-keyless/"]
image:https://img.shields.io/badge/License-Apache%202.0-blue.svg["License", link="https://github.com/gravitee-io/gravitee-policy-keyless/blob/master/LICENSE.txt"]
image:https://img.shields.io/badge/semantic--release-conventional%20commits-e10079?logo=semantic-release["Releases", link="https://github.com/gravitee-io/gravitee-policy-keyless/releases"]
image:https://circleci.com/gh/gravitee-io/gravitee-policy-keyless.svg?style=svg["CircleCI", link="https://circleci.com/gh/gravitee-io/gravitee-policy-keyless"]
endif::[]

== Phase

[cols="2*", options="header"]
|===
^|onRequest
^|onResponse

^.^| X
^.^|

|===

== Description

This security policy does not block any requests as it considers them as valid by default.

It sets multiple attributes during policy execution, as follows:

* `application`: Anonymous application value, which is equal to `1`.
* `user-id`: Internet Protocol (IP) address of the client or last proxy that sent the request.

== Compatibility matrix

|===
|Plugin version | APIM version

|1.x            | Up to 3.20
|3.x            | 4.0 to 4.5
|4.x            | 4.6 to latest

|===

== Errors

This policy cannot fail as it does not carry out any validation.
