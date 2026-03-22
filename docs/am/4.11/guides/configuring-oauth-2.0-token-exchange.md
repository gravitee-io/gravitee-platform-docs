# Configuring OAuth 2.0 Token Exchange

## User Binding

When a trusted issuer has `userBindingEnabled=true`, the domain evaluates `userBindingCriteria` against the token's claims to match a domain user. Each criterion specifies a user attribute (e.g., `email`, `username`) and an expression (e.g., `{#token['email']}`). The system queries users matching all criteria and returns the single matched user. If zero or multiple users match, the exchange fails. If user binding is disabled or no criteria are configured, a virtual user is created from the token claims.
