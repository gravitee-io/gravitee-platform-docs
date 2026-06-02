# WSDL Import Management API Reference

## Management API

The WSDL import feature exposes two Management API endpoints for creating and updating v4 HTTP Proxy APIs from WSDL descriptors. Both endpoints accept an `ImportWsdlDescriptor` payload and return the created or updated API definition. The WSDL is converted to OpenAPI and processed through the v4 OpenAPI import pipeline.

| Method | Endpoint | Description |
|:-------|:---------|:------------|
| POST | `/environments/{envId}/apis/_import/wsdl` | Create a v4 HTTP Proxy API from a WSDL descriptor. The WSDL is converted to OpenAPI and processed through the v4 OAI import pipeline. Payload can be inline WSDL (type: INLINE) or a remote URL (type: URL). User must have the ENVIRONMENT_API[CREATE] permission. |
| PUT | `/environments/{envId}/apis/{apiId}/_import/wsdl` | Update an existing API by importing a WSDL descriptor. The descriptor payload must be a valid WSDL 1.1 document, either as inline content or a remote URL. User must have the API_DEFINITION[UPDATE] permission. |

### ImportWsdlDescriptor Payload Structure

The `ImportWsdlDescriptor` payload defines the WSDL source and import options:

| Field | Type | Required | Default | Description |
|:------|:-----|:---------|:--------|:------------|
| `payload` | string | Yes | — | Inline WSDL content (when type is INLINE) or a remote URL (when type is URL). |
| `type` | enum | No | INLINE | Whether the payload is inline WSDL or a remote URL. Valid values: INLINE, URL. |
| `withDocumentation` | boolean | No | — | Generate a Swagger documentation page from the converted OpenAPI spec. |
| `withOASValidationPolicy` | boolean | No | — | Add an OAS Validation policy to every flow. |
| `withPolicies` | array of strings | No | — | Policy visitor IDs to apply (e.g. rest-to-soap, json-validation, mock, validate-request, xml-validation). |

**Field Behaviors:**

* **`payload`**: Contains inline WSDL XML when `type` is INLINE, or a remote URL when `type` is URL.
* **`withPolicies`**: When the array contains `rest-to-soap`, the platform automatically adds `xml-json` to the policy list. If `withPolicies` is an empty array, flow generation is skipped entirely. If `withPolicies` is null, flows are generated from OpenAPI paths without policies.
* **`withDocumentation`**: When true, a Swagger page is created with the converted OpenAPI YAML content (not the raw WSDL XML).
* **`withOASValidationPolicy`**: When true and `withPolicies` is non-empty, OAS validation is split into two flows (request in first flow, response in last flow).

### Example Payload

```typescript
export interface ImportWsdlDescriptor {
 /** The raw WSDL content (INLINE) or the URL to fetch it from (URL). */
 payload: string;
 /** Whether the payload is an inline WSDL string or a remote URL. Defaults to INLINE. */
 type?: 'INLINE' | 'URL';
 /** Generate a Swagger documentation page from the converted OpenAPI spec. */
 withDocumentation?: boolean;
 /** Add an OAS Validation policy to every flow. */
 withOASValidationPolicy?: boolean;
 /** Policy visitor IDs to apply (e.g. 'rest-to-soap', 'json-validation'). */
 withPolicies?: string[];
}
```

### Example Payload (OpenAPI YAML)

```yaml
ImportWsdlDescriptor:
 type: object
 required:
 - payload
 properties:
 payload:
 type: string
 description: Inline WSDL content (when type is INLINE) or a remote URL (when type is URL).
 type:
 type: string
 description: Whether the payload is inline WSDL or a remote URL.
 enum:
 - INLINE
 - URL
 default: INLINE
 withDocumentation:
 type: boolean
 description: Generate a Swagger documentation page from the converted OpenAPI spec.
 withOASValidationPolicy:
 type: boolean
 description: Add an OAS Validation policy to every flow.
 withPolicies:
 type: array
 description: Policy visitor IDs to apply (e.g. rest-to-soap, json-validation, mock, validate-request, xml-validation).
 items:
 type: string
 uniqueItems: true
```
