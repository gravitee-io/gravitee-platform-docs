---
hidden: false
noIndex: false
description: Control which teams reach which AI models with policy examples for team access, guardrails, and model size. Adapt an example to your own models.
---

# AI policy example

Practical examples of authorization policies for AI providers and models, including guardrails and model size restrictions.

## AI Model policy structure

AI Model policies target a specific model or provider and govern access at two levels:

| Resource group | Description |
|---------------|-------------|
| **AI Provider** | The LLM provider (for example, OpenAI, Anthropic) |
| **Model** | A specific model (for example, GPT-4o, Claude 3.5 Sonnet) |

## Example 1: Allow a team to use a specific model

```
// Policy: data-team-gpt4
// Target: gpt-4o

permit (
  principal in Group::"data-science",
  action == Action::"invoke",
  resource == Model::"gpt-4o"
);
```

## Example 2: Require PII guardrails

```
// Policy: require-pii-filter
// Target: claude-3-sonnet

permit (
  principal,
  action == Action::"invoke",
  resource == Model::"claude-3-sonnet"
)
when {
  context.guardrails.pii == true
};
```

Access is only permitted when the PII filter guardrail is enabled for the request.

## Example 3: Restrict large models to senior engineers

```
// Policy: large-models-senior-only
// Target: gpt-4o

forbid (
  principal,
  action == Action::"invoke",
  resource == Model::"gpt-4o"
)
when {
  ["large", "xlarge"].contains(resource.size) &&
  principal.level < 5
};
```

## Available condition snippets

| Condition | GAPL |
|-----------|------|
| **PII filter on** | `context.guardrails.pii == true` |

## Combining with MCP policies

AI Model policies work alongside MCP policies. An agent that invokes an MCP tool which calls an LLM is evaluated against both the MCP policy (for the tool invocation) and the AI Model policy (for the model call). Both must permit for the request to succeed.

## Next steps

* [MCP policy examples](mcp-policy-examples.md) — MCP access control patterns
* [API policy examples](api-policy-examples.md) — API access control patterns
* [Custom policies overview](custom-policies/custom-policies-overview.md) — Policies for non-routed resources
