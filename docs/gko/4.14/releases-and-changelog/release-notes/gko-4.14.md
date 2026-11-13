---
title: Gravitee Kubernetes Operator 4.14 Release Notes
description: Highlights and new features in the Gravitee Kubernetes Operator 4.14 release, including resources for Authorization Management. See what changed before upgrading.
---

# GKO 4.14

This page describes the new features introduced in GKO 4.14.

## Highlights

* `AuthzPdp`, `AuthzSchema`, `AuthzEntity`, and `AuthzPolicy` resources manage the PDP gateways, schema documents, entities, and policies of Authorization Management from Kubernetes.

## New features

GKO adds resources for Authorization Management.

#### Authorization Management resources

The `AuthzPdp` resource declares a PDP gateway with its AuthZEN endpoint. The `AuthzSchema`, `AuthzEntity`, and `AuthzPolicy` resources declare a schema document, an entity, and a policy, and name the PDP gateways they're published to through a reference to an `AuthzPdp` or a routing scope. GKO validates each resource against APIM before it's stored, unless it references an `AuthzPdp` that isn't synced yet, and drift detection covers the four resources. Every apply of an `AuthzPolicy` deploys the policy. These resources require APIM 4.14 with Authorization Management. For details, see [AuthzPdp](../../overview/custom-resource-definitions/authzpdp.md), [AuthzSchema](../../overview/custom-resource-definitions/authzschema.md), [AuthzEntity](../../overview/custom-resource-definitions/authzentity.md), and [AuthzPolicy](../../overview/custom-resource-definitions/authzpolicy.md).
