# Management API Reference: WSDL Import Endpoints

## Management API

| Method | Path | Description |
|:-------|:-----|:------------|
| POST | `/environments/{envId}/apis/_import/wsdl` | Create a v4 HTTP Proxy API from a WSDL descriptor. The WSDL is converted to OpenAPI and processed through the v4 OAI import pipeline. Payload can be inline WSDL (type: INLINE) or a remote URL (type: URL). User must have the ENVIRONMENT_API[CREATE] permission. |
| PUT | `/environments/{envId}/apis/{apiId}/_import/wsdl` | Update an existing API by importing a WSDL descriptor. The descriptor payload must be a valid WSDL 1.1 document, either as inline content or a remote URL. User must have the API_DEFINITION[UPDATE] permission. |

Both endpoints accept an `ImportWsdlDescriptor` payload. The same import options (REST to SOAP Transformer, documentation page, OpenAPI Specification Validation) apply to both endpoints.
