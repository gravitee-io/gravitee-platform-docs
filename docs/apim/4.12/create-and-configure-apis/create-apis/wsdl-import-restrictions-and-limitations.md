# WSDL Import Restrictions and Limitations

## Restrictions

- WSDL import supports **WSDL 1.1** only.
- WSDL is converted to **OpenAPI 3.x** internally. The conversion may not preserve all WSDL semantics.
- When `withPolicies` is an empty list `[]`, **no flows are generated**. The API has an empty flow list.
- The REST-to-SOAP policy automatically adds the `xml-json` policy as a dependency.
- OAS validation policy response validation is **deferred to the last flow** when WSDL format is used with policies. This allows the REST-to-SOAP transformation to execute first.
- Remote WSDL URLs are subject to SSRF protection (whitelist, private IP blocking) configured via `ImportConfiguration`.
- The documentation page generated from WSDL contains the **converted OpenAPI YAML**, not the original WSDL XML.
- WSDL import is available for **v4 HTTP Proxy APIs** only.
