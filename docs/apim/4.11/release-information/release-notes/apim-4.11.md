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
#### **Native Kafka Endpoint Management**

* Native Kafka APIs now support endpoint group and endpoint creation with visual drag-and-drop reordering to control endpoint priority.
* The first endpoint in the first endpoint group is automatically designated as the default endpoint and receives a "Default" badge.
* Security protocol configuration can be set at the endpoint level or inherited from the endpoint group, with badges indicating override or inheritance status.
* Load balancer configuration is optional for Native Kafka APIs and validation is automatically removed when a Kafka listener is detected.
* Endpoint tables display bootstrap servers and security protocol badges (e.g., `SASL_SSL`) for quick configuration visibility.
<!-- /PIPELINE:APIM-12500 -->

## Improvements

## Bug Fixes
