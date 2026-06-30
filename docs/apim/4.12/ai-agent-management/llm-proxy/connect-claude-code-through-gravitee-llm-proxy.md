---
description: Configure Claude Code to access Anthropic through a Gravitee LLM Proxy while preserving Claude Code OAuth login.
---

# Connect Claude Code through a Gravitee LLM Proxy

## Overview

Claude Code can connect to Anthropic through a Gravitee LLM Proxy while still allowing the end user to authenticate with Claude Code's normal `/login` flow. In this configuration, Gravitee uses an API Key plan to identify and govern the consumer, while the user's Claude OAuth token is passed through to Anthropic in the `Authorization` header.

Use this pattern when you want APIM-level governance, subscription control, analytics, and model governance without issuing or storing a shared Anthropic API key in Gravitee.

### How authentication works

There are two separate credentials in this flow:

* The **Gravitee API key** authenticates the consumer to the Gravitee Gateway. Claude Code sends it as a custom header, for example `X-Gravitee-Api-Key`.
* The **Claude OAuth token** authenticates the end user to Anthropic. Claude Code obtains and manages this token after the user runs `/login`.

The LLM Proxy endpoint must be configured with **Authentication: None**. Do not configure Bearer authentication or an Expression Language expression to copy the `Authorization` header. With no endpoint authentication configured, the request's existing `Authorization: Bearer <Claude OAuth token>` header can pass through to Anthropic.

## Prerequisites

* Access to Gravitee APIM Console. For more information, see [getting-started](../../getting-started/README.md).
* A deployed Gravitee Gateway with the LLM Proxy entrypoint available. For more information, see [proxy-your-llms.md](proxy-your-llms.md).
* A Claude Code user who can authenticate with `/login`.
* Permission to create an [API Key plan](../../secure-and-expose-apis/plans/api-key.md) and [subscription](../../secure-and-expose-apis/subscriptions/manage-subscriptions.md) for the user or the user's [application](../../secure-and-expose-apis/applications/create-an-application.md).

## Connect Claude Code to an LLM Proxy API

1. [Configure the LLM Proxy API](#configure-the-llm-proxy-api)
2. [Configure models](#configure-models)
3. [Create a plan and subscription](#create-a-plan-and-subscription)
4. [Configure Claude Code](#configure-claude-code)

### Configure the LLM Proxy API

1. Create or edit an LLM Proxy API. For more information about how to create an LLM Proxy API, see [proxy-your-llms.md](proxy-your-llms.md).
2. Set the API context path. Here is an example context path:

   ```text
   /claude-code
   ```

3. Add an LLM provider for Anthropic.
4. Configure the provider using the following values:

   | Field | Value |
   | --- | --- |
   | Request format | `Anthropic` |
   | Target URL | `https://api.anthropic.com` |
   | Authentication | `None` |

Do not add `/v1` to the target URL. Claude Code calls `/v1/messages`, and then the LLM Proxy handles the route when forwarding the request.

### Configure models

Claude Code sends Anthropic model IDs without a provider prefix. The LLM Proxy must allow unprefixed model names.

1. In the provider's model governance settings, set **Prefix needs** to the following message:

   ```text
   Models and aliases do not require a prefix
   ```

2. If all Claude Code models' name is explicitly configured as an alias, enable **Only use alias**.
3. Configure model access using one of the following options:

   * **For broad access:** Use unregistered model globbing. Here is an example of unregistered model globbing:

     ```text
     claude-*
     ```

     or, for all model IDs:

     ```text
     *
     ```

   * **Strict allowlist:** Add each model. Here is an example of adding each model:

     ```text
     claude-sonnet-4-6
     claude-opus-4-8
     claude-haiku-4-5-20251001
     ```

If the UI requires at least one model entry even when globbing is enabled, add a seed model such as `claude-sonnet-4-6`.

### Create a plan and subscription

1. Create an **API Key** plan on the LLM Proxy API.
2. Use the API key header expected by the client. Here is an example:

   ```text
   X-Gravitee-Api-Key
   ```

3. Publish or deploy the plan.
4. Create or select the user's application. For more information about creating an application, see [create-an-application.md](../../secure-and-expose-apis/applications/create-an-application.md).
5. Create a subscription from that application to the API Key plan. For more information about subscribing to a plan, see [manage-subscriptions.md](../../secure-and-expose-apis/subscriptions/manage-subscriptions.md).
6. If approval is required, approve the subscription.
7. Provide the user with the following information:

   * The LLM Proxy base URL.
   * The subscription API key.
   * The custom header definition. Here is an example custoemr header definition:

     ```text
     X-Gravitee-Api-Key: <subscription-api-key>
     ```

8. After changing endpoint, model, or plan configuration, deploy the API again.

### Configure Claude Code

1. Authenticate Claude Code using the following login:

```text
/login
```

2. Configure Claude Code to use the Gravitee Gateway URL and the Gravitee subscription API key. For user-level Claude Code settings, update `~/.claude/settings.json` with the following environment variables:

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "https://<gateway-host>/<api-context-path>",
    "ANTHROPIC_CUSTOM_HEADERS": "X-Gravitee-Api-Key: <subscription-api-key>"
  }
}
```

Here is an example configuration:

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "https://apim.example.com/claude-code",
    "ANTHROPIC_CUSTOM_HEADERS": "X-Gravitee-Api-Key: 00000000-0000-0000-0000-000000000000"
  }
}
```

{% hint style="warning" %}
Do not set `ANTHROPIC_API_KEY` or `ANTHROPIC_AUTH_TOKEN` for this flow. Those variables change Claude Code authentication behavior and bypass the intended `/login` OAuth flow.
{% endhint %}

3. After updating the settings file, restart Claude Code to reload the environment.

## Verification

 * The user must send a simple prompt. Here is an example prompt:

```text
Reply with exactly: proxy-ok
```

Claude Code makes the foolowing `POST` call:

```text
POST /v1/messages?beta=true
```

The call passesthrough the Gravitee Gateway with the following information:

```text
X-Gravitee-Api-Key: <subscription-api-key>
Authorization: Bearer <Claude OAuth token>
```

The Gravitee API key identifies the subscription. The OAuth token is passed to Anthropic.

The verification is successful when Claude Code returns a normal Claude response and the Gravitee request logs, analytics, or debug view show the request passing through the LLM Proxy API.

## Troubleshooting

### `GATEWAY_PLAN_UNRESOLVABLE` or `401 Unauthorized`

The request did not resolve to a valid Gravitee plan or subscription.

Check that:

* The user is sending the configured API key header, for example `X-Gravitee-Api-Key`.
* The API key belongs to an active subscription on the LLM Proxy API.
* The API is deployed after the plan and subscription were created.
* The request path uses the deployed API context path.

### `model_not_found`

The LLM Proxy did not resolve the requested model.

Check that:

* **Prefix needs** is set to **Models and aliases do not require a prefix**.
* The requested model is explicitly added, or unregistered model globbing matches it.
* The API was redeployed after changing model governance.
* Claude Code is sending the expected model ID, for example `claude-sonnet-4-6`.

### Anthropic authentication errors

If the request reaches Anthropic but fails authentication:

* Confirm the user is logged in to Claude Code with `/login`.
* Confirm the LLM Proxy endpoint authentication is set to **None**.
* Remove any Bearer or API Key authentication configured on the LLM Proxy endpoint.
* Confirm `ANTHROPIC_API_KEY` and `ANTHROPIC_AUTH_TOKEN` are not set in the Claude Code environment for this flow.

### Claude Code still calls Anthropic directly

Claude Code may need to be restarted after settings changes. Confirm that `ANTHROPIC_BASE_URL` is present in the active Claude Code environment and points to the Gravitee API context path.

## Reference configuration

### Gravitee LLM provider

```text
Request format: Anthropic
Target URL: https://api.anthropic.com
Authentication: None
Model governance: Models and aliases do not require a prefix
Unregistered model globbing: claude-* or *
```

### Claude Code settings

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "https://<gateway-host>/<api-context-path>",
    "ANTHROPIC_CUSTOM_HEADERS": "X-Gravitee-Api-Key: <subscription-api-key>"
  }
}
```
