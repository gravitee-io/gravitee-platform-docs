# APIM 4.11

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:APIM-12498 -->
#### **Multi-Tenant Endpoint Selection for Native Kafka APIs**

* A single Native Kafka API definition can now serve multiple backend Kafka clusters by automatically selecting endpoints based on the gateway's configured tenant identifier.
* Each endpoint can be tagged with one or more tenant identifiers, and gateways filter endpoints to match their configured tenant, eliminating the need for separate API definitions per environment.
* Configure the gateway tenant using the `tenant` property in `gravitee.yml` or the `GRAVITEE_TENANT` environment variable.
* Tenant filtering is optional—existing API definitions without tenant assignments continue to work unchanged.
<!-- /PIPELINE:APIM-12498 -->

## Improvements

## Bug Fixes
