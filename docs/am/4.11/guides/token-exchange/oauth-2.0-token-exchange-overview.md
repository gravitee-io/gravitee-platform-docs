# OAuth 2.0 Token Exchange Overview

## Overview

OAuth 2.0 Token Exchange (RFC 8693) enables clients to exchange one security token for another, supporting both impersonation (acting as the subject) and delegation (acting on behalf of the subject) scenarios. This feature allows cross-domain token exchange, scope downscoping, and integration with external JWT issuers. It is designed for API administrators and developers building multi-tier service architectures or integrating third-party identity providers.

## Prerequisites

- Token exchange must be enabled at the domain level (`enabled = true` in [Token Exchange Settings](../auth-protocols/oauth-2.0/token-exchange-gateway-configuration-reference.md#token-exchange-settings))
- OAuth2 client must be configured with appropriate scopes and token validity settings
- For external token exchange: trusted issuer must be configured with valid JWKS URL or PEM certificate
- For delegation: `allowDelegation` must be enabled
- For impersonation: `allowImpersonation` must be enabled
- At least one of `allowImpersonation` or `allowDelegation` must be enabled
