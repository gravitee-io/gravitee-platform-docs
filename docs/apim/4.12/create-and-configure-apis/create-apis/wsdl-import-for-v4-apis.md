# WSDL Import for v4 APIs

## Overview

WSDL Import for v4 APIs lets you create or update a v4 HTTP Proxy API from a WSDL 1.1 document. The Management API converts the WSDL into an OpenAPI 3 specification, then processes it through the same v4 OpenAPI import pipeline used for Swagger/OpenAPI imports. You can supply the WSDL inline (file upload) or as a remote HTTP(S) URL, subject to import whitelist and private-network settings.

## Key Concepts

### WSDL-to-OpenAPI Conversion

During conversion, each SOAP operation becomes an OpenAPI path. The backend SOAP address becomes the proxy endpoint URL. XSD message parts become JSON request-body schemas. SOAP metadata is stored as OpenAPI extensions (`x-graviteeio-soap-envelope`, `x-graviteeio-soap-action`) for use by gateway policies. The imported API name is extracted from the WSDL `<service>` element's `name` attribute (e.g., `CalculatorService`).

### Import Payload Types

| Type | Description | Example |
|:-----|:------------|:--------|
| INLINE | Raw WSDL content uploaded as a string | Full WSDL 1.1 document text |
| URL | Remote HTTP(S) URL pointing to a WSDL document | `https://example.com/service?wsdl` |

The default type is INLINE. When using URL, the payload is validated against the environment's import whitelist and private-network restrictions.

### REST to SOAP Transformer

The REST to SOAP Transformer policy (`rest-to-soap`) adds per-operation flows that translate REST/JSON calls to SOAP/XML. When enabled, the `xml-json` policy is automatically added to the policy list. Without policies, no flows are generated—only API metadata and endpoints are updated.

## Prerequisites

- v4 HTTP Proxy API support enabled in the environment
- ENVIRONMENT_API[CREATE] permission to create APIs via WSDL import
- API_DEFINITION[UPDATE] permission to update existing APIs via WSDL import
- WSDL 1.1 document with a valid `<service>` element and SOAP address binding
- (Optional) `rest-to-soap` policy plugin installed to enable REST-to-SOAP transformation
- (Optional) `oas-validation` policy plugin installed to enable OpenAPI Specification Validation

## Gateway Configuration

No gateway-specific configuration is required for WSDL import. The feature uses the same gateway settings as OpenAPI import.

## Creating an API from WSDL

Navigate to **APIs** > **Import API** and select the **WSDL** format. Supported file types are `.wsdl` and `.xml`.

1. Select **WSDL** as the import format.
2. Choose **File Upload** to provide inline WSDL content or **Remote URL** to fetch from an HTTP(S) endpoint.
3. Enter the WSDL content or URL in the **Payload** field.
4. Toggle **Apply REST to SOAP Transformer policy** to enable REST-to-SOAP transformation (visible only when the `rest-to-soap` policy is installed; default: enabled).
5. Toggle **Generate a Swagger documentation page** to publish a Swagger page from the converted OpenAPI specification (enabled by default when REST to SOAP Transformer is on).
6. Toggle **Add an OAS Validation policy** to validate requests and responses against the converted OpenAPI spec (enabled by default when REST to SOAP Transformer is on and the `oas-validation` policy is installed).
7. Review the import settings and confirm.

| Field | Description | Default |
|:------|:------------|:--------|
| **Payload** | Inline WSDL content (type: INLINE) or remote URL (type: URL) | — |
| **Type** | Whether the payload is inline WSDL or a remote URL | INLINE |
| **Apply REST to SOAP Transformer policy** | Adds per-operation flows that translate REST/JSON calls to SOAP/XML; automatically includes `xml-json` policy | Enabled (when `rest-to-soap` policy is installed) |
| **Generate a Swagger documentation page** | Publishes a Swagger page from the converted OpenAPI specification | Enabled (when REST to SOAP Transformer is on) |
| **Add an OAS Validation policy** | Validates requests and responses against the converted OpenAPI spec | Enabled (when REST to SOAP Transformer is on and `oas-validation` policy is installed) |

When REST to SOAP Transformer is disabled, the documentation and OAS validation toggles are disabled and unchecked.

## Management API Reference

### Create API from WSDL

**Endpoint:** `POST /environments/{envId}/apis/_import/wsdl`

Creates a v4 HTTP Proxy API from a WSDL descriptor. The WSDL is converted to OpenAPI and processed through the v4 OpenAPI import pipeline.

**Request body:**

```json
{
  "payload": "string",
  "type": "INLINE",
  "withDocumentation": true,
  "withOASValidationPolicy": true,
  "withPolicies": ["rest-to-soap"]
}
```

| Property | Type | Description | Default |
|:---------|:-----|:------------|:--------|
| `payload` | string | Inline WSDL content (when type is INLINE) or a remote URL (when type is URL) | — |
| `type` | string | Whether the payload is inline WSDL or a remote URL (`INLINE` or `URL`) | `INLINE` |
| `withDocumentation` | boolean | Generate a Swagger documentation page from the converted OpenAPI spec | `false` |
| `withOASValidationPolicy` | boolean | Add an OAS Validation policy to every flow | `false` |
| `withPolicies` | array | Policy visitor IDs to apply (e.g., `rest-to-soap`, `json-validation`, `mock`, `validate-request`, `xml-validation`) | `null` |

**Policy dependency injection:**
- When `withPolicies` contains `rest-to-soap`, the `xml-json` policy is automatically added.
- When `withPolicies` is an empty list, no flows are generated (`skipFlows = true`).
- When `withPolicies` is `null`, flows are generated from OpenAPI paths (`skipFlows = false`).

**OAS Validation policy placement:**
- When the format is WSDL and `withPolicies` is non-empty, the OAS Validation policy is added to the first flow (request phase) and the last flow (response phase, deferred).
- For non-WSDL formats or when `withPolicies` is empty/null, the OAS Validation policy is added to the same flow (not deferred).

### Update API from WSDL

**Endpoint:** `PUT /environments/{envId}/apis/{apiId}/_import/wsdl`

Updates an existing API by importing a WSDL descriptor. The descriptor payload must be a valid WSDL 1.1 document, either as inline content or a remote URL.

**Request body:** Same as Create API from WSDL.

## Restrictions

- Only WSDL 1.1 documents are supported.
- WSDL must contain a valid `<service>` element with a SOAP address binding.
- When `withPolicies` is an empty list, no flows are generated—all path-based flows are skipped.
- OAS Validation policy response validation is deferred to the last flow only when the format is WSDL and `withPolicies` is non-empty.
- Remote URL import respects the same whitelist and private IP restrictions as OpenAPI import. Blocked patterns (when `allowImportFromPrivate = false`): `http://localhost:*`, `http://127.0.0.1/*`, `http://169.254.*` (link-local), `http://192.168.*` (private).
- The REST to SOAP Transformer toggle in the Console is only visible when the `rest-to-soap` policy plugin is installed in the environment.
- The OAS Validation toggle in the Console is only visible when the `oas-validation` policy plugin is installed in the environment.

## Related Changes

The Console import form now enables the WSDL format card (previously disabled with a "Coming soon" tooltip). Remote URL source is now available for WSDL format alongside Gravitee and OpenAPI formats. When REST to SOAP Transformer is enabled, the documentation and OAS validation toggles are enabled and checked by default; when disabled, these toggles are disabled and unchecked. The review step displays the REST to SOAP Transformer status as a badge (Enabled or Disabled). URL validation for WSDL imports uses the same SSRF protection as OpenAPI imports, blocking private and link-local addresses when `allowImportFromPrivate` is false.
