---
hidden: false
noIndex: false
description: Design an MCP Proxy with policies applied at the server, method, and tool level, and edit an MCP Studio composition. Pick the guide for your task.
---

# Design

The Design group of an MCP Proxy controls which tools a Composite MCP Server exposes, and the policies the Policy Studio applies to every call.

* [**Edit MCP Studio composition**](../../edit-mcp-studio-composition.md): Change which tools an MCP Studio exposes, alias colliding tool names, and set upstream credentials.
* [**Add policies to your MCP server**](../../configure-your-mcp/add-policies-to-mcp-server.md): Control which consumers can invoke which tools with fine-grained authorization policies.
* [**Apply policies to specific MCP methods**](../../configure-your-mcp/apply-policies-to-mcp-methods.md): Target methods such as `resources/list`, `tools/call`, or `prompts/get` with a flow selector.
* [**Apply policies to individual tool invocations**](../../configure-your-mcp/apply-policies-to-tool-invocations.md): Constrain a single high-value tool invocation and leave other tools unconstrained.
* [**Layered governance for MCP tools**](../../configure-your-mcp/govern-mcp-tool-access.md): How authorization, rate limits, and response redaction combine on a Composite MCP Server.
