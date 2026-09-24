---
hidden: false
noIndex: false
description: >-
  Authorization Management decides who may do what across MCP, AI model, API,
  and agent traffic. Learn how the pieces fit and where to start.
---

# Authorization Management overview

Authorization Management is Gravitee's product line for deciding who may do what. It doesn't authenticate a caller and it doesn't route a request. It answers one question for every governed interaction: may this principal take this action on this resource, under these conditions?

Within Gamma, Authorization Management provides a dedicated console for modeling your authorization world, holding the principals and resources that policies refer to, authoring those policies, and deploying them to the gateways that enforce them.

<figure><img src="../.gitbook/assets/gamma-mcp-authorization-policies.png" alt="The MCP Policies page in Authorization Management, showing tiles for total policies, deployed, draft, and unique targets, above a searchable policy list with name, target, target gateways, status, and updated columns"><figcaption><p>The MCP Policies page. Every policy category shares this layout: counters at the top, a search box and a status filter, and the policies themselves with the gateways they target.</p></figcaption></figure>

## Why Authorization Management exists

Every runtime in an enterprise already has some notion of access control, and that is the problem. An estate that runs APIs, MCP servers, AI models, and agents side by side runs into the following:

* **Each protocol carries its own model.** An API gateway has plans and scopes, an MCP server has whatever its author wrote, and a model provider has a key that either works or doesn't. The same rule is expressed four ways and drifts between the copies.
* **Agent traffic collapses the identity chain.** An agent calls a tool with its own credential, so the upstream sees the agent rather than the person it acts for. Access is granted to the agent once and never narrowed again.
* **Permission lives in application code.** A check written inside a service can't be reviewed by anyone outside that service's team, can't be changed without a deployment, and can't be reported on across the estate.
* **A decision that costs a network hop gets skipped.** When authorization means calling a remote service on every request, latency budgets push teams to cache the answer, coarsen the check, or drop it.

## What Authorization Management does

Authorization Management separates the decision from the enforcement. The **Gamma console** is where you model entities, author policies, and register the gateways that will enforce them. The **Policy Decision Point (PDP)** is the engine that reaches the verdict, and it runs inside the gateway rather than beside it, so a decision costs no network call.

Authorization Management provides the following key capabilities:

* **Fine-grained policies across every traffic type.** One policy language covers MCP servers and their tools, AI providers and models, APIs down to the endpoint and data field, and A2A agents. See [Create, update, and delete policies](../configure/create-update-delete-policies.md).
* **A shared entity model.** Principals and resources are held once and reused by every policy. Resources are imported from the Catalog so their identifiers match what the gateway actually routes, and principals are synced from Gravitee Access Management, imported from a file, or created by hand. See [Import resources from Catalog](../manage/resources/import-resources-from-catalog.md) and [Sync principals from Access Management](../manage/principals/sync-principals-from-access-management.md).
* **In-gateway evaluation.** A deployed policy is compiled into an immutable snapshot inside each targeted gateway, and evaluated there. Nothing calls back to the control plane to decide a request. See [Authorization policy synchronization](../authz-gateway-sync.md).
* **Enforcement beyond the gateway.** The same engine is exposed over [AuthZEN 1.0](https://openid.net/specs/authorization-api-1_0.html) for enforcement points that aren't Gravitee proxies, including batch evaluation and subject, resource, and action search. See [Configure the Gravitee Gateway as a runtime](../evaluate/configure-gravitee-gateway-as-runtime.md).

## The building blocks

Five objects carry the whole model, and each one builds on the one before it:

| Building block | What it is | Start here |
| --- | --- | --- |
| **Schema** | The declaration of your authorization world: the entity types that exist, which types may contain which others, and the actions the engine reasons about. Everything else is written against it. | [Manage schemas](../manage/schemas/README.md) |
| **Entity** | A concrete principal or resource, with a canonical entity ID, typed attributes, and links to its parents. A `User` and a `Group` are principals; an `MCPServer`, a `Model`, and an `API` are resources. | [Manage principals](../manage/principals/README.md) |
| **Action** | The verb a policy authorizes, such as `call_tool`, `invoke`, or `read`. A policy can only grant or forbid an action that's defined here, and every action carries the reserved `action.` prefix in its entity ID. | [Manage actions](../manage/actions/README.md) |
| **Policy** | One or more `permit` and `forbid` statements over principals, actions, and resources, with optional conditions. A policy is a draft until you deploy it. | [Create, update, and delete policies](../configure/create-update-delete-policies.md) |
| **PDP gateway** | A registration that tells Authorization Management which decision engine a policy is aimed at, optionally bound to a sharding tag, and optionally publishing an AuthZEN endpoint. | [Configure the Gravitee Gateway as a runtime](../evaluate/configure-gravitee-gateway-as-runtime.md) |

Resources are imported rather than typed, because a policy only bites when its resource ID matches the identifier the gateway routes to. Import the target first, then write the policy against it.

## The policy language

Policies are written in Gravitee Authorization Policy Language (GAPL). A statement names a principal, an action, and a resource, and either permits or forbids the combination:

```
permit (
  principal == User::"alice",
  action == Action::"call_tool",
  resource == MCPServer::"github-server"
);
```

A statement can carry a `when` block of conditions that must hold at request time, so one statement covers what would otherwise need many:

```
permit (
  principal == Group::"platform-engineers",
  action == Action::"invoke",
  resource == Model::"gpt-4o"
)
when {
  context.time.hour >= 9 && context.time.hour < 17
};
```

`forbid` wins. Anything a forbid statement matches is denied even when a permit statement matches it too, so forbid is how you carve out an exception rather than rewrite the grant.

{% hint style="info" %}
GAPL will look familiar if you know Cedar, but it isn't Cedar. The parser rejects keywords GAPL doesn't implement, including `unless`, and reports them as diagnostics in the editor.
{% endhint %}

The editor offers a **Visual** mode that builds statements from chip pickers and compiles them to GAPL for you, and a **Code** mode with syntax highlighting. GAPL that the visual editor can't represent stays editable in Code mode, and the **Visual** toggle is disabled with an explanation rather than silently rewriting your policy.

## How a request is decided

At runtime, the pieces meet in the gateway:

1. A request reaches a proxy that carries the Authorization PEP policy in its flow. The policy builds a subject, action, and resource triple from the request.
2. It asks the PDP running in the same gateway process. There's no network hop, so the decision doesn't move the request's latency budget.
3. The PDP evaluates the triple against its committed snapshot and answers `PERMIT` or a denial.
4. On `PERMIT`, the request continues to the upstream. On a denial, or when no policy matches, the proxy fails the request with the deny status you configured.

Enforcement fails closed. A gateway that has no snapshot yet, a PDP that doesn't answer in time, and a request that matches no permit statement all end the same way: denied. For what flows from the console to the gateway and how long it takes to take effect, see [Authorization policy synchronization](../authz-gateway-sync.md).

## Where each task lives in the console

The Authorization Management sidebar groups its pages by what you do with them:

| Sidebar group | Page | What it covers |
| --- | --- | --- |
| **General** | **Quick Start** | Counts of MCP, agent, and AI model policies and of principals, a setup walkthrough, and a diagram of how a decision is reached. |
| **Policy Structure** | **Entities** | The principals and resources policies refer to, on two tabs, with their attributes, relationships, and source. |
| **Policy Structure** | **Actions** | The verbs policies may authorize, and the entity IDs they're referenced by. |
| **Policy Structure** | **Schema** | The entity types, containment rules, and action definitions everything else is written against. |
| **Policy Management** | **MCPs**, **AI Models**, **APIs**, **A2A Agents**, **Custom Policies** | One page per policy category, each with its own policy list, counters, search, and status filter. |
| **PDP Gateways** | **PDP Gateways** | The registered decision engines, the tag each is bound to, and the AuthZEN endpoints published for them. |

## Policy categories

A policy belongs to exactly one category, and the category decides what it can target and which resource types its statements may name:

| Category | What it governs | Target | Resource types |
| --- | --- | --- | --- |
| **MCP Policies** | What principals may do on an MCP server, its tools, prompts, and resources. | MCP Server | `MCPServer`, `MCPTool`, `MCPPrompt`, `MCPResource` |
| **AI Model Policies** | Who may invoke a provider or a specific model, and under what usage or cost ceilings. | Model | `LLMProvider`, `Model` |
| **API Policies** | Which principals reach an API and its endpoints, and which data fields they may see. | API | `API`, `Endpoint`, `DataField` |
| **A2A Policies** | Which principals may invoke each A2A agent. | Agent | `Agent` |
| **Custom Policies** | Anything not routed as an MCP, API, agent, or model: internal applications, data assets, and bespoke resources. | None | User-defined |

A custom policy has no target, which is what makes it the catch-all. See [Custom policies overview](../configure/custom-policies/custom-policies-overview.md).

## Conditions

Each category offers pre-built condition snippets in the editor, as chips you insert into a statement's `when` block. You can also type your own. The following table shows one snippet from each category:

| Category | Example condition | Full list |
| --- | --- | --- |
| **MCP** | `context.device.trusted == true` | [MCP policy examples](../configure/mcp-policy-examples.md) |
| **AI Model** | `context.usage.tokens_per_day(principal) < 50000` | [AI policy example](../configure/ai-policy-example.md) |
| **API** | `context.auth.scopes.contains("orders:read")` | [API policy examples](../configure/api-policy-examples.md) |
| **A2A** | `context.source.ip.in_cidr("10.0.0.0/8")` | [Create, update, and delete policies](../configure/create-update-delete-policies.md) |
| **Custom** | `context.auth.mfa == true` | [Custom policies overview](../configure/custom-policies/custom-policies-overview.md) |

Conditions test attributes on the principal, the resource, or the request context, so the values they read have to exist. An attribute a policy tests is declared in the schema and filled in on the entity.

## Policy lifecycle

A policy has one of the following statuses:

| Status | What it means |
| --- | --- |
| **Draft** | Saved but not enforced. Use it to stage and review a policy before it touches traffic. |
| **Deployed** | Published to the PDP gateways it targets, and enforced by them. |
| **Disabled** | Previously deployed and since undeployed. The policy is kept, and the gateways drop it. |

Deploying and undeploying both reach the gateway through the same synchronization path, so neither takes effect the instant you click. The console reports the state you asked for rather than a per-gateway acknowledgment.

## Use cases for Authorization Management

Each of the following tables pairs an outcome with the feature that delivers it.

### Govern what agents may do

| Outcome | Feature |
| --- | --- |
| An agent reaches only the MCP tools its identity permits, and a call that matches no permit is denied rather than allowed by omission. | [MCP policy examples](../configure/mcp-policy-examples.md) |
| A tool that's safe to read with and costly to write with is governed by two statements against one server, instead of two servers. | [Create, update, and delete policies](../configure/create-update-delete-policies.md) |
| Which principals may invoke a given A2A agent is decided centrally rather than by the agent itself. | [Create your first policy](create-your-first-policy.md) |
| An agent identity carries attributes, such as a tier or an owner, that conditions can test at request time. | [Add attributes to principals](../manage/principals/add-attributes-to-principals.md) |

### Control AI model access and spend

| Outcome | Feature |
| --- | --- |
| Access to an AI provider or a specific model is granted per principal rather than per API key. | [AI policy example](../configure/ai-policy-example.md) |
| A token budget or a cost ceiling is expressed as a condition on the grant itself, so exceeding it denies rather than warns. | [AI policy example](../configure/ai-policy-example.md) |
| A model is available to one group during business hours and to another at any time, from a single policy. | [Create, update, and delete policies](../configure/create-update-delete-policies.md) |

### Write policy against your existing identities

| Outcome | Feature |
| --- | --- |
| Principals come from your Gravitee Access Management directory rather than a second list maintained by hand. | [Sync principals from Access Management](../manage/principals/sync-principals-from-access-management.md) |
| A grant to a group is inherited by every member, so adding a person to the group is the only access change needed. | [Build principal relationships](../manage/principals/build-principal-relationships.md) |
| Resources carry the identifiers the gateway routes to, because they were imported from the Catalog rather than typed. | [Import resources from Catalog](../manage/resources/import-resources-from-catalog.md) |
| A principal that has no home in your directory, such as a service account, is created locally alongside the synced ones. | [Create a local principal](../manage/principals/create-a-local-principal.md) |

### Enforce the same decision everywhere

| Outcome | Feature |
| --- | --- |
| Every gateway reaches the same verdict locally, so authorization adds no network hop. | [Configure the Gravitee Gateway as a runtime](../evaluate/configure-gravitee-gateway-as-runtime.md) |
| A policy is scoped to the gateways of one region or one shard, rather than published everywhere. | [Configure the Gravitee Gateway as a runtime](../evaluate/configure-gravitee-gateway-as-runtime.md) |
| An enforcement point that isn't a Gravitee proxy asks the same engine over a standard AuthZEN API. | [Configure the Gravitee Gateway as a runtime](../evaluate/configure-gravitee-gateway-as-runtime.md) |
| A change made in the console is picked up by running gateways without a redeployment of the proxies. | [Policy syncs](../evaluate/policy-syncs.md) |

## How Authorization Management fits into Gamma

Gamma unifies its product lines under one platform: API Management, Event Stream Management, Agent Management, and Authorization Management. They share the following foundations:

* **A common Catalog.** This catalog holds APIs, events, tools, agents, MCP servers, and models.
* **A common authorization engine.** Authorization Management is that engine, and every other module writes its fine-grained access control here rather than inventing its own.
* **Common enforcement points.** The AI Gateway, API Gateway, and Event Gateway evaluate the same policies at the wire level.

Authorization Management is the only module that doesn't put traffic on the wire. It supplies the decision the others enforce. [Agent Management](../../agent-management/overview/README.md) contributes the MCP servers, models, and agents you import as resources, and its MCP and LLM proxies are where those policies bite. [API Management](../../api-management/get-started/api-management-overview.md) contributes the APIs, and its proxies enforce policy alongside their own plans and policy chains. [Event Stream Management](../../event-stream-management/get-started/event-stream-management-overview.md) contributes Kafka streams to the same Catalog.

For the platform as a whole, and for the modules Authorization Management sits beside, see the [Gamma overview](../../platform-management/overview.md).

## Next steps

If you're new to Authorization Management, work through the following quickstarts in order:

1. [**Create your first user**](create-your-first-user.md). Put a principal in place for policies to refer to.
2. [**Import your first resource from the AI Catalog**](import-your-first-resource-from-agent-catalog.md). Bring in a target whose ID matches what the gateway routes.
3. [**Create your first policy**](create-your-first-policy.md). Permit an action, deploy it, and watch the gateway pick it up.

To install or configure the platform underneath, see the [installation guides](../../platform-management/install/README.md).
