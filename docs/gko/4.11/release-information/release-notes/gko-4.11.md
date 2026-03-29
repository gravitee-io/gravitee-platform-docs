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
#### **LLM Analytics Dashboard Template**

* Introduces a pre-built dashboard template for monitoring LLM usage, token consumption, and costs across AI-powered APIs.
* Tracks six new metrics: tokens sent/received, token costs, total tokens, and total cost, computed via Elasticsearch scripted aggregations.
* Enables real-time visibility into LLM provider usage patterns, cost trends, and response status distribution.
* Requires `Environment-dashboard-c` permission to create dashboards from the template.
* Replaces the previous AI Gateway template with LLM-focused analytics.
<!-- /PIPELINE:GKO-2024 -->

## Improvements

## Bug Fixes
