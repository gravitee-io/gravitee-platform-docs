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
#### **Kafka Native API mTLS Authentication**

* Kafka Native APIs now support mutual TLS (mTLS) as a plan security type, enabling client certificate authentication for Kafka connections.
* The gateway validates client certificates against a configured truststore during connection establishment and enforces strict mutual exclusion between Keyless, mTLS, and authentication-based plans (OAuth2, JWT, API Key).
* Requires APIM 4.10+ and gateway SSL/TLS configuration with `kafka.ssl.clientAuth` set to `required` and a truststore containing the CA that signed client certificates.
* Publishing an mTLS plan automatically closes any conflicting published plans (Keyless or authentication-based) on the same API.
<!-- /PIPELINE:APIM-12520 -->

## Improvements

## Bug Fixes
