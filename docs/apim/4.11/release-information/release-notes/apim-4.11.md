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


<!-- PIPELINE:APIM-12500 -->
#### **Multiple Endpoint Groups for Native Kafka APIs**

* Native Kafka APIs now support multiple endpoint groups and endpoints, enabling flexible management of Kafka broker connections similar to HTTP proxy APIs.
* Endpoints can be reordered via drag-and-drop within a group, and the first endpoint in the first group is automatically designated as the default endpoint.
* Each endpoint requires bootstrap server configuration and can inherit or override group-level security protocol settings.
* The UI automatically adapts for Native Kafka APIs by hiding load balancer configuration (not required for Kafka) and displaying Kafka-specific properties like security protocol inheritance.
<!-- /PIPELINE:APIM-12500 -->

## Improvements

## Bug Fixes
