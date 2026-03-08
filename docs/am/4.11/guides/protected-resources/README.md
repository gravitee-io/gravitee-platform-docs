Protected Resources in Gravitee Access Management 4.11 now support full OAuth 2.0 client lifecycle management, including secret rotation, certificate-based authentication, and token exchange flows. These enhancements enable MCP Servers to authenticate using industry-standard OAuth 2.0 mechanisms and secure downstream API calls with access tokens. This feature is designed for API administrators managing resource servers and developers integrating MCP-based authorization systems.

### Token Introspection with Protected Resources

Token introspection resolves audience claims (`aud`) against both Applications and Protected Resources. The resolution order for a JWT with a single audience is:

1. Check for a matching Application client ID
2. Search Protected Resources
3. Validate against RFC 8707 resource identifiers

For JWTs with multiple audiences, all values are validated as resource identifiers. If a Protected Resource has a certificate configured, the system uses it for JWT signature verification. Otherwise, HMAC validation is assumed.

### Prerequisites

* Gravitee Access Management 4.11.0 or later
* Domain with OAuth 2.0 enabled
* For token exchange: domain-level `tokenExchangeSettings.enabled = true`
* For certificate-based authentication: valid certificate uploaded to the domain
* Appropriate permissions:
  * `PROTECTED_RESOURCE`: READ, UPDATE, DELETE
  * `PROTECTED_RESOURCE_MEMBER`: LIST, CREATE, DELETE
