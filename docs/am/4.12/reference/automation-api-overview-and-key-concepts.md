# Automation API Overview and Key Concepts

## Overview

The Automation API provides a machine-oriented HTTP interface for programmatically managing Access Management domains, identity providers, certificates, and reporters. It enables infrastructure-as-code workflows through declarative resource management with idempotent PUT operations, following the conventions of the API Management Automation API. The API is documented via an OpenAPI specification served at the configured entrypoint and is designed for use with automation tools like the Gravitee Terraform provider (currently in technical preview).

## Key Concepts

### Resource Hierarchy

The Automation API organizes resources under a three-level hierarchy: organizations contain environments, which contain domains. Each domain can have multiple identity providers, certificates, and reporters. All resources are identified by immutable keys that follow the pattern `^[a-z0-9]([a-z0-9-]*[a-z0-9])?$` with a maximum length of 255 characters.

### System Resources

System resources are pre-configured entities sourced from `gravitee.yml` rather than user-supplied configuration. Identity providers, certificates, and reporters can be marked as system resources by setting `system: true` in the request body. System identity providers use configuration from `domains.identities.default.*` in `gravitee.yml`, while system certificates reference the domain's default certificate. A domain can have only one system identity provider managed through the Automation API.

### Idempotent Operations

The API uses PUT operations for both resource creation and updates. When a resource with the specified key does not exist, the API creates it. When the resource already exists, the API updates it with the provided configuration. Re-submitting identical configuration for a system resource results in a no-op response with HTTP 200.

## Prerequisites

Before using the Automation API, ensure the following requirements are met:

* Access Management instance with Automation API enabled via `api.http.api.automation.enabled: true`
* Valid authentication credentials (JWT bearer token, opaque user service-account access token, or HTTP Basic credentials)
* Organization and environment identifiers for the target deployment
* For non-system resources: plugin type deployed and available in the Access Management instance
