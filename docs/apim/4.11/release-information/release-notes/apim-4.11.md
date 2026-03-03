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

* Bundle multiple V4 HTTP Proxy APIs into a single consumable product with unified plans and subscriptions, simplifying access management for multi-API workflows.
* Consumers subscribe to the API Product rather than individual APIs, with product-level plans evaluated before API-level plans in the gateway security chain.
* Requires a "universe" tier license and V4 HTTP Proxy APIs configured with `allowedInApiProducts=true`.
* API Product ID is injected into the execution context as `{#context.attributes['apiProduct']}` for policy expressions.
<!-- /PIPELINE:APIM-12371 -->

## Improvements

## Bug Fixes
