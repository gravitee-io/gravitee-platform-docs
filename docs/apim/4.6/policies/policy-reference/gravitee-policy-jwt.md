= JSON Web Token validator policy

== Phase

|===
|onRequest |onResponse

| X
|
|===

== Description

You can use the `jwt` policy to validate the token signature and expiration date before sending the API call to the target backend.

Some authorization servers use OAuth2 protocol to provide access tokens. These access token can be in JWS/JWT format. For the RFC standards, see:

- JWS (JSON Web Signature) standard RFC: https://tools.ietf.org/html/rfc7515

- JWT (JSON Web Token) standard RFC: (https://tools.ietf.org/html/rfc7519


== Compatibility with APIM

|===
|Plugin version | APIM version

|6.x                 | 4.6.x to latest
|5.x                 | 4.4.x to 4.5.x
|4.x                 | 4.0.x to 4.3.x
|2.x                 | 3.18.x to 3.20
|1.22.x              | 3.15.x to 3.17.x
|1.20.x to 1.21.x    | 3.10.x to 3.14.x
|Up to 1.19.x        | Up to 3.9.x
|===

=== JWT

A JWT is composed of three parts: a header, a payload and a signature.
You can see some examples here: http://jwt.io.

- The header contains attributes indicating the algorithm used to sign the token.

- The payload contains some information inserted by the AS (Authorization Server), such as the expiration date and UID of the user.

Both the header and payload are encoded with Base64, so anyone can read the content.

- The third and last part is the signature (for more details, see the RFC).

== Configuration

|===
|Property |Required |Description |Type |Default

|publicKeyResolver|X|Used to resolve the public key needed to validate the signature|enum|GIVEN_KEY
|resolverParameter||Needed if you use the `GATEWAY_KEYS` or `GIVEN_ISSUER` resolver (EL support)|string|
|connectTimeout||Max time to connect to the JWKS url (only useful when resolver is `JWKS_URL`)|integer|2000
|requestTimeout||Max time to fetch the JWKS url (only useful when resolver is `JWKS_URL`)|integer|2000
|followRedirects||Select this option if you want to automatically follow redirect (301, 302) when fecthing the JWKS (only useful when resolver is `JWKS_URL`)|boolean|false
|useSystemProxy||Select this option if you want use system proxy (only useful when resolver is `JWKS_URL`)|boolean|false
|extractClaims||Select this option if you want to extract claims into the request context|boolean|false
|clientIdClaim||Required if the client_id should be read from non-standard claims (azp, aud, client_id)|string|
|===


=== Specific configuration for Confirmation Method validation

|===
|Property |Required |Description |Type| Default

.^|confirmationMethodValidation.ignoreMissing
^.^|-
|Will ignore CNF validation if the token doesn't contain any CNF information.
^.^|boolean
^.^|false

.^|confirmationMethodValidation.certificateBoundThumbprint.enabled
^.^|-
|Will validate the certificate thumbprint extracted from the access_token with the one provided by the client.
^.^|boolean
^.^|false

.^|confirmationMethodValidation.certificateBoundThumbprint.extractCertificateFromHeader
^.^|-
|Enabled to extract the client certificate from request header. Necessary when the M-TLS connection is handled by a proxy.
^.^|boolean
^.^|false

.^|confirmationMethodValidation.certificateBoundThumbprint.headerName
^.^|-
|Name of the header where to find the client certificate.
^.^|string
^.^|ssl-client-cert
|===

To validate the token signature, the policy needs to use the associated Authorization Servers public key.

The policy prompts you to choose between three (`GIVEN_KEY`, `GIVEN_ISSUER`, `GATEWAY_ISSUER`) methods to retrieve the required public key.

 - `GIVEN_KEY` -- You provide the key (in `ssh-rsa`, `pem`, `crt` or `public-key` format)
 - `GIVEN_ISSUER` -- If you want to filter on several authorization servers then you only need to specify the issuer name; the gateway will only accept JWTs with a permitted issuer attribute. If `GATEWAY_KEYS` is set, the issuer is also used to retrieve the public key from the `gravitee.yml` file.
 - `GATEWAY_KEYS` -- You can set some public keys in the APIM Gateway `gravitee.yml` file

[source, yml]
----
policy:
  jwt:
    issuer:
      my.authorization.server:
        default: ssh-rsa myValidationKey anEmail@domain.com
        kid-2016: ssh-rsa myCurrentValidationKey anEmail@domain.com
----

The policy will inspect the JWT:

** header to extract the key id (`kid` attribute) of the public key. If no key id is found then it use the `x5t` field.
**** if `kid` is present and no key corresponding is found, the token is rejected.
**** if `kid` is missing and no key corresponding to `x5t` is found, the token is rejected.
** claims (payload) to extract the issuer (`iss` attribute)

Using these two values, the gateway can retrieve the corresponding public key.

Regarding the client_id, the standard behavior is to read it from the `azp` claim, then if not found in the `aud` claim and finally in the `client_id` claim.
You can override this behavior by providing a custom `clientIdClaim` in the configuration.

== Attributes

|===
|Name |Description

.^|jwt.token
|JWT token extracted from the ```Authorization``` HTTP header

.^|jwt.claims
|A map of claims registered in the JWT token body, used for extracting data from it. Only if `extractClaims` is enabled in the policy configuration.

|===


== Example

Given the following JWT claims (payload):

[source, json]
----
{
  "iss": "Gravitee.io AM",
  "sub": "1234567890",
  "name": "John Doe",
  "admin": true
}
----

You can extract the issuer from JWT using the following Expression Language statement:

[source]
----
{#context.attributes['jwt.claims']['iss']}
----

== Errors

=== HTTP status code

|===
|Code |Message

| ```401```
| Bad token format, content, signature, expired token or any other issue preventing the policy from validating the token

|===

You can use the response template feature to override the default response provided by the policy. These templates must be defined at the API level (see the API Console *Response Templates*
option in the API *Proxy* menu).

The error keys sent by the policy are as follows:

[cols="2*", options="header"]
|===
^|Key
^|Parameters

.^|JWT_MISSING_TOKEN
^.^|-

.^|JWT_INVALID_TOKEN
^.^|-

|===
