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


<!-- PIPELINE:APIM-13008 -->
#### **JMS Endpoint Connector for Message Broker Integration**

* Enables Gravitee APIM to produce and consume messages from JMS-compliant brokers (ActiveMQ, IBM MQ, Solace, etc.) using queue or topic messaging patterns.
* Supports multiple connection factory configuration methods: direct broker URL, provider-specific properties (hostname/port/channel), or JNDI lookup with custom properties.
* Configurable for producer mode (send messages with TEXT or BYTES format), consumer mode (receive messages with durable subscription support), or both capabilities simultaneously on the same endpoint.
* Requires `event-native` license pack and JMS provider client library placed in `./plugins/jms/ext/` directory.
* Topic consumers use shared or exclusive connections based on client ID and durability settings; queue consumers always use shared connections.
<!-- /PIPELINE:APIM-13008 -->

## Improvements

## Bug Fixes
