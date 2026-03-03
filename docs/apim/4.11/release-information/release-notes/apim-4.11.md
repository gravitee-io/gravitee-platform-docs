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

* Native Kafka APIs now support multiple endpoint groups and endpoints with drag-and-drop reordering for flexible broker configuration.
* Endpoint groups for Native Kafka APIs automatically use the `native-kafka` type and do not require load balancer configuration.
* The first endpoint in the first endpoint group is automatically designated as the default endpoint used by the API.
* Endpoints display Kafka-specific properties including bootstrap servers and security protocol inheritance status with visual badges.
* Security protocol settings can be inherited from the endpoint group or overridden at the individual endpoint level.
<!-- /PIPELINE:APIM-12500 -->

## Improvements

## Bug Fixes
