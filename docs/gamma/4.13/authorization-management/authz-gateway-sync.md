---
hidden: false
noIndex: false
description: Gamma continuously synchronizes policies and authorization data to every API Gateway that needs them. Learn what is synchronized, how a change becomes enforceable, and how engines are scoped.
---

# Authorization policy synchronization

Gamma Authorization Management evaluates authorization locally, inside the API Gateway. Policies and authorization data you manage in the Gamma console are continuously synchronized down to every Gateway that needs them. No request has to call back to the control plane for a decision.

## What is synchronized

Three kinds of document flow from the control plane to the Gateway:

* **Policies**, written in GAPL, Gravitee's authorization policy language.
* **Entities**, the authorization data policies evaluate against (principals, resources, their attributes, and parent relationships).
* **PDP targets**, the registrations that create and remove the decision engines a policy can be aimed at.

When you publish one of these, the change is recorded in the event store. Gateways check that store every few seconds and apply only what has changed since their last update.

## How a change becomes enforceable

1. The Gateway fetches the changed documents and routes each one to the decision engine responsible for its scope.
2. Documents are staged, not applied one by one. Once the batch is staged, the engine commits: it compiles the policy set, builds a new immutable snapshot, and swaps it in atomically.
3. Evaluations always run against one fully committed snapshot, so a half-applied policy set is never visible to traffic.

Synchronization is eventually consistent. A newly published policy becomes enforceable within seconds, not instantly, and the console reflects the intended state rather than a per-Gateway acknowledgment.

Until an engine has committed its first snapshot, it reports that it is not ready instead of guessing. Enforcement fails closed in that state, so a Gateway that has not yet caught up denies rather than allows.

## Engine scope

Every Gateway starts with a default decision engine, ready but empty. It answers immediately rather than leaving early traffic in an undefined state: with no policies loaded, nothing matches, and enforcement denies. The default engine only ever holds policies that are explicitly targeted at it.

Beyond that, each decision engine is identified by an environment and a **PDP target**, and holds its own snapshot. A commit on one engine is not visible to any other, so policies published in one environment or aimed at one PDP target are never evaluated for another. Engines are created and removed as targets are published and unpublished.

Where Gateways are sharded by tag, a policy must target the tagged PDP explicitly to reach that shard. A bare target ID is not a wildcard across shards.

This is a logical separation between engines hosted in the same Gateway process, not a process or network boundary.

## Evaluation against synchronized policies

A committed snapshot can be queried in three ways at runtime.

* **In-flow enforcement.** The Authorization PEP policy sits in an API or MCP proxy flow and asks the PDP about each request. `PERMIT` lets it through; a denial or no matching policy returns the deny status you configure, 403 by default. If no snapshot is available yet, the request is refused rather than allowed.
* **AuthZEN API.** An authorization API exposes the engine over AuthZEN 1.0 for enforcement points outside the Gateway. It covers single and batch evaluation, subject, resource, and action search, plus a discovery document.
* **AuthZEN endpoints on an existing API.** The same endpoints, published through a policy on a standard v4 API, when you want them on a path and plan you already control.
