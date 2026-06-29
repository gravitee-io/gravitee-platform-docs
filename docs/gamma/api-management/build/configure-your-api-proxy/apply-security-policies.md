---
hidden: false
noIndex: false
---

# Apply security policies

Policies are fine-grained rules that the API Gateway evaluates on every request and response. They run on top of security plans and provide capabilities like rate limiting, content transformation, header manipulation, and authorization checks.

## How policies work

Policies execute in a chain at two phases of the request lifecycle:

* **Request phase** — Evaluated after the security plan authenticates the consumer, before the request reaches your backend.
* **Response phase** — Evaluated after the backend responds, before the response is returned to the consumer.

Each policy in the chain can inspect, transform, or reject the request or response. If a policy rejects a request, subsequent policies in the chain are not executed.

## Authorization Management integration

<!-- Source: apis.ts (apisServiceConfig), PolicyEditorSheet.tsx, ServicePolicyPage.tsx @ c07f5cdff9 -->

In Gamma, API proxies can use **Authorization Management** for fine-grained, catalog-aware authorization that goes beyond plan-level authentication. The Policy Decision Point (PDP) runs directly inside the API Gateway with microsecond-scale latency and no network hop.

### Create an API authorization policy

1. From the Gamma console sidebar, select **Authorization**.
2. In the Authorization sidebar, select **APIs** to open the **API Policies** page.
3. The policy list shows KPI tiles (total policies, deployed count, draft count, and unique targets), a search bar, and a status filter (All, Draft, Deployed, Disabled).
4. Select **Create Policy for API**.
5. In the policy editor, enter a **Policy name** and optional **Description**.
6. Build the policy using either mode:

**Visual editor** (default):

   1. Each statement starts with an **effect** toggle — select **permit** or **forbid**.
   2. Pick **principals** — the users, groups, or agents this policy applies to.
   3. Pick **actions** — the operations being governed.
   4. Pick **resources** from the API resource groups:

      | Resource group | Entity type | Description |
      | --- | --- | --- |
      | **API** | `API` | The API proxy itself |
      | **Endpoints** | `Endpoint` | A specific endpoint within the API |
      | **Data Fields** | `DataField` | A data field within an API response |

   5. Optionally insert a **condition snippet**:

      | Condition | GAPL snippet |
      | --- | --- |
      | **Corporate IP range** | `context.source.ip.in_cidr("10.0.0.0/8")` |
      | **Scope present** | `context.auth.scopes.contains("orders:read")` |
      | **Rate < 100/min** | `context.rate.per_minute(principal) < 100` |
      | **Tenant match** | `context.request.header.x_tenant == principal.tenant` |

   6. Add additional statements as needed. Drag to reorder.

**Code editor** — Switch to the **Code** tab to write GAPL directly in a line-numbered editor. You can switch between Visual and Code modes; the editor syncs changes when possible.

7. Select **Create policy** to save as Draft, or **Create and Deploy policy** to save and deploy in one step.

### Deploy and manage

After creating a policy in Draft status:

* Select **Deploy to PDP** to activate it. The gateway syncs the policy within 30 seconds — no restart required.
* Select **Undeploy** on a deployed policy to disable it. The gateway drops it within 30 seconds.

For more details on the full policy language and all service categories, see [Create authorization policies](../../../authorization-management/configure/create-update-delete-policies.md).

## Common policy types

Gamma's initial release supports all existing Gravitee APIM policies (40+), including common policies like rate limiting, transform headers, assign content, authentication, validation, and traffic control. Policy behavior and configuration fields are identical to API Management.

| Policy                | Phase              | Description                                                             |
| --------------------- | ------------------ | ----------------------------------------------------------------------- |
| **Rate Limiting**     | Request            | Limits the number of requests a consumer can make within a time window. |
| **Transform Headers** | Request / Response | Add, remove, or modify HTTP headers.                                    |
| **Assign Content**    | Request / Response | Override the request or response body.                                  |

{% hint style="info" %}
Gamma inherits the existing APIM policy catalog. For the complete list of available policies and their configuration fields, refer to the [API Management policy reference documentation](https://documentation.gravitee.io/apim/guides/policies).
{% endhint %}

## Next steps

* [Establish consumer access](establish-consumer-access.md) — Create applications and subscriptions for your secured API.
