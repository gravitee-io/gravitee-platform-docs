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


<!-- PIPELINE:APIM-12550 -->
#### **A2A Proxy API Type for Agent-to-Agent Communication**

* Introduces a new A2A Proxy API type that enables routing requests between autonomous agents through Gravitee API Management.
* Supports REQUEST and RESPONSE flow phases with policy enforcement, using HTTP path-based flow selectors identical to standard proxy APIs.
* Requires an enterprise license with the AI pack feature enabled (`apim-a2a-proxy-reactor`).
* Compatible with 11 policies including transform-headers, assign-attributes, callout-http, interrupt, role-based-access-control, ipfiltering, ai-prompt-guard-rails, ratelimit, javascript, groovy, and retry.
* Current version is `1.0.0-alpha.1` (alpha release) and requires configuring a mandatory target URL for the backend agent service.
<!-- /PIPELINE:APIM-12550 -->

## Improvements

## Bug Fixes
