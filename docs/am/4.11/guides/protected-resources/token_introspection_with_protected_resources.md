### Token Introspection with Protected Resources

When introspecting a JWT, the system validates the `aud` claim against both OAuth clients and Protected Resources.

#### Single-Audience Token Validation

For tokens with a single audience value, the system performs the following steps:

1. Query `ClientSyncService` for a matching `clientId`
2. If no client is found, query `ProtectedResourceSyncService` for a matching `clientId`
3. If a Protected Resource is found, retrieve its certificate ID (or empty string for HMAC) for signature verification
4. If neither client nor Protected Resource is found, fall back to RFC 8707 resource identifier validation
5. If no match is found, `OAuth2AuthProvider` throws `InvalidTokenException` with message `"Client or resource not found: {aud}"`

#### Multi-Audience Token Validation

For tokens with multiple audience values, the system always uses RFC 8707 resource identifier validation. Client and Protected Resource lookup is skipped.
