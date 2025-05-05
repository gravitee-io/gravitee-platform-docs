= Gravitee Policy WS-Security Sign

== Phases

[cols="4*", options="header"]
|===
^|onRequest
^|onResponse
^|onMessageRequest
^|onMessageResponse

^.^| X
^.^|
^.^|
^.^|
|===

== Description

The `gravitee-policy-wssecurity-sign` project provides a policy for signing SOAP messages using WS-Security. This policy ensures the integrity and authenticity of SOAP messages by applying digital signatures.

NOTE: This policy is designed to work with at least APIM 4.5.

== Configuration

You can configure the policy with the following options:

[cols="5*", options=header]
|===
^| Property
^| Required
^| Description
^| Type
^| Default

.^|keyStoreBase64
^.^|X
.^|The Base64 encoded string of the keystore.
^.^|string
.^|

.^|keyStorePassword
^.^|X
.^|The password for the keystore.
^.^|string
.^|

.^|certificateAlias
^.^|X
.^|The alias of the certificate in the keystore.
^.^|string
.^|

.^|certificatePassword
^.^|X
.^|The password for the certificate.
^.^|string
.^|
|===

Example configuration:

[source, json]
----
{
    "keyStoreBase64": "base64-encoded-keystore",
    "keyStorePassword": "keystore-password",
    "certificateAlias": "certificate-alias",
    "certificatePassword": "certificate-password"
}
----

== Errors

The policy will fail under the following conditions:

|===
|Phase | Code | Error template key | Description

.^| REQUEST
.^| `400 - BAD REQUEST`
.^| `WS_SECURITY_SIGN_INVALID_INPUT`
.^| An error occurs during the signing process, such as wrong Envelope structure or format error.

.^| RESPONSE
.^| `500 - INTERNAL SERVER ERROR`
.^| `WS_SECURITY_SIGN_PROCESSING_ERROR`
.^| An error caused by the policy itself, such as an invalid configuration or an unexpected exception.
|===
