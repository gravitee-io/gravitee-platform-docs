# GKO 4.11

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:GKO-2026 -->
#### **Logs Engine API for Environment-Level Log Search**

* Provides a centralized API for searching and filtering v4 HTTP proxy API connection logs across an entire environment, enabling platform administrators and SREs to investigate incidents without navigating between individual API screens.
* Supports filtering by API, application, plan, HTTP method, status code, response time, and other dimensions using a flexible filter model with exact match, array match, and numeric range operators.
* Enforces permission-based access control, ensuring users only see logs for APIs they are authorized to view.
* Requires Gravitee APIM 4.11 or later with Elasticsearch or OpenSearch reporter configured and `RolePermission.API_ANALYTICS` with `RolePermissionAction.READ` for the environment.
<!-- /PIPELINE:GKO-2026 -->

## Improvements

## Bug Fixes
