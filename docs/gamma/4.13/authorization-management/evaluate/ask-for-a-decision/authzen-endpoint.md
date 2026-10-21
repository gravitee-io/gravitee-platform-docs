---
hidden: false
noIndex: false
description: Create the AuthZEN endpoint of a PDP gateway, and call it to evaluate requests, evaluate batches, and search subjects, resources, and actions.
---

# AuthZEN endpoint

An AuthZEN endpoint exposes the engine of a PDP gateway as an AuthZEN 1.0 API, on a path of your gateways. Applications and agents call it to ask for a decision, the way they call any HTTP API. Each PDP gateway can have one endpoint.

{% hint style="warning" %}
The endpoint has a keyless plan: any client that can reach your gateways can call it, including its search routes. To put the AuthZEN routes behind a plan and security of your choice, use the [AuthZEN PDP policy](authzen-policy.md) on an API of your own.
{% endhint %}

## Create an endpoint

You create an endpoint when you register a PDP gateway, or later from its **Endpoints** tab.

### When you register a PDP gateway

1. On the **PDP Gateways** page, click **Register PDP gateway**.
2. Fill in the gateway. For the fields, see [Configure the Gravitee Gateway as a runtime](../configure-gravitee-gateway-as-runtime.md).
3. Select **Create AuthZEN endpoint**.
4. In **Endpoint path**, keep the suggested path or enter your own. A PDP gateway with neither a **Target PDP ID** nor a sharding tag gets no suggestion, so enter a path.
5. Click **Register**.

### For an existing PDP gateway

1. On the **PDP Gateways** page, select the PDP gateway.
2. Open the **Endpoints** tab.
3. In **Endpoint path**, enter a path, or leave it empty to use the suggested path.
4. Click **Add endpoint**.

The suggested path is the **Target PDP ID** of the PDP gateway, or `default` when it has none, followed by `-<sharding tag>` when it has one: `/orders/`, `/orders-eu/`, `/default/`. A path must not overlap the path of another API in the environment, and must not be `/.well-known/authzen-configuration` or a path under it.

The endpoint is deployed on the gateways that host the PDP gateway. The **Endpoints** tab then lists the routes, with a button to copy each one. To remove the endpoint, click its delete icon, and then confirm. The gateways stop serving its routes.

## Routes

For an endpoint on `/orders/`, the gateway serves the following routes:

| Method | Route | Purpose |
|--------|-------|---------|
| `POST` | `/orders/access/v1/evaluation` | Evaluate one request |
| `POST` | `/orders/access/v1/evaluations` | Evaluate a batch of requests |
| `POST` | `/orders/access/v1/search/subject` | List the subjects that are permitted an action on a resource |
| `POST` | `/orders/access/v1/search/resource` | List the resources a subject is permitted an action on |
| `POST` | `/orders/access/v1/search/action` | List the actions a subject is permitted on a resource |
| `GET` | `/orders/.well-known/authzen-configuration` | The AuthZEN metadata of the endpoint |
| `GET` | `/.well-known/authzen-configuration/orders/` | The same metadata, at the discovery location of AuthZEN. Served only when no other API in the environment uses an overlapping path. The **Endpoints** tab shows whether it is |

## Evaluate a request

Send the subject, the action, the resource, and an optional context:

```json
{
  "subject": { "type": "User", "id": "alice", "properties": { "department": "finance" } },
  "action": { "name": "read" },
  "resource": { "type": "Document", "id": "q3-report" },
  "context": { "tenant": "acme" }
}
```

| Field | Required | Becomes |
|-------|----------|---------|
| `subject.type`, `subject.id` | Yes | `principal`, such as `User::"alice"` |
| `action.name` | Yes | `action`. For how the name becomes an action, see [Namespaces](../../gapl-reference/policy-statements.md#namespaces) |
| `resource.type`, `resource.id` | Yes | `resource` |
| `subject.properties` | No | Attributes of `principal`, for this request only |
| `resource.properties` | No | Attributes of `resource`, for this request only |
| `action.properties` | No | Keys of `context` |
| `context` | No | `context` |

A property replaces a stored attribute or context key with the same name. When the principal or the resource doesn't exist as an entity, its properties still make it an entity with those attributes and no parents. For how JSON values become GAPL values, see [The context record](../../gapl-reference/context.md#how-json-values-become-gapl-values).

The gateway also sets the following keys in `context`, and drops any value the request sends for them in `context`:

| Key | Value |
|-----|-------|
| `caller` | `"gateway"` |
| `requestId` | The ID of the gateway request |
| `environmentId`, `organizationId`, `apiId` | The IDs of the environment, the organization, and the endpoint |

A key of the same name in `action.properties` still replaces the value the gateway sets, so a caller can send its own `caller`.

The response gives the decision, the reason, and the statements that decided it:

```json
{
  "decision": true,
  "context": {
    "reason": "Permitted by policy 'engineering-reads-docs'",
    "matchedPolicies": [
      { "policyId": "91b3771b-457f-4c5e-aa02-a953fa679a1a#0", "policyName": "engineering-reads-docs", "effect": "PERMIT" }
    ]
  }
}
```

`decision` is `true` only for a permit. A forbid and a request that no statement matches both give `false`. For how the reason and the policy names are written, see [Annotations](../../gapl-reference/policy-statements.md#annotations).

## Evaluate a batch

Send the requests in `evaluations`. A `type`, `id`, or `name` that an evaluation doesn't set comes from the top level. An evaluation that sets its own `subject`, `action`, or `resource` takes their `properties` only from that object, and its own `context` replaces the top-level one:

```json
{
  "subject": { "type": "User", "id": "alice" },
  "resource": { "type": "Document", "id": "q3-report" },
  "evaluations": [
    { "action": { "name": "read" } },
    { "action": { "name": "delete" } }
  ],
  "options": { "evaluations_semantic": "execute_all" }
}
```

The response lists one result for each evaluation, in the same order:

```json
{
  "evaluations": [
    { "decision": true, "context": { "reason": "...", "matchedPolicies": [] } },
    { "decision": false, "context": { "reason": "...", "matchedPolicies": [] } }
  ]
}
```

`options.evaluations_semantic` sets how far the batch runs:

| Value | Behavior |
|-------|----------|
| `execute_all` | Evaluates every request. The default |
| `deny_on_first_deny` | Stops at the first `false` |
| `permit_on_first_permit` | Stops at the first `true` |

Each evaluation of a batch also gets `batchId`, `batchIndex`, and `batchSize` in `context`. A batch without `evaluations` is evaluated as one request.

An evaluation that is invalid, or that can't be evaluated, doesn't fail the batch. The answer is still `200`, and the entry of that evaluation has `decision: false` and a `context.reason` such as `invalid_request`, with a `message`, or `pdp_unavailable`.

## Search

A search route returns the subjects, resources, or actions that your policies permit. Send the parts you know, and an optional `page`. The following fields are required:

| Route | Required fields |
|-------|-----------------|
| `search/subject` | `subject.type`, `action.name`, `resource.type`, `resource.id` |
| `search/resource` | `subject.type`, `subject.id`, `action.name`, `resource.type` |
| `search/action` | `subject.type`, `subject.id`, `resource.type`, `resource.id` |

For example, a resource search:

```json
{
  "subject": { "type": "User", "id": "alice" },
  "action": { "name": "read" },
  "resource": { "type": "Document" },
  "page": { "limit": 50 }
}
```

```json
{
  "page": { "next_token": "" },
  "results": [
    { "type": "Document", "id": "q3-report" }
  ]
}
```

An action search returns names, such as `{ "name": "read" }`. A subject or resource search returns only entities that exist on the gateway. An action search returns the permitted actions among those a schema declares for the subject and resource types, and those that exist as `Action` entities.

To get the next page, send the same request with `page.token` set to the `next_token` of the previous answer. A token works only with the request it came from, and any other change gives `400`. A page can hold fewer results than `page.limit` even when more follow, so stop only when `next_token` is empty. `page.limit` is `100` by default, and at most `1000`. For how the schema shapes action search, see [What the gateway does with a schema](../../gapl-reference/schema-language.md#what-the-gateway-does-with-a-schema).

## Errors

| Status | When |
|--------|------|
| `400` | The body is empty, isn't JSON, is larger than 256 KiB, is missing a required field, or has a field of the wrong type. The message names the field, such as `missing required field: subject.id`. A page token that doesn't match the request also gives `400` |
| `404` | The route doesn't exist under the endpoint |
| `503` | The gateway hasn't loaded its policies yet, or the engine doesn't answer or fails |

An error answer has the form `{ "error": { "status": 400, "message": "..." } }`.
