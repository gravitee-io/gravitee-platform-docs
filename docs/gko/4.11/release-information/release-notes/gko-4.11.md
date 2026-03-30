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


<!-- PIPELINE:GKO-2024 -->
#### **LLM Analytics and Dashboard Template**

* Monitor token consumption and costs for Large Language Model integrations across your environment.
* Track total and average token counts, associated costs, and usage patterns by model and provider using new `LLM_PROMPT_TOTAL_TOKEN` and `LLM_PROMPT_TOKEN_COST` metrics.
* Create dashboards from the new LLM template (formerly AI Gateway) to visualize LLM-specific metrics and filter by API type, model, and provider.
* Requires `Environment-dashboard-r`, `Environment-dashboard-c`, `Environment-dashboard-u`, or `Environment-dashboard-d` permissions to view, create, update, or delete dashboards.
<!-- /PIPELINE:GKO-2024 -->

## Improvements

## Bug Fixes
