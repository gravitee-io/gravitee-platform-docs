= HTTP Signature Validator Policy

ifdef::env-github[]
image:https://img.shields.io/static/v1?label=Available%20at&message=Gravitee.io&color=1EC9D2["Gravitee.io", link="https://download.gravitee.io/#graviteeio-apim/plugins/policies/gravitee-policy-http-signature/"]
image:https://img.shields.io/badge/License-Apache%202.0-blue.svg["License", link="https://github.com/gravitee-io/gravitee-policy-http-signature/blob/master/LICENSE.txt"]
image:https://img.shields.io/badge/semantic--release-conventional%20commits-e10079?logo=semantic-release["Releases", link="https://github.com/gravitee-io/gravitee-policy-http-signature/releases"]
image:https://circleci.com/gh/gravitee-io/gravitee-policy-http-signature.svg?style=svg["CircleCI", link="https://circleci.com/gh/gravitee-io/gravitee-policy-http-signature"]
endif::[]

== Phase

[cols="2*", options="header"]
|===
^|onRequest
^|onResponse

^.^| X
^.^| -

|===

== Description

HTTP Signature is a kind of authentication method which is adding a new level of security. By using this policy, the
consumer is enforced to send a _signature_ which is used to identify the request temporarily and ensure that the
request is really coming from the requesting consumer, using a secret key.

The "Signature" authentication scheme is based on the model that the client must authenticate itself with a digital signature produced by either a private asymmetric key (e.g., RSA) or a shared symmetric key (e.g., HMAC).

You can use:

* Authorization header: For example: `Authorization: Signature "keyId="rsa-key-1",created=1630590825,expires=1630590831061,algorithm="hmac-sha256",headers="host",signature="Ib/KOuoDjyZPmLbKPvrnz+wj/kcEFZt5aPCxF4e7tO0="",`

* Signature header: For example, `Signature: "keyId="rsa-key-1",created=1630590825,expires=1630590831061,algorithm="hmac-sha256",headers="host",signature="Ib/KOuoDjyZPmLbKPvrnz+wj/kcEFZt5aPCxF4e7tO0="",`

NOTE: Current version of the policy does not support *Digest*, *(request-target)*, *Host* and *Path* header.


== Compatibility with APIM

|===
|Plugin version | APIM version
|1.x            | All supported versions
|===


== Configuration

|===
|Property |Required |Description |Default |Example

.^|scheme
^.^|X
|Signature Scheme (authorization header or signature header)
^.^| authorization
^.^| -

.^|secret
^.^|X
|The secret key used to generate and verify the signature (supports EL).
^.^| -
^.^| passphrase

.^|algorithms
^.^|-
|A list of supported HMAC digest algorithms.
^.^| -
^.^| -

.^|enforceHeaders
^.^| -
|List of headers the consumer must at least use for HTTP signature creation.
^.^| -
^.^| -

.^|clockSkew
^.^|-
|Clock Skew in seconds to prevent replay attacks.
^.^| 30
^.^| -

|===


[source, json]
.HTTP Signature Policy example:
----
{
  "http-signature": {
	"scheme":"AUTHORIZATION",
	"clockSkew":30,
	"secret":"my-passphrase",
	"algorithms":["HMAC_SHA256"],
	"enforceHeaders":["Date","Host"]
  }
}
----

== Http Status Code

|===
|Code |Message

.^| ```401```
| In case of:

* Missing or signature

* Request does not contain headers part of the signature

* Enforce HTTP headers not part of the signature
|===

== Errors

If you're looking to override the default response provided by the policy, you can do it
thanks to the response templates feature. These templates must be define at the API level (see `Response Templates`
from the `Proxy` menu).

Here are the error keys send by this policy:

[cols="2*", options="header"]
|===
^|Key
^|Parameters

.^|HTTP_SIGNATURE_INVALID_SIGNATURE
^.^|-

|===
