# GKO 4.11

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:GKO-2006 -->
#### **mTLS Client Certificate Management**

* The GKO Application CRD now supports multiple client certificates with validity and rotation management for application-level mutual TLS.
* Administrators can now upload, validate, and rotate client certificates directly through the Management Console (for applications managed outside of GKO).
* Supports scheduled certificate activation and grace-period rotation to prevent downtime during certificate updates.
* Certificates are validated on upload (SHA-256 fingerprint, uniqueness) and progress through lifecycle states: Scheduled, Active, Active with End Date, and Revoked.
* Requires APIM 4.11 or above and an API with an mTLS plan subscribed for the application.
<!-- /PIPELINE:GKO-2006 -->


<!-- PIPELINE:GKO-2025 -->
#### **MCP Analytics and Dashboard Templates**

* Monitor Model Context Protocol (MCP) API usage through dedicated facets for methods, tools, resources, and prompts in Analytics dashboards.
* Create pre-configured MCP dashboards from templates with 11 widgets covering request volume, latency percentiles (P90, P99), method distribution, and top-5 rankings.
* Filter analytics data by MCP-specific metadata fields: `MCP_PROXY_METHOD`, `MCP_PROXY_TOOL`, `MCP_PROXY_RESOURCE`, and `MCP_PROXY_PROMPT`.
* Requires Environment-level dashboard permissions (`dashboard-r`, `dashboard-c`, `dashboard-u`, `dashboard-d`) to create and manage MCP dashboards.
<!-- /PIPELINE:GKO-2025 -->

## Improvements

## Bug Fixes
