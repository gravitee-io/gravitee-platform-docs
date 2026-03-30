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

* Administrators can monitor Model Context Protocol (MCP) API usage through a pre-built dashboard template accessible via **Observability > Dashboards > Create from template**.
* The dashboard visualizes MCP method invocations, tool usage, resource access, and prompt retrieval using four new analytics facets mapped to Elasticsearch fields in the `additional-metrics` namespace.
* Requires `Environment-dashboard-r` permission to view dashboards and `Environment-dashboard-c` permission to create from templates.
* Dashboard filters and timeframes can be customized after creation to analyze usage patterns and identify abnormal behavior or underutilized tools.
<!-- /PIPELINE:GKO-2025 -->

## Improvements

## Bug Fixes
