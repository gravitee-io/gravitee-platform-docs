= Generate HTTP Signature Policy

ifdef::env-github[]
image:https://img.shields.io/static/v1?label=Available%20at&message=Gravitee.io&color=1EC9D2["Gravitee.io", link="https://download.gravitee.io/#graviteeio-apim/plugins/policies/gravitee-policy-generate-http-signature/"]
image:https://img.shields.io/badge/License-Apache%202.0-blue.svg["License", link="https://github.com/gravitee-io/gravitee-policy-generate-http-signature/blob/master/LICENSE.txt"]
image:https://img.shields.io/badge/semantic--release-conventional%20commits-e10079?logo=semantic-release["Releases", link="https://github.com/gravitee-io/gravitee-policy-generate-http-signature/releases"]
image:https://circleci.com/gh/gravitee-io/gravitee-policy-generate-http-signature.svg?style=svg["CircleCI", link="https://circleci.com/gh/gravitee-io/gravitee-policy-generate-http-signature"]
image:https://f.hubspotusercontent40.net/hubfs/7600448/gravitee-github-button.jpg["Join the community forum", link="https://community.gravitee.io?utm_source=readme", height=20]
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

HTTP Signature is a kind of authentication method which is adding a new level of security. Use this policy to generate a HTTP Signature with a set of headers, a max validity duration and some other settings.

The "Signature" authentication scheme is based on the model that the client must authenticate itself with a digital signature produced by either a private asymmetric key (e.g., RSA) or a shared symmetric key (e.g., HMAC).

You can use:

* Authorization header: For example: `Authorization: Signature "keyId="rsa-key-1",created=1630590825,expires=1630590831061,algorithm="hmac-sha256",headers="host",signature="Ib/KOuoDjyZPmLbKPvrnz+wj/kcEFZt5aPCxF4e7tO0="",`

* Signature header: For example, `Signature: "keyId="rsa-key-1",created=1630590825,expires=1630590831061,algorithm="hmac-sha256",headers="host",signature="Ib/KOuoDjyZPmLbKPvrnz+wj/kcEFZt5aPCxF4e7tO0="",`


NOTE: Current version of the policy does not support *Digest*, *(request-target)*, *Host* and *Path* header.

== Compatibility with APIM

|===
| Plugin version | APIM version

| Up to 1.x                   | All
|===

== Configuration

|===
|Property |Required |Description |Default |Example

.^|scheme
^.^|X
|Signature Scheme (authorization header or signature header)
^.^| authorization
^.^| -

.^|keyId
^.^|X
|The key id used to generate the signature (supports EL).
^.^| -
^.^| rsa-key-1

.^|secret
^.^|X
|The secret key used to generate and verify the signature (supports EL).
^.^| -
^.^| passphrase

.^|algorithm
^.^|X
|The HMAC digest algorithm
^.^| HMAC_SHA256
^.^| -

.^|headers
^.^| -
|List of headers to build the signature. If no headers, the request must at least contains `Date` header.
^.^| -
^.^| -

.^|created
^.^| X
|Include the created timestamp in the signature and (created) header
^.^| true
^.^| -

.^|expires
^.^| X
|Include the expires timestamp in the signature and (expires) header
^.^| true
^.^| -

.^|validityDuration
^.^|-
|Signature's maximum validation duration in seconds (minimum is 1). Applied when `expires` is set to true
^.^| 3
^.^| -

|===


[source, json]
.Generate HTTP Signature Policy example:
----
{
  "generate-http-signature": {
	"scheme":"AUTHORIZATION",
	"validityDuration":30,
	"keyId":"my-key-id",
	"secret":"my-passphrase",
	"algorithm":"HMAC_SHA256",
	"headers":["X-Gravitee-Header","Host"],
    "created": true,
    "expires": true
  }
}
----

== Http Status Code

|===
|Code |Message

.^| ```400```
| In case of:

* Request does not contain every header of configuration headers list

* Request does not contain 'Date' header and configuration headers list is empty. Policy needs at least 'Date' header to create a signature.

* Unable to sign because of bad configuration.
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

.^|HTTP_SIGNATURE_IMPOSSIBLE_GENERATION
^.^|-

|===

