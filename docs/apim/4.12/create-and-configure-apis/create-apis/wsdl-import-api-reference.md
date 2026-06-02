# WSDL Import API Reference

## Management API

### Creating an API from WSDL

Call `POST /environments/{envId}/apis/_import/wsdl` with an `ImportWsdlDescriptor` payload to create a new v4 HTTP Proxy API from a WSDL document.

**Request Body:**

```json
{
  "payload": "<definitions/>",
  "type": "INLINE",
  "withDocumentation": true,
  "withOASValidationPolicy": true,
  "withPolicies": ["rest-to-soap"]
}
```

**Response:**

```json
{
  "id": "api-id",
  "name": "CalculatorService",
  "apiVersion": "1.0"
}
```

**Property Reference:**

| Property | Type | Description | Default |
|:---------|:-----|:------------|:--------|
| `payload` | string | Inline WSDL content (when `type` is `INLINE`) or a remote URL (when `type` is `URL`). | — |
| `type` | string | Whether the payload is inline WSDL or a remote URL. Allowed values: `INLINE`, `URL`. | `INLINE` |
| `withDocumentation` | boolean | Generate a Swagger documentation page from the converted OpenAPI spec. | `false` |
| `withOASValidationPolicy` | boolean | Add an OAS Validation policy to every flow. | `false` |
| `withPolicies` | array | Policy visitor IDs to apply (e.g., `rest-to-soap`, `json-validation`, `mock`, `validate-request`, `xml-validation`). | `null` |

### Updating an API from WSDL

Call `PUT /environments/{envId}/apis/{apiId}/_import/wsdl` with an `ImportWsdlDescriptor` payload to update an existing API by importing a WSDL document. The request and response format is identical to the create endpoint.
