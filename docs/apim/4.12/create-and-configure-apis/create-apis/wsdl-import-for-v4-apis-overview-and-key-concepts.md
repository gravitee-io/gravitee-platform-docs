# WSDL Import for v4 APIs: Overview and Key Concepts

## Overview

WSDL import for v4 APIs allows you to create or update a v4 HTTP Proxy API from a WSDL 1.1 document. The Management API converts the WSDL into an OpenAPI 3 specification, then processes it through the same v4 OpenAPI import pipeline used for Swagger/OpenAPI imports. You can supply the WSDL inline (file upload) or as a remote HTTP(S) URL (subject to SSRF protection configured via import whitelist and private-network settings).

## Key Concepts

### WSDL-to-OpenAPI Conversion

During conversion:

* Each SOAP operation becomes an OpenAPI path
* The backend SOAP address becomes the proxy endpoint URL
* XSD message parts become JSON request-body schemas
* SOAP metadata is stored as OpenAPI extensions (`x-graviteeio-soap-envelope`, `x-graviteeio-soap-action`) for use by gateway policies

The conversion supports WSDL 1.1 only and may not preserve all WSDL semantics.

### Import Payload Types

| Type | Description | Example |
|:-----|:------------|:--------|
| `INLINE` | Raw WSDL content uploaded as a string | `<definitions xmlns="http://schemas.xmlsoap.org/wsdl/">...</definitions>` |
| `URL` | Remote HTTP(S) URL to fetch WSDL from | `https://example.com/calculator.wsdl` |

The `type` field defaults to `INLINE`. Remote WSDL URLs are subject to SSRF protection (whitelist, private IP blocking) configured via `ImportConfiguration`.

### REST-to-SOAP Transformation

The REST to SOAP Transformer policy (`rest-to-soap`) adds per-operation flows that translate REST/JSON calls to SOAP/XML. When enabled, the `xml-json` policy is automatically added as a dependency. Without policies, no flows are generated—only API metadata and endpoints are updated.
