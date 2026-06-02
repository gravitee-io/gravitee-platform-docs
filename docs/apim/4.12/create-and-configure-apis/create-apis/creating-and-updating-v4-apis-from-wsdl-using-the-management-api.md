# Creating and Updating v4 APIs from WSDL Using the Management API

### Management API

**Create a new API:**

```http
POST /environments/{envId}/apis/_import/wsdl
Content-Type: application/json

{
  "payload": "<definitions xmlns='http://schemas.xmlsoap.org/wsdl/'>...</definitions>",
  "type": "INLINE",
  "withDocumentation": true,
  "withOASValidationPolicy": true,
  "withPolicies": ["rest-to-soap"]
}
```

**Request fields:**

| Field | Type | Description |
|:------|:-----|:------------|
| `payload` | string | Inline WSDL content (when `type` is `INLINE`) or a remote URL (when `type` is `URL`) |
| `type` | string | Whether the payload is inline WSDL or a remote URL. Enum: `INLINE`, `URL`. Default: `INLINE` |
| `withDocumentation` | boolean | Generate a Swagger documentation page from the converted OpenAPI spec |
| `withOASValidationPolicy` | boolean | Add an OAS Validation policy to every flow |
| `withPolicies` | array | Policy visitor IDs to apply (e.g., `rest-to-soap`, `json-validation`, `mock`, `validate-request`, `xml-validation`) |

**Response:**

```json
{
  "id": "api-id",
  "name": "CalculatorService",
  "apiVersion": "1.0",
  ...
}
```

The `withPolicies` array accepts policy visitor IDs (`rest-to-soap`, `json-validation`, `mock`, `validate-request`, `xml-validation`). When `withPolicies` is an empty list `[]`, no flows are generated. When `withPolicies` contains `rest-to-soap`, the `xml-json` policy is automatically added.

**Error responses:**

| Exception | Description |
|:----------|:------------|
| `InvalidPathsException` | Imported paths conflict with existing APIs |
| `InvalidApiDefinitionException` | Converted OpenAPI spec is invalid |

## Updating an Existing API

### Management API

See [Management API](#management-api) above for details.
