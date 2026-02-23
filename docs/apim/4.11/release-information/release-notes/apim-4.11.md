# APIM 4.11

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:APIM-12520 -->
#### **mTLS Authentication for Kafka Native APIs**

* Kafka Native APIs now support mutual TLS (mTLS) plans, enabling certificate-based access control for Kafka connections.
* The Gateway validates client certificates by extracting the TLS session and verifying the certificate chain against a configured truststore.
* mTLS plans enforce strict mutual exclusion with Keyless and authentication plans (OAuth2, JWT, API Key)—publishing a conflicting plan type automatically closes existing incompatible plans.
* Requires Gateway configuration with `kafka.ssl.clientAuth: required` and a truststore containing the CA that signed client certificates.
* Subscriptions must include a Base64-encoded client certificate, with the certificate MD5 hash used as the security token.
<!-- /PIPELINE:APIM-12520 -->

## Improvements

## Bug Fixes
