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

* Native Kafka APIs now support endpoint group and endpoint creation with drag-and-drop reordering to manage multiple Kafka bootstrap servers and configure endpoint priority.
* Security protocols (e.g., `SASL_SSL`, `PLAINTEXT`) can be configured at the group level or overridden per endpoint, with protocol badges displayed in the endpoint table.
* The first endpoint in the first group is automatically designated as the default endpoint for the API.
* Endpoint groups for Native Kafka APIs use type `native-kafka` and do not require load balancer configuration.
* Drag-and-drop reordering is disabled in read-only mode, and endpoint management is not available for `MCP_PROXY` API types.
<!-- /PIPELINE:APIM-12500 -->

## Improvements

## Bug Fixes
