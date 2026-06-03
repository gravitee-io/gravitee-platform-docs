# WSDL Import Management API Reference

## Updating an Existing API

Call `PUT /environments/{envId}/apis/{apiId}/_import/wsdl` with an `ImportWsdlDescriptor` payload. The descriptor payload must be a valid WSDL 1.1 document, either as inline content (`type: INLINE`) or a remote URL (`type: URL`). The WSDL is converted to OpenAPI and processed through the v4 OpenAPI import pipeline. If `withPolicies` is an empty list, all existing flows are removed and no new flows are generated. If `withPolicies` is `null`, flows are generated from the converted OpenAPI paths.

### Management API

| Method | Path | Description |
|:-------|:-----|:------------|
| POST | `/environments/{envId}/apis/_import/wsdl` | Create a v4 HTTP Proxy API from a WSDL descriptor. The WSDL is converted to OpenAPI and processed through the v4 OpenAPI import pipeline. Payload can be inline WSDL (`type: INLINE`) or a remote URL (`type: URL`). User must have the ENVIRONMENT_API[CREATE] permission. |
| PUT | `/environments/{envId}/apis/{apiId}/_import/wsdl` | Update an existing API by importing a WSDL descriptor. The descriptor payload must be a valid WSDL 1.1 document, either as inline content or a remote URL. User must have the API_DEFINITION[UPDATE] permission. |

## Restrictions

- WSDL import requires WSDL 1.1 format (WSDL 2.0 is not supported).
- The `rest-to-soap` policy must be installed for the REST to SOAP Transformer toggle to appear in the Console.
- The `oas-validation` policy must be installed for the OpenAPI Specification Validation toggle to be enabled.
- When `withPolicies` is an empty list, no flows are generated (all existing flows are removed).
- SSRF protection applies to remote WSDL URLs; private IP addresses are blocked unless private imports are explicitly allowed.
- The `skipFlows` flag is set to `true` only when `withPolicies` is an empty list (not `null`).
- Supported file types for WSDL upload are `.wsdl` and `.xml`.

## Related Changes


The WSDL format card in the API import form is now enabled (previously disabled with a "Coming soon" tooltip). When the `rest-to-soap` policy is installed, a new toggle appears in the [import options step](creating-a-v4-api-from-wsdl-in-the-console.md#import-options): "Apply REST to SOAP Transformer policy" (default: enabled).
 When this toggle is enabled, the "Generate a Swagger documentation page" and "Add an OAS Validation policy" options are also enabled and checked by default (if the `oas-validation` policy is installed). When the toggle is disabled, both dependent options are disabled and unchecked. The review step displays the REST to SOAP Transformer status as "Enabled" or "Disabled" when the policy is installed.
