---
hidden: false
noIndex: false
description: Authorization Management enforces fine-grained, catalog-aware access control across API, MCP, AI model, and agent traffic. Learn how the pieces connect.
---

# Authorization Management overview

Authorization Management provides fine-grained, catalog-aware access control across all Gamma traffic types: APIs, MCP servers, AI models, agents, and custom resources. Policies are written in Gravitee Authorization Policy Language (GAPL), a subset of the Cedar policy language, and enforced at the wire level by Gamma's gateways.

## How it works

Authorization Management connects the following three things:

1. **Entities.** The things you want to protect, such as APIs, MCP tools, and AI models. Entities are registered in the Catalog or created directly in Authorization Management.
2. **Principals.** The identities making requests, such as users, groups, service accounts, and agent identities. Principals can be synced from Gravitee Access Management (AM) or from a [SCIM directory](../directories/sync-principals-from-a-scim-directory.md), imported from a file, or created locally. During an AM sync, progress is shown through live toast notifications, and the principal list updates dynamically without a page refresh.
3. **Policies.** Rules that grant or deny access. Each policy declares an effect of either `permit` or `forbid`, plus a principal, an action, a resource, and optional conditions.

When a request arrives at the API Gateway or AI Gateway, the Policy Decision Point (PDP) evaluates all applicable policies. The PDP returns a permit or deny decision at microsecond latency with no network hop.

## Policy language: GAPL

GAPL uses Cedar syntax. A policy looks like:

```
permit (
  principal == User::"alice",
  action == Action::"github.create-issue",
  resource == MCPTool::"github.create-issue"
);
```

Policies support optional `when` conditions for time-of-day restrictions, IP range checks, and custom attribute matching.

{% hint style="info" %}
A statement can have `when` and `unless` conditions, and you can write both in the **Code** view of the policy editor. See [Policy statements](../gapl-reference/policy-statements.md#conditions).
{% endhint %}

## Policy categories

Authorization Management organizes policies into service-specific categories. Each category has its own page with a policy list, KPI tiles, search, and status filter. The following table describes each policy category:

| Category              | What it governs                                                                                                                      | Entity types                               |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------ |
| **MCP Policies**      | Access to MCP servers, their tools, prompts, and resources.                                                                          | `MCPServer`, `MCPTool`, `MCPPrompt`, `MCPResource` |
| **AI Model Policies** | Access to AI providers and specific models, with cost and token usage constraints.                                                   | `LLMProvider`, `Model`                         |
| **API Policies**      | Access to API proxies, their endpoints, and data fields.                                                                             | `API`, `Endpoint`, `DataField`                   |
| **A2A Policies**      | Which principals can invoke each A2A agent.                                                                                          | `Agent`                                      |
| **Custom Policies**   | Policies for resources not routed as MCP, API, Agent, or AI Model: internal applications, data assets, and bespoke resources. | Custom (user-defined)                      |

## Condition snippets

Each policy category provides pre-built condition snippets you can insert into your policies.

### MCP conditions

The following conditions are available for MCP policies:

| Condition              | GAPL snippet                                       |
| ---------------------- | -------------------------------------------------- |
| **Business hours**     | `context.time.hour >= 9 && context.time.hour < 17` |
| **Trusted device**     | `context.device.trusted == true`                   |

### AI Model conditions

The following conditions are available for AI Model policies:

| Condition            | GAPL snippet                                      |
| -------------------- | ------------------------------------------------- |
| **PII filter on**    | `context.guardrails.pii == true`                  |

### API conditions

The following conditions are available for API policies:

| Condition              | GAPL snippet                                          |
| ---------------------- | ----------------------------------------------------- |
| **Scope present**      | `context.auth.scopes.contains("orders:read")`         |
| **Tenant match**       | `context.request.header.x_tenant == principal.tenant` |

### A2A conditions

The following conditions are available for A2A policies:

| Condition              | GAPL snippet                                       |
| ---------------------- | -------------------------------------------------- |
| **Business hours**     | `context.time.hour >= 9 && context.time.hour < 17` |
| **Trusted device**     | `context.device.trusted == true`                   |

### Custom conditions

The following conditions are available for custom policies:

| Condition              | GAPL snippet                                       |
| ---------------------- | -------------------------------------------------- |
| **MFA required**       | `context.auth.mfa == true`                         |
| **Business hours**     | `context.time.hour >= 9 && context.time.hour < 17` |
| **Owner only**         | `resource.owner == principal`                      |

## Policy lifecycle

Each policy has one of the following statuses:

| Status       | Description                                                                           |
| ------------ | ------------------------------------------------------------------------------------- |
| **Draft**    | The policy is saved but not enforced. Use this to prepare policies before deployment. |
| **Deployed** | The policy is active and enforced by the gateway PDP.                                 |
| **Disabled** | The policy was previously deployed but is now suspended without deletion.             |

## Integration with other product areas

Authorization Management integrates with the API Gateway and AI Gateway as a shared enforcement layer across the following product areas:

* **API Management.** API proxies reference Authorization Management policies for endpoint-level access control.
* **Agent Management.** MCP Proxies and LLM Proxies enforce authorization policies at the tool and model level. Policy entities are populated from the Catalog.

## Next steps

* [Create, update, and delete policies](../configure/create-update-delete-policies.md). Learn how to create, edit, and deploy policies for each service category.
