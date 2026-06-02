# WSDL Import for v4 APIs: Concepts and Conversion

## Overview

WSDL import for v4 APIs lets you create or update a v4 HTTP Proxy API from a WSDL 1.1 document. The Management API converts the WSDL into an OpenAPI 3 specification, then runs it through the same v4 OpenAPI import pipeline used for Swagger/OpenAPI imports. You can supply the WSDL inline (file upload) or as a remote HTTP(S) URL (subject to import whitelist and private-network settings).

## Key Concepts

### WSDL-to-OpenAPI Conversion

During conversion, each SOAP operation becomes an OpenAPI path; the backend SOAP address becomes the proxy endpoint URL; XSD message parts become JSON request-body schemas. SOAP metadata is stored as OpenAPI extensions (`x-graviteeio-soap-envelope`, `x-graviteeio-soap-action`) for use by gateway policies. The API name is derived from the WSDL `<service>` element (e.g., `CalculatorService`), and the endpoint URL is derived from the `<soap:address>` location.

| WSDL Element | API Property |
|:-------------|:-------------|
| `<service name="CalculatorService">` | `api.name = "CalculatorService"` |
| `<soap:address location="http://localhost:8080/calculator"/>` | Endpoint configuration contains `"http://localhost:8080/calculator"` |
| `<operation name="Add">` | Flow with path derived from operation |

### Import Payload Types

You can provide WSDL content in two ways: **INLINE** (raw WSDL XML string) or **URL** (remote HTTP(S) endpoint). The `type` property defaults to `INLINE`. Remote URLs are subject to SSRF protection—private IPs and link-local addresses are blocked by default unless `allowImportFromPrivate` is enabled in the import configuration.

### REST-to-SOAP Transformation

When the REST to SOAP Transformer policy (`rest-to-soap`) is enabled, the import generates per-operation flows that translate REST/JSON calls to SOAP/XML. The `xml-json` policy is automatically added as a dependency. Without policies (when `withPolicies` is an empty list `[]`), no flows are generated—only API metadata and endpoints are updated.

### Policy-Driven Flow Generation

Flow generation depends on the `withPolicies` setting. If `withPolicies` is `null`, standard OpenAPI-derived flows are generated. If `withPolicies` is an empty list `[]`, no flows are generated (`skipFlows = true`). If `withPolicies` contains `["rest-to-soap"]`, flows are generated from WSDL operations with SOAP transformation policies applied.

### OAS Validation Policy Placement

When OpenAPI Specification Validation (`oas-validation`) is enabled for WSDL imports with REST-to-SOAP transformation, request validation is placed in the first flow (request step only) and response validation is placed in the last flow (response step only). This ordering ensures response validation occurs after SOAP transformation. For standard OpenAPI imports, validation is placed in a single flow covering both request and response.

## Prerequisites

- Gravitee API Management v4 environment
- `rest-to-soap` policy plugin installed (to enable REST-to-SOAP transformation)
- `oas-validation` policy plugin installed (to enable OpenAPI Specification Validation)
- WSDL 1.1 document (inline XML or accessible HTTP(S) URL)
- For remote WSDL URLs: URL must not be blocked by SSRF protection (private IPs require `allowImportFromPrivate = true`)
