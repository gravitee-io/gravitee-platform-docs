---
hidden: false
noIndex: false
description: Answer AuthZEN 1.0 requests on a v4 API you already have with the Authz PDP AuthZen Endpoint policy, on its own path and plan.
---

# AuthZEN PDP policy

The **Authz PDP AuthZen Endpoint** policy answers AuthZEN 1.0 requests on a v4 HTTP proxy API that you already have. Use it when you want the AuthZEN routes on a path, a plan, and a security of your choice. Otherwise, the [AuthZEN endpoint](authzen-endpoint.md) of a PDP gateway gives you the same routes with no API to manage.

The policy asks the default engine of the gateway. It ends every request it handles with an AuthZEN answer, so the request never reaches the endpoint of the API.

## Add the policy

Each policy instance serves one kind of request, chosen in **Endpoint type**. To serve several routes, add one flow for each route, with a path that matches it, and one instance of the policy in each flow:

| Flow path | Endpoint type |
|-----------|---------------|
| `/access/v1/evaluation` | `EVALUATION` |
| `/access/v1/evaluations` | `EVALUATIONS` |
| `/access/v1/search/subject` | `SEARCH_SUBJECT` |
| `/access/v1/search/resource` | `SEARCH_RESOURCE` |
| `/access/v1/search/action` | `SEARCH_ACTION` |

Add the policy to the request phase of the flow.

## Requests and answers

The requests, the answers, and the error format are the same as those of the AuthZEN endpoint. For the details, see [Evaluate a request](authzen-endpoint.md#evaluate-a-request), [Evaluate a batch](authzen-endpoint.md#evaluate-a-batch), and [Search](authzen-endpoint.md#search).

One key of `context` differs. The policy sets `caller` to `"authzen"`, where the AuthZEN endpoint sets `"gateway"`. As with the endpoint, the gateway also sets `requestId`, `environmentId`, `organizationId`, and `apiId`, and drops any value the request sends for these keys in `context`. A key of the same name in `action.properties` still replaces the value the gateway sets.

In a batch, an evaluation that fails gets its own `false` entry and the batch answers `200`, whatever these two settings say. A search that fails always answers `503`.

## Configuration

The following table lists the configuration fields of the policy:

| Field | Default | Description |
|-------|---------|-------------|
| **Endpoint type** | `EVALUATION` | The kind of request this instance answers |
| **AuthZen body mapping** | The AuthZEN 1.0 fields | JSONPath expressions that read the subject, the action, the resource, their properties, and the context from the request body. For example, **Subject id path** is `$.subject.id` by default. Applies to `EVALUATION` and `EVALUATIONS` |
| **PDP evaluation timeout (ms)** | `1000` | How long the policy waits for a decision |
| **PDP unavailable HTTP status** | `503` | The status when a single evaluation fails or times out. `503` answers with an AuthZEN error, and `200` answers with a `false` decision |
| **Cold-start behaviour** | `DENY` | What the policy does before the gateway has loaded its policies: `DENY` fails at once, `RETRY_THEN_DENY` retries within the budget and then fails, and `PERMIT` answers with a permit |
| **Cold-start HTTP status** | `503` | The status when a single evaluation fails during a cold start. `503` answers with an AuthZEN error, and `200` answers with a `false` decision |
| **Cold-start retry budget (ms)** | `1500` | How long `RETRY_THEN_DENY` keeps retrying |
| **Cold-start retry delay (ms)** | `200` | The wait between two retries of `RETRY_THEN_DENY` |
| **Log every decision (SLF4J)** | Off | Writes one log line for each decision |
