---
hidden: false
noIndex: false
description: What your gateways record for each authorization decision, and where you read those records in Authorization Management.
---

# Decision records

Your gateways record each authorization decision they're asked for, with the rest of their analytics. The **Dashboards** and **Decisions** pages of Authorization Management read those records.

## What records a decision

A decision is recorded by what asked for it, not by the PDP gateway that evaluated it:

* The **PEP policy** records one decision for each evaluation it requests on an API's traffic.
* An **AuthZEN endpoint** of a PDP gateway records one decision for each evaluation request, and one for each item of a batch request that it returns.
* The **AuthZEN policy** records one decision for each evaluation request, and one for each item of a batch request that it returns. When a batch stops at its first permit or its first deny, the items after that one aren't recorded, even if they were already evaluated.

Search requests record no decision. The **Authorization — Overview** dashboard counts them under **Searches**.

The **Caller kind** column of the **Decisions** page shows what asked for each decision.

## What a decision record holds

Each record holds at least the following information:

* The decision, and what the caller enforced.
* The principal, the action, and the resource.
* The policies that matched, with their revision, and the reasons the PDP gave.
* The PDP gateway that evaluated the decision, the generation of the policy set it evaluated, and how long the evaluation took. A decision that failed or wasn't evaluated records **default** as the PDP gateway and `0` as the generation.
* The API the decision was requested on, with its plan and application when there's one, and the ID of the request.

## What has to be in place

The Elasticsearch reporter of the gateway writes decision records to the `gravitee-decisions-*` data streams, and the pages read them from there. An installation that stores no analytics in Elasticsearch shows empty **Dashboards** and **Decisions** pages. Gateways record decisions by default. To apply an index lifecycle policy to the decision data streams, set its name under `reporters.elasticsearch.lifecycle.policies.decisions` in `gravitee.yml`. With the Helm chart, set `es.lifecycle.enabled` to `true` and `es.lifecycle.policies.decisions` to the name of the policy.

The pages show the decisions requested on the APIs you can read. When you can't read any API, both pages are empty.

## Read the decisions

* [Monitor authorization decisions](../observe/monitor-authorization-decisions.md). The **Authorization — Overview** dashboard.
* [Review authorization decisions](../observe/review-authorization-decisions.md). The decisions one by one, with their reasons and matched policies.
