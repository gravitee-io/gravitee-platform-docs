= Gravitee Policy Template

== Phases

[cols="4*", options="header"]
|===
^|onRequest
^|onResponse
^|onMessageRequest
^|onMessageResponse

^.^| X
^.^| X
^.^| X
^.^| X
|===

== Description

A policy template to fork and use as a quick starter.

This policy will compare `X-Template-Policy` header value with its configuration `errorKey` field, if both values are equal, then the policy will interrupt the request with a failure execution error.

Implements `TemplatePolicy#onRequest(HttpExecutionContext context)` and `TemplatePolicy#onResponse(HttpExecutionContext context)` to develop your own policy.

NOTE: This policy is designed to work with at least APIM 4.0.0.

=== AM and APIM V2 API compatibility

To develop a policy working with AM or a v2 definition of an API in APIM, please follow link:./src/main/java/io/gravitee/policy/template/v3/TemplatePolicyV3.java[the v3 example implementation of the policy].



== Configuration

You can configure the policy with the following options:

[cols="5*", options=header]
|===
^| Property
^| Required
^| Description
^| Type
^| Default

.^|errorKey
^.^|X
.^|Policy will fail if header `X-Template-Policy` value is equal to this field.
^.^|string
^.^|"failure"

|===

Example configuration:

[source, json]
----
{
    "configuration": {
        "errorKey": "value-to-fail-the-policy"
    }
}
----

== Errors

With the provided default implementation, policy will fail if header `X-Template-Policy` value is equal to configured `errorKey` value.

|===
|Phase | Code | Error template key | Description

.^| REQUEST
.^| ```400 - BAD REQUEST```
.^| POLICY_TEMPLATE_ERROR_KEY
.^| An error occurs during request

.^| RESPONSE
.^| ```500 - INTERNAL SERVER ERROR```
.^| POLICY_TEMPLATE_ERROR_KEY
.^| An error occurs during response

|===
