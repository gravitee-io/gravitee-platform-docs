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
#### **Multi-Tenant Endpoint Support for Kafka APIs**

* Enables a single Kafka API definition to route traffic to different backend clusters based on the gateway's configured tenant identifier, eliminating the need to duplicate API definitions across deployment zones.
* Each endpoint in the first endpoint group can be tagged with one or more tenant identifiers; gateways automatically filter and activate only endpoints matching their configured tenant at startup and during hot-reload.
* Endpoints with no tenant tags are treated as shared and match any gateway, providing a fallback option during gradual rollout or for legacy gateways without tenant configuration.
* Configure the gateway tenant identifier using the `tenant` property in `gravitee.yml`, environment variable, or system property.
* If no endpoint matches the gateway's tenant after filtering, requests fail. Include at least one untagged endpoint to provide a fallback.
<!-- /PIPELINE:APIM-12498 -->


<!-- PIPELINE:APIM-12500 -->
#### **Multiple Endpoints for Native Kafka APIs**

* Native Kafka APIs can now define multiple endpoints within an endpoint group, enabling pre-configured cluster alternatives for disaster recovery, migration, and regional routing scenarios.
* The gateway routes new connections to the active endpoint based on tenant configuration or list order—publishers control which endpoint is active by reordering endpoints in the group.
* Endpoint switching is manual and publisher-initiated; the gateway does not perform automatic failover or health checks, and Kafka clients must handle reconnection when endpoints change.
* Tenant-aware routing is supported: if the gateway tenant matches an endpoint's tenant tag, that endpoint is selected; otherwise, the first endpoint in the group is used.
<!-- /PIPELINE:APIM-12500 -->

## Improvements

## Bug Fixes
