# Managing Trusted Issuers

Configure trusted issuers through the domain settings UI to enable token exchange with external JWT tokens.

1. Navigate to the Token Exchange settings and click **Add Trusted Issuer**.
2. Enter the issuer URL in the **Issuer** field. This value must match the `iss` claim in incoming JWTs.
3. Select the key resolution method:
   * **JWKS URL**: Provide the JWKS endpoint URL in the **JWKS URI** field.
   * **PEM**: Paste the PEM-encoded certificate in the **Certificate** field.
4. (Optional) Configure scope mappings:
   1. Enter the external scope name in the **External Scope** field.
   2. Enter the corresponding domain scope name in the **Domain Scope** field. The UI provides autocomplete for domain scopes.
   3. Repeat for additional scope mappings.
5. (Optional) Enable user binding to match external tokens to existing domain users:
   1. Toggle **Enable User Binding**.
   2. Click **Add User Binding Criterion**.
   3. Select a user attribute from the **Attribute** dropdown (e.g., `email`, `username`).
   4. Enter an EL expression in the **Expression** field (e.g., `{#token['email']}`).
   5. Repeat for additional user binding criteria.
6. Click **Save**.

The gateway validates the configuration and rejects it if:
* The issuer URL is missing or empty
* The issuer URL duplicates an existing trusted issuer
* The key resolution method is JWKS URL but the JWKS URI is missing
* The key resolution method is PEM but the certificate is missing
* Any external scope or domain scope in a scope mapping is empty
* User binding is enabled but no user binding criteria are defined
* Any user attribute or expression in a user binding criterion is empty
