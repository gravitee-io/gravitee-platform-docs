---
title: Gravitee Kubernetes Operator 4.12 Release Notes.
---

# GKO 4.12

## Highlights

* The `Subscription` CRD supports API Key plan subscriptions, including multiple custom keys per subscription with optional expiry dates and zero-downtime rotation through the operator and the APIM Automation API.

## Breaking Changes

* The `customApiKey` field is removed from the `Subscription` CRD schema. Update existing manifests to the `apiKeys` array format before upgrading. See [API key subscriptions](../../overview/custom-resource-definitions/subscription.md#api-key-subscriptions) for the new schema.

## New Features


<!-- PIPELINE:GKO-2550 -->
#### **API key rotation for subscriptions**

* The `Subscription` CRD accepts an `apiKeys` array, allowing multiple custom API keys per subscription with optional `expireAt` values.
* On every apply, GKO forwards the desired keys to APIM. APIM creates new keys, reactivates revoked keys whose values match entries in the spec, and revokes keys removed from the spec.
* Each key value is between 32 and 256 characters. Duplicate keys within the array are rejected by the admission webhook.
* Available for `API_KEY` plan types through the GKO `Subscription` CRD and the APIM Automation REST API.
<!-- /PIPELINE:GKO-2550 -->


<!-- PIPELINE:GKO-2567 -->
#### **Dictionary Management via Automation API and Kubernetes CRD**

* Create, update, and delete dictionaries programmatically using the Automation API or Kubernetes CRD to store key-value pairs for use in API policies and configurations.
* Manual dictionaries hold static properties, while dynamic dictionaries poll external HTTP endpoints at scheduled intervals using JOLT transformations to refresh values automatically.
* Dictionaries are identified by a human-readable ID (HRID) unique within an environment and can be deployed to the gateway (manual) or started/stopped (dynamic) to control availability.
* Requires `ENVIRONMENT_DICTIONARY` permissions with `CREATE`, `UPDATE`, `DELETE`, and `READ` actions; dynamic dictionaries require a reachable HTTP endpoint and valid JOLT specification.
<!-- /PIPELINE:GKO-2567 -->

## Improvements

## Bug Fixes
