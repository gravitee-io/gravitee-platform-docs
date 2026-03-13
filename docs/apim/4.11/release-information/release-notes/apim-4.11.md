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
#### **mTLS Plan Support for Kafka Native APIs**

* Kafka native APIs now support mTLS plans for client authentication using X.509 certificates, enabling accurate subscription resolution and metrics attribution.
* The gateway extracts the client certificate from the TLS session, computes its MD5 hash, and uses it as a security token to look up the subscription and populate connection context with `planId`, `applicationId`, and `subscriptionId`.
* Kafka native APIs enforce strict plan security mutual exclusion—you cannot mix Keyless, mTLS, and authentication plans (OAuth2, JWT, API Key) in published state. Publishing a plan of one type automatically closes all published plans of conflicting types.
* Requires Gravitee APIM 4.11 or later, `gravitee-policy-mtls` version 2.0.0-alpha.2 or later, and gateway configuration with `kafka.ssl.clientAuth=required` and appropriate truststore/keystore settings.
* Subscription certificates are loaded dynamically without requiring gateway restarts—when a subscription is created or updated with a new certificate, the gateway's trust store manager refreshes automatically.
<!-- /PIPELINE:APIM-12520 -->

## Improvements

## Bug Fixes
