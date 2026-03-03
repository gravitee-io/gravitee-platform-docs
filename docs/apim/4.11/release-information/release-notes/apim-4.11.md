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


<!-- PIPELINE:APIM-12498 -->
#### **Multi-Tenant Endpoint Support for Native Kafka APIs**

* Enables a single Kafka API definition to route traffic to different backend Kafka clusters based on the gateway's tenant configuration, eliminating the need to duplicate API definitions across environments.
* The gateway evaluates its configured `tenant` identifier against each endpoint's `tenants` array and selects the first matching endpoint. If no tenant is configured on the gateway, it matches any endpoint regardless of tenant restrictions.
* Configure the gateway-level `tenant` property in `gravitee.yml` and assign tenant identifiers to individual endpoints via the Management Console's multi-select dropdown.
* If no endpoint matches the gateway's tenant, requests fail with a `KafkaNoApiEndpointFoundException`.
<!-- /PIPELINE:APIM-12498 -->

## Improvements

## Bug Fixes
