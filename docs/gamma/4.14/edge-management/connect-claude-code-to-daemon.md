---
hidden: false
noIndex: false
description: Route the traffic of Claude Code through the Edge Daemon and confirm that it's intercepted. Learn why there's nothing to configure in Claude Code itself.
---

# Connect Claude Code to the Edge Daemon

## Overview

There's nothing to configure in Claude Code. Once the Edge Daemon runs on a device and **Claude Code** is one of the intercepted agents of the environment, the daemon captures its traffic. No environment variable, no setting in Claude Code, and no proxy configuration are needed. The install script that the console generates passes only the two gateway addresses of the environment to the installer of the daemon.

This page explains why, and how to confirm that interception works.

## Before you start

* The Edge Daemon is deployed and running on the device. See [Configure Kandji to deploy the Edge Daemon](connect/configure-kandji-daemon.md).
* Claude Code is installed on the same device.
* **Claude Code** is configured as an intercepted agent, with a target API on its route. See [Configure interception](connect/configure-edge-management.md).

## How it works

The installer of the daemon sets up a DNS resolver on the device that answers for the intercepted domains, a listener on port 443, and a certificate authority for those connections. It also sets `NODE_EXTRA_CA_CERTS` so that Node.js tools such as Claude Code trust that certificate authority. Claude Code therefore reaches the daemon when it calls `api.anthropic.com`, without any change on its side. The daemon forwards each request whose path matches one of the routes of the agent to the target API of that route on the gateway, where your policies, quotas, and analytics apply, and the gateway relays the request to Anthropic.

Because interception works per domain, the daemon sees every request that Claude Code sends to `api.anthropic.com`, including non-LLM calls such as telemetry and authentication. What happens to those depends on the routes of the agent. With the preset, only `/v1/messages` is forwarded to the gateway, and everything else passes through to Anthropic untouched. See [Everything else](connect/configure-edge-management.md#everything-else).

{% hint style="info" %}
**The daemon doesn't apply policies on the device.** It captures the request and forwards it. Your policies, quotas, and analytics are applied by the gateway, on the target API of the route, so no request is checked or blocked before it leaves the device.
{% endhint %}

{% hint style="info" %}
A Claude Code session that was already open when the daemon was installed isn't intercepted. Start a new session after the installation.
{% endhint %}

## Sign in on a route secured by OAuth2

When the route of the agent is secured by an OAuth2 plan, each developer signs in with your identity provider. When the gateway answers with a 401, the daemon gives the developer a sign-in prompt instead of the raw response. See [Secure a route with an OAuth2 plan](connect/configure-edge-management.md#secure-a-route-with-an-oauth2-plan).

## Verify the connection

1. Open Claude Code on the device and send a prompt.
2. In the Gamma console, open **Edge Management**.
3. Click **Proxied Traffic** and check that the request appears there, with the device, the tool, the model, and the token counts. See [Monitor proxied traffic](observe/monitor-proxied-traffic.md).

If nothing appears, use the following table:

| What you see                                                             | Where to look                                                                                                                                                                                                        |
| ------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| The device isn't listed on **Devices**, or reports as **Inactive**       | The daemon isn't running, or it can't reach the Reactor URL. A device is **Active** when a heartbeat was received in the last 2 minutes. See [Monitor your devices](observe/monitor-devices.md).                     |
| The device is **Active**, but no traffic appears                         | Claude Code isn't configured as an intercepted agent, or its route has no target API. See [Configure interception](connect/configure-edge-management.md).                                                            |
| The agent reports **Will not intercept** on the **Overview** page        | The target API can't serve the route. Most often, it hasn't been started and deployed. See [Understand the route verdicts](connect/configure-edge-management.md#understand-the-route-verdicts).                       |
| The traffic shows up under **Detected Shadow AI** instead                | The daemon runs and saw a direct connection to Anthropic, so it didn't intercept the request. Check that Claude Code is configured as an intercepted agent, and that the session was started after the installation. |
| The developer gets the raw 401 response instead of a sign-in prompt      | A response template of the target API replaces the gateway's 401. See [Requirements of a route secured by a plan](connect/proxy-api-reference.md#requirements-of-a-route-secured-by-a-plan).                           |
| The sign-in fails with `invalid_scope`                                   | The identity provider doesn't let the client of the application request `openid`, `offline_access`, or the scopes of the plan. See [Allow the scopes the daemon requests](connect/configure-edge-management.md#allow-the-scopes-the-daemon-requests). |

## Next steps

* **Watch the traffic.** See [Monitor proxied traffic](observe/monitor-proxied-traffic.md).
* **Check the fleet.** See [Monitor your devices](observe/monitor-devices.md).
