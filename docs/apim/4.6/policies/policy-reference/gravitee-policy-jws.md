= JWS validator policy

ifdef::env-github[]
image:https://img.shields.io/static/v1?label=Available%20at&message=Gravitee.io&color=1EC9D2["Gravitee.io", link="https://download.gravitee.io/#graviteeio-apim/plugins/policies/gravitee-policy-jws/"]
image:https://img.shields.io/badge/License-Apache%202.0-blue.svg["License", link="https://github.com/gravitee-io/gravitee-policy-jws/blob/master/LICENSE.txt"]
image:https://img.shields.io/badge/semantic--release-conventional%20commits-e10079?logo=semantic-release["Releases", link="https://github.com/gravitee-io/gravitee-policy-jws/releases"]
image:https://circleci.com/gh/gravitee-io/gravitee-policy-jws.svg?style=svg["CircleCI", link="https://circleci.com/gh/gravitee-io/gravitee-policy-jws"]
endif::[]

== Phase

=== V3 Engine

[cols="4*", options="header"]
|===
^|onRequest
^|onResponse
^|onRequestContent
^|onResponseContent

^.^| -
^.^| -
^.^| X
^.^| -

|===

=== V4 engine

[cols="4*", options="header"]
|===
^|onRequest
^|onResponse
^|onMessageRequest
^|onMessageResponse

^.^| X
^.^| -
^.^| -
^.^| -

|===

== Compatibility with APIM

|===
| Plugin version | APIM version
| 1.x            | Up to 4.5.x
| 2.x            | 4.6.x to latest
|===

== Description

You can use the `jws-validator` policy to validate the JWS token signature, certificate information and expiration date before sending the API call to the target backend.

JWT in JWS format enables secure content to be shared across security domains. The RFC standards are as follows:

- JWS (Json Web Signature) standard RFC: https://tools.ietf.org/html/rfc7515

- JOSE Header standard RFC: https://tools.ietf.org/html/rfc7515#section-4

- JWT (Json Web Token) standard RFC: https://tools.ietf.org/html/rfc7519

=== JWT

A JWT is composed of three parts: a header, a payload and a signature.
You can see some examples here: http://jwt.io.

- The header contains attributes indicating the algorithm used to sign the token.

- The payload contains some information inserted by the AS (Authorization Server), such as the expiration date and UID of the user.

Both the header and payload are encoded with Base64, so anyone can read the content.

- The third and last part is the signature (for more details, see the RFC).

== Input

----
======================= =================================================
Request Method          POST
Request Content-Type    application/jose+json
Request Body            eyJ0....ifQ.eyJzdWIiOiI...lIiwiYWRtaW4iOnRydWV9.TJVA95...h7HgQ
Response Codes          Backend response or 401 Unauthorized
======================= =================================================
----

According to the link:https://tools.ietf.org/html/rfc7515#section-4.1.10[JWS RFC], the JWT/JWS header must contain the following information if correct content is to be provided to the backend:

A `typ` value of `JOSE` can be used by applications to indicate that this object is a JWS or JWE using JWS Compact Serialization or the JWE Compact Serialization.
A `typ` value of `JOSE+JSON` can be used by applications to indicate that this object is a JWS or JWE using JWS JSON Serialization or JWE JSON Serialization.

The `cty` (content type) header parameter is used by JWS applications to declare the media type [IANA.MediaTypes] of the secured content (the payload).
To keep messages compact in typical scenarios, it is strongly recommended that senders omit the `application/` prefix of a media type value in a `cty` header parameter when no other `/` appears in the media type value.

NOTE: A recipient using the media type value must treat it as if `application/` were prepended to any `cty` value not containing a `/`.

== Example

A valid example of a JWS header is as follows:

[source, json]
----
{
 "typ":"JOSE+JSON",
 "cty":"json",
 "alg":"RS256",
 "x5c":"string",
 "kid":"string"
}
----

== Configuration

|===
|Property |Required |Description |Type |Default

|checkCertificateValidity||Check if the certificate used to sign the JWT is correct and has valid `not_before` and `not_after` dates|boolean|false
|checkCertificateRevocation||Check if the certificate used to sign the JWT is not revoked via the CRL Distribution Points. The CRL is stored inside the X509v3 CRL Distribution Extension Points.|boolean|false
|===

To validate the token signature, the policy needs to use the JWS validator policy public key set in the APIM Gateway `gravitee.yml` file:

[source, yml]
----
policy:
  jws:
    kid:
      default: ssh-rsa myValidationKey anEmail@domain.com
      kid-2016: /filepath/to/pemFile/certificate.pem
----

The policy will inspect the JWT/JWS header to extract the key id (`kid` attribute) of the public key. If no key id is found then it is set to `default`.

The gateway will be able to retrieve the corresponding public key and the JOSE Header using `x5c` (X.509 Certificate Chain). The header parameter will be used to verify certificate information
and check that the JWT was signed using the private key corresponding to the specified public key.

== Errors

=== HTTP status code

|===
|Code |Message

| ```401```
| Bad token format, content, signature, certificate, expired token or any other issue preventing the policy from validating the token

|===
