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
#### **MCP Analytics Dashboard Template**

* Introduces a pre-built dashboard template for monitoring Model Context Protocol (MCP) API usage, including method distribution, tool calls, resource reads, and prompt retrievals.
* Adds four MCP-specific analytics facets (`MCP_PROXY_METHOD`, `MCP_PROXY_TOOL`, `MCP_PROXY_RESOURCE`, `MCP_PROXY_PROMPT`) for filtering and aggregating MCP protocol data in Elasticsearch.
* Users with `Environment-dashboard-c` permission can create dashboards from the template via **Observability > Dashboards > Create from template**.
* Requires MCP-enabled APIs and active analytics data collection to populate dashboard widgets.
<!-- /PIPELINE:GKO-2025 -->

## Improvements

## Bug Fixes
