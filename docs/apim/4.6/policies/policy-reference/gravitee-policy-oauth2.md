= OAuth2 policy

ifdef::env-github[]
image:https://img.shields.io/static/v1?label=Available%20at&message=Gravitee.io&color=1EC9D2["Gravitee.io", link="https://download.gravitee.io/#graviteeio-apim/plugins/policies/gravitee-policy-oauth2/"]
image:https://img.shields.io/badge/License-Apache%202.0-blue.svg["License", link="https://github.com/gravitee-io/gravitee-policy-oauth2/blob/master/LICENSE.txt"]
image:https://img.shields.io/badge/semantic--release-conventional%20commits-e10079?logo=semantic-release["Releases", link="https://github.com/gravitee-io/gravitee-policy-oauth2/releases"]
image:https://circleci.com/gh/gravitee-io/gravitee-policy-oauth2.svg?style=svg["CircleCI", link="https://circleci.com/gh/gravitee-io/gravitee-policy-oauth2"]
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

You can use the `oauth2` policy to check access token validity during request processing using token introspection.

If the access token is valid, the request is allowed to proceed. If not, the process stops and rejects the request.

The access token must be supplied in the ```Authorization``` HTTP request header:

[source, shell]
----
$ curl -H "Authorization: Bearer |accessToken|" \
           http://gateway/api/resource
----

== Compatibility with APIM

|===
| Plugin version | APIM version
| 4.x            | 4.6.x to latest
| 3.x            | 4.0.x to 4.5.x
| 2.x            | 3.20.x
| 1.x            | Up to 3.19.x
|===

== Attributes

|===
|Name |Description

.^|oauth.access_token
|Access token extracted from ```Authorization``` HTTP header.

.^|oauth.payload
|Payload from token endpoint / authorization server, useful when you want to parse and extract data from it. Only if `extractPayload` is enabled in policy configuration.

|===

== Examples

Given the following introspection response payload:
[source, json]
----
{
    "active": true,
    "client_id": "VDE",
    "exp": 1497536237,
    "jti": "5e075c1c-f4eb-42a5-8b56-fd367133b242",
    "scope": "read write delete",
    "token_type": "bearer",
    "username": "flx"
}
----

You can extract the `username` from the payload using the following JsonPath:
[source]
----
{#jsonPath(#context.attributes['oauth.payload'], '$.username')}
----


== Configuration

The OAuth2 policy requires a resource to access an OAuth2 Authorization Server for token introspection.
APIM supports two types of authorization server:

* <<apim_resources_oauth2_generic.adoc#, Generic OAuth2 Authorization Server>> -- a resource which can be configured to cover any authorization server.
* <<apim_resources_oauth2_am.adoc#, Gravitee.io Access Management>> -- a resource which can be easily plugged into APIM using Gravitee.io Access Management with security domain support.

|===
|Property |Required |Description |Type| Default

.^|oauthResource
^.^|X
|The OAuth2 resource used to validate `access_token`. This must reference a valid Gravitee.io OAuth2 resource.
^.^|string
|

.^|oauthCacheResource
^.^|-
|The Cache resource used to store the `access_token`. This must reference a valid Gravitee.io Cache resource.
^.^|string
|

.^|extractPayload
^.^|-
|When the access token is validated, the token endpoint payload is saved in the ```oauth.payload``` context attribute
^.^|boolean
^.^|false

.^|checkRequiredScopes
^.^|-
|Whether the policy needs to check `required` scopes to access the underlying resource
^.^|boolean
^.^|false


.^|requiredScopes
^.^|-
|List of scopes to check to access the resource
^.^|boolean
^.^|array of string
|===

=== Configuration example

[source, json]
----
{
  "oauth2": {
    "oauthResource": "oauth2-resource-name",
    "oauthCacheResource": "cache-resource-name",
    "extractPayload": true,
    "checkRequiredScopes": true,
    "requiredScopes": ["openid", "resource:read", "resource:write"]
  }
}
----

== Errors

=== HTTP status code

|===
|Code |Message

.^| ```401```
| Issue encountered:

* No OAuth Authorization Server resource has been configured

* No OAuth authorization header was supplied

* No OAuth access token was supplied

* Access token can not be validated by authorization server

.^| ```503```
| Issue encountered:

* Access token can not be validated because of a technical error with
authorization server

* One of the required scopes was missing while introspecting access token

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

.^|OAUTH2_MISSING_SERVER
^.^|-

.^|OAUTH2_MISSING_HEADER
^.^|-

.^|OAUTH2_MISSING_ACCESS_TOKEN
^.^|-

.^|OAUTH2_INVALID_ACCESS_TOKEN
^.^|-

.^|OAUTH2_INVALID_SERVER_RESPONSE
^.^|-

.^|OAUTH2_INSUFFICIENT_SCOPE
^.^|-

.^|OAUTH2_SERVER_UNAVAILABLE
^.^|-

|===
