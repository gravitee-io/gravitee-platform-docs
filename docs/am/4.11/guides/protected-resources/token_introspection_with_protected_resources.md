### Token Introspection with Protected Resources

When a client introspects a token, the system resolves the audience and certificate using the following logic:

#### Single-Audience Tokens

For tokens with a single audience value, the system performs a sequential lookup:

1. Check if the audience matches an Application `clientId`
2. If no match, check if the audience matches a Protected Resource `clientId`
3. If no match, validate the audience as an RFC 8707 resource identifier

If a Protected Resource is matched, the system uses its configured certificate to verify the JWT signature. For HMAC-based verification, an empty string is used instead of a certificate ID.

#### Multi-Audience Tokens

Tokens with multiple audience values always use RFC 8707 resource identifier validation. The Application and Protected Resource `clientId` matching steps are bypassed.

#### Failure Behavior

If no match is found during audience resolution, the introspection request fails with `InvalidTokenException("Client or resource not found: <aud>")`.

#### Legacy RFC 8707 Validation Mode


The gateway [environment property](../../../getting-started/configuration/configure-am-gateway/) `legacy.rfc8707.enabled` (default `true`) controls legacy RFC 8707 validation behavior.
 When enabled, the caller's client ID must match the audience for RFC 8707 resource identifier validation to succeed. If the caller's client ID does not match, the request fails with `InvalidTokenException("The token was not issued for this client")`.

