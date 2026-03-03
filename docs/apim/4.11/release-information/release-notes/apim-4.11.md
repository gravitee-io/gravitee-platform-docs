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
#### **Native Kafka API Endpoint Management**

* Native Kafka APIs now support multiple endpoint groups and endpoints, enabling complex routing and failover configurations beyond the previous single-endpoint limitation.
* Endpoints can be created, edited, and reordered using drag-and-drop within endpoint groups, with the first endpoint in the first group automatically designated as the default connection target.
* Load balancer configuration is optional for Native Kafka endpoint groups, while security protocols can be inherited from the group or overridden at the endpoint level.
* APIs are classified as Native Kafka when defined with `type: NATIVE` and at least one `KAFKA` listener, which determines applicable validation rules and UI behaviors.
<!-- /PIPELINE:APIM-12500 -->

## Improvements

## Bug Fixes
