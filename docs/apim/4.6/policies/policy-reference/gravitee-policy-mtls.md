= mTLS policy

ifdef::env-github[]
image:https://img.shields.io/static/v1?label=Available%20at&message=Gravitee.io&color=1EC9D2["Gravitee.io", link="https://download.gravitee.io/#graviteeio-apim/plugins/policies/gravitee-policy-mtls/"]
image:https://img.shields.io/badge/License-Apache%202.0-blue.svg["License", link="https://github.com/gravitee-io/gravitee-policy-mtls/blob/master/LICENSE.txt"]
image:https://img.shields.io/badge/semantic--release-conventional%20commits-e10079?logo=semantic-release["Releases", link="https://github.com/gravitee-io/gravitee-policy-mtls/releases"]
image:https://circleci.com/gh/gravitee-io/gravitee-policy-mtls.svg?style=svg["CircleCI", link="https://circleci.com/gh/gravitee-io/gravitee-policy-mtls"]
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

You can use the `mtls` policy to verify a client certificate exists as part of the request.

This policy does not ensure that certificates are valid, since it is done directly by the server.

== Compatibility with APIM

|===
| Plugin version | APIM version
| 1.x            | 4.5 to latest
|===

== Errors
You can use the response template feature to override the default response provided by the policy. These templates must be defined at the API level (see the API Console *Response Templates*
option in the API *Entrypoints > Response Templates* menu).

The error keys sent by this policy are as follows:

[cols="2*", options="header"]
|===
^|Key
^|Parameters

.^|CLIENT_CERTIFICATE_MISSING
^.^|-
.^|CLIENT_CERTIFICATE_INVALID
^.^|-
.^|SSL_SESSION_REQUIRED
^.^|-

|===

