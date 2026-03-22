# OAuth 2.0 Token Exchange: Configuring Trusted Issuers

## Configuring Trusted Issuers

Administrators configure trusted issuers in the domain settings to accept external JWTs for token exchange.

1. Navigate to **Settings > Security Domain > Token Exchange** and select **Add Trusted Issuer**.
2. Enter the issuer URL exactly as it appears in the JWT `iss` claim.
3. Select the key resolution method:
   * **JWKS URL**: Fetch public keys dynamically from the issuer's JWKS endpoint.
   * **PEM**: Upload a PEM-encoded certificate.
4. (Optional) Define scope mappings to translate external scopes to domain scopes using key-value pairs.
5. (Optional) Enable user binding and add binding criteria with user attributes and EL expressions to resolve external subjects to domain users.
6. Save the configuration.

The gateway validates external JWTs against the trusted issuer's signature and applies scope mappings and user binding during token exchange.
