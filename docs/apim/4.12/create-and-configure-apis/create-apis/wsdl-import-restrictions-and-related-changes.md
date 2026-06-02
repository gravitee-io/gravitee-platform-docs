
# WSDL import: Restrictions and related changes


## Restrictions

WSDL import is subject to the following restrictions:

* **WSDL 1.1 only**: WSDL import supports WSDL 1.1 documents. is not supported.
* **v4 HTTP Proxy APIs only**: WSDL import creates v4 HTTP Proxy APIs. v2 APIs and Message APIs are not supported.
* **SSRF protection**: Remote WSDL URLs are subject to Server-Side Request Forgery (SSRF) protection. The following URL patterns are blocked by default unless `allowImportFromPrivate = true`:
 * `localhost`
 * `127.0.0.1`
 * `169.254.x.x` (link-local addresses)
 * `192.168.x.x` (private network addresses)
 * `file://` scheme
 * `ftp://` scheme
* **Documentation format**: The documentation page generated from a WSDL import contains the converted OpenAPI YAML specification, not the original WSDL XML.
* **Empty policy list behavior**: When `withPolicies` is an empty list `[]`, no flows are generated. The API will have no policies.
* **REST to SOAP Transformer visibility**: The REST to SOAP Transformer policy toggle is only visible when the `rest-to-soap` policy plugin is installed in the environment.
* **OAS validation flow structure**: When the REST to SOAP Transformer is enabled, the OAS validation policy is split into two flows: request validation in the first flow and response validation in the last flow.
* **SOAP 1.2 features**: WSDL import does not support SOAP 1.2-specific features beyond basic binding detection.

## Related Changes

The WSDL import feature introduces the following changes to the Console:

* **Format selection**: The WSDL format card in the API import wizard is now enabled and selectable. Previously, this card was disabled with a "Coming soon" tooltip.
* **Options step**: When the `rest-to-soap` policy is installed, the options step displays a new toggle for applying the REST to SOAP Transformer policy. This toggle controls the visibility and default state of the documentation and OAS validation toggles.
* **Review step**: When the `rest-to-soap` policy is installed, the review step displays the REST to SOAP Transformer status (Enabled or Disabled).
* **Service layer**: The Console service layer adds `importWsdlApi` and `updateApiFromWsdl` methods to call the new Management API endpoints.
