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


<!-- PIPELINE:APIM-12520 -->
#### **mTLS Authentication for Kafka Native APIs**

* Kafka Native APIs now support mutual TLS (mTLS) as a plan security type, enabling certificate-based access control for Kafka connections.
* Only one security category (Keyless, mTLS, or Authentication) can have published plans at a time—publishing a plan from one category automatically closes all published plans from the other categories.
* Requires Kafka gateway configuration with SSL client authentication enabled (`kafka.ssl.clientAuth: required`) and proper truststore/keystore setup.
* Client certificates must be signed by a CA trusted by the gateway; validation failures return asynchronous errors for Kafka connections or 401 Unauthorized for HTTP connections.
<!-- /PIPELINE:APIM-12520 -->

## Improvements

## Bug Fixes
