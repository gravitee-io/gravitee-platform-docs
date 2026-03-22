# Configuring and Validating Trusted Issuers for External JWT Tokens

## Managing Trusted Issuers

To configure a trusted issuer, navigate to the domain OAuth settings and add a new trusted issuer entry.

1. Enter the issuer URL exactly as it appears in the JWT `iss` claim.
2. Select the key resolution method: choose `JWKS_URL` and provide the JWKS endpoint URL, or choose `PEM` and paste the PEM-encoded certificate.
3. Define scope mappings by entering external scope names and their corresponding domain scope names. External scopes without a mapping entry are silently dropped.
4. Enable user binding and define criteria by specifying user attributes and SpEL expressions that evaluate against token claims. Multiple criteria are combined with AND logic.
5. Save the configuration.

### Validation Process

When a trusted issuer token is presented, the gateway performs the following validation:

1. Decode the JWT header to extract the `kid` (key ID).
2. Fetch the JWKS from the configured URL or parse the PEM certificate.
3. Verify the JWT signature using the public key.
4. Validate that the `iss` claim matches the trusted issuer URL.
5. Validate the `exp` and `nbf` claims to ensure the token is not expired or not yet valid.
6. Evaluate user binding criteria and look up the user. The lookup must return exactly one user or the exchange fails with `invalid_grant`.
7. Apply scope mappings to convert external scopes to domain scopes.

{% hint style="danger" %}
Signature verification failures, zero or multiple user matches, and SpEL evaluation errors all result in `invalid_grant` errors.
{% endhint %}
