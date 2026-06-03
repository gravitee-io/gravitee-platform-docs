# WSDL Import for v4 APIs: Overview and Conversion Process

## Overview

WSDL import for v4 APIs allows you to create or update a v4 HTTP Proxy API from a WSDL 1.1 document. The Management API converts the WSDL into an OpenAPI 3 specification, then processes it through the same v4 OpenAPI import pipeline used for Swagger/OpenAPI imports. You can supply the WSDL inline (file upload) or as a remote HTTP(S) URL (subject to import whitelist and private-network settings).

## Key Concepts

### WSDL-to-OpenAPI Conversion

During conversion:

* Each SOAP operation becomes an OpenAPI path
* The backend SOAP address becomes the proxy endpoint URL
* XSD message parts become JSON request-body schemas
* SOAP metadata is stored as OpenAPI extensions (`x-graviteeio-soap-envelope`, `x-graviteeio-soap-action`) for use by gateway policies

The converted OpenAPI 3 YAML is processed through the existing v4 OpenAPI import pipeline.

### Import Payload Types

| Type | Description | Example |
|:-----|:------------|:--------|
| INLINE | Raw WSDL content uploaded as a string (file upload) | Full WSDL 1.1 XML document |
| URL | Remote HTTP(S) URL pointing to a WSDL document | `https://example.com/service.wsdl` |

The `type` property defaults to `INLINE`. When `type` is `URL`, the URL is validated against the import whitelist and private-network settings. Private IP addresses (localhost, 127.0.0.1, 169.254.x.x, 192.168.x.x) are blocked unless private imports are explicitly allowed.

### REST-to-SOAP Transformation

The REST to SOAP Transformer policy (`rest-to-soap`) adds per-operation flows that translate REST/JSON calls to SOAP/XML. When enabled, the `xml-json` policy is automatically added to the policy list. Without policies, no flows are generated—only API metadata and endpoints are updated.

### Policy Placement

When the REST to SOAP Transformer is enabled and policies are applied, OpenAPI Specification Validation is split into two flows:

* **Request-only validation** in the first flow (named "OpenAPI Specification Validation")
* **Response-only validation** in the last flow (also named "OpenAPI Specification Validation")

This ordering ensures response validation occurs after SOAP transformation. For non-WSDL imports or when no policies are applied, validation remains in a single flow.

## Prerequisites

* WSDL 1.1 document (WSDL 2.0 is not supported)
* `ENVIRONMENT_API[CREATE]` permission (for creating APIs)
* `API_DEFINITION[UPDATE]` permission (for updating existing APIs)
* `rest-to-soap` policy installed (required for REST-to-SOAP transformation toggle to appear in Console)
* `oas-validation` policy installed (required for OpenAPI Specification Validation toggle to be enabled)


