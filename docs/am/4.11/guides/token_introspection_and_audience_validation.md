### Token Introspection and Audience Validation

When introspecting a token, the gateway validates the `aud` claim against Protected Resources to determine which resource the token is intended for and how to verify its signature.

#### Single-Audience Token Validation

For tokens with a single audience value, the gateway performs the following checks in order:

1. Check if the `aud` value matches an Application `clientId`
2. If no Application is found, check if the `aud` value matches a Protected Resource `clientId`
3. If no Protected Resource is found, fall back to RFC 8707 resource identifier validation

If a Protected Resource is matched in step 2, the gateway retrieves the associated certificate ID for JWT signature verification. If the Protected Resource uses HMAC-based validation instead of certificate-based authentication, an empty string is returned.

#### Multi-Audience Token Validation

For tokens with multiple audience values, the gateway always uses RFC 8707 resource identifier validation.

#### Certificate Retrieval for Signature Verification

When a Protected Resource is matched during audience validation, the gateway retrieves the certificate configuration to verify the JWT signature:

- If the Protected Resource has a certificate configured, the gateway uses certificate-based authentication to verify the token signature
- If no certificate is configured, the gateway uses HMAC-based validation

#### Error Handling

If the gateway cannot find a matching Application or Protected Resource during audience validation, it throws an `InvalidTokenException` with the message:

```
Client or resource not found: {aud}
```

where `{aud}` is the audience value from the token.
