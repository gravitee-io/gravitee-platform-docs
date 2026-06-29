---
hidden: false
noIndex: true
---

# MCP policy examples

Practical examples of authorization policies for MCP (Model Context Protocol) servers, tools, prompts, and resources.

## MCP policy structure

MCP policies target a specific MCP server and govern access to its surfaces. The policy editor's resource groups for MCP are:

| Resource group | Description |
|---------------|-------------|
| **MCP Server** | The server itself |
| **Tools** | Individual tools exposed by the server |
| **Prompts** | Prompt templates on the server |
| **Resources** | Data resources exposed via MCP |

## Example 1: Allow a group to invoke all tools on a server

```
// Policy: engineering-hr-tools
// Target: demo-hr-mcp

permit (
  principal in Group::"engineering",
  action == Action::"invoke",
  resource in MCPServer::"demo-hr-mcp"
);
```

This policy permits any member of the `engineering` group to invoke any tool on the `demo-hr-mcp` server. The `in` match mode on the resource clause means it covers the server and all child entities (tools, prompts, resources).

## Example 2: Restrict a specific tool to business hours

```
// Policy: hr-search-business-hours
// Target: demo-hr-mcp

permit (
  principal == User::"alice",
  action == Action::"invoke",
  resource == MCPTool::"demo-hr-mcp.search"
)
when {
  context.time.hour >= 9 && context.time.hour < 17
};
```

This policy permits Alice to invoke the `search` tool only during business hours (9 AM–5 PM).

## Example 3: Block an agent from sensitive tools

```
// Policy: block-agent-from-pii
// Target: demo-hr-mcp

forbid (
  principal == AgentIdentity::"research-bot",
  action == Action::"invoke",
  resource == MCPTool::"demo-hr-mcp.get-employee-ssn"
);
```

This policy explicitly forbids the `research-bot` agent from invoking a tool that returns PII data.

## Example 4: Require trusted device for admin tools

```
// Policy: admin-tools-trusted-device
// Target: demo-hr-mcp

permit (
  principal in Group::"admins",
  action == Action::"invoke",
  resource in MCPServer::"demo-hr-mcp"
)
when {
  context.device.trusted == true
};
```

## Available condition snippets

| Condition | GAPL |
|-----------|------|
| **Business hours** | `context.time.hour >= 9 && context.time.hour < 17` |
| **Trusted device** | `context.device.trusted == true` |
| **Corporate IP range** | `context.source.ip.in_cidr("10.0.0.0/8")` |

## Tips

{% hint style="info" %}
- Use `forbid` statements to create deny rules that override broader `permit` rules
- Scope policies to specific tools when the server exposes sensitive operations alongside safe ones
- Use the `in` match mode on MCPServer resources to cover all child tools in a single statement
{% endhint %}

## Next steps

* [API policy examples](api-policy-examples.md) — API access control patterns
* [AI policy example](ai-policy-example.md) — Token budget and cost policies
* [Create, update, and delete policies](create-update-delete-policies.md) — Full editor reference
