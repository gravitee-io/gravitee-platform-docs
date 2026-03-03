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


<!-- PIPELINE:APIM-12497 -->
#### **Entrypoint Connect Phase for Native Kafka APIs**

* Native Kafka APIs now support an Entrypoint Connect phase that executes policies when clients establish TCP connections, before SASL authentication occurs.
* Enables connection-level filtering (IP allowlists, rate limiting, TLS validation) to reject unauthorized clients before they reach the authentication layer.
* Policies in this phase can call `ctx.interrupt(reason)` to immediately close the socket and prevent further connection attempts.
* Available in the Policy Studio UI under the Global tab for Native APIs, with access to connection metadata including remote/local addresses and TLS session data.
* Requires APIM 4.11.x with Native Kafka reactor 6.x or Agent-to-Agent connectors 2.0.0-alpha.1.
<!-- /PIPELINE:APIM-12497 -->

## Improvements

## Bug Fixes
