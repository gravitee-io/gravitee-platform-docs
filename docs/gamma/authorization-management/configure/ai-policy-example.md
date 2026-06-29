---
hidden: false
noIndex: true
---

# AI policy example

Practical examples of authorization policies for AI providers and models, including token budget controls and cost ceilings.

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

## Example 2: Enforce a daily token budget

```
// Policy: token-budget-50k
// Target: gpt-4o

permit (
  principal,
  action == Action::"invoke",
  resource == Model::"gpt-4o"
)
when {
  context.usage.tokens_per_day(principal) < 50000
};
```

This policy permits model access only while the principal stays under 50,000 tokens per day.

## Example 3: Cost ceiling per principal

```
// Policy: cost-ceiling-100
// Target: gpt-4o

forbid (
  principal,
  action == Action::"invoke",
  resource == Model::"gpt-4o"
)
when {
  context.usage.cost_per_day(principal) >= 100
};
```

This policy denies access once the principal's daily cost reaches $100.

## Example 4: Require PII guardrails

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

## Example 5: Restrict large models to senior engineers

```
// Policy: large-models-senior-only
// Target: gpt-4o

forbid (
  principal,
  action == Action::"invoke",
  resource == Model::"gpt-4o"
)
when {
  resource.size in ["large", "xlarge"] &&
  principal.level < 5
};
```

## Available condition snippets

| Condition | GAPL |
|-----------|------|
| **Token budget** | `context.usage.tokens_per_day(principal) < 50000` |
| **Cost ceiling** | `context.usage.cost_per_day(principal) < 100` |
| **PII filter on** | `context.guardrails.pii == true` |
| **Model size small** | `resource.size in ["small", "medium"]` |

## Combining with MCP policies

AI Model policies work alongside MCP policies. An agent that invokes an MCP tool which calls an LLM is evaluated against both the MCP policy (for the tool invocation) and the AI Model policy (for the model call). Both must permit for the request to succeed.

## Next steps

* [MCP policy examples](mcp-policy-examples.md) — MCP access control patterns
* [API policy examples](api-policy-examples.md) — API access control patterns
* [Custom policies overview](custom-policies/custom-policies-overview.md) — Policies for non-routed resources
