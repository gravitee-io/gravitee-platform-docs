---
description: >-
  This article covers the new features released in Gravitee Access Management
  4.11.
---

# AM 4.11

## Highlights

* Magic Link Authentication enables passwordless login by sending time-limited, JWT-based authentication links via email.
* Domain-level certificate fallback prevents authentication failures by automatically using a backup certificate when an application's configured certificate can't load.
* Protected Resources support full OAuth 2.0 client lifecycle management with multiple client secrets, certificate-based auth, and RFC 8693 token exchange audience resolution.
* Agent Application Type enforces stricter OAuth grant type constraints for AI assistants and autonomous agents, with optional AgentCard metadata import via the A2A specification.
* OAuth 2.0 Token Exchange (RFC 8693) enables clients to exchange security tokens for impersonation and delegation scenarios with configurable scope handling and trusted external JWT issuers.
