---
hidden: true
---

# OAS Validation

{% hint style="warning" %}
**This feature requires** **Gravitee's Enterprise Edition. For more information about Gravitee Enterpise Edition, see** [Gravitee APIM Enterprise Edition](https://documentation.gravitee.io/apim/overview/gravitee-apim-enterprise-edition).
{% endhint %}

## Overview

The `oas-validation` policy validates aspects of the request and response from an upstream server definition according to the embedded OpenAPI Specification. In Gravitee, OAS files are not directly linked with the API definition, but you can use the specification as a resource in the API to define documentation and define flows and policies on the API.

You can load the load the OpenAPI specification with any of the following methods:

* &#x20;Load the OpenAPI specification from YAML or JSON inserted inline with the API.
* &#x20;Load it into a Content Provider Resource on the API and evolve that resource separately
* &#x20;Add the OAS Validation policy when importing a v4 proxy API from an OpenAPI specification to relevant paths and flows.&#x20;

{% hint style="info" %}
This policy was designed to work with at least version 4.4.0 of API Management (APIM).
{% endhint %}

## Examples

{% hint style="warning" %}
You can apply this policy to only v4 HTTP proxy APIs. You cannot apply this policy to v4 message APIs, v4 TCP proxy APIs or v2 APIs.
{% endhint %}

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

## Configuration

### Phases

The `oas-validation` policy supports the phases that are checked in the following table:

<table data-full-width="false"><thead><tr><th width="202">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="198">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>true</td><td>onRequest</td><td>true</td></tr><tr><td>onResponse</td><td>true</td><td>onResponse</td><td>true</td></tr><tr><td>onRequestContent</td><td>false</td><td>onMessageRequest</td><td>false</td></tr><tr><td>onResponseContent</td><td>false</td><td>onMessageResponse</td><td>false</td></tr></tbody></table>

### Options

You can configure the `oas-validation` policy with the following options:

#### Common options <a href="#user-content-common-options" id="user-content-common-options"></a>

<table><thead><tr><th width="137">Name</th><th width="195">Property</th><th data-type="checkbox">Required</th><th width="170">Description</th><th width="141">Type</th><th>Default</th></tr></thead><tbody><tr><td>OpenApi source from</td><td><code>sourceJson</code> or <code>sourceYaml</code> or <code>sourceUrl</code> or <code>resourceName</code></td><td>true</td><td>OpenAPI Specification in JSON or YAML format.</td><td>string</td><td><code>resourceName</code></td></tr><tr><td>Base path</td><td><code>basePath</code></td><td>false</td><td>Optional base path. This can be useful if e.g. your Swagger specification has been created for a public URL but you are validating requests against an internal URL where the URL paths differ.</td><td>string</td><td></td></tr><tr><td>Return detailed error report</td><td><code>validationOptions. returnDetailedErrorReport</code></td><td>false</td><td>Only for Bad Request (400) error. Return in the response the detailed error report. Like Schema validation errors on request/response body. This can be useful for debugging but can expose OpenApi schema details.</td><td>boolean</td><td>true</td></tr><tr><td>Strict operation path matching</td><td><code>validationOptions. strictOperationPathMatching</code></td><td>false</td><td>If true, a trailing slash indicates a different path than without.</td><td>boolean</td><td>true</td></tr></tbody></table>

#### Request Validation Options

{% hint style="info" %}
None of these options are required.
{% endhint %}

<table><thead><tr><th>Name</th><th width="201">Property</th><th>Description</th><th>Type</th><th>Default</th></tr></thead><tbody><tr><td>Validate path and method exist</td><td><code>validationOptions. validateRequestPathAndMethod</code></td><td>This will validate that the path (minus the base path) and associated HTTP method matches one of the path patterns defined in the OpenApi schema.</td><td>boolean</td><td>true</td></tr><tr><td>Validate request content type</td><td><code>validationOptions. validateRequestContentType</code></td><td>This will validate that the request matches the requestBody.content types defined in the OpenApi schema.</td><td>boolean</td><td>true</td></tr><tr><td>Validate request body</td><td><code>validationOptions. validateRequestBody</code></td><td>This will validate that the request matches the request body defined in the OpenApi schema. This is only apply if the content type is <code>application/json</code> or <code>application/x-www-form-urlencoded</code>.</td><td>boolean</td><td>true</td></tr><tr><td>Validate request parameters (PathParams, QueryParams, Headers, Cookie)</td><td><code>validationOptions. validateRequestParameters</code></td><td>This will validate that parameters marked as required for the request exist and all request parameters match the valid values.</td><td>boolean</td><td>true</td></tr><tr><td>Additional options for request parameters validation</td><td><code>validationOptions. validateRequestParameters</code></td><td>Uncheck the request parameters that you don’t want to validate. (may have an impact on parameter or security validation)</td><td>enum</td><td>[QUERY_PARAMS", "HEADERS", "COOKIES"]</td></tr><tr><td>validationOptions. validateRequestQueryParamsUnexpected</td><td><code>validationOptions. validateRequestQueryParamsUnexpected</code> </td><td>This will validate that no additional query parameters are passed that are not found in the OpenApi schema.</td><td>boolean</td><td>false</td></tr><tr><td>Validate request security</td><td><code>validationOptions. validateRequestSecurity</code></td><td>This will validate that the request has the required security defined in the OpenApi schema.</td><td>boolean</td><td>false</td></tr></tbody></table>

#### Response Validation Options

{% hint style="info" %}
None of these optinos are required.
{% endhint %}

| Name                           | Property                                         | Description                                                                                                      | Type    | Default |
| ------------------------------ | ------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------- | ------- | ------- |
| Validate response body         | `validationOptions. validateResponseBody`        | This will validate that the response matches the response body defined in the OpenApi schema.                    | boolean | true    |
| Validate response content type | `validationOptions. validateResponseContentType` | This will validate that the response matches the response content type defined in the OpenApi schema.            | boolean | true    |
| Validate response status code  | `validationOptions. validateResponseStatusCode`  | This will validate that the response status code matches the response status code defined in the OpenApi schema. | boolean | true    |

## Compatibility matrix

The following table shows the compatibility matrix for APIM and the `json-validation` policy:

| Plugin Version | Supported APIM versions |
| -------------- | ----------------------- |
| 1.x            | 4.4.0 and above         |

## Errors

| Phase              | Code                          | Error key                   | Description                                       |
| ------------------ | ----------------------------- | --------------------------- | ------------------------------------------------- |
| REQUEST            | `400 - BAD REQUEST`           | OAS\_VALIDATION\_ERROR\_KEY | Request does not match the OpenAPI Specification  |
| RESPONSE           | `500 - INTERNAL SERVER ERROR` | NO\_OAS\_RESOURCE\_KEY      | No resource configured                            |
| REQUEST / RESPONSE | `500 - INTERNAL SERVER ERROR` | NO\_OAS\_PROVIDED\_KEY      | No OpenAPI Specification provided                 |
| RESPONSE           | `500 - INTERNAL SERVER ERROR` | OAS\_VALIDATION\_ERROR\_KEY | Response does not match the OpenAPI Specification |

## Changelogs

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-oas-validation/blob/main/CHANGELOG.md" %}
