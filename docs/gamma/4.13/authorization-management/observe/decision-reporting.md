---
hidden: false
noIndex: false
description: Each authorization decision leaves a record that the Decisions page and the dashboards read. Learn which component reports it, where it's stored, and what to configure.
---

# Decision reporting

Every authorization decision leaves a decision record. The **Decisions** page and the authorization dashboards read these records, so what they show depends on what your gateways report.

## Which component reports a decision

The PDP evaluates a request and answers, but it doesn't report the decision. The component that asked the PDP reports it, once for each evaluation. The **Caller kind** of a decision names that component:

| Component | Caller kind | What it reports |
| --- | --- | --- |
| The Authorization PEP policy, on the flow of an API or an MCP server | **PEP policy** | One decision for each request it evaluates. |
| The AuthZEN endpoint of a PDP gateway | **AuthZEN endpoint** | One decision for each evaluation, including each evaluation of a batch request. |
| The AuthZEN policy, on the flow of an API | **AuthZEN policy** | One decision for each evaluation. |

A subject, resource, or action search returns candidates rather than a decision, so it leaves no decision record. The dashboards count searches from the traffic of the AuthZEN endpoint, or of the API that carries the AuthZEN policy.

## Where decision records are stored

The Elasticsearch reporter of the gateway writes each decision record to the `gravitee-decisions-*` data streams. The **Decisions** page and the dashboards read the records from there. When your gateways don't report to Elasticsearch, both stay empty.

To apply an index lifecycle policy to the decision data streams, set its name in the Elasticsearch reporter of the gateway:

```yaml
reporters:
  elasticsearch:
    lifecycle:
      policies:
        decisions: <policy name>
```

With the Helm chart, set `es.lifecycle.enabled` to `true`, and `es.lifecycle.policies.decisions` to the name of the policy. No policy is set by default.

## Failed and not-ready decisions

When the PDP doesn't answer within the **PDP evaluation timeout (ms)** of the Authorization PEP policy, 1000 by default, the policy denies the request with `503`, and the decision reads **Error** with the error type **Evaluation timeout**. When no PDP runs on the gateway, the error type is **PDP unavailable**, and any other failure is **Evaluation failed**.

While the PDP hasn't loaded its policies yet, the policy follows its **Cold-start behaviour**, and the decision reads **Not ready**. By default, the policy denies the request with `503`. Set to **PERMIT**, it lets the request through, and the decision records **Enforced** as **Allow**.

## Next steps

* [Review authorization decisions](review-authorization-decisions.md). Find a decision, and see why it was made.
* [Monitor authorization with dashboards](monitor-authorization-with-dashboards.md). Follow decisions over time.
