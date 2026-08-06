---
description: An overview about oas validation.
metaLinks:
  alternates:
    - oas-validation.md
---

# OAS Validation

{% hint style="warning" %}
**This feature requires Gravitee's Enterprise Edition.** For more information, see [Gravitee APIM Enterprise Edition](https://documentation.gravitee.io/apim/overview/gravitee-apim-enterprise-edition).
{% endhint %}

## At a glance

<!-- GEN:BEGIN at-a-glance -->
| Property | Value |
| --- | --- |
| Policy ID | `oas-validation` |
| Category | others |
| Plugin version | 2.x |
| Minimum APIM version | 4.4.0 |
| Supported API types | v4-http-proxy. **Not** v2, v4-message, v4-tcp-proxy |
| Phases | Request, Response |
| Licence | EE |
| Source | gravitee-io/gravitee-policy-oas-validation |
<!-- GEN:END at-a-glance -->

## Overview

The `oas-validation` policy validates aspects of the request and response against an embedded OpenAPI Specification.

In Gravitee, OAS files are not directly linked with the API definition, but you can use the specification as a resource on the API to define documentation and to drive this policy.

You can load the OpenAPI specification with any of the following methods:

* Insert YAML or JSON inline with the API
* Load it into a Content Provider Resource on the API and evolve that resource separately
* Add the OAS Validation policy when importing a v4 proxy API from an OpenAPI specification to relevant paths and flows

{% hint style="info" %}
This policy was designed to work with at least version 4.4.0 of API Management (APIM).
{% endhint %}

## How it works

The policy loads the configured OpenAPI Specification, selects a validator based on the detected OpenAPI version, and validates the configured aspects of the request and/or response. When validation fails, the policy rejects the call (unless logging-only mode is enabled).

<!-- VERIFY: confirm fail-open / logInsteadOfThrowError behaviour with policy owners before treating as final. -->

## Configuration reference

{% hint style="warning" %}
You can apply this policy to only v4 HTTP proxy APIs. You cannot apply this policy to v4 message APIs, v4 TCP proxy APIs, or v2 APIs.
{% endhint %}

<!-- GEN:BEGIN configuration -->
#### OpenAPI source

Exactly **one** of the following source properties is required.

| Property | Required | Type | Default | Description |
| --- | --- | --- | --- | --- |
| `resourceName` | One of | string | — | Resource name |
| `sourceJson` | One of | string | — | OpenApi source from an JSON editor |
| `sourceUrl` | One of | string | — | The url will be called when the api is deployed in the gateway or after a redeployment. |
| `sourceYaml` | One of | string | — | OpenApi source from an Yaml editor |

#### Common options

| Property | Required | Type | Default | Description |
| --- | --- | --- | --- | --- |
| `basePath` | No | string | — | Optional base path. This can be useful if e.g. your Swagger specification has been created for a public URL but you are validating requests against an internal URL where the URL paths differ. |
| `validationOptions.logInsteadOfThrowError` | No | boolean | `false` | If true, the validation errors will be logged instead of throwing an error. This can be useful to not block the request/response flow in case of validation errors. |
| `validationOptions.returnDetailedErrorReport` | No | boolean | `true` | Only for Bad Request (400) error. Return in the response the detailed error report. Like Schema validation errors on request/response body. This can be useful for debugging but can expose OpenApi schema details. |
| `validationOptions.strictOperationPathMatching` | No | boolean | `true` | If true, a trailing slash indicates a different path than without. |

#### Request validation options

| Property | Required | Type | Default | Description |
| --- | --- | --- | --- | --- |
| `validationOptions.validateRequestBody` | No | boolean | `true` | This will validate that the request matches the request body defined in the OpenApi schema. This is only apply if the content type is `application/json` or `application/x-www-form-urlencoded`. |
| `validationOptions.validateRequestContentType` | No | boolean | `true` | This will validate that the request matches the requestBody.content types defined in the OpenApi schema. |
| `validationOptions.validateRequestParameters` | No | boolean | `true` | This will validate that parameters marked as required for the request exist and all request parameters match the valid values. |
| `validationOptions.validateRequestParametersOptions` | No | array (`QUERY_PARAMS`, `HEADERS`, `COOKIES`) | `["QUERY_PARAMS","HEADERS","COOKIES"]` | Uncheck the request parameters that you don't want to validate. (may have an impact on parameter or security validation) |
| `validationOptions.validateRequestPathAndMethod` | No | boolean | `true` | This will validate that the path (minus the base path) and associated HTTP method matches one of the path patterns defined in the OpenApi schema. |
| `validationOptions.validateRequestQueryParamsUnexpected` | No | boolean | `false` | This will validate that no additional query parameters are passed that are not found in the OpenApi schema. |
| `validationOptions.validateRequestSecurity` | No | boolean | `false` | This will validate that the request has the required security defined in the OpenApi schema. |

#### Response validation options

| Property | Required | Type | Default | Description |
| --- | --- | --- | --- | --- |
| `validationOptions.validateResponseBody` | No | boolean | `true` | This will validate that the response matches the response body defined in the OpenApi schema. |
| `validationOptions.validateResponseContentType` | No | boolean | `true` | This will validate that the response matches the response content type defined in the OpenApi schema. |
| `validationOptions.validateResponseStatusCode` | No | boolean | `true` | This will validate that the response status code matches the response status code defined in the OpenApi schema. |
<!-- GEN:END configuration -->

## Phase compatibility

<!-- GEN:BEGIN phases -->
| v2 phase | Supported | v4 phase | Supported |
| --- | --- | --- | --- |
| onRequest | No | onRequest | Yes |
| onResponse | No | onResponse | Yes |
| onRequestContent | No | onMessageRequest | No |
| onResponseContent | No | onMessageResponse | No |
<!-- GEN:END phases -->

## Examples

{% tabs %}
{% tab title="HTTP Proxy Configuration" %}
Sample policy configuration:

```json
"configuration": {
    "sourceUrl": "query-params-openapi.yaml",
    "validationOptions": {
       "validateRequestBody": false,
       "validateRequestParametersOptions": ["HEADERS", "COOKIES"]
    }
}
```
{% endtab %}
{% endtabs %}

## Errors

<!-- GEN:BEGIN errors -->
| Phase | Code | Error key | Description |
| --- | --- | --- | --- |
| REQUEST | `400 - BAD REQUEST` | `OAS_VALIDATION_ERROR` | Request does not match the OpenAPI Specification |
| RESPONSE | `500 - INTERNAL SERVER ERROR` | `OAS_VALIDATION_ERROR` | Response does not match the OpenAPI Specification |
| REQUEST / RESPONSE | `500 - INTERNAL SERVER ERROR` | `NO_OAS_RESOURCE` | No resource configured |
| REQUEST / RESPONSE | `500 - INTERNAL SERVER ERROR` | `NO_OAS_PROVIDED` | No OpenAPI Specification provided |
| REQUEST / RESPONSE | `500 - INTERNAL SERVER ERROR` | `UNABLE_TO_LOAD_OAS_KEY` | The OpenAPI Specification could not be loaded or is unsupported |
| REQUEST / RESPONSE | `500 - INTERNAL SERVER ERROR` | `JSON_VALIDATION_PROCESSING_EXCEPTION_KEY` | Error while processing or validating against the OpenAPI Specification |
<!-- GEN:END errors -->

## Compatibility

<!-- GEN:BEGIN compatibility -->
| Plugin version | APIM versions |
| --- | --- |
| 2.x | 4.8.x to latest |
| 1.x | 4.6.x to 4.11.x |
<!-- GEN:END compatibility -->

## Changelog

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-oas-validation/blob/main/CHANGELOG.md" %}

## Related

* Policy reference index
* Content Provider Resource
* OpenAPI import
