# APIM 4.11

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:APIM-12439 -->
#### **AI-Powered PII Filtering Policy**

* Automatically detects and redacts Personally Identifiable Information (PII) in API request and response payloads using AI token classification models
* Supports configurable redaction rules based on AI confidence thresholds (0.0–1.0) and PII categories (PERSON, LOCATION, EMAIL, etc.)
* Requires Enterprise license with `agent-mesh` pack, write permissions to `$GRAVITEE_HOME/models` directory for automatic model downloads, and sufficient heap memory for model loading
* Includes streaming detection safeguards that reject streaming requests when response filtering is enabled to prevent incomplete redaction
<!-- /PIPELINE:APIM-12439 -->


<!-- PIPELINE:APIM-12371 -->
#### **API Products**

* Bundle multiple V4 HTTP Proxy APIs into a single subscribable package with unified access control and product-level plans (API Key, JWT, or mTLS).
* Manage subscriptions at the product level instead of individual APIs, enabling API product managers to package and monetize APIs at scale.
* APIs must have the `allowedInApiProducts` flag enabled to be included in products; APIs can belong to multiple products while maintaining their own direct subscription plans.
* Requires Enterprise Universe tier license and environment-level permissions for API Product management.
* Plans and subscriptions now support a reference model with `referenceType` (API or API_PRODUCT) and `referenceId` fields; the legacy `api` field is deprecated as of 4.11.0.
<!-- /PIPELINE:APIM-12371 -->

## Improvements

## Bug Fixes
