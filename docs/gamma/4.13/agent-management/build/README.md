---
hidden: false
noIndex: false
description: Create and configure the AI Gateway components that govern LLM, MCP, and A2A traffic, along with the agent identities for the agents in your infrastructure.
---

# Build

Create and configure the AI Gateway components that govern LLM, MCP, and A2A traffic, along with agent identities for every agent that touches your infrastructure.

* [**Create an MCP proxy**](create-an-mcp-proxy.md). Set up an MCP Proxy in front of an upstream MCP server to add authentication, policies, and observability to every tool invocation.
* [**Configure your MCP proxy**](configure-your-mcp/README.md). Configure mediation, credential management, and the MCP Proxy's connection to upstream servers.
  * [**Add policies to your MCP server**](configure-your-mcp/add-policies-to-mcp-server.md). Apply fine-grained authorization policies at the tool level.
  * [**Apply policies to specific MCP methods**](configure-your-mcp/apply-policies-to-mcp-methods.md). Target policies at individual MCP protocol methods, such as `resources/list`, `tools/call`, or `prompts/get`.
  * [**Apply policies to individual tool invocations**](configure-your-mcp/apply-policies-to-tool-invocations.md). Govern a specific, high-value tool invocation without constraining the rest of the server.
* [**Create an MCP Studio**](create-an-mcp-studio.md). Compose tools, resources, prompts, and skills from multiple sources into a Composite MCP Server.
  * [**Edit tool composition**](edit-mcp-studio-composition.md). Select and alias the tools exposed by your MCP Studio, and configure authentication to the upstream servers they come from.
* [**Create an LLM Proxy**](create-an-llm-proxy.md). Configure an LLM Proxy to route model traffic through the AI Gateway with authentication, cost attribution, and observability.
* [**Configure an LLM Proxy**](configure-an-llm-proxy.md). Configure guardrails, PII filtering, rate limiting, security plans, and policies.
* [**Create an agent identity**](create-an-agent-identity.md). Register an agent as a User-embedded, Hosted delegated, or Autonomous OAuth client, identified by a client ID or a CIMD metadata document.
* [**Configure your Access Management instance**](configure-your-access-management-instance.md). Connect the module to Gravitee Access Management, select an environment and domain, and check that the domain has the capabilities agent identities rely on.
* [**Expose your agent with the A2A Proxy**](expose-agent-with-a2a-proxy.md). Make an agent's skills discoverable and callable across trust boundaries with per-skill authorization.
* [**Configure your A2A Proxy**](configure-your-a2a-proxy/README.md). Manage security, access controls, and flows for your A2A Proxy using the Policy Studio.
  * [**Add policies to your A2A Proxy**](configure-your-a2a-proxy/add-policies-to-a2a-proxy.md). Attach security, transformation, and logic policies to agent-to-agent communications.
