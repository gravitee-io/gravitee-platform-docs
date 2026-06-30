---
title: Gravitee Kubernetes Operator 4.12 Release Notes.
---

# GKO 4.12

## Highlights

* The `Subscription` CRD supports API Key plan subscriptions, including multiple custom keys per subscription with optional expiry dates and zero-downtime rotation through the operator and the APIM Automation API.

## Breaking Changes

* The `customApiKey` field is removed from the `Subscription` CRD schema. Update existing manifests to the `apiKeys` array format before upgrading. See [API key subscriptions](../../overview/custom-resource-definitions/subscription.md#api-key-subscriptions) for the new schema.

## New Features

#### **API key rotation for subscriptions**

* The `Subscription` CRD accepts an `apiKeys` array, allowing multiple custom API keys per subscription with optional `expireAt` values.
* On every apply, GKO forwards the desired keys to APIM. APIM creates new keys, reactivates revoked keys whose values match entries in the spec, and revokes keys removed from the spec.
* Each key value is between 32 and 256 characters. Duplicate keys within the array are rejected by the admission webhook.
* Available for `API_KEY` plan types through the GKO `Subscription` CRD and the APIM Automation REST API.

#### Full support of webhook APIs

&#x20;The `Subscription` CRD now accepts a `consumerConfiguration`  object, allowing to configure an entrypoint and webhook configuration ( `callbackUrl`, `auth`, `headers`, `ssl`...).

#### **Dictionary Management**&#x20;

* New Dictionary CRD allow to manage Dictionaries declaratively in association with the `ManagementContext` CRD
* Supports both MANUAL dictionaries (static key-value pairs) and DYNAMIC dictionaries (auto-refreshing data from external HTTP endpoints with JOLT transformations).
* Dictionary deployment states control gateway availability: deployed MANUAL dictionaries expose data to policies, while started DYNAMIC dictionaries enable scheduled polling.
*
* Requires `ENVIRONMENT_DICTIONARY` permissions with `CREATE`, `UPDATE`, `DELETE`, and `READ` actions; dynamic dictionaries require a reachable HTTP endpoint and a valid JOLT specification.

#### Next-generation Developer Portal structure and Document Management

* Three CRD are now available to manage navigation in the next-generation Developer Portal.
  * `Portal`Only one CR instance is allowed per environment, and it maintains the navigation tree.
  * `PortalListing`: control API placement and sequence within the navigation tree.
  * `Documentation`: represents a page, supports Gravitee Markdown, OpenAPI, and AsyncAPI formats and can be bound to either the portal or a specific API.&#x20;
* API Definition (v4) now has a new property: `portalNavigation`. It gives an API publisher the opportunity to control the navigation structure of the docs pages for that API.

## Bug Fixes

* Updating ApiV4Definition to change plan generalConditions to a new page HRID causes reconciliation failure (HTTP 500) [#11327](https://github.com/gravitee-io/issues/issues/11327)
