---
title: Gravitee Kubernetes Operator 4.14 Release Notes
description: Highlights and new features in the Gravitee Kubernetes Operator 4.14 release, including resources for Authorization Management. See what changed before upgrading.
---

# GKO 4.14

This page describes the new features and breaking changes introduced in GKO 4.14.

## Highlights

* `AuthzPdp`, `AuthzSchema`, `AuthzEntity`, and `AuthzPolicy` resources manage the PDP gateways, schema documents, entities, and policies of Authorization Management from Kubernetes.
* A manual `Dictionary` declares secret values that APIM stores encrypted, and a dynamic `Dictionary` with `encryptOnFetch` set to `true` encrypts every value it fetches.

## Breaking changes

This release changes how GKO handles an existing configuration.

### Plan order of `ApiV4Definition`

GKO now sends an API's plans sorted by their `order`, so APIM keeps that order. Before, plans were sent sorted by key and `order` had no effect. With drift detection on and set to `deny`, an API whose plans all set `order`, in an order different from their keys, can have its first update after the upgrade refused on the plan order. To fix it, apply a spec change with the annotation `gravitee.io/drift-detection: "false"` set, then remove the annotation. An apply that only adds the annotation doesn't sync the API, so APIM keeps the old order.

## New features

GKO adds resources for Authorization Management and encrypted properties for dictionaries.

#### Authorization Management resources

The `AuthzPdp` resource declares a PDP gateway with its AuthZEN endpoint. The `AuthzSchema`, `AuthzEntity`, and `AuthzPolicy` resources declare a schema document, an entity, and a policy, and name the PDP gateways they're published to through a reference to an `AuthzPdp` or a routing scope. GKO validates each resource against APIM before it's stored, unless it references an `AuthzPdp` that isn't synced yet, and drift detection covers the four resources. Every apply of an `AuthzPolicy` deploys the policy. These resources require APIM 4.14 with Authorization Management. For details, see [AuthzPdp](../../overview/custom-resource-definitions/authzpdp.md), [AuthzSchema](../../overview/custom-resource-definitions/authzschema.md), [AuthzEntity](../../overview/custom-resource-definitions/authzentity.md), and [AuthzPolicy](../../overview/custom-resource-definitions/authzpolicy.md).

#### Encrypted dictionary properties

A manual `Dictionary` declares secret values under `manual.encryptedProperties`, each one written in the resource or taken from a Kubernetes Secret. APIM stores them encrypted from the first apply and never returns them. A dynamic `Dictionary` with `dynamic.encryption.encryptOnFetch` set to `true` stores every value it fetches encrypted. Drift detection counts a value that APIM returns masked as unchanged, and a drift report doesn't show the values of encrypted properties. With APIM 4.14, a key that APIM stores encrypted is refused under `manual.properties`, so declare it under `manual.encryptedProperties`. The feature also ships in GKO 4.13.3. For details, see [Encrypt dictionary properties](../../overview/custom-resource-definitions/managing-dictionaries-via-kubernetes-crd/README.md#encrypt-dictionary-properties) and [Drift detection](../../overview/drift-detection.md).
