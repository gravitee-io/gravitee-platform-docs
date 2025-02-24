= API Key policy

ifdef::env-github[]
image:https://img.shields.io/static/v1?label=Available%20at&message=Gravitee.io&color=1EC9D2["Gravitee.io", link="https://download.gravitee.io/#graviteeio-apim/plugins/policies/gravitee-policy-apikey/"]
image:https://img.shields.io/badge/License-Apache%202.0-blue.svg["License", link="https://github.com/gravitee-io/gravitee-policy-apikey/blob/master/LICENSE.txt"]
image:https://img.shields.io/badge/semantic--release-conventional%20commits-e10079?logo=semantic-release["Releases", link="https://github.com/gravitee-io/gravitee-policy-apikey/releases"]
image:https://circleci.com/gh/gravitee-io/gravitee-policy-apikey.svg?style=svg["CircleCI", link="https://circleci.com/gh/gravitee-io/gravitee-policy-apikey"]
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

You can use the `api-key` policy to enforce API Key checks during request processing, allowing only apps with approved API
keys to access your APIs.

This policy ensures that API Keys are valid, have not been revoked or expired and are approved to consume the specific
resources associated with your API.

== Compatibility with APIM

|===
| Plugin version | APIM version
| 5.x            | 4.6.x to latest
| 4.x            | 4.0.x to 4.5.x
| 2.x            | 3.x
|===

== Configuration

=== Policy
You can configure the following policy level options:

|===
|Property |Required |Description |Type |Default

.^|`propagateApiKey`
^.^|-
|Propagate API Key to upstream API
^.^|boolean
^.^|_false_

|===


[source, json]
.Configuration
----
"api-key": {
  "propagateApiKey": false
}
----

=== Gateway
You can also configure the policy in the APIM Gateway configuration file (`gravitee.yml`).
You can customize the `X-Gravitee-Api-Key` header and `api-key` query parameter.

[source, yaml]
.Configuration
----
policy:
  api-key:
    header: My-Custom-Api-Key
    param: custom-api-key
----

== Errors
You can use the response template feature to override the default response provided by the policy. These templates must be defined at the API level (see the API Console *Response Templates*
option in the API *Proxy* menu).

The error keys sent by this policy are as follows:

[cols="2*", options="header"]
|===
^|Key
^|Parameters

.^|API_KEY_MISSING
^.^|-
.^|API_KEY_INVALID_KEY
^.^|-

|===
