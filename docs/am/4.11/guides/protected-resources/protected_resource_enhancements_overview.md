### Overview

Protected Resources in now support secret management, certificate binding, membership control, and search capabilities. These enhancements enable Protected Resources to authenticate like Applications and participate in token introspection and token exchange workflows.

A Protected Resource represents an OAuth 2.0 resource server that can validate access tokens and participate in authorization flows. With the new capabilities, Protected Resources can:

* Manage multiple client secrets for authentication
* Reference certificates for mTLS authentication
* Control access through role-based memberships
* Be discovered through search queries

These features are particularly relevant for MCP Server integrations, where Protected Resources act as token exchange participants.

### Prerequisites

Before configuring Protected Resources with these capabilities, ensure the following:

* Domain with OAuth 2.0 enabled
* For certificate binding: Valid certificate uploaded to the domain certificate store
* For membership management: Users or groups defined in the domain identity providers
* For token introspection: Protected Resource must have a unique `clientId` within the domain

### Protected Resource Secrets

Protected Resources maintain a list of client secrets for authentication. Each secret has a unique ID, optional name, expiration date, and associated settings. At least one secret must exist at all times.

Secrets can be created, renewed, or deleted. When renewing a secret, the system generates a new value while preserving the secret's metadata. The system automatically generates secure random values and tracks expiration dates for notification purposes.

### Certificate Binding

Protected Resources can reference a certificate for mTLS authentication scenarios. The certificate field stores a certificate ID that must exist in the domain's certificate store. Certificate deletion is blocked if any Protected Resource references it, preventing broken authentication configurations.
