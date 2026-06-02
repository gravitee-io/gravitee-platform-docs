# WSDL Import: Restrictions and Related Changes

## Restrictions

- WSDL import only supports WSDL 1.1 documents.
- WSDL is converted to OpenAPI 3.x internally; SOAP-specific features (e.g., WS-Security headers) are not preserved in the OpenAPI specification.
- When `withPolicies` is an empty list (`[]`), no flows are generated (the API will have an empty flows array).
- The `rest-to-soap` policy automatically adds the `xml-json` policy as a dependency; this cannot be disabled.
- WSDL imports from private IP ranges (localhost, 127.0.0.1, 192.168.x.x, 169.254.x.x) are blocked by default unless `allowImportFromPrivate` is enabled in the import configuration.
- File protocol (`file:///`) and FTP URLs (`ftp://`) are always blocked.
- The "Apply REST to SOAP Transformer policy" toggle is only visible when the `rest-to-soap` policy plugin is installed; otherwise, the toggle is hidden and WSDL import behaves like a standard OpenAPI import.
- When REST-to-SOAP is enabled for WSDL, the OAS validation policy is split into two flows: request validation in the first flow, response validation in the last flow.
- Invalid WSDL XML, empty payloads, or invalid URL syntax result in `SwaggerDescriptorException` with the message "Failed to convert WSDL to OpenAPI specification."
- Blocked URLs result in `UrlForbiddenException`.

## Related Changes

### UI Changes

The WSDL format card in the v4 API import form is now enabled and selectable, replacing the previous "Coming soon" disabled state.

The import options step displays a new "Apply REST to SOAP Transformer policy" toggle for WSDL format, which controls the visibility and default state of the "Create documentation page from spec" and "Add OAS Validation policy" toggles.

The review step displays the REST-to-SOAP Transformer status as either Enabled or Disabled.

WSDL format now supports both file upload (inline content) and remote URL import sources.

### API Changes

Two new REST API endpoints are available:

| Method | Path | Description |
|:-------|:-----|:------------|
| POST | `/environments/{envId}/apis/_import/wsdl` | Create a v4 HTTP Proxy API from a WSDL descriptor |
| PUT | `/environments/{envId}/apis/{apiId}/_import/wsdl` | Update an existing API by importing a WSDL descriptor |
