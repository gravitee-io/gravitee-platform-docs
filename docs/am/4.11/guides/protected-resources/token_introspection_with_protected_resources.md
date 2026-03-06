### Token Introspection with Protected Resources

When introspecting a token, the system resolves the audience (`aud` claim) using the following process:

1. Check if the audience matches an Application client ID
2. If not found, check if the audience matches a Protected Resource client ID
3. For single-audience tokens: if neither is found, fall back to RFC 8707 resource identifier validation
4. For multi-audience tokens: validate all audiences as resource identifiers

If the audience cannot be resolved through any of these methods, introspection fails with the error message `"The token is invalid"` and detail `"Client or resource not found: {aud}"`.

This audience resolution process enables Protected Resources to participate as token recipients in OAuth 2.0 flows. The system prioritizes Applications over Protected Resources when matching client IDs.
