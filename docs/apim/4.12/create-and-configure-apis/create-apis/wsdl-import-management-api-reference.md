# WSDL Import Management API Reference

## Management API

### Creating APIs via REST API

Submit a POST request to `/environments/{envId}/apis/_import/wsdl` with an `ImportWsdlDescriptor` payload:

| Property | Type | Description | Default |
|:---------|:-----|:------------|:--------|
| `payload` | string | Inline WSDL content (when `type` is `INLINE`) or a remote URL (when `type` is `URL`) | Required |
| `type` | string | Whether the payload is inline WSDL or a remote URL. Enum: `INLINE`, `URL` | `INLINE` |
| `withDocumentation` | boolean | Generate a Swagger documentation page from the converted OpenAPI specification | `false` |
| `withOASValidationPolicy` | boolean | Add an OAS Validation policy to every flow | `false` |
| `withPolicies` | array | Policy visitor IDs to apply (e.g., `rest-to-soap`, `json-validation`, `mock`, `validate-request`, `xml-validation`) | `null` |

The endpoint returns a 201 Created response with the full `ApiV4` definition.

### Updating APIs via REST API

Submit a PUT request to `/environments/{envId}/apis/{apiId}/_import/wsdl` with an `ImportWsdlDescriptor` payload. The request body schema and behavior match the creation endpoint. The endpoint returns a 200 OK response with the updated `ApiV4` definition.

**Error Conditions:**

| Exception | Condition |
|:----------|:----------|
| `ApiNotFoundException` | The target API does not exist |
| `InvalidPathsException` | The converted API paths conflict with existing APIs |

### Policy Dependency Injection

When `withPolicies` includes `rest-to-soap`, the `xml-json` policy is automatically added as a dependency to enable XML-to-JSON conversion. This dependency cannot be disabled.

**OAS Validation Policy Placement:**

| Condition | Request Flow | Response Flow |
|:----------|:-------------|:--------------|
| `withPolicies` is empty or `null` | OAS validation in single flow (request + response) | Same flow |
| `withPolicies` contains `rest-to-soap` | OAS validation in first flow (request only) | OAS validation in last flow (response only) |

When `withPolicies` includes `rest-to-soap`, OAS validation is split into two flows: request validation in the first flow and response validation in the last flow, allowing SOAP-to-REST transformation to occur before response validation.

### Flow Generation Rules

| `withPolicies` Value | Flows Generated |
|:---------------------|:----------------|
| `null` | Standard OpenAPI-derived flows |
| `[]` (empty list) | No flows (empty flows array) |
| `["rest-to-soap"]` | Standard OpenAPI-derived flows with REST-to-SOAP transformation policies applied |
