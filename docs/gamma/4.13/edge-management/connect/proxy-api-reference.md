---
hidden: false
noIndex: false
description: What an API must be to receive the traffic that an Edge Daemon route forwards to it, and what Edge Management builds when you create one from the picker. Browse the reference.
---

# Target API reference

## Overview

A target API is the API that a route of an intercepted agent forwards to. It's a standard API on your gateway, with its own page, plans, policies, and analytics. Edge Management points at it and doesn't own it.

You can point a route at an API you already have, or have Edge Management create one from the picker. Either way, the route is checked against the requirements below, and the verdict is shown under the route. See [Choose the target API of a route](configure-edge-management.md#choose-the-target-api-of-a-route).

## What a route requires of its target API

The following requirements apply to the `/v1/messages` route of the **Claude Code** preset, whose traffic is LLM traffic. The requirements are listed in the order the console shows them.

| Requirement                                                                       | Severity       |
| --------------------------------------------------------------------------------- | -------------- |
| The API must be an LLM Proxy API.                                                 | Blocking       |
| The API must receive its traffic through a `llm-proxy` entrypoint.                | Blocking       |
| The API must be started and deployed.                                             | Blocking       |
| The API must call its backend through a `llm-proxy` endpoint.                     | Blocking       |
| Every endpoint must target the `ANTHROPIC` provider.                              | Blocking       |
| Endpoints are expected to point at `https://api.anthropic.com:443`.               | Recommendation |
| Usage enforcement should be enabled, so intercepted traffic is accounted for.     | Recommendation |
| The API should have no changes waiting to be deployed.                            | Recommendation |
| The route must forward to a path the API exposes.                                 | Blocking       |
| The path the route forwards to should already be deployed.                        | Recommendation |

A blocking requirement that isn't met means that the route reports **Will not intercept**: the daemon forwards the traffic, and the API doesn't serve it. A recommendation that isn't met means that the route reports **Check**: the route works, and something is worth looking at.

Unfold **What this route needs** under the route to see the reason of each unmet requirement. For example, a stopped API reports that the gateway doesn't serve it, an API edited after its last deployment reports that the verdict describes what the gateway serves rather than what the console shows, and a path exposed on a virtual host reports that it can't be intercepted.

{% hint style="info" %}
An API whose usage enforcement is off still serves the traffic, but token usage isn't recorded, so the **Proxied Traffic** page shows its requests without token counts.
{% endhint %}

Requirements are only checked for the routes that the module describes. A route you added yourself, such as an extra route on a preset or a route of a custom agent, reports **Not checked**: nothing describes what it needs, so nothing is checked. It's yours to get right.

{% hint style="warning" %}
An API published on a virtual host can't be a target, and its path isn't offered by the picker. See [Choose the target API of a route](configure-edge-management.md#choose-the-target-api-of-a-route).
{% endhint %}

## What Edge Management creates for you

When you create the target API of the **Claude Code** route from the picker, Edge Management builds an LLM Proxy API that satisfies every blocking requirement above:

| Setting                 | Value                                                           |
| ----------------------- | --------------------------------------------------------------- |
| API type                | LLM Proxy                                                       |
| Entrypoint              | `llm-proxy`, with usage enforcement enabled                     |
| Endpoint                | `llm-proxy`, targeting the `ANTHROPIC` provider at `https://api.anthropic.com`, with no authentication |
| Context path            | The one you entered                                             |
| Plan                    | **Keyless**, published, with automatic validation               |
| Model list              | `claude-sonnet-4-5`                                             |
| Model governance        | Model pattern `*`, so every model is accepted                   |
| Visibility              | Private                                                         |
| State                   | Stopped, never deployed                                         |

Two of those settings are permissive by design, so that interception works the moment the API is deployed, and both are yours to tighten:

* **The keyless plan.** The connection between the daemon and the gateway isn't authenticated, so a secured plan would reject the requests of the daemon. Expose these APIs on trusted networks only.
* **Model governance.** The API accepts any model, because guessing a narrower list would break the agent on the next model it picks.

The API is created stopped and undeployed, and the route reports **Will not intercept** until you start and deploy it from its own page. The description of the API states this on the API itself.

## Working with a target API

A target API is a standard API of your gateway. Configure its policies, its logging, and its analytics on the page of the API itself. For an LLM Proxy API, see [Configure an LLM Proxy](../../agent-management/build/configure-an-llm-proxy.md).

{% hint style="warning" %}
Edge Management doesn't keep a route and its target API in step. Someone can rename a context path, stop the API, or change its type long after the route was mapped, and the route keeps forwarding to a path that nothing serves. The route verdict and the **Interception readiness** card of the **Overview** page are what make that drift visible. Acting on it is up to you.
{% endhint %}
