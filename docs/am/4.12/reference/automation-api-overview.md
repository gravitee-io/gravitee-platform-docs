# Automation API Overview

## Overview

The Automation API provides a machine-oriented HTTP interface for managing Access Management resources declaratively. It enables infrastructure-as-code workflows by exposing domain, identity provider, certificate, and reporter resources through a stable, versioned OpenAPI specification served at the configured entrypoint. The API follows the conventions of the APIM Automation API and is designed for CI/CD pipelines, Terraform providers, and other automation tools that require idempotent, key-based resource management.

## Key Concepts

### Automation API vs Management REST API

The Automation API is a separate HTTP endpoint optimized for declarative resource management. Unlike the Management REST API, which uses database-generated identifiers, the Automation API uses stable, user-defined keys for all resources. Resources created through the Automation API are isolated from those created via the Management REST API or UI. For example, identity providers created outside the Automation API are not returned by Automation API list endpoints. The API is primarily documented via the generated OpenAPI specification served at the configured entrypoint when the API is enabled.

### Resource Keys

Every resource in the Automation API is identified by a **key**: a stable, immutable identifier you define when creating the resource. Keys are scoped to their parent resource. For example, identity provider keys are unique within a domain. Once created, a resource's key can't be changed. Keys enable idempotent PUT operations — sending the same PUT request multiple times produces the same result.

| Resource | Key Scope | Example Key |
|:---------|:----------|:------------|
| Domain | Environment | `example-domain` |
| Identity Provider | Domain | `corporate-ldap` |
| Certificate | Domain | `signing-cert` |
| Reporter | Domain | `audit-kafka` |

### System Resources

Identity providers and reporters can be marked as **system resources** by setting `system: true`. System identity providers are built from the `domains.identities.default.*` configuration in `gravitee.yml` and require only a `key` field — all other configuration is inherited from the gateway configuration file. System resources are immutable through the Automation API. Re-PUTting a system resource is an idempotent no-op. Each domain can have at most one system identity provider.

### Terraform Provider (Technical Preview)

The Access Management Terraform provider is currently in technical preview. It consumes the Automation API to enable infrastructure-as-code workflows.

## Prerequisites

Before using the Automation API, ensure the following requirements are met:

* Access Management gateway version 4.6 or later
* A user account with organization-level permissions
* Either a JWT bearer token or an opaque user service-account access token for authentication
* For Helm deployments: Helm chart version supporting `api.http.api.automation.*` values 
