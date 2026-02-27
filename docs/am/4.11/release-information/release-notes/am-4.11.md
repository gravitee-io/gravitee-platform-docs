# AM 4.11

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:AM-6322 -->
#### **Agent Application Type for Machine-to-Machine Integrations**

* Introduces a new Agent application type designed for automated workflows (CI/CD pipelines, monitoring agents, resource management tools) with enforced security controls that restrict grant types to `authorization_code` and `client_credentials` only.
* Automatically strips forbidden grant types (`implicit`, `password`, `refresh_token`) during application creation via DCR or Management API, and rejects token requests using these flows at runtime.
* Supports declarative agent configuration through agent cards—JSON manifests fetched from a configured URL with SSRF protection (blocks private IPs, enforces HTTPS, limits response size to 512 KB, 5-second timeout).
* Enables zero-downtime secret rotation for protected resources through dedicated endpoints for creating, renewing, and deleting multiple secrets with independent lifecycles.
* Requires `APPLICATION[CREATE]` or `APPLICATION[UPDATE]` permission to manage agent applications and `PROTECTED_RESOURCE[CREATE]` permission for secret management.
<!-- /PIPELINE:AM-6322 -->

## Improvements

## Bug Fixes
