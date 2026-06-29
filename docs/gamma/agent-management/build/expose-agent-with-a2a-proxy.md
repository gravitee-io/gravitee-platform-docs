---
hidden: false
noIndex: true
---

# Expose your agent with the A2A Proxy
<!-- Source: CreateA2aProxyPage.tsx, FetchAgentCardUseCase.java -->

The A2A (Agent-to-Agent) Proxy makes an agent's skills discoverable and callable by other agents — across trust boundaries, providers, and organizations. It implements the A2A protocol by serving a `/.well-known/agent.json` descriptor that advertises the agent's skills, and then governs every invocation through the AI Gateway.

## What the A2A Proxy does

When you expose an agent through the A2A Proxy:

1. **Skill discovery** — The proxy serves `/.well-known/agent.json`, the A2A standard for advertising agent capabilities. Other agents or systems can discover what this agent can do by reading the descriptor.
2. **Per-skill authorization** — The proxy publishes each discovered skill to Authorization Management as a cataloged entity. This means you can write fine-grained authorization policies at the skill level: _"Agent X can invoke the `analyze-contract` skill but not the `execute-payment` skill."_
3. **Wire-level governance** — Every skill invocation passes through the AI Gateway with full observability, authentication, and policy enforcement — the same governance applied to MCP and LLM traffic.

## How skill publishing works

When an agent is exposed through the A2A Proxy:

1. The proxy reads the agent's declared skills (from the Catalog or the agent's A2A descriptor)
2. Each skill is published to Authorization Management as a cataloged entity with metadata (skill name, description, input/output schemas)
3. Authorization policies can reference individual skills as resources
4. When another agent invokes a skill, the AI Gateway evaluates the applicable policies before forwarding the invocation

This is structurally different from tool-level authorization on MCP Proxies — skills represent higher-level capabilities that may span multiple tool invocations.

## Create an A2A Proxy

1. From the Gamma console sidebar, select **Agent Management**.
2. Navigate to **Build** and select **A2A Proxies**.
3. Select **Create A2A proxy** to launch the wizard.
4. **Step 1: Define**: Provide a name and optional description for your proxy.
5. **Step 2: Connect**: Enter the target A2A endpoint URL. The gateway will resolve its configuration by fetching `/.well-known/agent-card.json`.
6. **Step 3: Secure**: Attach security plans to control who can access the proxy.
7. **Step 4: Review**: Confirm the settings and select **Create A2A proxy**.

The A2A Proxy is created and begins serving the `/.well-known/agent-card.json` descriptor. Other agents and systems can now discover and invoke this agent's skills through the AI Gateway.

## The `/.well-known/agent-card.json` descriptor

The A2A Proxy generates and serves an agent card descriptor at:

```
https://<your-gateway-host>/<context-path>/.well-known/agent-card.json
```

This descriptor includes standard capabilities and inline skills. For example:

```json
{
  "agentType": "AUTONOMOUS",
  "capabilities": {
    "mcp": true
  },
  "skills": [
    {
      "name": "analyze-contract",
      "description": "Analyzes a PDF contract for compliance."
    }
  ]
}
```

## Next steps

* [Create an agent identity](create-an-agent-identity.md) — An agent must have an identity before it can be exposed through the A2A Proxy.
* [Add policies to your MCP server](configure-your-mcp/add-policies-to-mcp-server.md) — The policy model for skill-level authorization follows the same pattern as tool-level authorization.
