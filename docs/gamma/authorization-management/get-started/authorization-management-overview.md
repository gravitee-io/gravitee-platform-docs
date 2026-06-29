---
hidden: false
noIndex: false
---

# Authorization Management overview
<!-- GAP-STRUCTURAL: Missing procedural content source -->

Authorization Management provides fine-grained, catalog-aware access control across all Gamma traffic types — APIs, MCP servers, AI models, agents, events, and custom resources. Policies are written in GAPL (Gravitee Authorization Policy Language), a subset of the Cedar policy language, and enforced at the wire level by Gamma's gateways.



## How it works

Authorization Management connects three things:

1. **Entities** — The things you want to protect (APIs, MCP tools, AI models). Entities are registered in the Catalog or created directly in Authorization Management.
2. **Principals** — The identities making requests (users, groups, agents). Principals can be synced from your identity provider via SCIM, synchronized from Access Management (AM), or created locally. When synchronizing users from AM, sync progress is surfaced via live toast notifications, and the principal list updates dynamically without requiring a page refresh.
3. **Policies** — Rules that grant or deny access. Each policy declares an effect (`permit` or `forbid`), a principal, an action, a resource, and optional conditions.

When a request arrives at the API Gateway, AI Gateway, or Event Gateway, the Policy Decision Point (PDP) evaluates all applicable policies and returns a permit or deny decision at microsecond latency with no network hop.

## Policy language: GAPL

GAPL (Gravitee Authorization Policy Language) uses Cedar syntax. A policy looks like:

```
permit (
  principal == user::"alice",
  action == action::"invoke",
  resource == MCPTool::"github-create-issue"
);
```

Policies support optional `when` conditions for time-of-day restrictions, IP range checks, token budgets, and custom attribute matching.

{% hint style="info" %}
GAPL supports a subset of the Cedar policy language optimized for the Gamma visual editor. Cedar features like `unless` clauses are not available in the GAPL editor.
{% endhint %}

## Policy categories

Authorization Management organizes policies into service-specific categories. Each category has its own page with a policy list, KPI tiles, search, and status filter.

| Category              | What it governs                                                                                                                  | Entity types                               |
| --------------------- | -------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------ |
| **MCP Policies**      | Access to MCP servers, their tools, prompts, and resources.                                                                      | MCPServer, MCPTool, MCPPrompt, MCPResource |
| **AI Model Policies** | Access to AI providers and specific models, with cost and token usage constraints.                                               | LLMProvider, LLMModel                      |
| **API Policies**      | Access to API proxies, their endpoints, and data fields.                                                                         | API, Endpoint, DataField                   |
| **Custom Policies**   | Policies for resources not routed as MCP, API, Agent, LLM, or Event — internal applications, data assets, and bespoke resources. | Custom (user-defined)                      |

## Condition snippets

Each policy category provides pre-built condition snippets you can insert into your policies:

### MCP conditions

| Condition              | GAPL snippet                                       |
| ---------------------- | -------------------------------------------------- |
| **Business hours**     | `context.time.hour >= 9 && context.time.hour < 17` |
| **Trusted device**     | `context.device.trusted == true`                   |
| **Corporate IP range** | `context.source.ip.in_cidr("10.0.0.0/8")`          |

### AI Model conditions

| Condition            | GAPL snippet                                      |
| -------------------- | ------------------------------------------------- |
| **Token budget**     | `context.usage.tokens_per_day(principal) < 50000` |
| **Cost ceiling**     | `context.usage.cost_per_day(principal) < 100`     |
| **PII filter on**    | `context.guardrails.pii == true`                  |
| **Model size small** | `resource.size in ["small", "medium"]`            |

### API conditions

| Condition              | GAPL snippet                                          |
| ---------------------- | ----------------------------------------------------- |
| **Corporate IP range** | `context.source.ip.in_cidr("10.0.0.0/8")`             |
| **Scope present**      | `context.auth.scopes.contains("orders:read")`         |
| **Rate limit**         | `context.rate.per_minute(principal) < 100`            |
| **Tenant match**       | `context.request.header.x_tenant == principal.tenant` |

## Policy lifecycle

Each policy has a status:

| Status       | Description                                                                           |
| ------------ | ------------------------------------------------------------------------------------- |
| **Draft**    | The policy is saved but not enforced. Use this to prepare policies before deployment. |
| **Deployed** | The policy is active and enforced by the gateway PDP.                                 |
| **Disabled** | The policy was previously deployed but is now suspended without deletion.             |

## Integration with other product areas
<!-- GAP: 126 · Narrowed · AGENT and EVENT policy types exist in entity-kind-registry.ts but have no dedicated ServicePageConfig files or policy management pages. DashboardPage.tsx confirms Agents and 'Users and groups' cards show 'Coming soon'. Needs: Engineering input -->

Authorization Management is not isolated — it integrates with the API Gateway, AI Gateway, and Event Gateway as a shared enforcement layer:

* **API Management** — API proxies reference Authorization Management policies for endpoint-level access control. The API overview checklist includes an "Apply authorization" step.
* **Agent Management** — MCP Proxies and LLM Proxies enforce authorization policies at the tool and model level. Policy entities are populated from the Catalog.
* **Event Stream Management** — Kafka services can be governed by authorization policies targeting virtual clusters, topics, and consumer groups.

## Next steps

* [Create authorization policies](../configure/create-update-delete-policies.md) — Learn how to create, edit, and deploy policies for each service category.
