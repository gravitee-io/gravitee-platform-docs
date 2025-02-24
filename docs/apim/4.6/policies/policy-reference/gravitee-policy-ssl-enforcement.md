= SSL enforcement policy

ifdef::env-github[]
image:https://img.shields.io/static/v1?label=Available%20at&message=Gravitee.io&color=1EC9D2["Gravitee.io", link="https://download.gravitee.io/#graviteeio-apim/plugins/policies/gravitee-policy-ssl-enforcement/"]
image:https://img.shields.io/badge/License-Apache%202.0-blue.svg["License", link="https://github.com/gravitee-io/gravitee-policy-ssl-enforcement/blob/master/LICENSE.txt"]
image:https://img.shields.io/badge/semantic--release-conventional%20commits-e10079?logo=semantic-release["Releases", link="https://github.com/gravitee-io/gravitee-policy-ssl-enforcement/releases"]
image:https://circleci.com/gh/gravitee-io/gravitee-policy-ssl-enforcement.svg?style=svg["CircleCI", link="https://circleci.com/gh/gravitee-io/gravitee-policy-ssl-enforcement"]
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

You can use the `ssl-enforcement` policy to filter incoming SSL requests. It allows you to restrict or
allow access only to requests with client certificate authentication or only to a subset of valid clients.

This policy is mainly used in plan configuration to allow access to
consumers for a given set of certificates.

== Compatibility with APIM

|===
| Plugin version | APIM version
| 1.x            | All supported versions
|===

== Configuration

|===
|Property |Required |Description |Type| Default

.^|requiresSsl
^.^|-
|Is SSL requires to access this resource?
^.^|boolean
^.^|true

.^|requiresClientAuthentication
^.^|-
|Is client authentication required to access this resource?
^.^|boolean
^.^|false

.^|whitelistClientCertificates
^.^|-
|List of allowed X.500 names (from client certificate)
^.^|array of strings
^.^|-

|===

=== Configuration example

[source, json]
"ssl-enforcement" : {
    "requiresSsl": true,
    "requiresClientAuthentication": true,
    "whitelistClientCertificates": [
        "CN=localhost,O=GraviteeSource,C=FR"
    ]
}

[[gravitee-policy-resource-filtering-ant]]
=== Ant style path pattern
URL mapping matches URLs using the following rules:

* `?` matches one character
* `*` matches zero or more characters
* `**` matches zero or more directories in a path

== Errors

=== HTTP status codes
|===
|Code |Message

.^| ```401```
| Access to the resource is unauthorized according to policy rules

.^| ```403```
| Access to the resource is forbidden according to policy rules

|===

=== Default response override

You can use the response template feature to override the default responses provided by the policy. These templates must be defined at the API level (see the API Console *Response Templates*
option in the API *Proxy* menu).

=== Error keys

The error keys sent by this policy are as follows:

[cols="2*", options="header"]
|===
^|Key
^|Parameters

.^|SSL_ENFORCEMENT_SSL_REQUIRED
^.^|-

.^|SSL_ENFORCEMENT_AUTHENTICATION_REQUIRED
^.^|-

.^|SSL_ENFORCEMENT_CLIENT_FORBIDDEN
^.^|name (X.500 name from client certificate)

|===
