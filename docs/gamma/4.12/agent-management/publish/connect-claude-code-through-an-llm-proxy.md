---
hidden: false
noIndex: false
description: Configure Claude Code to reach Anthropic through an LLM Proxy while users keep their own OAuth login. Follow the steps to set up the plan and headers.
---

# Connect Claude Code through an LLM Proxy

## Overview

Claude Code can reach Anthropic through an LLM Proxy while the end user still authenticates with Claude Code's normal `/login` flow. In this configuration, the AI Gateway uses an API Key plan to identify and govern the consumer, and the user's Claude OAuth token passes through to Anthropic in the `Authorization` header.

Use this pattern when you want governance, subscription control, analytics, and model governance without issuing or storing a shared Anthropic API key in Gravitee.

### How authentication works

There are two separate credentials in this flow:

* The **Gravitee API key** authenticates the consumer to the AI Gateway. Claude Code sends it in a custom header, for example `X-Gravitee-Api-Key`.
* The **Claude OAuth token** authenticates the end user to Anthropic. Claude Code obtains and manages this token after the user runs `/login`.

The two credentials must occupy different positions in the request. Claude Code always puts its OAuth token in `Authorization: Bearer`, so the API Key plan must read the Gravitee key from a custom header instead.

The LLM Proxy provider must be configured with **No authentication**. Do not configure a bearer token or an Expression Language expression to copy the `Authorization` header. With no provider authentication configured, the request's existing `Authorization: Bearer <Claude OAuth token>` header passes through to Anthropic unchanged.

## Prerequisites

* Access to the Gamma console. For more information, see [AI management overview](../get-started/ai-management-overview.md).
* A deployed AI Gateway. For more information, see [Self-hosted installation guides](../../platform-management/install/self-hosted-installation-guides/README.md) and [Hybrid installation guides](../../platform-management/install/hybrid-installation-guides/README.md).
* A Claude Code user who can authenticate with `/login`.
* Permission to create a plan and a subscription on the LLM Proxy. For more information, see [Manage subscriptions](manage-subscriptions.md).

## Connect Claude Code to an LLM Proxy

1. [Configure the LLM Proxy](#configure-the-llm-proxy)
2. [Configure model governance](#configure-model-governance)
3. [Create a plan and subscription](#create-a-plan-and-subscription)
4. [Configure Claude Code](#configure-claude-code)

### Configure the LLM Proxy

1. Create an LLM Proxy. For more information, see [Create an LLM Proxy](../build/create-an-llm-proxy.md).
2. Add a provider in inline mode and configure it with the following values:

   | Field | Value |
   | --- | --- |
   | Provider name | `Anthropic` |
   | Request format | `Anthropic` |
   | Target URL | `https://api.anthropic.com` |
   | Authentication | `No authentication` |

3. Set the context path. Here is an example context path:

   ```text
   /claude-code
   ```

{% hint style="warning" %}
Do not add `/v1` to the target URL. The LLM Proxy appends `/v1/messages` when it forwards the request to Anthropic, so a target URL that already ends in `/v1` produces `/v1/v1/messages` and the request fails.
{% endhint %}

### Configure model governance

Claude Code sends Anthropic model IDs without a provider prefix, so the LLM Proxy must accept unprefixed model names.

To edit governance on an existing LLM Proxy, open the LLM Proxy detail page, navigate to **General** > **Models**, and then edit the provider.

1. Set **Prefix policy** to the following:

   ```text
   No prefix required
   ```

2. Choose one of the following **Model access** options. The two options are mutually exclusive.

   * **For broad access:** Select **Accept unregistered models (glob)**, and then set **Unregistered models glob**. Here is an example glob:

     ```text
     claude-*
     ```

     or, for all model IDs:

     ```text
     *
     ```

   * **For a strict allowlist:** Select **Registered models only**, and then add each model explicitly. Here is an example of adding each model:

     ```text
     claude-sonnet-4-6
     claude-opus-4-8
     claude-haiku-4-5-20251001
     ```

{% hint style="info" %}
A provider requires at least one model even when a glob is set. Add a seed model such as `claude-sonnet-4-6`.

Do not enable **Hide real model names (alias only)** for this flow. Claude Code sends real Anthropic model IDs, and that option hides them behind aliases, so every request would be rejected. The option is available only in **Registered models only** mode.
{% endhint %}

### Create a plan and subscription

1. On the LLM Proxy detail page, navigate to **Consumer Access** > **Plans**, and then add an **API Key** plan.
2. In the plan's API key configuration, select **Custom header**, and then set the header name to the following:

   ```text
   X-Gravitee-Api-Key
   ```

{% hint style="warning" %}
The plan wizard selects **Authorization: Bearer** by default and labels it as recommended. That mode does not work for this flow. Claude Code already uses `Authorization: Bearer` for its Claude OAuth token, so the AI Gateway would try to resolve the OAuth token as a Gravitee API key and reject the request with `GATEWAY_PLAN_UNRESOLVABLE` or `401 Unauthorized`. Select **Custom header** instead.
{% endhint %}

3. Leave **Propagate to upstream** disabled so that the Gravitee API key is not forwarded to Anthropic.
4. Navigate to **Consumer Access** > **Consumers**, and then select **Create subscription**.
5. Select the user's application and the API Key plan.
6. If the plan requires validation, accept the subscription. For more information, see [Manage subscriptions](manage-subscriptions.md).
7. Provide the user with the following information:

   * The AI Gateway base URL and the LLM Proxy context path.
   * The subscription API key.
   * The custom header definition. Here is an example custom header definition:

     ```text
     X-Gravitee-Api-Key: <subscription-api-key>
     ```

8. After changing provider, model, or plan configuration, redeploy the LLM Proxy. Select **Deploy** from the **Out of sync** banner, or navigate to **Operations** > **Deployment**.

### Configure Claude Code

1. Authenticate Claude Code using the following login:

```text
/login
```

2. Configure Claude Code to use the AI Gateway URL and the Gravitee subscription API key. For user-level Claude Code settings, update `~/.claude/settings.json` with the following environment variables:

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "https://<gateway-host>/<context-path>",
    "ANTHROPIC_CUSTOM_HEADERS": "X-Gravitee-Api-Key: <subscription-api-key>"
  }
}
```

Here is an example configuration:

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "https://ai-gateway.example.com/claude-code",
    "ANTHROPIC_CUSTOM_HEADERS": "X-Gravitee-Api-Key: 00000000-0000-0000-0000-000000000000"
  }
}
```

{% hint style="warning" %}
Do not set `ANTHROPIC_API_KEY` or `ANTHROPIC_AUTH_TOKEN` for this flow. Those variables change Claude Code authentication behavior and bypass the intended `/login` OAuth flow.
{% endhint %}

3. After updating the settings file, restart Claude Code to reload the environment.

## Verify the connection

1. Send a simple prompt from Claude Code. Here is an example prompt:

   ```text
   Reply with exactly: proxy-ok
   ```

Claude Code makes the following `POST` call:

```text
POST /v1/messages
```

The call passes through the AI Gateway with the following headers:

```text
X-Gravitee-Api-Key: <subscription-api-key>
Authorization: Bearer <Claude OAuth token>
```

The Gravitee API key identifies the subscription. The OAuth token is passed to Anthropic.

The verification is successful when Claude Code returns a normal Claude response and the LLM Proxy's analytics or agent log show the request passing through. For more information, see [Inspect your agent log](../observe/inspect-your-agent-log.md).

## Troubleshooting

### `GATEWAY_PLAN_UNRESOLVABLE` or `401 Unauthorized`

The request did not resolve to a valid plan or subscription.

Check that:

* The API Key plan uses **Custom header**, not **Authorization: Bearer**.
* The plan's header name matches the header Claude Code sends, for example `X-Gravitee-Api-Key`.
* The API key belongs to an accepted subscription on the LLM Proxy.
* The LLM Proxy was redeployed after the plan and subscription were created.
* The request path uses the deployed context path.

### `model_not_found`

The LLM Proxy did not resolve the requested model.

Check that:

* **Prefix policy** is set to **No prefix required**.
* The requested model is explicitly added, or the unregistered models glob matches it.
* **Hide real model names (alias only)** is disabled.
* The LLM Proxy was redeployed after changing model governance.
* Claude Code is sending the expected model ID, for example `claude-sonnet-4-6`.

### Anthropic authentication errors

If the request reaches Anthropic but fails authentication:

* Confirm the user is logged in to Claude Code with `/login`.
* Confirm the provider authentication is set to **No authentication**.
* Remove any bearer token or API key authentication configured on the provider.
* Confirm `ANTHROPIC_API_KEY` and `ANTHROPIC_AUTH_TOKEN` are not set in the Claude Code environment for this flow.

### Claude Code still calls Anthropic directly

Claude Code may need to be restarted after settings changes. Confirm that `ANTHROPIC_BASE_URL` is present in the active Claude Code environment and points to the LLM Proxy context path.

## Reference configuration

### LLM Proxy provider

```text
Request format: Anthropic
Target URL: https://api.anthropic.com
Authentication: No authentication
Prefix policy: No prefix required
Model access: Accept unregistered models (glob)
Unregistered models glob: claude-* or *
```

### API Key plan

```text
API key location: Custom header
Header name: X-Gravitee-Api-Key
Propagate to upstream: disabled
```

### Claude Code settings

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "https://<gateway-host>/<context-path>",
    "ANTHROPIC_CUSTOM_HEADERS": "X-Gravitee-Api-Key: <subscription-api-key>"
  }
}
```

## Next steps

* [Configure an LLM Proxy](../build/configure-an-llm-proxy.md). Attach guardrails, PII filtering, and rate limiting policies in the LLM Studio, and review per-token cost attribution.
* [Consume your LLM Proxy with LangChain](consume-your-llm-proxy-with-langchain.md). Route an application through the same proxy.
* [Connect Claude Code to the Edge Daemon](../../edge-management/connect-claude-code-to-daemon.md). Route employee device traffic through a local daemon before it reaches the AI Gateway.
