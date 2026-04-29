# GKO 4.12

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:GKO-2550 -->
#### **API Key Subscription Management**

* GKO now supports declarative management of API Key subscriptions alongside existing JWT, OAuth, and mTLS subscription types.
* You can provide custom API keys (32-256 characters) or let APIM generate them automatically, and source key values from Kubernetes Secrets to keep credentials out of manifests.
* API key rotation is handled declaratively by updating the `apiKeys` list in the Subscription spec—GKO automatically creates new keys, revokes removed keys, and reactivates previously revoked keys.
* Requires GKO configured to sync with APIM control plane (`local=false` for v2 APIs or `syncFrom=MANAGEMENT` for v4 APIs).
<!-- /PIPELINE:GKO-2550 -->

## Improvements

## Bug Fixes
