---
hidden: true
---

# OAS Validation

## Phases <a href="#user-content-phases" id="user-content-phases"></a>

| onRequest | onResponse | onMessageRequest | onMessageResponse |
| --------- | ---------- | ---------------- | ----------------- |
| X         | X          |                  |                   |

## Description <a href="#user-content-description" id="user-content-description"></a>

This policy allows you to validate an incoming request or response against an OpenAPI Specification (OAS).

| Note | This policy is designed to work with at least APIM 4.4.0. |
| ---- | --------------------------------------------------------- |

## Configuration <a href="#user-content-configuration" id="user-content-configuration"></a>

You can configure the policy with the following options:

### Common options <a href="#user-content-common-options" id="user-content-common-options"></a>

| Name                           | Description                                                                                                                                                                                                         | Property                                                                                          |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| OpenApi source from            | OpenAPI Specification in Json or Yaml format.                                                                                                                                                                       | `sourceJson` or `sourceYaml` or `sourceUrl` or `resourceName` (string) (required) (default: true) |
| Base path                      | Optional base path. This can be useful if e.g. your Swagger specification has been created for a public URL but you are validating requests against an internal URL where the URL paths differ.                     | `basePath` (string) (optional)                                                                    |
| Return detailed error report   | Only for Bad Request (400) error. Return in the response the detailed error report. Like Schema validation errors on request/response body. This can be useful for debugging but can expose OpenApi schema details. | `validationOptions. returnDetailedErrorReport` (boolean) (default: true)                          |
| Strict operation path matching | If true, a trailing slash indicates a different path than without.                                                                                                                                                  | `validationOptions. strictOperationPathMatching` (boolean) (default: true)                        |

### Request validation options <a href="#user-content-request-validation-options" id="user-content-request-validation-options"></a>

| Name                                                                   | Description                                                                                                                                                                                      | Property                                                                                               |
| ---------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------ |
| Validate path and method exist                                         | This will validate that the path (minus the base path) and associated HTTP method matches one of the path patterns defined in the OpenApi schema.                                                | `validationOptions. validateRequestPathAndMethod` (boolean) (default: true)                            |
| Validate request content type                                          | This will validate that the request matches the requestBody.content types defined in the OpenApi schema.                                                                                         | `validationOptions. validateRequestContentType` (boolean) (default: true)                              |
| Validate request body                                                  | This will validate that the request matches the request body defined in the OpenApi schema. This is only apply if the content type is `application/json` or `application/x-www-form-urlencoded`. | `validationOptions. validateRequestBody` (boolean) (default: true)                                     |
| Validate request parameters (PathParams, QueryParams, Headers, Cookie) | This will validate that parameters marked as required for the request exist and all request parameters match the valid values.                                                                   | `validationOptions. validateRequestParameters` (boolean) (default: true)                               |
| Additional options for request parameters validation                   | Uncheck the request parameters that you don’t want to validate. (may have an impact on parameter or security validation)                                                                         | `validationOptions. validateRequestParameters` (enum) (default: "QUERY\_PARAMS", "HEADERS", "COOKIES") |
| validationOptions. validateRequestQueryParamsUnexpected                | This will validate that no additional query parameters are passed that are not found in the OpenApi schema.                                                                                      | `validationOptions. validateRequestQueryParamsUnexpected` (boolean) (default: false)                   |
| Validate request security                                              | This will validate that the request has the required security defined in the OpenApi schema.                                                                                                     | `validationOptions. validateRequestSecurity` (boolean) (default: false)                                |

### Response validation options <a href="#user-content-response-validation-options" id="user-content-response-validation-options"></a>

| Name                           | Description                                                                                                      | Property                                                                   |
| ------------------------------ | ---------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| Validate response body         | This will validate that the response matches the response body defined in the OpenApi schema.                    | `validationOptions. validateResponseBody` (boolean) (default: true)        |
| Validate response content type | This will validate that the response matches the response content type defined in the OpenApi schema.            | `validationOptions. validateResponseContentType` (boolean) (default: true) |
| Validate response status code  | This will validate that the response status code matches the response status code defined in the OpenApi schema. | `validationOptions. validateResponseStatusCode` (boolean) (default: true)  |

## Errors <a href="#user-content-errors" id="user-content-errors"></a>

| Phase              | Code                          | Error key                   | Description                                       |
| ------------------ | ----------------------------- | --------------------------- | ------------------------------------------------- |
| REQUEST            | `400 - BAD REQUEST`           | OAS\_VALIDATION\_ERROR\_KEY | Request does not match the OpenAPI Specification  |
| RESPONSE           | `500 - INTERNAL SERVER ERROR` | NO\_OAS\_RESOURCE\_KEY      | No resource configured                            |
| REQUEST / RESPONSE | `500 - INTERNAL SERVER ERROR` | NO\_OAS\_PROVIDED\_KEY      | No OpenAPI Specification provided                 |
| RESPONSE           | `500 - INTERNAL SERVER ERROR` | OAS\_VALIDATION\_ERROR\_KEY | Response does not match the OpenAPI Specification |
