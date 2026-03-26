# OAuth 2.0 Token Exchange Concepts

## Overview

OAuth 2.0 Token Exchange ([RFC 8693](https://datatracker.ietf.org/doc/html/rfc8693)) allows a client to request a new security token by presenting an existing one. This enables scenarios where one service needs to act as, or on behalf of, a user or another service, without requiring the user to re-authenticate.

Gravitee Access Management supports two Token Exchange paradigms:

**Impersonation:** The issued token represents the subject directly. The requesting client acts _as_ the subject. There is no indication in the token that a different party initiated the exchange.

**Delegation:** The issued token represents the subject but includes an `act` (actor) claim identifying the party that is acting on the subject's behalf. The actor's identity is preserved in the token.

**Key behaviors:**

* No refresh tokens are issued during token exchange.
* The issued token's expiration is bounded by the subject token's remaining lifetime.
* The `client_id` claim in the issued token identifies the requesting client.
* When an ID token is requested, it is returned in the `access_token` response field with the `token_type` set to `"N_A"`.

This implementation allows administrators to configure trusted external JWT issuers, scope handling modes, and user binding rules. It is designed for API platform administrators managing cross-domain authentication and developers integrating token-based workflows.