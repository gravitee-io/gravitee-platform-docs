### Token Introspection with Protected Resources

Token introspection now resolves both Applications and Protected Resources as valid audiences. When a token's `aud` claim is validated, the system follows this resolution workflow:

1. Check for an Application with matching `clientId`
2. If no Application is found, search for a Protected Resource with matching `clientId`
3. If neither is found, fall back to resource identifier validation per RFC 8707
4. For multi-audience tokens, validation always uses the resource identifier flow

If resolution fails, the error message is `"Client or resource not found: {aud}"`.

This capability enables Protected Resources to introspect tokens issued to them without requiring Application registration.
