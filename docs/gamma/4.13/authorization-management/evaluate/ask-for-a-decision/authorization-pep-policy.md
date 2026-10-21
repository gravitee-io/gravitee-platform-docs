---
hidden: false
noIndex: false
description: Configure the Gravitee Authorization PEP (GAPL) policy, and learn how it builds the principal, action, resource, and context that your policies evaluate.
---

# Authorization PEP policy

The **Gravitee Authorization PEP (GAPL)** policy enforces your authorization policies on the gateway. It runs in the request phase of a flow, asks the default engine of the gateway for a decision on every request, and lets the request through only when the decision is a permit.

You can add it to the flows of HTTP proxy, MCP proxy, LLM proxy, and A2A proxy APIs. When you turn on fine-grained authorization on a Composite MCP Server, Agent Management adds it to the flows of the server for you. For details, see [Govern MCP tool access](../../../agent-management/build/configure-your-mcp/govern-mcp-tool-access.md).

## What happens to a request

| Decision | What the policy does |
|----------|----------------------|
| **Permit** | The request continues through the flow |
| **Forbid** or **Not applicable** | The request ends with **HTTP status on deny**, `403` by default, and **Body on deny** |
| The engine doesn't answer within **PDP evaluation timeout**, or isn't running | The request ends with `503` |
| The PDP rejects the request, for example because it's malformed | The request ends with `500` |
| The gateway hasn't loaded its policies yet | **Cold-start behaviour** decides |

## How the request is built

The policy turns each gateway request into the request your policies evaluate:

| Your policies read | Built from |
|--------------------|-----------|
| `principal` | **Subject type** and **Subject expression**, as `<Subject type>::"<value>"`, such as `User::"alice"` |
| `action` | **Action expression**. For how the name becomes an action, see [Namespaces](../../gapl-reference/policy-statements.md#namespaces) |
| `resource` | **Resource type** and **Resource expression**, as `<Resource type>::"<value>"` |
| Attributes of `principal` | **Subject properties (EL-mapped)** |
| Attributes of `resource` | **Resource properties (EL-mapped)** |
| `context` | The keys the gateway sets, **Context (EL-mapped)**, and **Action properties (EL-mapped)** |

A property replaces a stored attribute with the same name, for that request only. When the principal or the resource doesn't exist as an entity, its properties still make it an entity with those attributes and no parents.

### Keys the gateway sets in context

| Key | Value | Present |
|-----|-------|---------|
| `caller` | `"pep"` | Always |
| `requestId` | The ID of the gateway request | Always |
| `environmentId` | The ID of the environment | Always |
| `organizationId` | The ID of the organization | Always |
| `apiId` | The ID of the API | Always |
| `conversationId` | The conversation ID | When an LLM, A2A, or MCP proxy has set one for the request, or else when the request has an `X-Gravitee-Conversation-Id` header of up to 200 characters |
| `agent` | The calling agent, an `AgentIdentity` entity | When **Agent identity resolution** is on and the token identifies an agent |
| `agent_origin` | The agent the call started from, an `AgentIdentity` entity | With `agent`, when the token names an origin |
| `agent_chain` | The agents the call went through, a `Set` of `AgentIdentity` entities | With `agent`, when the token carries a chain |
| `noSnapshotPolicy` | `"permit"` | When **Cold-start behaviour** is `PERMIT` |

The gateway sets no other key. A key such as `context.time` or `context.device` is present only when you add it under **Context (EL-mapped)**.

### Add your own context keys

Each row of **Context (EL-mapped)** adds one key to `context`. The value is a literal or a Gravitee Expression Language expression, evaluated for each request. A value is evaluated as an expression only when the whole value starts with `{#` and ends with `}`:

| Attribute name | Value |
|----------------|-------|
| `tenant` | `acme` |
| `clientIp` | `{#request.remoteAddress}` |
| `region` | `{#request.headers['X-Region'][0]}` |

A literal arrives as a `String`. An expression arrives as the type it evaluates to, so a header value arrives as a `String` even when it holds digits: compare it with `context.retries == "3"`, not with `context.retries == 3`. When an expression fails, the key is left out.

A row named `requestId` replaces the request ID. A row named `caller`, `environmentId`, `organizationId`, or `apiId` is overwritten by the gateway, and so is a row named `conversationId` when the request has a conversation ID. While **Agent identity resolution** is on, the configuration form refuses rows named `agent`, `agent_origin`, and `agent_chain`.

A row of **Action properties (EL-mapped)** with the name of a context key replaces that key, including the keys the gateway sets, such as `caller`.

## Configuration

| Field | Default | Description |
|-------|---------|-------------|
| **Subject type** | | The entity type of the principal, such as `User`. A literal, or an expression evaluated for each request |
| **Subject expression** | | An expression that reads the principal ID from the request, such as `{#request.headers['X-User-ID'][0]}` |
| **Subject properties (EL-mapped)** | | Attribute name and expression pairs added to the principal |
| **Action expression** | | An expression that reads the action name, such as `{#request.method.toLowerCase()}` |
| **Action properties (EL-mapped)** | | Name and expression pairs added to `context` |
| **Resource type** | `Resource` when empty | The entity type of the resource. A literal, or an expression |
| **Resource expression** | | An expression that reads the resource ID, such as `{#request.path}` |
| **Resource properties (EL-mapped)** | | Attribute name and expression pairs added to the resource |
| **Agent identity resolution** | Off | Reads the calling agent from the access token and sets `agent`, `agent_origin`, and `agent_chain`. The token claims must be on the request: enable payload extraction on the OAuth2 plan, or place a JWT policy before this one |
| **Context (EL-mapped)** | | Name and expression pairs added to `context` |
| **HTTP status on deny** | `403` | The status of a denied request, between `400` and `499` |
| **Body on deny** | | The message of a denied request. A client that accepts JSON, with an `Accept` header of `application/json` or `*/*`, gets `{"message": "<Body on deny>", "http_status_code": <HTTP status on deny>}`, and any other client gets the message as plain text |
| **Log every decision (SLF4J)** | Off | Writes one log line for each decision |
| **Emit tracing span** | Off | Emits an OpenTelemetry span for each decision. Gateway tracing must be on |
| **Record subject and resource ids on the span (PII)** | Off | Adds the principal and resource IDs to the span. Applies only when **Emit tracing span** is on |
| **PDP evaluation timeout (ms)** | `1000` | How long the policy waits for a decision before it ends the request with `503` |
| **Cold-start behaviour** | `DENY` | What the policy does before the gateway has loaded its policies: `DENY` ends the request with `503`, `RETRY_THEN_DENY` retries within the budget and then ends it with `503`, and `PERMIT` lets it through |
| **Cold-start retry budget (ms)** | `1500` | How long `RETRY_THEN_DENY` keeps retrying |
| **Cold-start retry delay (ms)** | `200` | The wait between two retries of `RETRY_THEN_DENY` |
