# GKO 4.12

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:GKO-2550 -->
#### **API Key Rotation for Subscriptions**

* Manage multiple API keys per subscription with optional expiry dates, enabling seamless key rotation without service interruption.
* Replace or add API keys by updating the `apiKeys` array in the subscription spec—the system automatically creates new keys, reactivates revoked keys, and revokes keys removed from the spec.
* Available for `API_KEY` plan types via the Automation REST API and Kubernetes Operator; each key must be 32–256 characters.
* Apply the updated Kubernetes CRD (`gravitee.io_subscriptions.yaml`) before using the `apiKeys` field in Kubernetes resources.
<!-- /PIPELINE:GKO-2550 -->

## Improvements

## Bug Fixes
