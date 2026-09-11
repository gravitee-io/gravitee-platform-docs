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
A Claude Code session that was already open when the daemon was installed isn't intercepted. Start a new session after the installation.
{% endhint %}

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

## Next steps

* **Watch the traffic.** See [Monitor proxied traffic](observe/monitor-proxied-traffic.md).
* **Check the fleet.** See [Monitor your devices](observe/monitor-devices.md).
