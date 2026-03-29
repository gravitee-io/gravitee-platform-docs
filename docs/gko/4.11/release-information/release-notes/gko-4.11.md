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
#### **LLM Analytics and Dashboard Templates**

* Monitor Large Language Model usage, token consumption, and costs through dedicated metrics and dashboard templates.
* Two computed metrics track total tokens (`LLM_PROMPT_TOTAL_TOKEN`) and token costs (`LLM_PROMPT_TOKEN_COST`) per request, with support for `COUNT` and `AVG` aggregations.
* Filter and segment analytics by LLM provider and model using new `LLM_PROXY_MODEL` and `LLM_PROXY_PROVIDER` facets.
* Create dashboards from pre-built templates via **Observability > Dashboards > Create from template** to visualize LLM performance and optimize AI integration costs.
* Requires `Environment-dashboard-r`, `Environment-dashboard-c`, `Environment-dashboard-u`, and `Environment-dashboard-d` permissions for dashboard management.
<!-- /PIPELINE:GKO-2024 -->

## Improvements

## Bug Fixes
